import torch
import numpy as np
from PIL import Image

def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.
    """
    return tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def convert_to_tensor(image_pil):
    """
    Converts a PIL image to a torch tensor. 
    Ensures the tensor is in the shape [C, H, W] for RGB or [1, H, W] for grayscale.
    """
    # Convert the PIL image to a numpy array and normalize the pixel values to [0, 1]
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    
    if len(image_np.shape) == 3:  # RGB Image [H, W, C]
        # Transpose the image to [C, H, W]
        image_tensor_out = torch.tensor(image_np.transpose(2, 0, 1))
    elif len(image_np.shape) == 2:  # Grayscale Image [H, W]
        # Add a channel dimension for grayscale images
        image_tensor_out = torch.tensor(image_np).unsqueeze(0)
    else:
        raise ValueError(f"Unsupported image shape: {image_np.shape}")

    return image_tensor_out
