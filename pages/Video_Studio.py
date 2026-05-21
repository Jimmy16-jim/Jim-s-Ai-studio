import streamlit as st
import tempfile
import os
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---------------- SAFE MOVIEPY IMPORT WITH ERROR DISPLAY ---------------- #

try:
    from moviepy.editor import VideoFileClip
    from moviepy.video.fx.all import crop
    MOVIEPY_AVAILABLE = True
    MOVIEPY_ERROR = ""
except Exception as e:
    MOVIEPY_AVAILABLE = False
    MOVIEPY_ERROR = str(e)

st.set_page_config(page_title="AI Video Studio", page_icon="🎥", layout="wide")

# ---------------- BACKGROUND IMAGES ---------------- #

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

vid_bg1 = image_to_base64("assets/video1.jpg")
vid_bg2 = image_to_base64("assets/video2.jpg")

# ---------------- UI CSS ---------------- #

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    animation: videoStudioBg 18s infinite;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

@keyframes videoStudioBg {{
    0% {{
        background-image: linear-gradient(rgba(0,0,0,.75), rgba(0,0,0,.9)), url("data:image/jpg;base64,{vid_bg1}");
    }}
    50% {{
        background-image: linear-gradient(rgba(0,0,0,.75), rgba(0,0,0,.9)), url("data:image/jpg;base64,{vid_bg2}");
    }}
    100% {{
        background-image: linear-gradient(rgba(0,0,0,.75), rgba(0,0,0,.9)), url("data:image/jpg;base64,{vid_bg1}");
    }}
}}

[data-testid="stSidebar"] {{
    background: rgba(20,8,8,.97);
    border-right: 1px solid rgba(255,100,0,.35);
}}

.title {{
    font-size: 55px;
    font-weight: 900;
    text-align: center;
    color: white;
    text-shadow: 0 0 22px orange;
    margin-bottom: 20px;
}}

.info-box {{
    background: rgba(0,0,0,.58);
    padding: 24px;
    border-radius: 20px;
    color: white;
    border: 1px solid rgba(255,255,255,.16);
    margin-bottom: 25px;
}}

.stButton>button {{
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color: white;
    font-size: 17px;
    font-weight: 800;
}}

.stButton>button:hover {{
    box-shadow: 0 0 25px orange;
    transform: scale(1.02);
}}

[data-testid="stFileUploader"] {{
    background: rgba(255,255,255,.08);
    border-radius: 16px;
    padding: 14px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎥 AI Video Studio</div>', unsafe_allow_html=True)

if st.button("🏠 Back to Home"):
    st.switch_page("App.py")

st.markdown("""
<div class="info-box">
<h3>🚀 Video Editing & Reel Converter</h3>
<p>
Convert landscape videos into vertical reels, trim clips, add captions, and apply creative video filters such as cinematic, black & white, gaming RGB, warm tone, cool tone, and AI clear enhancement.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MOVIEPY CHECK ---------------- #

if not MOVIEPY_AVAILABLE:
    st.error("Video Studio could not load MoviePy on Streamlit Cloud.")
    st.write("Please copy this error and send it:")
    st.code(MOVIEPY_ERROR)
    st.info("This debug message helps identify the exact missing dependency.")
    st.stop()

# ---------------- PILLOW FIX FOR MOVIEPY ---------------- #

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------------- VIDEO FUNCTIONS ---------------- #

def save_uploaded_video(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, uploaded_file.name)

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    return input_path


def convert_to_vertical(clip):
    w, h = clip.size
    target_ratio = 9 / 16
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        clip = crop(
            clip,
            width=new_w,
            height=h,
            x_center=w / 2,
            y_center=h / 2
        )
    else:
        new_h = int(w / target_ratio)
        clip = crop(
            clip,
            width=w,
            height=new_h,
            x_center=w / 2,
            y_center=h / 2
        )

    return clip.resize((720, 1280))


def add_caption_to_frame(frame, text):
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)

    try:
        caption_font = ImageFont.truetype("arial.ttf", 46)
    except:
        caption_font = ImageFont.load_default()

    w, h = img.size
    box_height = 110
    y_box = h - box_height - 45

    draw.rectangle(
        (45, y_box, w - 45, y_box + box_height),
        fill=(0, 0, 0)
    )

    bbox = draw.textbbox((0, 0), text, font=caption_font)
    text_w = bbox[2] - bbox[0]

    x = (w - text_w) // 2
    y = y_box + 30

    draw.text((x, y), text, font=caption_font, fill=(255, 255, 255))

    return np.array(img)


def apply_video_filter(frame, effect):
    arr = frame.astype(np.float32)

    if effect == "Black & White":
        gray = np.mean(arr, axis=2)
        arr[:, :, 0] = gray
        arr[:, :, 1] = gray
        arr[:, :, 2] = gray

    elif effect == "Cinematic":
        arr *= 0.9
        arr[:, :, 0] *= 1.08
        arr[:, :, 2] *= 0.85
        arr = (arr - 128) * 1.25 + 128

    elif effect == "Gaming RGB":
        arr[:, :, 0] *= 1.25
        arr[:, :, 1] *= 1.10
        arr[:, :, 2] *= 1.45
        arr = (arr - 128) * 1.25 + 128

    elif effect == "Warm Tone":
        arr[:, :, 0] *= 1.25
        arr[:, :, 1] *= 1.08
        arr[:, :, 2] *= 0.88

    elif effect == "Cool Tone":
        arr[:, :, 0] *= 0.88
        arr[:, :, 1] *= 1.05
        arr[:, :, 2] *= 1.35

    elif effect == "AI Clear Video":
        arr = (arr - 128) * 1.30 + 128
        arr *= 1.08

    return np.clip(arr, 0, 255).astype(np.uint8)


def process_video(input_path, start_time, end_time, make_vertical, caption_text, effect, quality):
    video = VideoFileClip(input_path)

    duration = video.duration
    start_time = max(0, min(start_time, duration))
    end_time = max(start_time + 1, min(end_time, duration))

    clip = video.subclip(start_time, end_time)

    if make_vertical:
        clip = convert_to_vertical(clip)

    if effect != "No Filter":
        clip = clip.fl_image(lambda frame: apply_video_filter(frame, effect))

    if caption_text.strip():
        clip = clip.fl_image(lambda frame: add_caption_to_frame(frame, caption_text.strip()))

    output_path = os.path.join(tempfile.mkdtemp(), "jim_ai_studio_video.mp4")

    if quality == "Fast Export":
        fps = 24
        preset = "ultrafast"
        bitrate = "1500k"
    elif quality == "Balanced Export":
        fps = 24
        preset = "fast"
        bitrate = "2500k"
    else:
        fps = 30
        preset = "medium"
        bitrate = "4000k"

    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=fps,
        preset=preset,
        bitrate=bitrate,
        threads=2,
        verbose=False,
        logger=None
    )

    clip.close()
    video.close()

    return output_path


# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("## ⚙️ Video Studio Controls")

uploaded_video = st.sidebar.file_uploader("Upload Video", ["mp4", "mov", "avi"])

tool = st.sidebar.selectbox("Choose Tool", [
    "Trim Video",
    "Convert to Reel Format",
    "Add Caption",
    "Reel + Caption",
    "Video Filters & Effects"
])

effect = st.sidebar.selectbox("Video Filter", [
    "No Filter",
    "Black & White",
    "Cinematic",
    "Gaming RGB",
    "Warm Tone",
    "Cool Tone",
    "AI Clear Video"
])

quality = st.sidebar.selectbox("Export Quality", [
    "Fast Export",
    "Balanced Export",
    "High Quality"
])

preset = st.sidebar.selectbox("Quick Duration Preset", [
    "Custom",
    "15 sec Reel",
    "30 sec Short",
    "60 sec Clip"
])

start_time = st.sidebar.number_input(
    "Start Time (seconds)",
    min_value=0.0,
    value=0.0,
    step=1.0
)

if preset == "15 sec Reel":
    end_time = start_time + 15
elif preset == "30 sec Short":
    end_time = start_time + 30
elif preset == "60 sec Clip":
    end_time = start_time + 60
else:
    end_time = st.sidebar.number_input(
        "End Time (seconds)",
        min_value=1.0,
        value=10.0,
        step=1.0
    )

caption_text = ""
make_vertical = False

if tool == "Convert to Reel Format":
    make_vertical = True

elif tool == "Add Caption":
    caption_text = st.sidebar.text_input("Caption Text", "Follow for more!")

elif tool == "Reel + Caption":
    make_vertical = True
    caption_text = st.sidebar.text_input("Caption Text", "Best moment 🔥")

elif tool == "Video Filters & Effects":
    make_vertical = st.sidebar.checkbox("Convert to 9:16 Reel Format", value=False)
    caption_text = st.sidebar.text_input("Optional Caption Text", "")

generate = st.sidebar.button("🚀 Generate Video")

# ---------------- MAIN ---------------- #

if uploaded_video:
    input_path = save_uploaded_video(uploaded_video)

    st.subheader("📹 Uploaded Video Preview")
    st.video(input_path)

    st.info("Tip: Use short 5–10 second MP4 clips first for online testing.")

    if generate:
        try:
            with st.spinner("🎬 Processing video... Please wait."):
                output_path = process_video(
                    input_path=input_path,
                    start_time=start_time,
                    end_time=end_time,
                    make_vertical=make_vertical,
                    caption_text=caption_text,
                    effect=effect,
                    quality=quality
                )

            st.success("✅ Video generated successfully!")

            st.subheader("🎬 Output Video")
            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    "💾 Download Video",
                    f.read(),
                    file_name="jim_ai_studio_video.mp4",
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(
                "Something went wrong while processing the video. "
                "Please try a smaller clip, shorter duration, or Fast Export mode."
            )
            st.caption(f"Technical error: {e}")

else:
    st.info("👈 Upload a video from sidebar to start.")