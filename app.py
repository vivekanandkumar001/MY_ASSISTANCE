# app.py — Streamlit control UI for MY_ASSISTANCE
import streamlit as st
import os, shutil, yaml, requests, json, glob, time
from pathlib import Path

# ---------- CONFIG ----------
REPO_OWNER = os.getenv("REPO_OWNER", "vivekanandkumar001")
REPO_NAME = os.getenv("REPO_NAME", "MY_ASSISTANCE")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE", "ci_schedule.yml")  # GitHub workflow filename
GITHUB_API = "https://api.github.com"

# Secrets expected in Hugging Face Space Settings -> Repository secrets
# - GITHUB_PAT : Personal access token (repo/workflow dispatch permission)
# - HF_TOKEN (optional)
# - YOUTUBE_TOKENS (optional big JSON)
# Make sure these are set in HF Space settings.

# ---------- HELPERS ----------
def read_yaml(path):
    if not os.path.exists(path): return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def list_scripts():
    os.makedirs("data/scripts", exist_ok=True)
    return sorted(glob.glob("data/scripts/*.txt"))

def read_file(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def ensure_dirs():
    for p in ["data/approved","data/scripts","data/thumbnails","data/uploads","logs"]:
        os.makedirs(p, exist_ok=True)

def move_to_approved(script_path):
    ensure_dirs()
    base = os.path.basename(script_path)
    dest = os.path.join("data/approved", base)
    shutil.copy2(script_path, dest)
    return dest

def trigger_github_workflow(mode="daily", episode_file=None):
    pat = st.secrets.get("GITHUB_PAT", None)
    if not pat:
        return False, "GITHUB_PAT secret missing in Space settings."

    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "ref": "main",
        "inputs": {
            "mode": mode,
            "episode_file": episode_file or ""
        }
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code in (204, 201):
        return True, "Workflow dispatched successfully."
    else:
        return False, f"Failed to dispatch: {r.status_code} {r.text}"

# ---------- UI ----------
st.set_page_config(page_title="MY_ASSISTANCE Control Panel", layout="wide")
st.title("🤖 MY_ASSISTANCE — Control & Preview")
st.markdown("Use this UI to preview scripts, approve them, and trigger GitHub Actions (which runs the generator & uploader).")

ensure_dirs()

# Left: settings and trigger
with st.sidebar:
    st.header("Quick Actions")
    if st.button("🔄 Refresh script list"):
        st.experimental_rerun()

    st.markdown("**Trigger GitHub workflow**")
    mode = st.selectbox("Mode to run", ["daily","weekly","single"], index=0)
    ep_file_select = None
    if mode == "single":
        scripts = [""] + [os.path.basename(p) for p in list_scripts()]
        ep_file_select = st.selectbox("Select script to run (single)", scripts)
    if st.button("▶ Trigger workflow now"):
        ep = ep_file_select if ep_file_select else None
        ok, msg = trigger_github_workflow(mode=mode, episode_file=ep)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    st.markdown("---")
    st.markdown("**Settings**")
    conf = read_yaml("config/settings.yaml")
    st.code(conf if conf else "settings.yaml not found or empty")
    st.markdown("**Secrets** (check HF Space → Settings → Repository secrets)")
    st.write("- GITHUB_PAT: required")
    st.write("- HF_TOKEN: optional (for HF generation)")
    st.write("- YOUTUBE tokens: upload tokens for channels")

# Right: scripts list + preview + approve
st.subheader("Generated scripts (data/scripts)")
scripts = list_scripts()
if not scripts:
    st.info("No scripts found in data/scripts. Run generator or push scripts into this folder.")
else:
    for s in scripts[::-1]:  # newest first
        cols = st.columns([1,4,1])
        with cols[0]:
            st.write(os.path.basename(s))
            st.write(f"{time.ctime(os.path.getmtime(s))}")
            if st.button("Preview", key=f"preview_{s}"):
                st.session_state["preview"] = s
            if st.button("Approve (copy)", key=f"approve_{s}"):
                dest = move_to_approved(s)
                st.success(f"Copied to approved: {dest}")
        with cols[1]:
            st.markdown("---")
            snippet = read_file(s)
            st.code(snippet[:4000])  # show up to 4000 chars
        with cols[2]:
            # Thumbnail preview if exists
            thumb_path = os.path.join("data/thumbnails", os.path.basename(s).replace(".txt",".jpg"))
            if os.path.exists(thumb_path):
                st.image(thumb_path, width=220)
            else:
                st.write("No thumbnail yet")

# Preview pane for single script
if st.session_state.get("preview"):
    p = st.session_state["preview"]
    st.markdown("### Preview: " + os.path.basename(p))
    st.code(read_file(p))
    if st.button("🔁 Re-generate thumbnail for preview"):
        # touch a thumbnail creation (simple placeholder)
        from ai_core.thumbnail_creator import create_thumbnail
        title = os.path.basename(p).replace(".txt","")
        new_thumb = create_thumbnail(title, "Preview")
        st.image(new_thumb)
        st.success("Thumbnail created for preview.")

st.markdown("---")
st.write("Logs:")
if os.path.exists("logs/activity.log"):
    with open("logs/activity.log","r",encoding="utf-8") as f:
        lines = f.readlines()[-200:]  # show last 200 lines
        st.code("".join(lines[-200:]))
else:
    st.write("No logs yet.")
