import streamlit as st
from ai_core.config_loader import load_secrets
import openai
import requests

# -------------------- #
# 🔐 Load all secrets
# -------------------- #
secrets = load_secrets()

# Set environment tokens
openai.api_key = secrets.get("openai_api_key")
HF_TOKEN = secrets.get("huggingface_token")
GROQ_API_KEY = secrets.get("groq_api_key")
YOUTUBE_CLIENT_ID = secrets.get("youtube_client_id")
YOUTUBE_CLIENT_SECRET = secrets.get("youtube_client_secret")
GOOGLE_PROJECT_ID = secrets.get("google_project_id")

# -------------------- #
# ⚙️ Streamlit UI Setup
# -------------------- #
st.set_page_config(page_title="MY_ASSISTANCE AI", layout="wide")

st.title("🤖 MY_ASSISTANCE — Smart AI Automation")
st.markdown("Your personal AI system that creates, automates, and uploads content!")

# Sidebar Info
st.sidebar.title("Settings")
st.sidebar.info("Configure and control your AI Assistant here.")

# -------------------- #
# 🎥 AI YouTube Assistant Section
# -------------------- #
st.header("🎬 YouTube Content Automation")

topic = st.text_input("Enter your video topic:", placeholder="e.g. 'The hidden science of dreams'")
generate_btn = st.button("🚀 Generate Script")

if generate_btn:
    if not openai.api_key:
        st.error("⚠️ OpenAI API key missing! Please add it to your Hugging Face Secrets.")
    else:
        with st.spinner("🤖 Generating script..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional Hindi YouTube scriptwriter."},
                        {"role": "user", "content": f"Create a detailed 10-minute Hindi YouTube script on: {topic}"}
                    ],
                    temperature=0.8
                )
                script = response.choices[0].message["content"]
                st.subheader("📜 Generated Script:")
                st.write(script)

                # Option to save
                with open("generated_script.txt", "w", encoding="utf-8") as f:
                    f.write(script)
                st.success("✅ Script saved successfully as generated_script.txt")
            except Exception as e:
                st.error(f"Error generating script: {e}")

# -------------------- #
# 🧠 Groq AI Assistant (optional)
# -------------------- #
st.header("🧩 Advanced AI (Groq Integration)")

if st.button("Run Groq Test"):
    if not GROQ_API_KEY:
        st.error("⚠️ Groq API key missing! Add it to your secrets.")
    else:
        st.info("🔄 Testing Groq model...")
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            data = {"model": "mixtral-8x7b", "prompt": "Hello Groq!", "temperature": 0.7}
            response = requests.post("https://api.groq.com/v1/completions", json=data, headers=headers)
            st.success("✅ Groq Response:")
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------- #
# 📺 YouTube Upload (Future Integration)
# -------------------- #
st.header("📤 YouTube Auto Upload (Coming Soon)")
st.info("This feature will automatically upload your generated video or audio to YouTube using OAuth2 credentials.")

st.caption("Made by Vivekanand Kumar 🚀 | Powered by OpenAI, Hugging Face & Groq")

