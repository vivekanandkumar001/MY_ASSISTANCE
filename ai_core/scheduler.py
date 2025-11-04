import yaml, os, time
from ai_core.content_generator import generate_content_plan
from ai_core.auto_voiceover import generate_voice
from ai_core.thumbnail_creator import create_thumbnail
from ai_core.video_editor import create_video
from ai_core.ai_uploader import upload_video

def process_channel(name, data):
    print(f"\n🎬 Processing Channel: {name}")

    script, topic = generate_content_plan(name, data["niche"])
    voice = generate_voice(script)
    thumb = create_thumbnail(topic, name)
    video = create_video(voice, thumb, name)

    description = f"{topic}\n\n#AI #Facts #Motivation #Sanatan #Science"
    token_path = f"youtube/tokens/token_{name}.json"

    upload_video(video, topic, description, thumb, token_path)
    print(f"✅ Uploaded Successfully: {topic}")

def run_daily():
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    for ch, info in config["channels"].items():
        process_channel(ch, info)

if __name__ == "__main__":
    print("🚀 MY_ASSISTANCE v2 - Auto Mode ON")
    while True:
        run_daily()
        print("\n🕒 Sleeping for 24 hours...\n")
        time.sleep(86400)
