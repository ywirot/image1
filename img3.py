import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="Blend Two Rose Images", layout="centered")
st.title("🌹 Blending Two Rose Images")

# URLs of two rose images (ขนาดไม่เท่ากัน)
url1 = "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg?auto=compress&cs=tinysrgb&h=400"
url2 = "https://images.pexels.com/photos/1020895/pexels-photo-1020895.jpeg?auto=compress&cs=tinysrgb&h=300"

# Slider for alpha blending
alpha = st.slider("🔄 Blending Ratio", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# Load both images
try:
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    img1 = Image.open(BytesIO(response1.content)).convert("RGBA")
    img2 = Image.open(BytesIO(response2.content)).convert("RGBA")

    # Resize second image to match the first
    img2_resized = img2.resize(img1.size)

    # Blend images
    blended = Image.blend(img1, img2_resized, alpha)

    # Show original images side by side
    st.subheader("🔍 Original Images")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Rose Image 1", use_container_width=True)
    with col2:
        st.image(img2_resized, caption="Rose Image 2 (resized)", use_container_width=True)

    # Show blended result
    st.subheader("🎨 Blended Image")
    st.image(blended, caption=f"Blended with alpha={alpha}", use_container_width=True)

except Exception as e:
    st.error("❌ Failed to load or process images.")
    st.code(str(e), language="python")
