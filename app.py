# Create app.py content

import io
import streamlit as st
from PIL import Image
from utils import load_image, apply_style_transfer, upscale_image

st.set_page_config(layout="wide")
st.title("🎨 Neural Style Transfer + Upscaling App")

st.sidebar.header("Upload Images")
content_file = st.sidebar.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_file = st.sidebar.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

if content_file and style_file:
    content_img = load_image(content_file)
    style_img = load_image(style_file)

    st.image(content_img, caption="Content Image", width=300)
    st.image(style_img, caption="Style Image", width=300)

    if st.button("Apply Style Transfer 🎨"):
        with st.spinner("Stylizing..."):
            stylized = apply_style_transfer(content_img, style_img)
            st.image(stylized, caption="Stylized Image", use_container_width =True)
            st.session_state.stylized_image = stylized

    if "stylized_image" in st.session_state:
        if st.button("Upscale Image 4× 🔍"):
            with st.spinner("Upscaling..."):
                upscaled = upscale_image(st.session_state.stylized_image, scale=4)
                st.image(upscaled, caption="Upscaled Image", use_container_width =True)
                st.session_state.upscaled_image = upscaled


            # Download button
        if "upscaled_image" in st.session_state:
            # Save to BytesIO buffer in PNG format
            img_buffer = io.BytesIO()
            st.session_state.upscaled_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Proper download button
            st.download_button(
                "Download Upscaled Image",
                data=img_buffer,
                file_name="upscaled_image.png",
                mime="image/png"
            )

