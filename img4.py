import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_title="Object Detection with YOLOv5", layout="centered")
st.title("🚀 Object Detection using YOLOv5")

# Sample image URL (you can replace this or allow upload)
image_url = "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v0Bm-HQxWtpbQ0Yq463uqw.jpeg"

# Load image from URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")
st.image(image, caption="📸 Input Image", use_container_width=True)

# Load YOLOv5 model (from PyTorch Hub)
st.subheader("🔍 Detecting objects...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# Perform detection
results = model(image)

# Filter for specific object classes
target_classes = {'bus', 'person', 'bicycle'}  # YOLOv5 detects "person" for both man/woman
df = results.pandas().xyxy[0]
filtered_df = df[df['name'].isin(target_classes)]

# Display detected objects
st.markdown("### 📝 Detected Objects")
if not filtered_df.empty:
    for label in sorted(filtered_df['name'].unique()):
        count = filtered_df[filtered_df['name'] == label].shape[0]
        st.write(f"- **{label.capitalize()}** (× {count})")
else:
    st.write("No target objects detected.")

# Display image with bounding boxes
st.subheader("🖼️ Detection Results with Bounding Boxes")
fig, ax = plt.subplots()
results.render()  # Draw boxes on results.ims[0]
ax.imshow(results.ims[0])
ax.axis("off")
st.pyplot(fig)
