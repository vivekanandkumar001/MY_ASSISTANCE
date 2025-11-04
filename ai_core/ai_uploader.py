from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os, json, time

def upload_video(video_path, title, description, thumbnail, token_path):
    with open(token_path, "r", encoding="utf-8") as f:
        creds_data = json.load(f)

    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(creds_data)
    youtube = build("youtube", "v3", credentials=creds)

    print(f"🚀 Uploading: {title}")
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "24"
        },
        "status": {"privacyStatus": "public"}
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")
    print("✅ Upload complete!")

    video_id = response["id"]
    youtube.thumbnails().set(videoId=video_id, media_body=thumbnail).execute()
    print(f"📸 Thumbnail applied to {title}")
    return video_id
