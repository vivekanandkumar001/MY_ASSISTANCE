# ai_core/utils.py
import os, json, logging
from datetime import datetime

def ensure_dirs():
    for p in ["data/scripts","data/uploads","data/thumbnails","data/voice_clips","logs","youtube/tokens"]:
        os.makedirs(p, exist_ok=True)

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def log(msg):
    os.makedirs("logs", exist_ok=True)
    s = f"{datetime.utcnow().isoformat()} | {msg}"
    with open("logs/activity.log","a",encoding="utf-8") as f:
        f.write(s + "\n")
    print(s)
