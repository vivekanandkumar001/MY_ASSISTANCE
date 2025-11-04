from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(title, channel):
    os.makedirs("data/thumbnails", exist_ok=True)
    img = Image.new('RGB', (1280, 720), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 300), title, fill=(255, 255, 0), font=font)
    path = f"data/thumbnails/{channel}_{title.replace(' ', '_')}.jpg"
    img.save(path)
    return path
