import streamlit as st
import requests
from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans

# -------------------------
# 기본 설정
# -------------------------
st.set_page_config(page_title="AI Music & Album Art", layout="wide")

# -------------------------
# 다크 UI
# -------------------------
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

st.title("🎧 AI Music + Album Cover Generator")

# -------------------------
# 탭 분리
# -------------------------
tab1, tab2 = st.tabs(["🎵 음악 재생", "🎨 앨범 커버 생성"])

# -------------------------
# 🎵 1. 음악 플레이어
# -------------------------
with tab1:
    st.header("🎵 음악 재생")

    audio_file = st.file_uploader("음악 파일 업로드 (mp3)", type=["mp3"])

    if audio_file:
        st.audio(audio_file, format="audio/mp3")

        st.success("음악 재생 중 🎶")

# -------------------------
# 🎨 2. 앨범 커버 생성
# -------------------------
with tab2:
    st.header("🎨 AI 앨범 커버 생성")

    mood = st.selectbox(
        "분위기 선택",
        ["감성", "힙합", "밝음", "어두움", "몽환적"]
    )

    genre = st.selectbox(
        "장르",
        ["pop", "hip hop", "lofi", "electronic", "rock"]
    )

    generate_btn = st.button("🤖 앨범 커버 생성")

# -------------------------
# AI 이미지 생성
# -------------------------
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"
}

def generate_cover(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# -------------------------
# 실행
# -------------------------
if generate_btn:
    prompt = f"""
album cover art,
{genre} music,
{mood} mood,
modern design,
high quality, artistic, 4k
"""

    with st.spinner("AI가 앨범 커버 생성 중..."):
        img_bytes = generate_cover(prompt)

    st.image(img_bytes)

    st.download_button(
        "📥 다운로드",
        data=img_bytes,
        file_name="album_cover.png",
        mime="image/png"
    )
