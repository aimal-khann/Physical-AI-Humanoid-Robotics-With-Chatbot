import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import cohere
from qdrant_client import QdrantClient

# --- IMPORT AGENTS ---
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import set_tracing_disabled, function_tool

# --- CONFIGURATION ---
load_dotenv()
set_tracing_disabled(disabled=True)

# 1. LOAD KEYS (Make sure these are in your .env file)
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. DATABASE CONFIGURATION
# !!! CRITICAL: This must match the model you used to ingest data !!!
# If you used Subhan's script, keep this as "embed-english-v3.0".
# If you get a "Dimension Mismatch" error, change this to "embed-english-light-v3.0".
EMBEDDING_MODEL = "embed-english-v3.0" 
QDRANT_COLLECTION_NAME = "humanoid_ai_book"

# 3. INITIALIZE CLIENTS
try:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    cohere_client = cohere.Client(COHERE_API_KEY)
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    print(f"✅ Clients Initialized. Using Model: {EMBEDDING_MODEL}")
except Exception as e:
    print(f"❌ STARTUP ERROR: {e}")

# 4. SETUP OPENAI MODEL (The Brain)
model = OpenAIChatCompletionsModel(
    model="gpt-4o", # You can also use "gpt-3.5-turbo"
    openai_client=openai_client
)

# 5. DEFINE THE TOOL (The Hands)
@function_tool
def retrieve_textbook_info(query: str) -> str:
    """
    Searches the Qdrant database for relevant text chunks from the textbook.
    """
    print(f"   🔎 [Tool] Searching for: '{query}'")
    
    try:
        # A. Generate Embedding
        response = cohere_client.embed(
            texts=[query],
            model=EMBEDDING_MODEL,
            input_type="search_query"
        )
        query_vector = response.embeddings[0]

        # B. Search Qdrant (Fetching 10 chunks for better context)
        result = qdrant_client.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_vector,
            limit=10 
        )
        
        # C. Handle Empty Results
        if not result.points:
            print("   ⚠️ [Tool] Search successful, but found 0 matching chunks.")
            return "No relevant information found in the textbook for this query."
            
        # D. Format Output
        contents = ""
        for point in result.points:
            source = point.payload.get("url", "Unknown Source")
            text = point.payload.get("text", "")
            contents += f"--- SOURCE: {source} ---\n{text}\n\n"
            
        print(f"   ✅ [Tool] Found {len(result.points)} relevant chunks.")
        return contents
        
    except Exception as e:
        print(f"   ❌ [CRITICAL TOOL ERROR]: {e}")
        # Return the actual error to the Agent so it knows something broke
        return f"SYSTEM ERROR: The database search failed due to: {str(e)}"

# 6. DEFINE THE STRICT AGENT
agent = Agent(
    name="TextbookBot",
    instructions="""
    You are the specialized AI Assistant for the 'Physical AI & Humanoid Robotics' textbook.
    
    YOUR STRICT RULES:
    1. **Primary Source:** You must answer strictly using ONLY the content provided by the `retrieve_textbook_info` tool.
    2. **Refusal Policy:** If the user asks about topics NOT in the book (e.g., politics, celebrities, movies), strictly refuse. Say: "I can only answer questions related to the Physical AI textbook."
    3. **Uncertainty:** If the tool returns "No relevant information found", explicitly state: "This specific topic is not covered in the textbook." Do NOT make up an answer.
    4. **System Errors:** If the tool returns a "SYSTEM ERROR", apologize and tell the user technical maintenance is required.
    """,
    model=model,
    tools=[retrieve_textbook_info]
)

# 7. FASTAPI SERVER
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"\n📩 User: {request.message}")
    try:
        # Using 'await' prevents the server from freezing
        result = await Runner.run(agent, input=request.message)
        print("✅ Reply sent.")
        return {"reply": result.final_output}
    except Exception as e:
        print(f"❌ [API ERROR]: {e}")
        raise HTTPException(status_code=500, detail=str(e))