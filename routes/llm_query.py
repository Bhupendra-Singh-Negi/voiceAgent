from google import genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

# Initialize GenAI client (automatically uses GEMINI_API_KEY from env if not passed)
client = genai.Client()


class QueryRequest(BaseModel):
    text: str

@router.post("/llm/query")
async def query_llm(request: QueryRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.text
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
