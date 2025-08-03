from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

# Load API keys from .env
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class TTSRequest(BaseModel):
    text: str
    voice_id: str = "en-US-terrell"
    

@app.post("/generate-audio")
async def generate_audio(payload: TTSRequest):
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY  # Or "Authorization": f"Bearer {MURF_API_KEY}" if required
    }
    body = {
        "text": payload.text,
        "voice_id": payload.voice_id,
        "format": "mp3"
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=headers, json=body)
        if res.status_code == 200:
            data = res.json()
            audio_url = data.get("audioUrl") or data.get("audio_url")
            if audio_url:
                return {"audio_url": audio_url}
            else:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Request succeeded, but no audio URL found. Check Murf's response format.", "murf_response": data}
                )
        else:
            return JSONResponse(status_code=res.status_code, content={"error": res.text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
