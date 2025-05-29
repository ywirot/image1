import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Image Viewer", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main { background-color: #fdf6f0; color: #333; }
        h1 { color: #d14b8f; text-align: center; }
        .caption { font-size: 16px; text-align: center; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌹 Image Viewer with X-Y Axes</h1>", unsafe_allow_html=True)

# --- Image Options ---
image_options = {
    "Rose": "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg",
    "Sunflower": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg",
    "Lavender": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg"  # ใส่ลิงก์ใหม่ได้
}

# --- User Input ---
selected_image_name = st.selectbox("📸 Select an image:", list(image_options.keys()))
image_url = image_options[selected_image_name]

scale_percent = st.slider("🔧 Resize Image (%)", min_value=10, max_value=200, value=100, step=10)
flip_option = st.radio("🔁 Flip Image", ("No Flip", "Flip Horizontally", "Flip Vertically"))

# --- Load and Display Image ---
try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert("RGB")

    # --- Flip ---
    if flip_option == "Flip Horizontally":
        image = ImageOps.mirror(image)
    elif flip_option == "Flip Vertically":
        image = ImageOps.flip(image)

    # --- Resize ---
    width, height = image.size
    new_size = (int(width * scale_percent / 100), int(height * scale_percent / 100))
    image_resized = image.resize(new_size)

    # --- Display with Axes ---
    fig, ax = plt.subplots()
    ax.imshow(image_resized)
    ax.set_title(f"{selected_image_name} | Size: {scale_percent}% | {flip_option}")
    ax.set_xlabel("X-axis (pixels)")
    ax.set_ylabel("Y-axis (pixels)")
    ax.grid(False)

    st.pyplot(fig)

    st.markdown(f'<p class="caption">Image: {selected_image_name} from Pexels</p>', unsafe_allow_html=True)

except requests.exceptions.RequestException as e:
    st.error("❌ Failed to load image.")
    st.code(str(e), language="python")
