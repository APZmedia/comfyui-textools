from PIL import Image, ImageDraw, ImageFont
import torch
import numpy as np

def load_font(font_path, font_size):
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        try:
            return ImageFont.truetype(default_font, font_size)
        except IOError:
            raise RuntimeError("Cannot load default font. Ensure the font path is correct.")

def convert_tensor_to_pil(image_tensor):
    image_np = image_tensor.cpu().numpy()

    if image_np.ndim == 4:  # Batch of images
        image_np = image_np[0]  # Take the first image in the batch
    if image_np.ndim == 3:  # Single image
        if image_np.shape[0] == 1:  # Grayscale
            image_np = image_np.squeeze(0)
            return Image.fromarray((image_np * 255).astype(np.uint8), mode='L')
        else:  # RGB
            image_np = np.transpose(image_np, (1, 2, 0))
            return Image.fromarray((image_np * 255).astype(np.uint8), mode='RGB')
    elif image_np.ndim == 2:  # Grayscale without channel
        return Image.fromarray((image_np * 255).astype(np.uint8), mode='L')

def convert_pil_to_tensor(image_pil):
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    image_tensor_out = torch.tensor(image_np)

    if image_tensor_out.ndim == 2:  # Grayscale
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)  # Add channel dimension
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)  # Add batch dimension
    elif image_tensor_out.ndim == 3:  # RGB
        image_tensor_out = torch.permute(image_tensor_out, (2, 0, 1))  # Convert to (channels, height, width)
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)  # Add batch dimension

    return image_tensor_out
