import json
import os
from datetime import datetime
import streamlit as st
from ollama import Client
from event_data import EVENT_NAME, VENUE_INFO, FAQS, SCHEDULE, SPEAKERS

from dotenv import load_dotenv
load_dotenv()


# Page config
st.set_page_config(page_title=f"{EVENT_NAME} Assistant", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #7c6af7;
    --accent2:   #f97316;
    --text:      #e8e8f0;
    --muted:     #6b6b80;
    --user-bg:   #16161f;
    --ai-bg:     #0f0f1a;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
}
[data-testid="stMain"] { background: var(--bg) !important; }
#MainMenu, footer { visibility: hidden; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
    min-width: 320px !important;
    max-width: 320px !important;
    width: 320px !important;
    transform: none !important;
    visibility: visible !important;
}
[data-testid="stSidebar"] * { font-family: 'Space Mono', monospace !important; }

/* ── Header: keep it structurally present but visually blend it into the background ── */

[data-testid="stHeader"] {
    background: var(--bg) !important;
    box-shadow: none !important;
}
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
    visibility: hidden !important;
}

.app-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #7c6af7 0%, #f97316 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.app-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.model-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,106,247,0.15), rgba(249,115,22,0.1));
    border: 1px solid rgba(124,106,247,0.3);
    color: #a89cf7;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 4px 10px;
    border-radius: 3px;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}

[data-testid="stChatMessage"] {
    border-radius: 8px;
    border: 1px solid var(--border);
    margin-bottom: 12px;
    padding: 4px 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.7;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--user-bg);
    border-left: 3px solid var(--accent);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: var(--ai-bg);
    border-left: 3px solid var(--accent2);
}

[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.15) !important;
}

[data-testid="stSelectbox"] > div > div {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-size: 0.75rem !important;
}
[data-testid="stTextArea"] textarea {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-size: 0.75rem !important;
}
[data-testid="stTextArea"] textarea:focus { border-color: var(--accent) !important; }

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    font-size: 0.7rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;}

.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
.stop-btn > button {
    border-color: rgba(249,115,22,0.5) !important;
    color: var(--accent2) !important;
    animation: pulse-border 1.5s ease-in-out infinite;
}
.stop-btn > button:hover {
    background: rgba(249,115,22,0.1) !important;
    border-color: var(--accent2) !important;
}
@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 0 0 rgba(249,115,22,0.3); }
    50%       { box-shadow: 0 0 0 4px rgba(249,115,22,0.0); }
}

/* Suggested-prompt chips shown on first load */
.suggested-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 1.5rem 0 0.75rem 0;
}
.suggested-grid .stButton > button {
    text-align: left !important;
    padding: 0.9rem 1rem !important;
    height: auto !important;
    white-space: normal !important;
    font-size: 0.8rem !important;
    letter-spacing: normal !important;
    text-transform: none !important;}

hr { border-color: var(--border) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""", unsafe_allow_html=True)


FALLBACK_MESSAGE = ("❌ I'm having trouble reaching my brain right now. "
    "Please ask a volunteer nearby, or check the printed schedule at the help desk.")


QUICK_ACTIONS = {"📅 My next session?": "What's my next session?",
    "📍 Venue / help desk?": "Where is the venue and help desk?",
    "📶 WiFi info?": "What is the WiFi SSID and password?",
    "🎓 Certificate process?": "How do I get my certificate?",
    "🍽️ Is food provided?": "Is food provided at the summit?",
    "🤝 Hackathon Queries?": "Hackathon Team Information?"}


#========== Ollama Cloud client ==========
@st.cache_resource
def get_client():
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        return None
    return Client(host="https://ollama.com", headers={"Authorization": f"Bearer {api_key}"})


# ── Event grounding ────
def build_system_prompt(selected_track: str | None) -> dict:
    """Builds the system message that grounds the assistant in real event data."""
    context = {
        "event_name": EVENT_NAME,
        "venue_info": VENUE_INFO,
        "faqs": FAQS,
        "schedule": SCHEDULE,
        "speakers": SPEAKERS,
        "current_time": datetime.now().strftime("%H:%M"),
        "participant_selected_track": selected_track or "not specified"}
    
    content = ("You are the official AI assistant for IBM Z Summit 2026, a student tech "
        "summit. Answer participant questions ONLY using the EVENT_DATA JSON below. "
        "Be warm, concise, and practical — most participants are asking on their phone between sessions.\n\n"
        "Rules:\n"
        "1. If the answer is not in EVENT_DATA, say clearly: "
        "\"I don't have that info — please ask a volunteer or check the help desk!\" "
        "Do NOT guess or invent details (rooms, times, names, policies).\n"
        "2. If asked about 'my next session' or similar, use current_time and the "
        "participant's selected track (if given) to figure out the next upcoming "
        "session from the schedule.\n"
        "3. Keep answers short — 2-4 sentences unless a list is clearly needed.\n\n"
        f"EVENT_DATA:\n{json.dumps(context, indent=2)}")
    
    return {"role": "system", "content": content}


# Session state 
for key, val in [("messages", []), ("streaming", False),
                  ("stop_signal", False), ("token_count", 0),
                  ("sidebar_open", True)]:
    if key not in st.session_state:
        st.session_state[key] = val

if not st.session_state.sidebar_open:
    st.markdown("<style>[data-testid='stSidebar']{ display: none !important; }</style>",
        unsafe_allow_html=True)


# ====================Sidebar ========================
with st.sidebar:
    st.markdown("### ✦ CONFIGURATION")
    st.markdown("---")

    selected_model = "gpt-oss:20b"

    tracks = sorted({s["track"] for s in SCHEDULE})
    selected_track = st.selectbox("Your track (optional)",
        options=["Not specified"] + tracks,
        help="Used to personalize 'what's my next session' answers.")
    
    if selected_track == "Not specified":
        selected_track = None

    st.markdown("---")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.token_count = 0
        st.rerun()

    st.markdown("---")
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.65rem;color:#6b6b80;line-height:2.2'>
    ◦ MESSAGES &nbsp;&nbsp; {len(st.session_state.messages)}<br>
    ◦ TOKENS &nbsp;&nbsp;&nbsp;&nbsp; ~{st.session_state.token_count}
    </div>
    """, unsafe_allow_html=True)


# ================HEADER ==========================
toggle_col, _ = st.columns([0.06, 0.94])
with toggle_col:
    if st.button("☰", key="sidebar_toggle", help="Show/hide sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

st.markdown(f'<div class="app-title">{"Zenith".upper()}</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Your AI guide to IBM Z Summit 2026 · v1.0</div>', unsafe_allow_html=True)
st.markdown(f'<div class="model-badge">▶ &nbsp;{selected_model}</div>', unsafe_allow_html=True)

client = get_client()
if client is None:
    st.warning("⚠️ No Ollama Cloud API key configured. Add `OLLAMA_API_KEY`")

# =============Chat history =========================
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ================ First-load suggested-question grid ==========================
main_action_clicked = None
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"Hi! 👋 I'm your assistant for **{EVENT_NAME}**. Ask me anything, or tap a question below to get started.")

    st.markdown('<div class="suggested-label">Frequently asked</div>', unsafe_allow_html=True)
    st.markdown('<div class="suggested-grid">', unsafe_allow_html=True)
    grid_cols = st.columns(2)
    for i, (label, question) in enumerate(QUICK_ACTIONS.items()):
        with grid_cols[i % 2]:
            if st.button(label, use_container_width=True, key=f"main_{i}"):
                main_action_clicked = question
    st.markdown('</div>', unsafe_allow_html=True)

# ── Stop button placeholder ───
stop_placeholder = st.empty()

# ── Chat input ───
user_typed = st.chat_input("Ask anything about the summit…", disabled=st.session_state.streaming)
prompt = main_action_clicked or user_typed

if prompt and client is not None:
    system_msg = build_system_prompt(selected_track)
    messages_to_send = [system_msg] + st.session_state.messages + [{"role": "user", "content": prompt}]

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    st.session_state.streaming = True
    st.session_state.stop_signal = False

    with stop_placeholder.container():
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("⏹  Stop generating", key="stop_btn"):
            st.session_state.stop_signal = True
        st.markdown('</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="🤖"):
        box = st.empty()
        full_res = ""
        stopped = False

        try:
            for part in client.chat(selected_model, messages=messages_to_send, stream=True):
                if st.session_state.stop_signal:
                    stopped = True
                    break
                chunk = part.message.content or ""
                full_res += chunk
                st.session_state.token_count += len(chunk.split())
                box.markdown(full_res + " ▌")

            if stopped:
                full_res += "\n\n`⏹ Stopped by user`"

            box.markdown(full_res or FALLBACK_MESSAGE)

        except Exception:
            full_res = FALLBACK_MESSAGE
            box.warning(full_res)

    st.session_state.messages.append({"role": "assistant", "content": full_res})
    st.session_state.streaming = False
    st.session_state.stop_signal = False
    stop_placeholder.empty()
    st.rerun()
elif prompt and client is None:
    st.error("Add your OLLAMA_API_KEY before chatting.")
