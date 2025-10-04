from gtts import gTTS

def generate_tts_response(text: str, filename: str = "response.mp3") -> str:
    tts = gTTS(text)
    filepath = f"/tmp/{filename}"
    tts.save(filepath)
    return filepath