from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def create_video(voice_path, thumbnail_path, channel):
    os.makedirs("data/uploads", exist_ok=True)
    image_clip = ImageClip(thumbnail_path).set_duration(30)
    audio_clip = AudioFileClip(voice_path)
    video = image_clip.set_audio(audio_clip)
    output = f"data/uploads/{channel}_video.mp4"
    video.write_videofile(output, fps=24)
    return output
