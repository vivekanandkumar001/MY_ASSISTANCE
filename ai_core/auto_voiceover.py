from gtts import gTTS
import os

def generate_voice(script_path, language="hi"):
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()

    tts = gTTS(text=text, lang=language, slow=False)
    voice_path = script_path.replace("scripts", "voice_clips").replace(".txt", ".mp3")
    os.makedirs(os.path.dirname(voice_path), exist_ok=True)
    tts.save(voice_path)
    return voice_path
