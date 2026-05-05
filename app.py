import streamlit as st
import requests
import io
from PIL import Image
import numpy as np

# -------------------------
# 설정
# -------------------------
st.set_page_config(page_title="AI Music Visualizer", layout="wide")

st.markdown("""
<style>
html, body {background-color:#0b0f19; color:white;}
.stButton>button {
    background: linear-gradient(90deg,#6a5cff,#8f7cff);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎧 AI Music → Album Cover Generator")

# -------------------------
# 탭
# -------------------------
tab1, tab2 = st.tabs(["🎵 음악 분석", "🎨 앨범 커버 생성"])

# -------------------------
# 음악 분석 함수
# -------------------------
def analyze_music(file):
    name = file.name.lower()

    mood = "balanced"
    genre = "electronic"

    if "sad" in name:
        mood = "sad emotional"
    elif "happy" in name:
        mood = "bright happy"
    elif "dark" in name:
        mood = "dark moody"
    elif "love" in name:
        mood = "romantic"

    if "hiphop" in name:
        genre = "hip hop"
    elif "rock" in name:
        genre = "rock"
    elif "lofi" in name:
        genre = "lofi"
    elif "pop" in name:
        genre = "pop"

    return mood, genre

# -------------------------
# AI API
# -------------------------
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# -------------------------
# 1. 음악 탭
# -------------------------
with tab1:
    st.header("🎵 음악 분석 & 재생")

    audio_file = st.file_uploader("MP3 업로드", type=["mp3"])

    if audio_file:
        st.audio(audio_file)

        mood, genre = analyze_music(audio_file)

        st.success(f"분석된 분위기: {mood}")
        st.success(f"추정 장르: {genre}")

# -------------------------
# 2. 앨범 생성 탭
# -------------------------
with tab2:
    st.header("🎨 AI 앨범 커버 생성")

    st.write("음악을 먼저 업로드하면 자동으로 반영됩니다")

    generate_btn = st.button("🤖 자동 생성")

# -------------------------
# 실행
# -------------------------
if generate_btn and audio_file:

    mood, genre = analyze_music(audio_file)

    prompt = f"""
album cover art,
{genre} music,
{mood} mood,
modern graphic design,
high quality, 4k, artistic
"""

    st.write("🎯 생성 프롬프트:", prompt)

    images = []

    with st.spinner("AI가 여러 개 생성 중..."):
        for i in range(3):
            img_bytes = generate_image(prompt)
            images.append(img_bytes)

    st.subheader("🎨 결과 선택")

    cols = st.columns(3)

    for i, img in enumerate(images):
        with cols[i]:
            st.image(img)
            st.download_button(
                f"다운로드 {i+1}",
                data=img,
                file_name=f"cover_{i+1}.png",
                mime="image/png"
            )

elif generate_btn:
    st.warning("먼저 음악 파일을 업로드하세요!")
