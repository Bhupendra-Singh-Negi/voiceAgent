from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice_id: str = "en-US-terrell"
