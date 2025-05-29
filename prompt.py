import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import numpy as np

st.set_page_config(page_title="แสดงรูปภาพ", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #fdf6f0; color: #333; }
        h1 { color: #d14b8f; text-align: center; }
        .caption { font-size: 16px; text-align: center; color: #666; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🌹 Rosa rubiginosa (กุหลาบป่า)</h1>", unsafe_allow_html=True)

# รูปภาพจาก URL
image_url = "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"

# ตัวปรับขนาดภาพ
scale_percent = st.slider("ปรับขนาดภาพ (%):", min_value=10, max_value=200, value=100, step=10)

try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # ปรับขนาดภาพ
    width, height = image.size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    resized_image = image.resize((new_width, new_height))

    # แสดงภาพ
    st.image(resized_image, caption="ภาพจาก Pexels.com", use_container_width=False)
    st.markdown('<p class="caption">กุหลาบป่าจากยุโรป 🌿</p>', unsafe_allow_html=True)

except requests.exceptions.RequestException as e:
    st.error("❌ ไม่สามารถโหลดรูปภาพจาก URL ได้")
    st.code(str(e), language="python")
