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

# ==== Sidebar Inputs ====
st.sidebar.header("📥 เลือกรูปแบบการนำเข้ารูปภาพ")
input_method = st.sidebar.radio("วิธีการเลือกภาพ:", ["ภาพตัวอย่าง", "อัปโหลดภาพ", "ป้อน URL รูปภาพ"])

search_keyword = st.sidebar.text_input("🔍 ป้อนคำค้นหา (ไม่บังคับ)", placeholder="เช่น: VISA, บัตร, ...")

# ==== Sidebar: Sample Images ====
sample_choice = None
if input_method == "ภาพตัวอย่าง":
    for label, url in sample_images.items():
        st.sidebar.image(url, caption=label, use_container_width=True)
        if st.sidebar.button(f"ใช้ {label}"):
            sample_choice = url
            st.session_state.selected_sample_label = label

# ==== Main Title ====
st.title("🚗 Text Recognition (OCR) + Keyword Search")
st.write("เลือกรูปภาพเพื่อตรวจจับข้อความจากภาพ (รองรับภาษาไทยและอังกฤษ)\nพร้อมค้นหาคำที่ต้องการ")

# ==== Image Selection Logic ====
images_to_process = []

if input_method == "ภาพตัวอย่าง" and sample_choice:
    try:
        response = requests.get(sample_choice)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        images_to_process.append((image, st.session_state.selected_sample_label))
        st.success(f"✅ โหลด {st.session_state.selected_sample_label} สำเร็จ")
    except:
        st.error("❌ ไม่สามารถโหลดภาพตัวอย่างได้")

elif input_method == "อัปโหลดภาพ":
    uploaded_file = st.file_uploader("📷 เลือกรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        images_to_process.append((image, uploaded_file.name))

elif input_method == "ป้อน URL รูปภาพ":
    image_url = st.text_input("🔗 วางลิงก์ URL ของรูปภาพที่ต้องการตรวจจับข้อความ")
    if image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            images_to_process.append((image, "ภาพจาก URL"))
            st.success("✅ โหลดภาพจาก URL สำเร็จ")
        except:
            st.error("❌ ไม่สามารถโหลดภาพจาก URL ได้ กรุณาตรวจสอบลิงก์")

# ==== OCR Processing ====
if images_to_process:
    found_in_any = False

    for img, label in images_to_process:
        st.image(img, caption=f"📸 {label}", use_container_width=True)

        img_array = np.array(img)

        with st.spinner(f"🔍 กำลังตรวจจับข้อความใน {label}..."):
            results = reader.readtext(img_array)

        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        found_texts = []
        matched = False

        for idx, (bbox, text, confidence) in enumerate(results, start=1):
            if confidence > 0.4:
                found_texts.append((idx, text, confidence))
                points = [tuple(point) for point in bbox]
                draw.line(points + [points[0]], fill="red", width=3)
                draw.text(points[0], str(idx), fill="yellow", font=font)

                # ตรวจสอบคำค้นหา
                if search_keyword and search_keyword.lower() in text.lower():
                    matched = True
                    found_in_any = True

        # แสดงผลลัพธ์ OCR
        st.image(img, caption=f"🟥 ตรวจพบข้อความใน {label}", use_container_width=True)

        if found_texts:
            st.write(f"### 📝 ข้อความที่ตรวจพบใน {label}:")
            for idx, text, conf in found_texts:
                st.write(f"{idx}. **{text}** ({conf*100:.2f}%)")
        else:
            st.warning(f"ไม่พบข้อความที่มีความมั่นใจเพียงพอใน {label}")

        # ถ้ามีคำค้นหา และเจอคำค้น
        if search_keyword:
            if matched:
                st.success(f"✅ พบคำค้นหา \"{search_keyword}\" ใน {label}")
            else:
                st.info(f"❌ ไม่พบคำค้นหา \"{search_keyword}\" ใน {label}")

    # ถ้าไม่มีภาพไหนพบคำค้น
    if search_keyword and not found_in_any:
        st.warning("🔍 ไม่พบคำค้นหาในภาพใด ๆ")

else:
    st.info("กรุณาเลือกรูปภาพเพื่อเริ่มตรวจจับข้อความ")

