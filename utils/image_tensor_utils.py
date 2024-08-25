import torch
import numpy as np
from PIL import Image

def pil_to_tensor(image_pil):
    """
    Convert a PIL image to a PyTorch tensor.
    The tensor will have shape [C, H, W] where C is the number of channels.
    """
    # Convert PIL image to numpy array
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    
    # Handle grayscale images (2D array)
    if image_np.ndim == 2:
        image_np = np.expand_dims(image_np, axis=2)  # Add channel dimension [H, W] -> [H, W, 1]
    
    # Transpose array from [H, W, C] to [C, H, W]
    image_np = np.transpose(image_np, (2, 0, 1))
    
    # Convert numpy array to tensor
    image_tensor = torch.from_numpy(image_np)
    return image_tensor

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [C, H, W].
    """
    # Ensure the tensor has shape [C, H, W]
    if image_tensor.ndim == 4:
        image_tensor = image_tensor.squeeze(0)  # Remove the batch dimension

    # Convert tensor to numpy array and scale to [0, 255]
    image_np = image_tensor.mul(255).byte().cpu().numpy()

    # Handle grayscale images (single channel)
    if image_np.shape[0] == 1:
        image_np = image_np[0]  # Remove channel dimension [1, H, W] -> [H, W]
    else:
        image_np = np.transpose(image_np, (1, 2, 0))  # Convert [C, H, W] -> [H, W, C]

    # Ensure the numpy array is in uint8 format
    image_np = image_np.astype(np.uint8)

    # Convert numpy array back to PIL Image
    image_pil = Image.fromarray(image_np)
    return image_pil
