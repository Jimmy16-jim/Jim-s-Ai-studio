import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import numpy as np
import io
import random
import base64

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_bg1 = image_to_base64("assets/image1.jpg")
img_bg2 = image_to_base64("assets/image2.jpg")

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
# ---------------- UI ---------------- #
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    animation: imageStudioBg 24s infinite;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

@keyframes imageStudioBg {{
    0% {{
        background-image: linear-gradient(rgba(0,0,0,.72), rgba(0,0,0,.88)), url("data:image/jpg;base64,{img_bg1}");
    }}
    25% {{
        background-image: linear-gradient(rgba(0,0,0,.72), rgba(0,0,0,.88)), url("data:image/jpg;base64,{img_bg2}");
    }}
 
    100% {{ background-image: linear-gradient(rgba(0,0,0,.72), rgba(0,0,0,.88)), url("data:image/jpg;base64,{img_bg1}");
    }}
}}

[data-testid="stSidebar"] {{
    background: rgba(8,8,22,.97);
    border-right: 1px solid rgba(0,255,255,.25);
}}

.main-title {{
    font-size: 56px;
    font-weight: 900;
    text-align: center;
    color: white;
    text-shadow: 0 0 22px cyan;
}}

.stButton>button {{
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg,#00e5ff,#0066ff);
    color: white;
    font-weight: 800;
}}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">🎨 AI Image Studio</div>', unsafe_allow_html=True)

# ---------------- HELPERS ---------------- #

def resize_fast(img, max_size=900):
    img = img.convert("RGB")
    img.thumbnail((max_size, max_size))
    return img

def download_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

@st.cache_data
def remove_bg_fast(img_bytes):
    from rembg import remove
    return remove(img_bytes)

# ---------------- RELIABLE EFFECTS ---------------- #

def cyberpunk(img):
    img = ImageEnhance.Color(img).enhance(2.3)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    arr = np.array(img).astype(np.float32)
    arr[:, :, 2] *= 1.45
    arr[:, :, 0] *= 1.15
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def neon_glow(img):
    glow = img.filter(ImageFilter.GaussianBlur(5))
    img = ImageEnhance.Color(img).enhance(1.8)
    return Image.blend(img, glow, 0.35)

def gaming_sharp(img):
    img = ImageEnhance.Sharpness(img).enhance(2.2)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Color(img).enhance(1.25)
    return img

def cinematic(img):
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Brightness(img).enhance(0.9)
    img = ImageEnhance.Color(img).enhance(1.15)
    return img

def sketch(img):
    gray = ImageOps.grayscale(img)
    inv = ImageOps.invert(gray)
    blur = inv.filter(ImageFilter.GaussianBlur(8))
    sketch_img = Image.blend(gray, blur, 0.35)
    return ImageOps.autocontrast(sketch_img).convert("RGB")

def background_remove(img):
    b = io.BytesIO()
    img.save(b, format="PNG")
    out = remove_bg_fast(b.getvalue())
    return Image.open(io.BytesIO(out)).convert("RGBA")

def profile_picture(img):
    size = 800
    img = ImageOps.fit(img, (size, size))

    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((25, 25, size-25, size-25), fill=255)

    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)

    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((18, 18, size-18, size-18), outline=(0, 255, 255, 255), width=16)
    rd.ellipse((42, 42, size-42, size-42), outline=(255, 0, 255, 170), width=8)

    return Image.alpha_composite(output, ring).convert("RGB")

def meme_generator(img, top, bottom):
    img = ImageOps.fit(img, (1080, 1080))
    draw = ImageDraw.Draw(img)
    f = font(70)

    def center_text(text, y):
        text = text.upper()
        box = draw.textbbox((0, 0), text, font=f, stroke_width=5)
        x = (1080 - (box[2] - box[0])) // 2
        draw.text((x, y), text, font=f, fill="white", stroke_width=5, stroke_fill="black")

    if top:
        center_text(top, 45)
    if bottom:
        center_text(bottom, 900)

    return img

def poster_maker(img, title):
    img = ImageOps.fit(img, (900, 1200))
    img = cinematic(img).convert("RGBA")

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 55))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 900, 900, 1200), fill=(0, 0, 0, 190))

    title_font = font(78)
    sub_font = font(34)

    text = title.upper() if title else "CREATIVE POSTER"
    draw.text((45, 940), text, font=title_font, fill="yellow", stroke_width=4, stroke_fill="black")
    draw.text((50, 1090), "Made with Jim's AI Studio", font=sub_font, fill="white")

    return img.convert("RGB")

def youtube_thumbnail(img, text, style):
    img = ImageOps.fit(img, (1280, 720))
    bg = img.filter(ImageFilter.GaussianBlur(8))
    bg = ImageEnhance.Brightness(bg).enhance(0.65)

    subject = ImageOps.fit(img, (620, 620))
    subject = ImageEnhance.Contrast(subject).enhance(1.2)
    subject = ImageEnhance.Sharpness(subject).enhance(1.8)

    bg.paste(subject, (60, 60))

    draw = ImageDraw.Draw(bg)
    big = font(95)
    small = font(62)

    words = text.upper().split() if text else ["BEST", "THUMBNAIL"]
    mid = max(1, len(words)//2)
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    color = {
        "Gaming 🎮": "yellow",
        "Tech 💻": "cyan",
        "Vlog 📸": "white"
    }.get(style, "yellow")

    x, y = 700, 340

    draw.rectangle((680, 310, 1240, 610), fill=(0, 0, 0))
    draw.text((x, y), line1, font=big, fill=color, stroke_width=5, stroke_fill="black")
    draw.text((x, y + 105), line2, font=small, fill="white", stroke_width=4, stroke_fill="black")

    draw.polygon([(620, 360), (690, 395), (620, 430)], fill="red")
    draw.ellipse((70, 70, 650, 650), outline="yellow", width=8)

    if style == "Gaming 🎮":
        bg = gaming_sharp(bg)
    elif style == "Tech 💻":
        bg = cyberpunk(bg)
    else:
        bg = cinematic(bg)

    return bg

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("## ⚙️ Image Studio Controls")

tool = st.sidebar.selectbox("Choose Tool", [
    "Basic Effects",
    "Background Remover",
    "YouTube Thumbnail",
    "Meme Generator",
    "Poster Maker",
    "Profile Picture Maker"
])

uploaded = st.sidebar.file_uploader("Upload Image", ["jpg", "jpeg", "png"])

effect = None
top_text = ""
bottom_text = ""
title_text = ""
thumb_text = ""
thumb_style = "Gaming 🎮"

if tool == "Basic Effects":
    effect = st.sidebar.selectbox("Choose Effect", [
        "Original",
        "Cyberpunk",
        "Neon Glow",
        "Gaming Sharp",
        "Cinematic",
        "Sketch",
        "Grayscale"
    ])

elif tool == "YouTube Thumbnail":
    thumb_text = st.sidebar.text_input("Thumbnail Text", "BEST AI TOOL EVER")
    thumb_style = st.sidebar.selectbox("Thumbnail Style", ["Gaming 🎮", "Tech 💻", "Vlog 📸"])

elif tool == "Meme Generator":
    top_text = st.sidebar.text_input("Top Text", "WHEN AI WORKS")
    bottom_text = st.sidebar.text_input("Bottom Text", "FIRST TRY")

elif tool == "Poster Maker":
    title_text = st.sidebar.text_input("Poster Title", "AI CREATOR")

run = st.sidebar.button("🚀 Generate")

# ---------------- MAIN ---------------- #

if uploaded:
    img = resize_fast(Image.open(uploaded))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Original")
        st.image(img, use_container_width=True)
 
if run:

     try:

         with st.spinner("Generating image..."):

          if tool == "Basic Effects":

                if effect == "Cyberpunk":
                    out = cyberpunk(img)

                elif effect == "Neon Glow":
                    out = neon_glow(img)

                elif effect == "Gaming Sharp":
                    out = gaming_sharp(img)

                elif effect == "Cinematic":
                    out = cinematic(img)

                elif effect == "Sketch":
                    out = sketch(img)

                elif effect == "Grayscale":
                    out = ImageOps.grayscale(img).convert("RGB")

                else:
                    out = img

          elif tool == "Background Remover":
                out = background_remove(img)

          elif tool == "YouTube Thumbnail":
                out = youtube_thumbnail(img, thumb_text, thumb_style)

          elif tool == "Meme Generator":
                out = meme_generator(img, top_text, bottom_text)

          elif tool == "Poster Maker":
                out = poster_maker(img, title_text)

          elif tool == "Profile Picture Maker":
                out = profile_picture(img)

          else:
                out = img

         st.success("✅ Image generated successfully!")

         with col2:
            st.subheader("🎨 Output")
            st.image(out, use_container_width=True)

         st.download_button(
            "💾 Download Output",
            download_bytes(out.convert("RGB")),
            "output.png"
        )

     except Exception as e:

        st.error("Something went wrong while processing the image.")
        st.caption(f"Technical error: {e}")

else:

    st.info("👈 Upload a clear image from the sidebar. For best results, use portraits, product photos, or simple backgrounds.")

    