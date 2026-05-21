import streamlit as st
import base64
import time

st.set_page_config(
    page_title="Jim's AI Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- LOCAL BACKGROUND LOADER ----------

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg1 = image_to_base64("assets/main1.jpg")
bg2 = image_to_base64("assets/main2.jpg")
bg3 = image_to_base64("assets/main3.jpg")
bg4 = image_to_base64("assets/main4.jpg")

# ---------- CSS ----------

st.markdown(f"""
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{
    display: none;
}}

[data-testid="stAppViewContainer"] {{
    animation: mainBg 28s infinite;
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
}}

@keyframes mainBg {{
    0% {{
        background-image: linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,.72)), url("data:image/jpg;base64,{bg1}");
    }}
    25% {{
        background-image: linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,.72)), url("data:image/jpg;base64,{bg2}");
    }}
    50% {{
        background-image: linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,.72)), url("data:image/jpg;base64,{bg3}");
    }}
    75% {{
        background-image: linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,.72)), url("data:image/jpg;base64,{bg4}");
    }}
    100% {{
        background-image: linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,.72)), url("data:image/jpg;base64,{bg1}");
    }}
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

.hero-title {{
    font-size: 84px;
    font-weight: 950;
    text-align: center;
    color: white;
    text-shadow: 0 0 28px cyan;
    margin-bottom: 5px;
}}

.hero-subtitle {{
    font-size: 25px;
    text-align: center;
    color: #f5f5f5;
    margin-bottom: 30px;
    text-shadow: 0 0 10px black;
}}

.badge-row {{
    text-align: center;
    margin-bottom: 45px;
}}

.badge {{
    display: inline-block;
    background: rgba(0, 229, 255, .14);
    color: white;
    padding: 9px 18px;
    margin: 6px;
    border-radius: 999px;
    border: 1px solid rgba(0,255,255,.35);
    font-weight: 700;
}}

.card {{
    background: rgba(0,0,0,.58);
    padding: 34px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,.20);
    min-height: 430px;
    transition: .3s;
    box-shadow: 0 12px 40px rgba(0,0,0,.5);
}}

.card:hover {{
    transform: translateY(-10px) scale(1.02);
    border: 1px solid cyan;
    box-shadow: 0 0 35px rgba(0,255,255,.65);
}}

.icon {{
    font-size: 72px;
    text-align: center;
    margin-bottom: 15px;
}}

.card-title {{
    font-size: 34px;
    font-weight: 900;
    text-align: center;
    color: white;
    margin-bottom: 18px;
}}

.card-text {{
    font-size: 18px;
    color: #eeeeee;
    line-height: 1.8;
}}

.tag {{
    display: inline-block;
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.18);
    padding: 6px 11px;
    border-radius: 999px;
    margin: 5px 4px;
    font-size: 13px;
    color: white;
}}

.stButton>button {{
    width: 100%;
    height: 56px;
    border-radius: 16px;
    border: none;
    font-size: 18px;
    font-weight: 900;
    background: linear-gradient(90deg,#00e5ff,#0066ff);
    color: white;
    transition: .3s;
    margin-top: 18px;
}}

.stButton>button:hover {{
    transform: scale(1.03);
    box-shadow: 0 0 28px cyan;
}}

.stats {{
    background: rgba(0,0,0,.55);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 24px;
    padding: 25px;
    margin-top: 45px;
    color: white;
    text-align: center;
}}

.stat-num {{
    font-size: 36px;
    font-weight: 900;
    color: #00e5ff;
}}

.footer {{
    text-align:center;
    margin-top:40px;
    font-size:16px;
    color:white;
    text-shadow: 0 0 8px black;
}}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------

st.markdown("""
<div class="hero-title">🎬 Jim's AI Studio</div>
<div class="hero-subtitle">
AI Powered Creator Platform for Image Editing, Video Tools & Content Generation 🚀
</div>

<div class="badge-row">
    <span class="badge">⚡ Fast Tools</span>
    <span class="badge">🎨 Creator Friendly</span>
    <span class="badge">🤖 AI Inspired</span>
    <span class="badge">💻 Built with Python</span>
</div>
""", unsafe_allow_html=True)

# ---------- TOOL CARDS ----------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="icon">🎨</div>
        <div class="card-title">AI Image Studio</div>
        <div class="card-text">
            Edit images, create thumbnails, remove backgrounds, generate posters, memes and profile pictures.
            <br><br>
            <span class="tag">Background Remover</span>
            <span class="tag">Thumbnail Maker</span>
            <span class="tag">Poster Maker</span>
            <span class="tag">Image Effects</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Launch Image Studio"):
        with st.spinner("Launching Image Studio..."):
            time.sleep(0.4)
        st.switch_page("pages/Image_Studio.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="icon">🎥</div>
        <div class="card-title">AI Video Studio</div>
        <div class="card-text">
            Convert videos into short clips, add captions, create reel format videos and export content.
            <br><br>
            <span class="tag">Video Trim</span>
            <span class="tag">Reel Format</span>
            <span class="tag">Captions</span>
            <span class="tag">Shorts Tools</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎬 Launch Video Studio"):
        with st.spinner("Launching Video Studio..."):
            time.sleep(0.4)
        st.switch_page("pages/Video_Studio.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="icon">🧠</div>
        <div class="card-title">AI Text Studio</div>
        <div class="card-text">
            Generate scripts, captions, titles, hashtags, monetization plans and creator guidance.
            <br><br>
            <span class="tag">Scripts</span>
            <span class="tag">Captions</span>
            <span class="tag">Titles</span>
            <span class="tag">Creator Guide</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🧠 Launch Text Studio"):
        with st.spinner("Launching Text Studio..."):
            time.sleep(0.4)
        st.switch_page("pages/Text_Studio.py")

# ---------- DASHBOARD STATS ----------

st.markdown("""
<div class="stats">
    <h2>🚀 Studio Dashboard</h2>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown('<div class="stats"><div class="stat-num">3</div>Studios</div>', unsafe_allow_html=True)

with s2:
    st.markdown('<div class="stats"><div class="stat-num">15+</div>Creator Tools</div>', unsafe_allow_html=True)

with s3:
    st.markdown('<div class="stats"><div class="stat-num">Free</div>No Paid API</div>', unsafe_allow_html=True)

with s4:
    st.markdown('<div class="stats"><div class="stat-num">Fast</div>Local Processing</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------

st.markdown("""
<div class="footer">
⚡ Developed by Jimmy | Jim's AI Studio © 2026
</div>
""", unsafe_allow_html=True)