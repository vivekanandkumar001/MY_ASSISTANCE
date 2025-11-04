import os
import streamlit as st
import requests
from openai import OpenAI

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
# 🧠 YouTube Script Generator
# =========================
def generate_youtube_script(topic):
    """Generates a Hindi YouTube script using OpenAI."""
    try:
        api_key = load_secret("openai_api_key")
        if not api_key:
            return "⚠️ Missing OpenAI API key. Please set it in Hugging Face secrets."

        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ Updated model (lightweight & latest)
            messages=[
                {"role": "system", "content": "You are a creative Hindi YouTube scriptwriter."},
                {"role": "user", "content": f"Write a detailed 10-minute Hindi YouTube script on: {topic}"}
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error generating script: {str(e)}"


# =========================
# ⚙️ Groq API Integration
# =========================
def test_groq_integration():
    """Tests Groq API with llama-3.1-70b-versatile."""
    try:
        groq_api_key = load_secret("groq_api_key")
        if not groq_api_key:
            return {"error": "Missing Groq API key. Please set it in Hugging Face secrets."}

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-70b-versatile",  # ✅ Updated & available model
            "messages": [
                {"role": "system", "content": "You are a powerful AI assistant that writes creative Hindi YouTube scripts."},
                {"role": "user", "content": "Write a short motivational script about how AI is revolutionizing content creation."}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        if "error" in result:
            return result
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return {"error": str(e)}


# =========================
# 🧭 Streamlit UI
# =========================
st.subheader("🎬 YouTube Content Automation")

topic = st.text_input("Enter your video topic:", placeholder="e.g. 'The hidden science of dreams'")

if st.button("🚀 Generate Script"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating your Hindi YouTube script..."):
            script = generate_youtube_script(topic)
        st.text_area("📝 Generated Script", script, height=400)


# =========================
# 💡 Groq Integration Section
# =========================
st.subheader("🧩 Advanced AI (Groq Integration)")

if st.button("Run Groq Test"):
    with st.spinner("🧠 Testing Groq model..."):
        result = test_groq_integration()
    st.success("✅ Groq Response:")
    st.json(result)


# =========================
# 🚀 Future Upload Automation
# =========================
st.subheader("📤 YouTube Auto Upload (Coming Soon)")
st.info("This feature will automatically upload your generated video or audio to YouTube using OAuth2 credentials.")


# =========================
# 🧾 Footer
# =========================
st.markdown("---")
st.markdown("Made by **Vivekanand Kumar 🚀** | Powered by **OpenAI, Hugging Face & Groq**")
