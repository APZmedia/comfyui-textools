import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, C, H, W] or [C, H, W].
    """
    if image_tensor.ndim == 4:
        image_tensor = image_tensor.squeeze(0)  # Remove the batch dimension if present

    # Ensure the tensor is in CPU and convert to numpy array
    image_np = image_tensor.cpu().numpy()

    # Handle grayscale images (C=1)
    if image_np.shape[0] == 1:
        image_np = image_np.squeeze(0)  # Remove the channel dimension for grayscale

    # Convert to uint8 if necessary
    if image_np.dtype != np.uint8:
        image_np = (image_np * 255).astype(np.uint8)

    # Ensure the correct shape order for PIL [H, W, C]
    if image_np.ndim == 2:  # Grayscale image
        return Image.fromarray(image_np, mode='L')
    elif image_np.shape[2] == 3:  # RGB image
        return Image.fromarray(image_np, mode='RGB')
    elif image_np.shape[2] == 4:  # RGBA image
        return Image.fromarray(image_np, mode='RGBA')
    else:
        raise ValueError(f"Unsupported image shape: {image_np.shape}")

def pil_to_tensor(image_pil):
    """
    Convert a PIL image to a PyTorch tensor.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    if image_np.ndim == 2:  # Grayscale image
        image_np = np.expand_dims(image_np, axis=2)
    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # Add batch dimension [1, C, H, W]
    return image_tensor
    