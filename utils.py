# Create utils.py content
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
from RealESRGAN import RealESRGAN
import io
import torch

# Load TF-Hub Style Transfer model
style_model = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = RealESRGAN(device, scale=4)
# model.load_weights('weights/RealESRGAN_x4.pth', download=True)

def load_image(image_file):
    img = Image.open(image_file)
    img = img.convert("RGB")
    return img

def apply_style_transfer(content_img, style_img):
    content_tensor = tf.convert_to_tensor(np.array(content_img).astype(np.float32))[tf.newaxis, ...] / 255.0
    style_tensor = tf.convert_to_tensor(np.array(style_img).astype(np.float32))[tf.newaxis, ...] / 255.0
    outputs = style_model(content_tensor, style_tensor)
    stylized = outputs[0][0].numpy()
    stylized = (stylized * 255).astype(np.uint8)
    return Image.fromarray(stylized)

def upscale_image(image: Image.Image, scale: int = 4) -> Image.Image:
    try:
        model = RealESRGAN(device, scale=scale)
        model.load_weights(f'weights/realesrgan-x{scale}',download=True)
        if image.mode != "RGB":
            image = image.convert("RGB")
        upscaled = model.predict(image)
        return upscaled
    except Exception as e:
        print(f"[Upscale Error] {e}")
        return image