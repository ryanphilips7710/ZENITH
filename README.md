# README — Zenith: IBM Z Summit 2026 AI Assistant

An AI-powered chat assistant built with Python and Streamlit to help participants navigate IBM Z Summit 2026, grounded in real event data and served via Ollama Cloud.

Submitted for: **IBM Z Student Club — Technical Team Recruitment, Round 1**

---

## Project Overview

Zenith is a conversational assistant that answers participant questions about IBM Z Summit 2026 — schedule, venue, speakers, certificates, and general logistics — through a chat interface accessible from any participant's phone or laptop. Instead of relying on volunteers to repeatedly answer the same questions throughout the day, participants can ask Zenith directly and get an instant, accurate answer grounded in the actual event data.

The assistant is built as a single Streamlit application, deployable as a public web link, with no backend server or database required beyond the structured event data bundled with the app itself.

## Problem Statement

IBM Z Summit 2026 expects 500+ participants across technical workshops, hands-on labs, a hackathon, guest speaker sessions, networking activities, and competitions. With an event of this scale, several operational pain points emerge:

- Volunteers are repeatedly asked the same questions (schedule, venue, WiFi, certificates), pulling them away from higher-value tasks.
- Printed schedules and static FAQ sheets go stale the moment something changes and don't scale to hundreds of simultaneous questions.
- Participants have no single, always-available source of truth for logistics during the event.

**Chosen problem area:** AI Powered Event Assistant — building a reliable, always-on assistant that answers participant questions instantly, freeing up volunteer time and improving the overall participant experience.

## Features

- **Conversational chat interface** with streaming responses (answers appear token-by-token, not all at once) and a "Stop generating" control to cancel a response mid-stream.
- **Grounded, non-hallucinating answers** — the assistant is instructed to answer only from real event data (schedule, venue info, FAQs, speaker bios) and to say plainly "I don't have that info" rather than invent details like room numbers or times.
- **Personalized schedule lookup** — participants can optionally select their track, and ask things like "what's my next session?"; the assistant resolves this against the current time and the live schedule.
- **First-load suggested questions** — a grid of tappable, frequently-asked questions (next session, venue/help desk, WiFi, certificate process, food, hackathon info) so a first-time visitor sees what they can ask instead of facing a blank chat box.
- **Collapsible sidebar** — a custom show/hide toggle for the configuration panel (track selector, clear chat, live message/token counters), built with Streamlit session state rather than relying on the framework's default (and version-inconsistent) sidebar control.
- **Resilient fallback handling** — if the AI backend is unreachable or errors out, the app shows a friendly fallback message pointing the participant to a volunteer or the help desk, instead of crashing or exposing a raw error.
- **Dark, custom-themed UI** — a distinct visual identity (custom fonts, color palette, styled chat bubbles) built entirely with CSS layered over Streamlit's default components.

## Technology Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend / App framework | **Streamlit** | Rapid to build, deployable as a public web app with no separate frontend/backend split, ideal for a fast-turnaround project. |
| Language | **Python 3** | Native fit with Streamlit; simple to reason about and extend. |
| LLM inference | **Ollama Cloud** (`gpt-oss:20b`) | Hosted inference with no local GPU required. `gpt-oss:20b` was chosen deliberately over larger models — it's a lighter/faster model well-suited to a structured lookup task like this, and it preserves scarce concurrency slots on the hosting plan under simultaneous use, rather than a bigger model that would hold each request longer. |
| Knowledge grounding | **Structured Python data** (`event_data.py`), injected into the system prompt | A full RAG/vector-store pipeline is unnecessary overhead for a knowledge base this size (a handful of KB of schedule/FAQ text). Context-injection is simpler to build, has fewer moving parts to fail live, and is trivial to update — just edit one file. |
| Secrets management | `python-dotenv` (local `.env`) / Streamlit Secrets (deployed) | Keeps the Ollama Cloud API key out of source control while working identically in local development and on Streamlit Community Cloud. |
| Styling | Custom CSS (Google Fonts: Syne, Space Mono) | Gives the app a distinct visual identity beyond Streamlit's default look. |

## Setup Instructions

### 1. Clone and install dependencies
```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install -r requirements.txt
```

### 2. Get an Ollama Cloud API key
Sign up and generate a key at [ollama.com/settings/keys](https://ollama.com/settings/keys).

### 3. Configure your API key locally
Create a `.env` file in the project root:
```
OLLAMA_API_KEY=your-real-key-here
```

### 4. Run the app
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`.

### 5. Deploy (optional)
Push the repo to GitHub, then deploy on [Streamlit Community Cloud](https://share.streamlit.io):
- Point the app at `app.py`.
- Under **App settings → Secrets**, add:
  ```
  OLLAMA_API_KEY = "your-real-key-here"
  ```
  (`.env` is for local use only — it is not present on the deployed container.)

### 6. Keep event data current
All event-specific content — schedule, venue info, FAQs, speaker bios — lives in `event_data.py`. Update this file directly whenever event details change; no other code changes are needed.

## Future Scope

- **Live registration/attendance integration** — tie the assistant into a real participant database for deeper personalization (e.g. "your team's next hackathon checkpoint").
- **Multilingual support** for non-English-speaking participants.
- **Human escalation path** — a button that pings a volunteer (e.g. via Telegram) when the assistant can't answer a question.
- **FAQ caching layer** — answer exact-match common questions directly from `event_data.py` without an LLM call, further reducing latency and backend load during peak concurrent usage.
- **Analytics dashboard** — track which questions are asked most often, to inform logistics planning for future summits.
- **Downloadable calendar export** — let participants export the schedule as an `.ics` file to their phone's calendar app.
