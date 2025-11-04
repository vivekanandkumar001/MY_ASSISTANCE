import random, datetime, os, requests, json

HF_API = None
if os.path.exists("config/api_keys.json"):
    with open("config/api_keys.json", "r") as f:
        HF_API = json.load(f).get("huggingface_token")

def hf_generate(prompt):
    if not HF_API:
        return f"[Local Script] {prompt}"
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {HF_API}"}
    payload = {"inputs": prompt}
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        return data[0]["generated_text"] if isinstance(data, list) else str(data)
    except Exception as e:
        return f"Error generating text: {e}"

def get_trending_topic(niche):
    topics = {
        "AI & Tech": ["AI changing the world", "Future of Robotics", "ChatGPT Secrets"],
        "Facts & Mysteries": ["Unsolved mysteries of India", "Dark secrets of ocean"],
        "Psychology & Motivation": ["Power of Subconscious Mind", "Daily motivation hacks"],
        "Science & Universe": ["Time travel explained", "Black holes secrets"],
        "Hindu Mythology (Animated Series)": ["Story of Hanuman", "Birth of Narasimha"]
    }
    return random.choice(topics.get(niche, ["AI Innovations"]))

def generate_script(topic, niche):
    prompt = f"Write a 1-minute Hinglish YouTube video script about '{topic}' in niche '{niche}'."
    text = hf_generate(prompt)
    return f"# {topic}\n\n{text}"

def generate_content_plan(channel, niche):
    os.makedirs("data/scripts", exist_ok=True)
    topic = get_trending_topic(niche)
    script = generate_script(topic, niche)
    filename = f"{channel}_{datetime.date.today()}_{topic.replace(' ', '_')}.txt"
    filepath = os.path.join("data/scripts", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script)
    return filepath, topic
