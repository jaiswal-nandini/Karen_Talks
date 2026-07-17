import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# ── Config ────────────────────────────────────────────────────────────────────
load_dotenv()

# ── config ─────────────────────────────
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found. Check your .env file")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Karen Talks", layout="wide", initial_sidebar_state="expanded")

# ── Palettes ──────────────────────────────────────────────────────────────────
MODES = {
    "🔥 Inferno": {
        "dark":  {"bg":"#0c0402","surface":"#180905","card":"#231007","accent":"#ff4500","accent2":"#ff8c00","text":"#fff0e8","sub":"#b86e4a","border":"#4a1808","glow":"rgba(255,69,0,0.3)","badge_bg":"#300f00","utext":"#fff"},
        "light": {"bg":"#fffaf8","surface":"#fff0e8","card":"#ffe4d4","accent":"#bf3000","accent2":"#d45a00","text":"#180800","sub":"#7a3c1e","border":"#f5c0a0","glow":"rgba(180,48,0,0.15)","badge_bg":"#fff3ec","utext":"#fff"},
    },
    "❄️ Arctic": {
        "dark":  {"bg":"#010c16","surface":"#061a2a","card":"#0b2638","accent":"#00c8ff","accent2":"#0090cc","text":"#e0f7ff","sub":"#5aaec4","border":"#0c4060","glow":"rgba(0,200,255,0.3)","badge_bg":"#021c2e","utext":"#000"},
        "light": {"bg":"#f6fbff","surface":"#e8f7ff","card":"#d0eeff","accent":"#006896","accent2":"#004e72","text":"#001520","sub":"#2a6070","border":"#9ad0e8","glow":"rgba(0,104,150,0.15)","badge_bg":"#eaf6ff","utext":"#fff"},
    },
    "☠️ Venom": {
        "dark":  {"bg":"#020c03","surface":"#061608","card":"#0a200d","accent":"#35f00e","accent2":"#00bb00","text":"#d5ffe0","sub":"#52b460","border":"#0f4015","glow":"rgba(53,240,14,0.3)","badge_bg":"#051508","utext":"#000"},
        "light": {"bg":"#f4fff5","surface":"#e0ffe3","card":"#c5f5ca","accent":"#166a00","accent2":"#0d5000","text":"#011602","sub":"#2a5e2e","border":"#88d490","glow":"rgba(22,106,0,0.15)","badge_bg":"#e8ffe9","utext":"#fff"},
    },
    "👑 Monarch": {
        "dark":  {"bg":"#09050e","surface":"#120a1c","card":"#1b0e2c","accent":"#b96ef5","accent2":"#8b28e0","text":"#f0e6ff","sub":"#9870b8","border":"#381568","glow":"rgba(185,110,245,0.3)","badge_bg":"#18092c","utext":"#000"},
        "light": {"bg":"#faf6ff","surface":"#f2e8ff","card":"#e6d2ff","accent":"#741ec4","accent2":"#54149a","text":"#130030","sub":"#622a90","border":"#c8a0f0","glow":"rgba(116,30,196,0.15)","badge_bg":"#f5eeff","utext":"#fff"},
    },
    "🩸 Crimson": {
        "dark":  {"bg":"#0b0204","surface":"#180408","card":"#22060d","accent":"#e0183e","accent2":"#b81035","text":"#ffe4ec","sub":"#bc5870","border":"#500818","glow":"rgba(224,24,62,0.3)","badge_bg":"#22060e","utext":"#fff"},
        "light": {"bg":"#fff5f7","surface":"#ffd8e2","card":"#ffbfcf","accent":"#a00026","accent2":"#7a001c","text":"#1e0008","sub":"#7a1e38","border":"#f09aaa","glow":"rgba(160,0,38,0.15)","badge_bg":"#ffe8ee","utext":"#fff"},
    },
}

BRIGHTNESS_OPTIONS = ["🌙 Dark", "☀️ Light", "⚡ Auto (Time)", "🌡️ Auto (Ambient)"]
THEME_CYCLE = {
    "🌙 Dark": "☀️ Light",
    "☀️ Light": "⚡ Auto (Time)",
    "⚡ Auto (Time)": "🌡️ Auto (Ambient)",
    "🌡️ Auto (Ambient)": "🌙 Dark",
}
THEME_ICONS = {
    "🌙 Dark": "🌙",
    "☀️ Light": "☀️",
    "⚡ Auto (Time)": "⚡",
    "🌡️ Auto (Ambient)": "🌡️",
}

# ── Personas ──────────────────────────────────────────────────────────────────
AVATARS = {
    # ── Indian Icons ──────────────────────────────────────────────────────────
    "🕊️ Mahatma Gandhi": {
        "emoji": "🕊️", "name": "Mahatma Gandhi",
        "background": (
            "Father of the Indian Nation (1869–1948). Led India's independence movement against British colonial rule "
            "through non-violent civil disobedience. Lawyer turned ascetic, deeply spiritual, uncompromising on truth (Satyagraha) "
            "and non-violence (Ahimsa). Assassinated in 1948."
        ),
        "beliefs": (
            "Non-violence is the highest moral law — violence only breeds more violence. "
            "Truth is God. Swaraj (self-rule) must begin within oneself. "
            "The means are as sacred as the ends. Simple living, high thinking."
        ),
        "style": "Calm, parabolic, uses moral weight and self-sacrifice, gentle but immovable, asks you to examine your own soul",
        "bio": "He defeated an empire without firing a single shot. Will disarm your argument with truth alone.",
    },
    "🌹 Jawaharlal Nehru": {
        "emoji": "🌹", "name": "Jawaharlal Nehru",
        "background": (
            "First Prime Minister of independent India (1947–1964). Cambridge-educated, secular visionary, "
            "architect of modern India's democratic and scientific institutions. Author of 'The Discovery of India'. "
            "Champion of non-alignment, industrialisation, and socialist democracy."
        ),
        "beliefs": (
            "Science and rationalism must guide a modern nation. "
            "Secularism is India's civilisational strength, not a concession. "
            "Non-alignment gives developing nations dignity and sovereignty. "
            "Democracy is the only legitimate path to progress."
        ),
        "style": "Eloquent, intellectually sweeping, uses historical context, idealistic but pragmatic, occasionally impatient with cynicism",
        "bio": "Built a nation from scratch. Will debate you with 5,000 years of civilisational perspective.",
    },
    "⚡ B.R. Ambedkar": {
        "emoji": "⚡", "name": "B.R. Ambedkar",
        "background": (
            "Father of the Indian Constitution. Dalit scholar, jurist, and social reformer (1891–1956). "
            "First Law Minister of India. Faced brutal caste discrimination yet earned multiple doctorates from Columbia and LSE. "
            "Converted to Buddhism to reject caste hierarchy. Architect of India's constitutional framework."
        ),
        "beliefs": (
            "Caste is India's gravest injustice — a systematic denial of humanity. "
            "Liberty, equality, and fraternity are inseparable. "
            "Education is the weapon of liberation for the oppressed. "
            "Constitutional morality must override social morality when society is unjust."
        ),
        "style": "Razor-sharp, forensic, cites law and data, confrontational toward power, unapologetically Dalit in perspective",
        "bio": "Wrote the Constitution of the world's largest democracy. Will dissect your argument with law, data, and lived injustice.",
    },
    "🐯 Bal Gangadhar Tilak": {
        "emoji": "🐯", "name": "Bal Gangadhar Tilak",
        "background": (
            "Indian independence activist and scholar (1856–1920). Called 'Lokmanya' (beloved of the people). "
            "First to demand complete Indian self-rule (Swaraj). Imprisoned multiple times by the British. "
            "Believed in aggressive nationalism and mass political mobilisation."
        ),
        "beliefs": (
            "Swaraj is my birthright and I shall have it. "
            "Freedom cannot be begged for — it must be seized. "
            "Cultural pride and national identity are the backbone of liberation. "
            "The masses, not elites, are the true engine of revolution."
        ),
        "style": "Fierce, uncompromising, rousing, uses cultural pride and historical grievance, demands action not patience",
        "bio": "Declared Swaraj a birthright from a colonial jail. Will challenge your patience for half-measures.",
    },
    # ── Global Icons ──────────────────────────────────────────────────────────
    "🦁 Winston Churchill": {
        "emoji": "🦁", "name": "Winston Churchill",
        "background": "British PM during WWII (1940–45, 1951–55). Nobel Prize-winning writer, legendary orator, stubborn aristocrat with razor wit.",
        "beliefs": "Freedom and democracy must be defended at all costs. Appeasement is cowardice. Strong decisive leadership beats consensus.",
        "style": "Commanding, oratorical, grand historical metaphors, dry sarcasm, never concedes",
        "bio": "The British Bulldog. Defends democracy with blood, toil, tears, and rhetoric.",
    },
    "🔬 Marie Curie": {
        "emoji": "🔬", "name": "Marie Curie",
        "background": "Polish physicist & chemist. Only person to win Nobel Prizes in two sciences. Overcame enormous gender barriers in academia.",
        "beliefs": "Science and evidence must guide all decisions. Hard work and rigour transcend gender or origin. Knowledge must be shared freely.",
        "style": "Precise, methodical, quietly fierce, cites evidence, dismisses superstition with cold facts",
        "bio": "Discovered radioactivity. Will irradiate your weak arguments with data.",
    },
    "⚖️ Socrates": {
        "emoji": "⚖️", "name": "Socrates",
        "background": "Ancient Greek philosopher (470–399 BC). Founder of Western philosophy. Executed for corrupting the youth. Taught by relentless questioning.",
        "beliefs": "The unexamined life is not worth living. True wisdom is knowing you know nothing. Every belief must survive rigorous questioning.",
        "style": "Socratic method — probing questions, exposes contradictions, feigns ignorance to trap opponents",
        "bio": "He died rather than stop questioning. Your argument will not survive the elenchus.",
    },
    "🚀 Elon Musk": {
        "emoji": "🚀", "name": "Elon Musk",
        "background": "Tech billionaire. CEO of Tesla and SpaceX, owner of X. Free-speech absolutist and techno-optimist known for first-principles reasoning.",
        "beliefs": "Humanity must become multi-planetary. Free speech is democracy's bedrock. Bureaucracy kills innovation. First principles beat convention.",
        "style": "Blunt, meme-literate, uses engineering analogies, dismisses critics as legacy thinkers, confidently contrarian",
        "bio": "Sent a car into space. Will first-principles your argument into dust.",
    },
    "✊ Malcolm X": {
        "emoji": "✊", "name": "Malcolm X",
        "background": "African-American Muslim minister and civil rights activist (1925–1965). Advocated Black self-defence and self-determination against systemic racism.",
        "beliefs": "Black liberation by any means necessary. Systemic racism cannot be politely dismantled. Self-respect and self-determination are non-negotiable.",
        "style": "Fierce, direct, no patience for compromise, uses historical injustice as evidence, morally absolute",
        "bio": "By any means necessary. Will dismantle your comfort with historical truth.",
    },
    "🍎 Steve Jobs": {
        "emoji": "🍎", "name": "Steve Jobs",
        "background": "Co-founder of Apple and Pixar. Perfectionist, visionary, notoriously demanding. Built the world's most valuable brand.",
        "beliefs": "Design and simplicity are the highest intelligence. Focus means saying no to a thousand things. Technology and humanities must intersect.",
        "style": "Reality-distortion field, charismatic, dismissive of mediocrity, visionary language, never settles",
        "bio": "Changed six industries. Will tell you your idea is not insanely great.",
    },
    "✏️ Custom Persona": {
        "emoji": "✏️", "name": "", "background": "", "beliefs": "", "style": "",
        "bio": "Your own creation. Define this persona's soul.",
    },
}

STYLES = ["Calm", "Assertive", "Aggressive", "Sarcastic", "Socratic", "Poetic"]

# ── Logo SVG ──────────────────────────────────────────────────────────────────
def make_logo(accent: str, glow: str) -> str:
    return f"""
<svg viewBox="0 0 420 80" xmlns="http://www.w3.org/2000/svg" style="width:min(420px,90vw);height:auto;display:block;">
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.7"/>
    </linearGradient>
    <filter id="gf" x="-20%" y="-60%" width="140%" height="220%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <!-- speech bubble icon -->
    <g id="bubble">
      <rect x="0" y="0" width="34" height="26" rx="7" fill="{accent}" opacity="0.95"/>
      <polygon points="6,26 14,34 20,26" fill="{accent}" opacity="0.95"/>
      <circle cx="8"  cy="13" r="3" fill="white" opacity="0.9"/>
      <circle cx="17" cy="13" r="3" fill="white" opacity="0.9"/>
      <circle cx="26" cy="13" r="3" fill="white" opacity="0.9"/>
    </g>
  </defs>
  <!-- glow layer -->
  <text x="55" y="58" font-family="'Playfair Display',Georgia,serif" font-size="52"
        font-weight="700" font-style="italic" fill="{accent}" opacity="0.18" filter="url(#gf)"
        letter-spacing="1">Karen</text>
  <text x="237" y="58" font-family="'Bebas Neue',Impact,sans-serif" font-size="46"
        font-weight="400" fill="{accent}" opacity="0.18" filter="url(#gf)"
        letter-spacing="4">TALKS</text>
  <!-- bubble icon -->
  <use href="#bubble" transform="translate(8,20)"/>
  <!-- main wordmark -->
  <text x="55" y="58" font-family="'Playfair Display',Georgia,serif" font-size="52"
        font-weight="700" font-style="italic" fill="url(#lg)"
        letter-spacing="1">Karen</text>
  <text x="237" y="58" font-family="'Bebas Neue',Impact,sans-serif" font-size="46"
        font-weight="400" fill="{accent}" opacity="0.55"
        letter-spacing="4">TALKS</text>
  <!-- divider dot -->
  <circle cx="229" cy="46" r="4" fill="{accent}" opacity="0.8"/>
</svg>"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def resolve_brightness(pref: str) -> str:
    if pref == "🌙 Dark":   return "dark"
    if pref == "☀️ Light":  return "light"
    return "light" if 6 <= datetime.now().hour < 19 else "dark"

def get_active_avatar():
    key = st.session_state.avatar_key
    av = AVATARS[key].copy()
    if key == "✏️ Custom Persona":
        av["name"]       = st.session_state.custom_name       or "Unknown Debater"
        av["background"] = st.session_state.custom_background or "A mysterious figure with strong opinions."
        av["beliefs"]    = st.session_state.custom_beliefs    or "Stands firmly by their convictions."
        av["style"]      = st.session_state.custom_style      or "Direct and confident."
        av["bio"]        = st.session_state.custom_bio        or "Your custom debate persona."
    return av, key

def build_prompt(user_input: str, avatar: dict, style: str) -> str:
    return f"""You are not an AI assistant. You are roleplaying as a REAL PERSON with a strong, consistent identity.

PERSONA:
Name: {avatar['name']}
Background: {avatar['background']}
Core Beliefs: {avatar['beliefs']}
Communication Style: {avatar['style']}

DEBATE RULES:
- The user will challenge your decisions, beliefs, or actions.
- Defend your point of view as this person — take a CLEAR STANCE, do NOT stay neutral.
- Use logic, philosophy, emotion, or historical reasoning appropriate to this persona.
- You may question the user, counter-argue, or justify your decisions.
- Debate style modifier: {style} — adjust your delivery accordingly.
- Keep responses natural and human-like. Under 140 words. Memorable and sharp.

IMPORTANT: Stay fully in character. Never say "as an AI". Never give generic answers.

User: {user_input}
{avatar['name']}:"""

def get_debate_response(user_input: str, avatar: dict, style: str) -> str:
    try:
        return model.generate_content(build_prompt(user_input, avatar, style)).text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def award_point(role: str):
    st.session_state.scores["user" if role == "user" else "karen"] += 1

def next_theme(current: str) -> str:
    return THEME_CYCLE.get(current, "🌙 Dark")

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in {
    "messages": [], "mode": "🔥 Inferno", "brightness": "🌙 Dark",
    "avatar_key": "🕊️ Mahatma Gandhi",
    "custom_name": "", "custom_background": "", "custom_beliefs": "",
    "custom_style": "", "custom_bio": "",
    "debate_style": "Calm", "round": 0,
    "scores": {"user": 0, "karen": 0},
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Resolve active palette ────────────────────────────────────────────────────
b_key = resolve_brightness(st.session_state.brightness)
m = MODES[st.session_state.mode][b_key]
is_dark = (b_key == "dark")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&family=Bebas+Neue&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
  --bg:      {m['bg']};
  --surface: {m['surface']};
  --card:    {m['card']};
  --accent:  {m['accent']};
  --accent2: {m['accent2']};
  --text:    {m['text']};
  --sub:     {m['sub']};
  --border:  {m['border']};
  --glow:    {m['glow']};
  --badge:   {m['badge_bg']};
  --utext:   {m['utext']};
  --shadow:  {'rgba(0,0,0,0.4)' if is_dark else 'rgba(0,0,0,0.08)'};
  --radius:  14px;
}}

html, body, [data-testid="stApp"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 15px;
  transition: background 0.35s ease, color 0.35s ease;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  transition: background 0.35s ease;
}}
[data-testid="stSidebar"] * {{ color: var(--text) !important; }}

/* ── Selectbox ── */
[data-baseweb="select"] > div {{
  background: var(--card) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
  font-size: 0.875rem !important;
}}
[data-baseweb="select"] * {{ color: var(--text) !important; }}
[data-baseweb="popover"] {{ background: var(--surface) !important; }}
[data-baseweb="menu"]    {{ background: var(--surface) !important; }}
[data-baseweb="menu"] li:hover {{ background: var(--card) !important; }}

/* ── Inputs ── */
textarea, input[type="text"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
}}

/* ── Buttons ── */
.stButton > button {{
  background: transparent !important;
  color: var(--accent) !important;
  border: 1.5px solid var(--accent) !important;
  border-radius: 10px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.06em !important;
  padding: 8px 18px !important;
  transition: all 0.2s ease !important;
  text-transform: uppercase !important;
}}
.stButton > button:hover {{
  background: var(--accent) !important;
  color: var(--bg) !important;
  box-shadow: 0 0 20px var(--glow) !important;
  transform: translateY(-1px) !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
  background: var(--card) !important;
  border: 1.5px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: var(--radius) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
}}
[data-testid="stChatInput"] {{
  background: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
}}

hr {{ border-color: var(--border) !important; opacity: 0.35; }}
.stMarkdown p, .stMarkdown li {{ color: var(--text) !important; font-size: 0.9rem; line-height: 1.7; }}
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 99px; }}

/* ── Sidebar section labels ── */
.sidebar-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--sub);
  text-transform: uppercase;
  margin: 18px 0 6px;
  opacity: 0.8;
}}

/* ── Top bar ── */
.topbar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 6px;
}}
.tagline {{
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 400;
  letter-spacing: 0.22em;
  color: var(--sub);
  text-transform: uppercase;
  margin: 0 0 18px;
  opacity: 0.75;
}}

/* ── Theme Toggle Button ── */
.theme-toggle {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 16px;
  border-radius: 999px;
  background: var(--card);
  border: 1.5px solid var(--border);
  cursor: pointer;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  color: var(--sub);
  text-transform: uppercase;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}}
.theme-toggle:hover {{
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: 0 0 12px var(--glow);
}}
.theme-dot {{
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 6px var(--glow);
  flex-shrink: 0;
}}

/* ── Pill badges ── */
.pill {{
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 11px; border-radius: 999px;
  background: var(--badge); border: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; letter-spacing: 0.1em;
  color: var(--sub); text-transform: uppercase;
}}
.pill.accent {{ color: var(--accent); }}

/* ── Stats row ── */
.stats-row {{
  display: flex; gap: 0; align-items: stretch;
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); margin-bottom: 20px;
  overflow: hidden;
}}
.stat-cell {{
  flex: 1; padding: 10px 16px;
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 2px;
}}
.stat-cell:last-child {{ border-right: none; }}
.stat-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem; letter-spacing: 0.18em;
  color: var(--sub); text-transform: uppercase;
}}
.stat-val {{
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem; font-weight: 700;
  color: var(--accent);
  line-height: 1.2;
}}

/* ── Chat bubbles ── */
.bubble-wrap {{ display:flex; gap:10px; margin:12px 0; align-items:flex-end; }}
.bubble-wrap.user {{ flex-direction:row-reverse; }}
.av-chip {{
  width:34px; height:34px; border-radius:50%;
  background:var(--card); border:1.5px solid var(--border);
  display:flex; align-items:center; justify-content:center;
  font-size:1rem; flex-shrink:0;
}}
.bubble {{
  max-width:70%; padding:13px 17px; border-radius:18px;
  line-height:1.65; font-size:0.9rem; position:relative;
  animation: popIn 0.22s cubic-bezier(.34,1.5,.64,1);
}}
@keyframes popIn {{
  from {{ opacity:0; transform:scale(0.9) translateY(5px); }}
  to   {{ opacity:1; transform:scale(1) translateY(0); }}
}}
.bubble.user {{
  background:var(--accent); color:var(--utext) !important;
  border-bottom-right-radius:3px;
  box-shadow:0 3px 20px var(--glow); font-weight:500;
}}
.bubble.karen {{
  background:var(--card); border:1px solid var(--border);
  border-bottom-left-radius:3px; color:var(--text) !important;
  box-shadow:0 2px 10px var(--shadow);
}}
.rnd-badge {{
  font-family:'JetBrains Mono',monospace; font-size:0.62rem;
  color:var(--sub); letter-spacing:0.18em;
  text-transform:uppercase; margin-bottom:3px; opacity:0.7;
}}

/* ── Avatar card (sidebar) ── */
.av-card {{
  background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius); padding:14px; margin-bottom:10px;
  position:relative; overflow:hidden;
}}
.av-card::before {{
  content:''; position:absolute; inset:0;
  background:linear-gradient(135deg,var(--glow) 0%,transparent 55%);
  pointer-events:none;
}}
.av-name {{
  font-family:'Playfair Display',serif; font-size:1.1rem;
  font-weight:700; color:var(--accent); line-height:1.3;
}}
.av-bio {{
  font-family:'Inter',sans-serif; font-size:0.78rem;
  color:var(--sub); margin-top:5px; line-height:1.55;
  font-style:italic;
}}

/* ── Empty state ── */
.empty-state {{
  text-align:center; padding:52px 20px; color:var(--sub);
}}
.empty-emoji {{ font-size:3.5rem; margin-bottom:12px; }}
.empty-name {{
  font-family:'Playfair Display',serif; font-size:1.6rem;
  font-weight:700; font-style:italic; color:var(--accent);
  letter-spacing:0.02em;
}}
.empty-bio {{
  font-size:0.85rem; max-width:380px; margin:10px auto;
  line-height:1.8; color:var(--sub); font-style:italic;
}}
.empty-cta {{
  margin-top:20px; font-family:'JetBrains Mono',monospace;
  font-size:0.64rem; letter-spacing:0.25em; opacity:0.4;
  text-transform:uppercase;
}}

/* ── Auto mode info ── */
.auto-info {{
  background:var(--card); border:1px solid var(--border);
  border-radius:10px; padding:10px 13px; margin-top:8px;
  font-family:'JetBrains Mono',monospace; font-size:0.67rem;
  color:var(--sub); line-height:1.65;
}}
.auto-info strong {{ color:var(--accent); }}

/* ── Score chips in sidebar ── */
.score-chip {{
  text-align:center; background:var(--card);
  border:1px solid var(--border); border-radius:12px; padding:10px;
}}
.score-chip-lbl {{
  font-family:'JetBrains Mono',monospace; font-size:0.62rem;
  color:var(--sub); letter-spacing:0.14em; text-transform:uppercase;
}}
.score-chip-val {{
  font-family:'Playfair Display',serif; font-size:2rem;
  font-weight:700; color:var(--accent); line-height:1.2;
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="font-family:\'Playfair Display\',serif;font-size:1.4rem;'
        f'font-weight:700;font-style:italic;color:var(--accent);letter-spacing:0.02em;margin-bottom:2px;">Karen Talks</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.6rem;'
        f'letter-spacing:0.2em;color:var(--sub);text-transform:uppercase;opacity:0.7;">Debate Engine</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Theme Toggle (sidebar) ────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Theme Toggle</div>', unsafe_allow_html=True)
    b_idx = BRIGHTNESS_OPTIONS.index(st.session_state.brightness) if st.session_state.brightness in BRIGHTNESS_OPTIONS else 0
    new_b = st.selectbox("", BRIGHTNESS_OPTIONS, index=b_idx, key="b_sel", label_visibility="collapsed")
    if new_b != st.session_state.brightness:
        st.session_state.brightness = new_b
        st.rerun()

    if "Auto" in st.session_state.brightness:
        hour = datetime.now().hour
        rl = "☀️ Light" if 6 <= hour < 19 else "🌙 Dark"
        desc = (
            f"Time now <strong>{hour:02d}:xx</strong> → <strong>{rl}</strong>. Light: 06:00–18:59."
            if "Time" in st.session_state.brightness
            else f"Reads browser preference. Resolving to <strong>{rl}</strong>."
        )
        st.markdown(f'<div class="auto-info">{desc}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Arena Mode ────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Arena Mode</div>', unsafe_allow_html=True)
    m_keys = list(MODES.keys())
    new_mode = st.selectbox("", m_keys, index=m_keys.index(st.session_state.mode), key="mode_sel", label_visibility="collapsed")
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode
        st.rerun()

    st.markdown("---")

    # ── Debate Style ──────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Debate Style</div>', unsafe_allow_html=True)
    st.session_state.debate_style = st.selectbox("", STYLES, index=STYLES.index(st.session_state.debate_style), key="style_sel", label_visibility="collapsed")

    st.markdown("---")

    # ── Persona ───────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Persona</div>', unsafe_allow_html=True)
    av_keys = list(AVATARS.keys())
    cur_av = av_keys.index(st.session_state.avatar_key) if st.session_state.avatar_key in av_keys else 0
    new_av = st.selectbox("", av_keys, index=cur_av, key="av_sel", label_visibility="collapsed")
    if new_av != st.session_state.avatar_key:
        st.session_state.avatar_key = new_av
        st.rerun()

    av, av_key = get_active_avatar()
    disp_name = av["name"] or (av_key.split(" ", 1)[1] if " " in av_key else av_key)

    st.markdown(f"""
    <div class="av-card">
      <div style="font-size:2.2rem;margin-bottom:8px;">{av['emoji']}</div>
      <div class="av-name">{disp_name}</div>
      <div class="av-bio">"{av['bio']}"</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.avatar_key == "✏️ Custom Persona":
        for lbl, key, kw in [
            ("Name", "custom_name", {"placeholder": "e.g. Nikola Tesla"}),
            ("Background", "custom_background", {"height": 68}),
            ("Core Beliefs", "custom_beliefs", {"height": 58}),
            ("Communication Style", "custom_style", {"placeholder": "e.g. Visionary, uses metaphors"}),
            ("Bio (one-liner)", "custom_bio", {"placeholder": "Short tagline"}),
        ]:
            st.markdown(f'<div class="sidebar-label">{lbl}</div>', unsafe_allow_html=True)
            if "height" in kw:
                st.session_state[key] = st.text_area(
                "",
                value=st.session_state[key],
                height=kw["height"], 
                key=f"area_{key}",
                label_visibility="collapsed")
            else:
                st.session_state[key] = st.text_input(
                "",
                value=st.session_state[key],
                key=f"key_{key}",
                label_visibility="collapsed"
            )

    st.markdown("---")

    # ── Scoreboard ────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Scoreboard</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="score-chip"><div class="score-chip-lbl">You</div><div class="score-chip-val">{st.session_state.scores["user"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="score-chip"><div class="score-chip-lbl">{disp_name}</div><div class="score-chip-val" style="color:var(--accent2);">{st.session_state.scores["karen"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Reset Match"):
        st.session_state.messages = []
        st.session_state.scores = {"user": 0, "karen": 0}
        st.session_state.round = 0
        st.rerun()


# ── Main area ─────────────────────────────────────────────────────────────────
    
av, av_key = get_active_avatar()
disp_name = av["name"] or (av_key.split(" ", 1)[1] if " " in av_key else av_key)
b_icon = THEME_ICONS.get(st.session_state.brightness, "🌙")
next_b = next_theme(st.session_state.brightness)

# Top bar: Logo left, Theme Toggle button right
logo_col, spacer_col, toggle_col = st.columns([5, 3, 2])

with logo_col:
    st.markdown(make_logo(m["accent"], m["glow"]), unsafe_allow_html=True)

with toggle_col:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    # The clickable cycle button — this is called a "Theme Toggle"
    if st.button(f"{b_icon}  Theme Toggle", key="theme_toggle_btn"):
        st.session_state.brightness = next_b
        st.rerun()
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.6rem;'
        f'color:var(--sub);letter-spacing:0.1em;margin-top:4px;opacity:0.7;">'
        f'Next → {next_b}</div>',
        unsafe_allow_html=True
    )

# Tagline
st.markdown(
    f'<p class="tagline">AI Debate Engine &nbsp;·&nbsp; {st.session_state.mode} &nbsp;·&nbsp; {disp_name} &nbsp;·&nbsp; {st.session_state.debate_style}</p>',
    unsafe_allow_html=True
)

st.markdown("<hr style='margin:0 0 16px;'>", unsafe_allow_html=True)

# Stats row
st.markdown(f"""
<div class="stats-row">
  <div class="stat-cell">
    <div class="stat-label">Your Points</div>
    <div class="stat-val">{st.session_state.scores['user']}</div>
  </div>
  <div class="stat-cell">
    <div class="stat-label">Karen's Points</div>
    <div class="stat-val" style="color:var(--accent2);">{st.session_state.scores['karen']}</div>
  </div>
  <div class="stat-cell">
    <div class="stat-label">Round</div>
    <div class="stat-val">{st.session_state.round}</div>
  </div>
  <div class="stat-cell">
    <div class="stat-label">Style</div>
    <div class="stat-val" style="font-size:0.95rem;">{st.session_state.debate_style}</div>
  </div>
  <div class="stat-cell">
    <div class="stat-label">Display</div>
    <div class="stat-val" style="font-size:0.95rem;">{b_icon} {b_key.capitalize()}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
with st.container():
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="empty-state">
          <div class="empty-emoji">{av['emoji']}</div>
          <div class="empty-name">{disp_name}</div>
          <div class="empty-bio">"{av['bio']}"</div>
          <div class="empty-cta">Type your argument below to begin the debate</div>
        </div>
        """, unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        role   = msg["role"]
        txt    = msg["content"]
        rnd    = msg.get("round", "")
        is_usr = (role == "user")
        w_cls  = "user" if is_usr else ""
        b_cls  = "user" if is_usr else "karen"
        chip   = "🧑" if is_usr else av["emoji"]

        st.markdown(f"""
        <div class="bubble-wrap {w_cls}">
          <div class="av-chip">{chip}</div>
          <div>
            {'<div class="rnd-badge">Round ' + str(rnd) + '</div>' if rnd else ''}
            <div class="bubble {b_cls}">{txt}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not is_usr and i == len(st.session_state.messages) - 1:
            c1, c2, _ = st.columns([1.4, 1.7, 5])
            with c1:
                if st.button("👍  I won", key=f"w_{i}"):
                    award_point("user"); st.rerun()
            with c2:
                if st.button(f"💀  {disp_name} won", key=f"l_{i}"):
                    award_point("karen"); st.rerun()
# ── Validation ──
def validate_custom_persona():
    if st.session_state.avatar_key == "✏️ Custom Persona":
        if not st.session_state.custom_name.strip():
            return "⚠️ Please enter a name for Custom Persona"
        if not st.session_state.custom_beliefs.strip():
            return "⚠️ Please define core beliefs"
    return None                    

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input(f"Challenge {disp_name} — make your argument…")

if user_input:
    error = validate_custom_persona()
    if error:
        st.error(error)
        st.stop()

    st.session_state.round += 1
    st.session_state.messages.append({"role": "user", "content": user_input, "round": st.session_state.round})
    av, _ = get_active_avatar()
    with st.spinner(f"{av['emoji']}  {disp_name} is preparing a response…"):
        reply = get_debate_response(user_input, av, st.session_state.debate_style)
    st.session_state.messages.append({"role": "assistant", "content": reply, "round": st.session_state.round})
    st.rerun()
