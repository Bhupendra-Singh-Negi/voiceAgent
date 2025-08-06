from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
import shutil

# Load env
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")
# print("MURF_API_KEY:", MURF_API_KEY)

# FastAPI app
app = FastAPI()

# Mount static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
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
        "api-key": MURF_API_KEY
    }
    body = {
        "text": payload.text,
        "voiceId": payload.voice_id,
        "format": "mp3"
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=headers, json=body)
        if res.status_code == 200:
            data = res.json()
            print("Murf response:", data)  # keep for debug
            audio_url = data.get("audioFile") or data.get("audioUrl") or data.get("audio_url")
            if audio_url:
                return {"audio_url": audio_url}
            else:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Request succeeded, but no audio URL found. Check Murf's response format.",
                        "murf_response": data
                    }
                )
        else:
            return JSONResponse(status_code=res.status_code, content={"error": res.text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_kb": round(os.path.getsize(file_location) / 1024, 2)
    }