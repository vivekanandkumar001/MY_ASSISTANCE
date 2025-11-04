import os
import streamlit as st
import requests

st.set_page_config(
    page_title="MY_ASSISTANCE — Smart AI Automation",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MY_ASSISTANCE — Smart AI Automation")
st.markdown("Your personal AI system that creates, automates, and uploads content!")

# =========================
# 🧩 Helper: Load Secrets
# =========================
def load_secret(name):
    return os.getenv(name)

# =========================
# 🧠 Groq-based Script Generator (Free)
# =========================
def generate_youtube_script(topic):
    """Generates a Hindi YouTube script using Groq Llama model (free)."""
    try:
        groq_api_key = load_secret("groq_api_key")
        if not groq_api_key:
            return "⚠️ Missing Groq API key. Please set it in Hugging Face secrets."

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-70b-versatile",  # ✅ Free & current Groq model
            "messages": [
                {"role": "system", "content": "You are a talented Hindi YouTube scriptwriter who writes engaging and emotionally rich video scripts."},
                {"role": "user", "content": f"Write a detailed 10-minute Hindi YouTube script about {topic}. Use storytelling style and emotions."}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        if "error" in result:
            return f"❌ Groq API Error: {result['error']['message']}"
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error generating script: {str(e)}"

# =========================
# 🧭 Streamlit UI
# =========================
st.subheader("🎬 YouTube Content Automation")

topic = st.text_input("Enter your video topic:", placeholder="e.g. 'Shri Krishna’s hidden wisdom for AI age'")

if st.button("🚀 Generate Script"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating your Hindi YouTube script (Groq)..."):
            script = generate_youtube_script(topic)
        st.text_area("📝 Generated Script", script, height=400)

# =========================
# 🚀 Future Upload Automation
# =========================
st.subheader("📤 YouTube Auto Upload (Coming Soon)")
st.info("This feature will automatically upload your generated video or audio to YouTube using OAuth2 credentials.")

# =========================
# 🧾 Footer
# =========================
st.markdown("---")
st.markdown("Made by **Vivekanand Kumar 🚀** | Powered by **Groq & Hugging Face**")
