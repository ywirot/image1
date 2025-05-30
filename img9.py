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

# ==== Sidebar: Keyword Input ====
st.sidebar.header("🔎 ค้นหาคำในภาพ")
search_keyword = st.sidebar.text_input("ป้อนคำค้นหา (ภาษาไทย/อังกฤษ)")

# ==== Main Title ====
st.title("🚗 Text Recognition (OCR) with Keyword Search")
st.write("OCR หลายภาพ + ค้นหาคำที่ต้องการ (ภาษาไทย/อังกฤษ)")

# ==== OCR Processing for All Images ====
ocr_results = []

with st.spinner("📥 กำลังโหลดและประมวลผลภาพ..."):
    for label, url in sample_images.items():
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        except:
            st.warning(f"❌ โหลด {label} ไม่สำเร็จ")
            continue
        
        img_array = np.array(image)
        results = reader.readtext(img_array)

        text_data = []
        for bbox, text, conf in results:
            text_data.append({
                "bbox": bbox,
                "text": text,
                "conf": conf
            })

        ocr_results.append({
            "label": label,
            "image": image,
            "text_data": text_data
        })

st.success("✅ OCR เสร็จสิ้นสำหรับทุกภาพแล้ว!")

# ==== Search Keyword ====
if search_keyword:
    st.info(f"🔍 ค้นหาคำว่า: **{search_keyword}**")

    found_any = False

    for result in ocr_results:
        label = result["label"]
        image = result["image"].copy()  # ทำสำเนาภาพ เพื่อวาดผล
        text_data = result["text_data"]

        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        matched = False
        for item in text_data:
            text = item["text"]
            bbox = item["bbox"]
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

# ==== แสดงข้อความที่ OCR พบในแต่ละภาพ (ฟีเจอร์เดิม) ====
st.divider()
st.write("## 📝 ข้อความที่พบจาก OCR แต่ละภาพ")
for result in ocr_results:
    label = result["label"]
    text_data = result["text_data"]
    st.write(f"### 📌 {label}")
    if text_data:
        for idx, item in enumerate(text_data, start=1):
            st.write(f"{idx}. **{item['text']}** ({item['conf']*100:.2f}%)")
    else:
        st.warning("ไม่พบข้อความที่มีความมั่นใจเพียงพอ")
