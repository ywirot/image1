import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #fdf6f0;
            color: #333;
        }
        h1 {
            color: #d14b8f;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .caption {
            font-size: 16px;
            text-align: center;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌹 ดอกกุหลาบป่า (Rosa rubiginosa)</h1>", unsafe_allow_html=True)

# --- Load and display image from URL ---
image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e6/Rosa_rubiginosa_1.jpg"
response = requests.get(image_url)

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="ภาพจาก Wikimedia Commons", use_column_width="always")
else:
    st.error("ไม่สามารถโหลดรูปภาพจาก URL ได้")

# --- Additional description ---
st.markdown('<p class="caption">ภาพของ Rosa rubiginosa หรือกุหลาบป่า มีถิ่นกำเนิดในยุโรปและเอเชียตะวันตก 🌿</p>', unsafe_allow_html=True)
