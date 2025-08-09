from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import shutil
from fastapi.middleware.cors import CORSMiddleware
import assemblyai as aai
from routes import generate_audio, transcribe_audio, upload_audio, echo_audio, llm_query
# Load env
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")
# print("MURF_API_KEY:", MURF_API_KEY)

# FastAPI app
app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your AssemblyAI API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


# Mount static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



app.include_router(generate_audio.router)
app.include_router(upload_audio.router)
app.include_router(transcribe_audio.router)
app.include_router(echo_audio.router)
app.include_router(llm_query.router)