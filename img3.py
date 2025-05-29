import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Blend Thai Woman Expressions", layout="centered")
st.title("🇹🇭 Blend Smiling and Laughing Thai Woman with X-Y Axes")

# 🔗 ภาพผู้หญิงไทยคนเดียวกันในอิริยาบถต่างกัน (จาก Pexels)
url1 = "https://www.sumupth.com/wp-content/uploads/2024/07/8826-1024x683.jpg"  # Smiling
url2 = "https://storage-wp.thaipost.net/2022/12/%E0%B8%84%E0%B8%B3-%E0%B8%9C%E0%B8%81%E0%B8%B2.jpg"  # Laughing

# 🔄 blending control
alpha = st.slider("🔄 Blending Ratio (alpha)", 0.0, 1.0, 0.5, 0.05)

try:
    # Load images
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    img1 = Image.open(BytesIO(response1.content)).convert("RGBA")
    img2 = Image.open(BytesIO(response2.content)).convert("RGBA")

    # Resize to match
    img2_resized = img2.resize(img1.size)

    # Blend
    blended_img = Image.blend(img1, img2_resized, alpha)

    # Show originals
    st.subheader("🧍 Original Photos")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Smiling Thai Woman", use_container_width=True)
    with col2:
        st.image(img2_resized, caption="Laughing Thai Woman", use_container_width=True)

    # Show blended result
    st.subheader("🎨 Blended Image with X-Y Axes")
    fig, ax = plt.subplots()
    ax.imshow(blended_img)
    ax.set_title(f"Blended Image (alpha = {alpha})", fontsize=12)
    ax.set_xlabel("X-axis (pixels)")
    ax.set_ylabel("Y-axis (pixels)")
    ax.grid(False)
    st.pyplot(fig)

except Exception as e:
    st.error("❌ Failed to load or process images.")
    st.code(str(e), language="python")
