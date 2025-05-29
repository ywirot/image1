import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Image Viewer", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #fdf6f0; color: #333; }
        h1 { color: #d14b8f; text-align: center; }
        .caption { font-size: 16px; text-align: center; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌼 Image Viewer with Thumbnails and Axes</h1>", unsafe_allow_html=True)

# --- Image URLs ---
image_urls = {
    "Rose": "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg",
    "Sunflower": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg",
    "Lavender": "https://images.pexels.com/photos/580899/pexels-photo-580899.jpeg"
}

# --- Display thumbnails in columns ---
st.markdown("### Select an image:")

cols = st.columns(3)
selected_image_name = None

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        try:
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content))
            st.image(img.resize((150, 100)), caption=name, use_container_width=False)
            if st.button(f"Select {name}"):
                selected_image_name = name
        except:
            st.warning(f"⚠️ Failed to load thumbnail for {name}")

# --- Default selection if not clicked ---
if selected_image_name is None:
    selected_image_name = list(image_urls.keys())[0]

# --- User Controls ---
scale_percent = st.slider("🔧 Resize Image (%)", 10, 200, 100, 10)
flip_option = st.radio("🔁 Flip Image", ("No Flip", "Flip Horizontally", "Flip Vertically"))

# --- Load Selected Image ---
try:
    selected_url = image_urls[selected_image_name]
    response = requests.get(selected_url, timeout=10)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Flip
    if flip_option == "Flip Horizontally":
        image = ImageOps.mirror(image)
    elif flip_option == "Flip Vertically":
        image = ImageOps.flip(image)

    # Resize
    width, height = image.size
    new_size = (int(width * scale_percent / 100), int(height * scale_percent / 100))
    resized_image = image.resize(new_size)

    # Display with matplotlib
    st.markdown(f"### Displaying: **{selected_image_name}**")
    fig, ax = plt.subplots()
    ax.imshow(resized_image)
    ax.set_title(f"{selected_image_name} | Size: {scale_percent}% | {flip_option}")
    ax.set_xlabel("X-axis (pixels)")
    ax.set_ylabel("Y-axis (pixels)")
    ax.grid(False)
    st.pyplot(fig)

    st.markdown(f'<p class="caption">Image: {selected_image_name} from Pexels</p>', unsafe_allow_html=True)

except Exception as e:
    st.error("❌ Failed to load selected image.")
    st.code(str(e), language="python")
