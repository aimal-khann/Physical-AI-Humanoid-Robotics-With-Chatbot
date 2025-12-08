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

# 1. LOAD KEYS
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. DATABASE CONFIGURATION
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

# 4. SETUP OPENAI MODEL
model = OpenAIChatCompletionsModel(
    model="gpt-4o",
    openai_client=openai_client
)

# 5. DEFINE THE TOOL
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

        # B. Search Qdrant
        result = qdrant_client.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_vector,
            limit=10 
        )
        
        if not result.points:
            print("   ⚠️ [Tool] Search successful, but found 0 matching chunks.")
            return "No relevant information found in the textbook for this query."
            
        contents = ""
        for point in result.points:
            source = point.payload.get("url", "Unknown Source")
            text = point.payload.get("text", "")
            contents += f"--- SOURCE: {source} ---\n{text}\n\n"
            
        print(f"   ✅ [Tool] Found {len(result.points)} relevant chunks.")
        return contents
        
    except Exception as e:
        print(f"   ❌ [CRITICAL TOOL ERROR]: {e}")
        return f"SYSTEM ERROR: The database search failed due to: {str(e)}"

# 6. AGENT
agent = Agent(
    name="TextbookBot",
    instructions="""
    You are the specialized AI Assistant for the 'Physical AI & Humanoid Robotics' textbook.
    
    RULES:
    1. You must answer strictly using ONLY the content from the `retrieve_textbook_info` tool.
    2. If the user asks about topics NOT in the book, refuse: "I can only answer questions related to the Physical AI textbook."
    3. If the tool returns "No relevant information found", say: "This specific topic is not covered in the textbook."
    4. If the tool returns a "SYSTEM ERROR", apologize and state technical maintenance is required.
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

# -----------------------------------------
# ✅ ORIGINAL ENDPOINT (still available)
# -----------------------------------------
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"\n📩 User: {request.message}")
    try:
        result = await Runner.run(agent, input=request.message)
        print("✅ Reply sent.")
        return {"reply": result.final_output}
    except Exception as e:
        print(f"❌ [API ERROR]: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# ✅ NEW ENDPOINT: /ask
# -----------------------------------------
@app.post("/ask")
async def ask_endpoint(request: ChatRequest):
    print(f"\n📩 User (/ask): {request.message}")
    try:
        result = await Runner.run(agent, input=request.message)
        print("✅ Reply sent from /ask.")
        return {"answer": result.final_output}
    except Exception as e:
        print(f"❌ [API ERROR /ask]: {e}")
        raise HTTPException(status_code=500, detail=str(e))
