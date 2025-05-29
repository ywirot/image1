import streamlit as st
from PIL import Image
import requests
from io import BytesIO

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
image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e6/Rosa_rubiginosa_1.jpg"

try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()  # ถ้ามี error เช่น 404 จะ throw exception
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="ภาพจาก Wikimedia Commons", use_column_width="always")
    st.markdown('<p class="caption">กุหลาบป่าจากยุโรป 🌿</p>', unsafe_allow_html=True)

except requests.exceptions.RequestException as e:
    st.error("❌ ไม่สามารถโหลดรูปภาพจาก URL ได้")
    st.code(str(e), language="python")
