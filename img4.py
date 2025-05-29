import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
import matplotlib.pyplot as plt

st.set_page_config(page_title="Animal Detection", layout="centered")
st.title("🦒🕊️ Animal Detection: Elephant, Horse, Giraffe, Bird")

# ✅ ใช้ภาพที่มีสัตว์หลายชนิด
image_url = "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v0Bm-HQxWtpbQ0Yq463uqw.jpeg"

# โหลดภาพ
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")
st.image(image, caption="Wildlife Image: Elephant, Giraffe, Zebra, Birds", use_container_width=True)

# โหลดโมเดล YOLOv5 จาก PyTorch Hub
st.subheader("🔍 Running YOLOv5 Object Detection...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# ตรวจจับวัตถุ
results = model(image)

# แสดงผลลัพธ์
labels = results.pandas().xyxy[0]['name'].tolist()
st.markdown("### 📝 Detected Objects:")
if labels:
    for label in sorted(set(labels)):
        count = labels.count(label)
        st.write(f"- {label} (x{count})")
else:
    st.write("No animals detected.")

# แสดงภาพพร้อม bounding boxes
st.markdown("### 🖼️ Image with Bounding Boxes")
fig, ax = plt.subplots()
results.render()
ax.imshow(results.ims[0])
ax.axis('off')
st.pyplot(fig)
