# youtube/dry_upload_test.py
from ai_core.ai_uploader import upload_video
import os, json

def dry_run(token_path):
    # create a tiny dummy mp4 to test auth + upload permissions in 'private' mode
    test_video = "data/uploads/dummy_test.mp4"
    open(test_video, "wb").write(b"TEST")  # small file placeholder
    title = "TEST UPLOAD - Dry Run (Keep private)"
    desc = "Dry run upload test. Delete after verification."
    thumb = None
    print("Attempting dry upload (privacy=private)...")
    vid = upload_video(test_video, title, desc, thumb, token_path)
    print("Returned video id:", vid)

if __name__ == "__main__":
    # run for one channel token as test
    path = "youtube/tokens/token_The_AI_Lab_Presents.json"
    if not os.path.exists(path):
        print("Token missing:", path)
    else:
        dry_run(path)
