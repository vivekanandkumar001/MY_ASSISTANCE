# ai_core/movie_generator.py
import os, datetime, json, time
from ai_core.animation_ai import create_animated_scenes
from ai_core.tts_ai import generate_long_voice
from ai_core.bgm_generator import add_bgm
from ai_core.movie_publisher import upload_episode

# Configurable lengths
EPISODE_DURATION_MIN = 8   # target minutes for episode (used by external renderer)
MOVIE_DURATION_MIN = 45    # movie minutes

SERIES_NAME = "Warriors of Dharma"

def build_episode_video(script_path, ep_no):
    # 1) generate long voiceover
    voice_path = generate_long_voice(script_path)
    # 2) create animated scenes (placeholder / external API)
    raw_video = create_animated_scenes(script_path)  # returns mp4 path
    # 3) add bgm & finalize
    final_video = add_bgm(raw_video)
    # 4) return final video path
    return final_video

def create_and_publish_episode(ep_no, auto_publish=True):
    # create prompt/script using series_engine helper (series_engine will call this)
    script_path = f"data/scripts/{SERIES_NAME}_Ep{ep_no}.txt"
    if not os.path.exists(script_path):
        raise FileNotFoundError(script_path)
    title = f"{SERIES_NAME} - Episode {ep_no}"
    # build video
    final_video = build_episode_video(script_path, ep_no)
    # choose thumbnail (could be auto-generated)
    thumb = f"data/thumbnails/{SERIES_NAME}_Ep{ep_no}.jpg"
    # upload
    description = f"{title}\n\nA story from the hidden pages of Bharat. #SanatanChronicles"
    upload_episode(final_video, title, description, thumb, "Sanatan_Chronicles")
    return final_video

def build_movie(week_no):
    # Collect multiple episode scripts or generate a new long script via HF
    movie_script = f"data/scripts/{SERIES_NAME}_Movie_Week{week_no}.txt"
    # If script not exists, series_engine will generate it
    if not os.path.exists(movie_script):
        raise FileNotFoundError(movie_script)
    # build voice + scenes
    voice = generate_long_voice(movie_script)
    raw_video = create_animated_scenes(movie_script)  # longer render
    final_video = add_bgm(raw_video)
    # upload as movie
    title = f"{SERIES_NAME} — Movie Week {week_no}"
    thumb = f"data/thumbnails/{SERIES_NAME}_Movie_Week{week_no}.jpg"
    upload_episode(final_video, title, movie_script, thumb, "Sanatan_Chronicles")
    return final_video
