import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np
import requests
from io import BytesIO

# ==== Load OCR Reader (Thai + English) ====
@st.cache_resource
def load_reader():
    return easyocr.Reader(['th', 'en'], gpu=False)

reader = load_reader()

# ==== Sample Images ====
sample_images = {
    "ภาพตัวอย่าง 1": "https://www.iri.com/blog/wp-content/uploads/2021/12/darkshield-ocr-image-preprocessing-visa-original-768x511.jpg",
    "ภาพตัวอย่าง 2": "https://www.iri.com/blog/wp-content/uploads/2021/12/darkshield-ocr-image-preprocessing-final-skewed-result-714x350.png",
    "ภาพตัวอย่าง 3": "https://www.iri.com/blog/wp-content/uploads/2021/12/darkshield-ocr-image-preprocessing-fig-3.png"
}

# ==== Search Keyword Input ====
st.sidebar.header("🔎 ค้นหาคำในภาพ")
search_keyword = st.sidebar.text_input("ป้อนคำค้นหา (ภาษาไทย/อังกฤษ)")

# ==== Main Title ====
st.title("🚗 Text Recognition (OCR) with Keyword Search")
st.write("ค้นหาคำที่ต้องการในหลายภาพ (OCR รองรับภาษาไทยและอังกฤษ)")

if search_keyword:
    st.info(f"กำลังค้นหาคำว่า: **{search_keyword}**")
    
    found_any = False  # Flag ว่าพบคำหรือไม่
    
    for label, url in sample_images.items():
        # โหลดภาพ
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        except:
            st.warning(f"❌ โหลด {label} ไม่สำเร็จ")
            continue
        
        # ทำ OCR
        img_array = np.array(image)
        results = reader.readtext(img_array)

        # ตรวจสอบคำค้นหา
        matched = False
        draw = ImageDraw.Draw(image)
        
        # กำหนด font
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        for idx, (bbox, text, conf) in enumerate(results, start=1):
            if search_keyword.lower() in text.lower():
                matched = True
                found_any = True
                points = [tuple(point) for point in bbox]
                draw.line(points + [points[0]], fill="red", width=3)
                draw.text(points[0], text, fill="yellow", font=font)
        
        if matched:
            st.image(image, caption=f"📸 พบคำค้นใน: {label}", use_container_width=True)
    
    if not found_any:
        st.warning("ไม่พบคำที่ค้นหาในภาพใด ๆ")
else:
    st.info("กรุณากรอกคำค้นหาในแถบด้านซ้ายเพื่อเริ่มค้นหา")
