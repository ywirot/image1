import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import easyocr
import matplotlib.pyplot as plt
import numpy as np

# Streamlit config
st.set_page_config(page_title="Text Detection with EasyOCR", layout="centered")
st.title("📖 OCR with EasyOCR (Thai & English)")

# Image URL (you can change or let user upload)
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Thai_text_sample.jpg/800px-Thai_text_sample.jpg"

# Load image from URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert("RGB")

# Show original image
st.image(image, caption="📸 Input Image", use_container_width=True)

# Run EasyOCR
st.subheader("🔍 Reading text using EasyOCR...")
reader = easyocr.Reader(['th', 'en'])  # Thai + English
results = reader.readtext(np.array(image))

# Display detected text
st.markdown("### 📝 Detected Text:")
if results:
    for bbox, text, conf in results:
        st.write(f"- **{text}** (Confidence: {conf:.2f})")
else:
    st.write("No text found.")

# Show image with bounding boxes using matplotlib
st.subheader("🖼️ Image with Text Boxes")
fig, ax = plt.subplots()
ax.imshow(image)
for bbox, text, conf in results:
    points = np.array(bbox).astype(int)
    x, y = points[0]
    ax.plot(*zip(*(list(points) + [points[0]])), color='red', linewidth=1)
    ax.text(x, y - 5, text, fontsize=8, color='red', backgroundcolor='white')
ax.axis('off')
st.pyplot(fig)
