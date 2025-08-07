from fastapi import FastAPI, APIRouter, UploadFile, File
import assemblyai as aai
import os
from starlette.concurrency import run_in_threadpool

router = APIRouter()

@router.post("/transcribe/file")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_data = await file.read()

    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.slam_1)

    # Run blocking function in threadpool
    transcript = await run_in_threadpool(transcriber.transcribe, audio_data, config)

    return {
        "filename": file.filename,
        "text": transcript.text
    }
