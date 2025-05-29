import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="Object Detection: Bus, Person, Bicycle", layout="centered")
st.title("🚀 Object Detection: Bus, Person, Bicycle")

# Image URL (contains multiple objects)
image_url = "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v0Bm-HQxWtpbQ0Yq463uqw.jpeg"

# Load image from URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")

# Show original image
st.image(image, caption="📸 Input Image", use_container_width=True)

# Load YOLOv5s model
st.subheader("🔍 Detecting objects...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# Run object detection
results = model(image)

# Filter results for specific classes
target_classes = {'bus', 'person', 'bicycle'}
df = results.pandas().xyxy[0]
filtered_df = df[df['name'].isin(target_classes)]

# Display detected objects
st.markdown("### 📝 Detected Objects")
if not filtered_df.empty:
    for label in sorted(filtered_df['name'].unique()):
        count = filtered_df[filtered_df['name'] == label].shape[0]
        st.write(f"- **{label.capitalize()}** (× {count})")
else:
    st.write("No target objects (bus, person, bicycle) were detected.")

# Show image with bounding boxes
st.subheader("🖼️ Detection Results with Bounding Boxes")
fig, ax = plt.subplots()
results.render()
ax.imshow(results.ims[0])
ax.axis("off")
st.pyplot(fig)
