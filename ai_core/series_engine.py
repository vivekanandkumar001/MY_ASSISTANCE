# ai_core/series_engine.py
import os, json, time, datetime, random
from ai_core.tts_ai import generate_long_voice
from ai_core.movie_generator import create_and_publish_episode, build_movie

# helper: simple HF text generator stub (you can replace model)
def hf_generate(prompt, hf_token=None):
    # If HF token not set, fallback to simple template
    if not hf_token:
        return "Ek kahani: " + prompt
    # (If HF token provided, call HF inference API here)
    return "Generated long screenplay for: " + prompt

SERIES_NAME = "Warriors of Dharma"
EPISODE_COUNT = 100

def generate_episode_script(ep_no, hf_token=None):
    hero = random.choice(["Veer Bhadr","Rishi Kaushik","Mahaveer Satyajit","Bharat Arjun"])
    title = f"Episode {ep_no}: Rise of {hero}"
    prompt = f"Write detailed Hinglish screenplay for '{title}' in cinematic style, length ~{8} minutes."
    text = hf_generate(prompt, hf_token)
    os.makedirs("data/scripts", exist_ok=True)
    path = f"data/scripts/{SERIES_NAME}_Ep{ep_no}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path, title

def generate_movie_script(week_no, hf_token=None):
    title = f"{SERIES_NAME} Movie Week {week_no}"
    prompt = f"Write a cinematic Hinglish screenplay for a movie titled '{title}', length ~45 minutes."
    text = hf_generate(prompt, hf_token)
    os.makedirs("data/scripts", exist_ok=True)
    path = f"data/scripts/{SERIES_NAME}_Movie_Week{week_no}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path, title

def run_daily_episode(ep_no, hf_token=None, auto_publish=True):
    script_path, title = generate_episode_script(ep_no, hf_token)
    # create & publish
    create_and_publish_episode(ep_no, auto_publish=auto_publish)
    return title

def run_weekly_movie(week_no, hf_token=None):
    movie_script, title = generate_movie_script(week_no, hf_token)
    build_movie(week_no)
    return title

if __name__ == "__main__":
    # Example local run to generate an episode (useful for first-time testing)
    ep_index = 1
    for ep in range(1, 4):  # test generate 3 episodes quickly (for dev)
        print(f"Generating test episode {ep}")
        run_daily_episode(ep, hf_token=None, auto_publish=False)
        time.sleep(2)
    print("Test run complete.")
