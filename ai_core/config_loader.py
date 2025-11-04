import os
import json

def load_secrets():
    """
    Load all secret keys automatically from either:
    1. Hugging Face Space environment variables (when deployed)
    2. Local config/secrets.json file (for local development)
    """

    # Priority 1 — Environment variables (for HF Spaces)
    secrets = {
        "huggingface_token": os.getenv("HF_TOKEN"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "groq_api_key": os.getenv("GROQ_API_KEY"),
        "youtube_client_id": os.getenv("YOUTUBE_CLIENT_ID"),
        "youtube_client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
        "google_project_id": os.getenv("GOOGLE_PROJECT_ID"),
    }

    # Check if any key missing
    if not all(secrets.values()):
        # Priority 2 — Local config file fallback
        try:
            with open("config/secrets.json", "r") as f:
                local_secrets = json.load(f)
                # Fill missing keys only
                for key, value in local_secrets.items():
                    if not secrets.get(key):
                        secrets[key] = value
        except FileNotFoundError:
            print("⚠️ Warning: config/secrets.json not found. Please add it or set environment variables.")
        except json.JSONDecodeError:
            print("⚠️ Warning: config/secrets.json is not valid JSON. Please fix formatting.")

    # Final check for missing keys
    missing_keys = [k for k, v in secrets.items() if not v]
    if missing_keys:
        print(f"⚠️ Missing secrets: {', '.join(missing_keys)}")
    else:
        print("✅ All secrets loaded successfully!")

    return secrets
