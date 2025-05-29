import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="แสดงรูปภาพพร้อมแกน", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main { background-color: #fdf6f0; color: #333; }
        h1 { color: #d14b8f; text-align: center; }
        .caption { font-size: 16px; text-align: center; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌹 Rosa rubiginosa (กุหลาบป่า)</h1>", unsafe_allow_html=True)

# --- รูปภาพจาก URL ---
image_url = "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"

# --- ควบคุมการแสดงผลโดยผู้ใช้ ---
scale_percent = st.slider("🔧 ปรับขนาดภาพ (%)", min_value=10, max_value=200, value=100, step=10)
flip_option = st.radio("🔁 ต้องการพลิกภาพหรือไม่?", ("ไม่พลิก", "Flip แนวนอน", "Flip แนวตั้ง"))

# --- โหลดและแสดงภาพ ---
try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert("RGB")

    # --- Flip ภาพตามที่เลือก ---
    if flip_option == "Flip แนวนอน":
        image = ImageOps.mirror(image)
    elif flip_option == "Flip แนวตั้ง":
        image = ImageOps.flip(image)

    # --- Resize ภาพ ---
    width, height = image.size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    resized_image = image.resize((new_width, new_height))

    # --- แสดงภาพผ่าน matplotlib พร้อมแกน X-Y ---
    fig, ax = plt.subplots()
    ax.im
