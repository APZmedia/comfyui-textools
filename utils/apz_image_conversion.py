# image_conversion.py
from PIL import Image
import torch
import numpy as np

def tensor_to_pil(image_tensor):
    image_np = image_tensor.cpu().numpy().squeeze(0)
    image_pil = Image.fromarray((image_np * 255).astype(np.uint8))
    return image_pil

def pil_to_tensor(image_pil):
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    image_tensor = torch.tensor(image_np).unsqueeze(0)
    return image_tensor
