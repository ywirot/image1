import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Blend Smiling and Laughing Woman", layout="centered")
st.title("😊 Blend Two Expressions of the Same Woman with X-Y Axes")

# 🔗 URLs ของภาพผู้หญิงคนเดียวกันในสองอิริยาบถ
url1 = "https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg?auto=compress&cs=tinysrgb&h=400"  # Smiling
url2 = "https://images.pexels.com/photos/1130624/pexels-photo-1130624.jpeg?auto=compress&cs=tinysrgb&h=400"  # Laughing and leaning back

# 🔄 Slider ปรับค่าการ Blending
alpha = st.slider("🔄 Blending Ratio (alpha)", 0.0, 1.0, 0.5, 0.05)

try:
    # โหลดภาพทั้งสอง
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    img1 = Image.open(BytesIO(response1.content)).convert("RGBA")
    img2 = Image.open(BytesIO(response2.content)).convert("RGBA")

    # ปรับขนาดให้เท่ากัน
    img2_resized = img2.resize(img1.size)

    # ผสมภาพ
    blended_img = Image.blend(img1, img2_resized, alpha)

    # แสดงภาพต้นฉบับ
    st.subheader("🧍 Original Images")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Smiling Woman", use_container_width=True)
    with col2:
        st.image(img2_resized, caption="Laughing Woman (resized)", use_container_width=True)

    # แสดงผลลัพธ์พร้อมแกน X-Y
    st.subheader("🎨 Blended Result with X-Y Axes")
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
