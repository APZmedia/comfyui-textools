import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [C, H, W] or [H, W, C].
    """

    # Debugging: Print the initial shape and dtype
    print(f"Initial tensor shape: {image_tensor.shape}, dtype: {image_tensor.dtype}")

    # Ensure the tensor is on the CPU and squeeze out any singleton dimensions
    image_np = image_tensor.cpu().numpy()

    # Convert to uint8 if necessary
    if image_np.dtype != np.uint8:
        image_np = (image_np * 255).astype(np.uint8)

    # Handle grayscale and RGB images
    if image_np.ndim == 2:  # Grayscale image
        return Image.fromarray(image_np, mode='L')
    elif image_np.ndim == 3:
        if image_np.shape[0] in [1, 3, 4]:  # [C, H, W] format
            image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]
        # At this point, image_np should be [H, W, C]
        if image_np.shape[2] == 1:  # Single channel, grayscale
            return Image.fromarray(image_np.squeeze(), mode='L')
        elif image_np.shape[2] == 3:  # RGB
            return Image.fromarray(image_np, mode='RGB')
        elif image_np.shape[2] == 4:  # RGBA
            return Image.fromarray(image_np, mode='RGBA')
    else:
        raise ValueError(f"Unsupported image shape for conversion to PIL: {image_np.shape}")

    raise ValueError(f"Failed to convert tensor with shape {image_tensor.shape} to PIL image")

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
