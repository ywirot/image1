import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Page config
st.set_page_config(page_title="YOLO Object Detection", layout="centered")
st.title("🚀 Object Detection using Ultralytics YOLO")

# Image URL (You can replace or allow upload)
image_url = "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v0Bm-HQxWtpbQ0Yq463uqw.jpeg"
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")
st.image(image, caption="📸 Input Image", use_container_width=True)

# Load YOLOv8 model (YOLOv5 also available via ultralytics)
st.subheader("🔍 Detecting objects with YOLOv8...")
model = YOLO("yolov8n.pt")  # or yolov5s.pt if you prefer YOLOv5

# Run detection
results = model(image)

# Filter only specific classes (YOLO class names)
target_classes = {"bus", "person", "bicycle"}
names = model.names
detected = []

# Get detections
st.markdown("### 📝 Detected Objects")
for r in results:
    boxes = r.boxes
    if boxes is not None:
        for box in boxes:
            cls = int(box.cls[0].item())
            label = names[cls]
            if label in target_classes:
                detected.append(label)

# Show count
if detected:
    for label in sorted(set(detected)):
        count = detected.count(label)
        st.write(f"- **{label.capitalize()}** (× {count})")
else:
    st.write("No target objects (bus, person, bicycle) detected.")

# Show result image
st.subheader("🖼️ Image with Bounding Boxes")
res_img = results[0].plot()  # Draw boxes
st.image(res_img, use_container_width=True)
