import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import easyocr
import matplotlib.pyplot as plt

st.set_page_config(page_title="Text Detection with EasyOCR", layout="centered")
st.title("📖 OCR with EasyOCR (Thai & English)")

# โหลดภาพจาก URL หรืออัปโหลด
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Thai_text_sample.jpg/800px-Thai_text_sample.jpg"
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")

st.image(image, caption="📸 Input Image", use_container_width=True)

# โหลดโมเดล OCR
st.subheader("🔍 Reading text...")
reader = easyocr.Reader(['th', 'en'])  # รองรับภาษาไทยและอังกฤษ

# แปลงภาพเป็นข้อมูล OCR
results = reader.readtext(np.array(image))

# แสดงผลลัพธ์
st.markdown("### 📝 Detected Text:")
if results:
    for bbox, text, conf in results:
        st.write(f"- **{text}** (Confidence: {conf:.2f})")
else:
    st.write("ไม่พบข้อความในภาพ")

# แสดงภาพพร้อมกรอบข้อความ
st.subheader("🖼️ Text Boxes")
fig, ax = plt.subplots()
ax.imshow(image)
for bbox, text, conf in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    x, y = top_left
    ax.plot([p[0] for p in bbox] + [bbox[0][0]], [p[1] for p in bbox] + [bbox[0][1]], 'r-')
    ax.text(x, y - 5, text, fontsize=8, color='red')
ax.axis('off')
st.pyplot(fig)
