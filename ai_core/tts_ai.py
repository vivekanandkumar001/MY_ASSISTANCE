from gtts import gTTS
import os

def generate_long_voice(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"🔊 Generating voiceover for {os.path.basename(script_path)}")
    tts = gTTS(text, lang="hi")
    audio_path = f"data/voice_clips/{os.path.basename(script_path).replace('.txt', '.mp3')}"
    tts.save(audio_path)
    return audio_path
