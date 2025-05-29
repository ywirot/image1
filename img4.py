import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
import matplotlib.pyplot as plt

st.set_page_config(page_title="Object Detection (Bus, People, Bike, Tree)", layout="centered")
st.title("🚀 Object Detection: Bus, Person, Bike, Tree")

# 🔗 ภาพตัวอย่างที่มีวัตถุหลากหลาย
image_url = "https://images.pexels.com/photos/3803835/pexels-photo-3803835.jpeg?auto=compress&cs=tinysrgb&h=640"

# โหลดภาพจาก URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")

st.image(image, caption="📸 Input Image", use_container_width=True)

# โหลด YOLOv5 model (ใช้ yolov5s ที่เบาและเร็ว)
st.subheader("🔍 Detecting objects...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# ตรวจจับวัตถุ
results = model(image)

# กรองเฉพาะวัตถุที่ต้องการ
allowed_classes = {'bus', 'person', 'bicycle'}  # YOLOv5 ใช้ 'person', 'bicycle' แทน man/woman/bike

df = results.pandas().xyxy[0]
filtered_df = df[df['name'].isin(allowed_classes)]

# แสดงรายการวัตถุที่ตรวจพบ
st.markdown("### 📝 Detected Objects:")
if not filtered_df.empty:
    for label in sorted(filtered_df['name'].unique()):
        count = filtered_df[filtered_df['name'] == label].shape[0]
        st.write(f"- {label} (x{count})")
else:
    st.write("No target objects (bus, person, bicycle) found.")

# แสดงภาพพร้อม Bounding Boxes
st.subheader("🖼️ Detection with Bounding Boxes")
fig, ax = plt.subplots()
results.render()
ax.imshow(results.ims[0])
ax.axis('off')
st.pyplot(fig)
