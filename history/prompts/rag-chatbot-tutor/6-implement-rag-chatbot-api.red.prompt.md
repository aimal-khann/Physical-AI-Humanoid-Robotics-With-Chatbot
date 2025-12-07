--- 
id: 6
title: "Implement RAG Chatbot API"
stage: "red"
date: 2025-12-07
surface: "agent"
model: "gemini-1.5-flash"
feature: "rag-chatbot-tutor"
branch: "1-rag-chatbot-tutor"
user: "(unknown)"
command: "/sp.implement Implement Phase 3 task T024 and T025 to create the chatbot API.

Create a file \"rag_backend/main.py\" with the following python code:

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv(\"QDRANT_URL\")
QDRANT_API_KEY = os.getenv(\"QDRANT_API_KEY\")
COHERE_API_KEY = os.getenv(\"COHERE_API_KEY\")
QDRANT_COLLECTION_NAME = os.getenv(\"QDRANT_COLLECTION_NAME\", \"textbook_content\")

# Initialize App
app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],  # For hackathon, allow all. In production, specify domain.
    allow_credentials=True,
    allow_methods=[\" * \"],
    allow_headers=[\"*\"]
)

# Initialize Clients
try:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    cohere_client = cohere.Client(COHERE_API_KEY)
except Exception as e:
    print(f\"Error initializing clients: {e}\")

class ChatRequest(BaseModel):
    message: str

@app.get(\"/")
def health_check():
    return {\"status\": \"online\", \"message\": \"Physical AI Textbook Chatbot API\"}

@app.post(\"/chat\")
def chat_endpoint(request: ChatRequest):
    user_query = request.message
    
    # 1. Generate Embedding for the query
    try:
        embed_response = cohere_client.embed(
            texts=[user_query],
            model=\"embed-english-light-v3.0\",
            input_type=\"search_query"
        )
        query_vector = embed_response.embeddings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f\"Embedding error: {e}\")

    # 2. Search Qdrant for relevant chunks
    try:
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f\"Database search error: {e}\")

    # 3. Construct Context from results
    context_text = ""
    sources = []
    for result in search_results:
        context_text += f\"---\"
        context_text += f\"\n{result.payload['content']}\n"
        sources.append(result.payload['title'])

    # 4. Generate Answer using Cohere
    prompt = f\"""
    You are an AI Tutor for a \"Physical AI & Humanoid Robotics\" textbook.
    Answer the user's question strictly based on the context provided below.
    If the answer is not in the context, say \"I can't find that in the textbook.\"
    
    Context:
    {context_text}
    
    Question: {user_query}
    
    Answer:
    \"""
    
    try:
        response = cohere_client.chat(
            message=prompt,
            model=\"command-r-plus\",
            temperature=0.3
        )
        answer = response.text
    except Exception as e:
        answer = \"I'm having trouble generating an answer right now.\"

    return {
        \"reply\": answer,
        \"sources\": list(set(sources)) # Unique sources
    }"
labels: ["implementation", "backend", "api"]
links:
  spec: "specs/1-rag-chatbot-tutor/spec.md"
  plan: "specs/1-rag-chatbot-tutor/plan.md"
  tasks: "specs/1-rag-chatbot-tutor/tasks.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "rag_backend/main.py"
tests_yaml: []
---

## Prompt

```text
/sp.implement Implement Phase 3 task T024 and T025 to create the chatbot API.

Create a file "rag_backend/main.py" with the following python code:

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

# Initialize App
app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon, allow all. In production, specify domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Clients
try:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    cohere_client = cohere.Client(COHERE_API_KEY)
except Exception as e:
    print(f"Error initializing clients: {e}")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "Physical AI Textbook Chatbot API"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_query = request.message
    
    # 1. Generate Embedding for the query
    try:
        embed_response = cohere_client.embed(
            texts=[user_query],
            model="embed-english-light-v3.0",
            input_type="search_query"
        )
        query_vector = embed_response.embeddings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    # 2. Search Qdrant for relevant chunks
    try:
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database search error: {e}")

    # 3. Construct Context from results
    context_text = ""
    sources = []
    for result in search_results:
        context_text += f"---"
        context_text += f"\n{result.payload['content']}\n"
        sources.append(result.payload['title'])

    # 4. Generate Answer using Cohere
    prompt = f"""
    You are an AI Tutor for a "Physical AI & Humanoid Robotics" textbook.
    Answer the user's question strictly based on the context provided below.
    If the answer is not in the context, say "I can't find that in the textbook."
    
    Context:
    {context_text}
    
    Question: {user_query}
    
    Answer:
    """
    
    try:
        response = cohere_client.chat(
            message=prompt,
            model="command-r-plus",
            temperature=0.3
        )
        answer = response.text
    except Exception as e:
        answer = "I'm having trouble generating an answer right now."

    return {
        "reply": answer,
        "sources": list(set(sources)) # Unique sources
    }
```

## Response

```text
The following tasks have been completed for Phase 3: RAG Chatbot Implementation:

- Created `rag_backend/main.py` which includes:
    - A FastAPI application with CORS middleware.
    - Initialization of Qdrant and Cohere clients, with error handling.
    - A health check endpoint (`GET /`).
    - A `POST /chat` endpoint that handles:
        - Generating an embedding for the query using Cohere.
        - Searching Qdrant for relevant chunks.
        - Constructing a context from the search results.
        - Generating an answer using Cohere's chat model, based *strictly* on the provided context, and explicitly states if the answer is not in the context.
        - Returning the AI-generated reply and unique sources.

**Note for the user**: Due to file access limitations, I was unable to automatically mark tasks T024 and T025 as complete in `specs/1-rag-chatbot-tutor/tasks.md`. Please manually mark them as `[x]` in the `tasks.md` file.

The folder structure is correct with `main.py` in place.
```

## Outcome

Successfully implemented the requested chatbot API tasks.

## Evaluation
The user's request to implement the chatbot API tasks for the RAG backend was successfully fulfilled. The `main.py` script was created with all specified functionalities, including FastAPI endpoint definition, client initialization, query embedding, Qdrant search, context construction, and Cohere-based answer generation.

```