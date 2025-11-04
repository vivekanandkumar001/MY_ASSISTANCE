from ai_core.ai_uploader import upload_video

def upload_episode(video, title, description, thumbnail, channel):
    token_path = f"youtube/tokens/token_{channel}.json"
    upload_video(video, title, description, thumbnail, token_path)
