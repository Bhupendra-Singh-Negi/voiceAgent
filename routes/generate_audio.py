from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import assemblyai as aai
import os
import httpx
from models.tts_request import TTSRequest


router = APIRouter()
app=FastAPI()
@router.post("/generate-audio")
async def generate_audio(payload: TTSRequest):
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": os.getenv("MURF_API_KEY")
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
