from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import assemblyai as aai
import os
import requests
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
MURF_VOICE_ID = "en-US-terrell"  # Or any available Murf voice

@router.post("/tts/echo")
async def tts_echo(audio_file: UploadFile = File(...)):
    try:
        # 1. Transcribe
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)
        print("Transcript:", transcript)
        if transcript.status == aai.TranscriptStatus.error:
            print("Transcription error:", transcript.error)
            return JSONResponse(status_code=500, content={"error": f"Transcription failed: {transcript.error}"})
        text = transcript.text
        if not text:
            print("No speech detected.")
            return JSONResponse(status_code=400, content={"error": "No speech detected in the audio."})

        # 2. Murf API request
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {"text": text, "voiceId": "en-US-terrell", "format": "mp3"}
        print("Sending payload to Murf:", payload)
        response = requests.post(url, json=payload, headers=headers)
        print("Murf status:", response.status_code, "Murf response:", response.text)
        response.raise_for_status()
        data = response.json()
        audio_url = data.get("audioFile")
        if audio_url:
            return JSONResponse(content={"audio_url": audio_url, "text": text})
        else:
            print("No audioFile in Murf response:", data)
            return JSONResponse(status_code=500, content={"error": "Murf API did not return an audio file.", "details": data})

    except Exception as e:
        import traceback
        print("Exception in /tts/echo:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})