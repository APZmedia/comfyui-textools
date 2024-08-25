import torch
import numpy as np
from PIL import Image

def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def convert_to_tensor(image_pil):
    image_tensor_out = torch.tensor(np.array(image_pil).astype(np.float32) / 255.0)
    return torch.unsqueeze(image_tensor_out, 0)
