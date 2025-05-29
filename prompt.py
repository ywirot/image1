import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ชื่อหน้าเว็บ
st.title("แสดงภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e6/Rosa_rubiginosa_1.jpg"

# ดึงข้อมูลรูปภาพจาก URL
response = requests.get(image_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="Rosa rubiginosa", use_column_width=True)
else:
    st.error("ไม่สามารถโหลดรูปภาพจาก URL ได้")
