# apz_image_conversion.py

from PIL import Image
import torch
import numpy as np

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, C, H, W] or [C, H, W].
    """
    if image_tensor.ndim == 4 and image_tensor.shape[0] == 1:
        image_tensor = image_tensor.squeeze(0)  # Remove the batch dimension if it exists and is 1

    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()  # Convert [C, H, W] to [H, W, C]
    
    # Convert to uint8 format (0-255) if not already
    image_np = (image_np * 255).astype(np.uint8)

    return Image.fromarray(image_np)

def pil_to_tensor(image_pil):
    """
    Convert a PIL image to a PyTorch tensor.
    The tensor will have shape [C, H, W] where C is the number of channels.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    if image_np.ndim == 2:  # Grayscale image
        image_np = np.expand_dims(image_np, axis=2)
    image_tensor = torch.from_numpy(image_np).permute(2, 0, 1)  # Convert [H, W, C] to [C, H, W]
    return image_tensor.unsqueeze(0)  # Add a batch dimension
