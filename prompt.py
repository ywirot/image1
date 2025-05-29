import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Display Image with Axes", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main { background-color: #fdf6f0; color: #333; }
        h1 { color: #d14b8f; text-align: center; }
        .caption { font-size: 16px; text-align: center; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌹 Rosa rubiginosa (Sweet Briar Rose)</h1>", unsafe_allow_html=True)

# --- Image URL ---
image_url = "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"

# --- User Controls ---
scale_percent = st.slider("🔧 Resize Image (%)", min_value=10, max_value=200, value=100, step=10)
flip_option = st.radio("🔁 Flip Image", ("No Flip", "Flip Horizontally", "Flip Vertically"))

# --- Load and Display Image ---
try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert("RGB")

    # --- Flip Image ---
    if flip_option == "Flip Horizontally":
        image = ImageOps.mirror(image)
    elif flip_option == "Flip Vertically":
        image = ImageOps.flip(image)

    # --- Resize Image ---
    width, height = image.size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    resized_image = image.resize((new_width, new_height))

    # --- Display Image with Axes using Matplotlib ---
    fig, ax = plt.subplots()
    ax.imshow(resized_image)
    ax.set_title(f"Size: {scale_percent}% - {flip_option}", fontsize=12)
    ax.set_xlabel("X-axis (pixels)")
    ax.set_ylabel("Y-axis (pixels)")
    ax.grid(False)

    st.pyplot(fig)

    st.markdown('<p class="caption">Image source: Pexels | Sweet Briar Rose with X-Y axes 🌿</p>', unsafe_allow_html=True)

except requests.exceptions.RequestException as e:
    st.error("❌ Failed to load image from URL.")
    st.code(str(e), language="python")
