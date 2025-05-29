import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Streamlit page config
st.set_page_config(page_title="YOLO Object Detection", layout="centered")
st.title("🚀 Object Detection using YOLOv8")

# Step 1: Load image from URL
image_url = "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v0Bm-HQxWtpbQ0Yq463uqw.jpeg"
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")
st.image(image, caption="📸 Input Image", use_container_width=True)

# Step 2: Load YOLOv8 model (small model for speed)
st.subheader("🔍 Running YOLOv8 inference...")
model = YOLO("yolov8n.pt")  # You can use yolov5s.pt or yolov8s.pt as well

# Step 3: Run detection
results = model(image)

# Step 4: Filter target classes
target_classes = {"bus", "person", "bicycle"}
names = model.names
detected_labels = []

st.markdown("### 📝 Detected Objects")
for r in results:
    for box in r.boxes:
        class_id = int(box.cls[0].item())
        label = names[class_id]
        if label in target_classes:
            detected_labels.append(label)

# Step 5: Display detection summary
if detected_labels:
    for label in sorted(set(detected_labels)):
        count = detected_labels.count(label)
        st.write(f"- **{label.capitalize()}** (× {count})")
else:
    st.write("No target objects (bus, person, bicycle) detected.")

# Step 6: Show result image with bounding boxes
st.subheader("🖼️ Image with Bounding Boxes")
result_image = results[0].plot()  # This draws box_
