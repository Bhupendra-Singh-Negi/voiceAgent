from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    upload_dir = "transcribe"
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": os.path.getsize(file_location)
    }
    
