import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [C, H, W], [H, W, C], and [B, C, H, W].
    """
    # Ensure the tensor is on the CPU and convert to numpy array
    image_np = image_tensor.cpu().numpy()

    # Handle batch of images
    if image_np.ndim == 4:  # [B, C, H, W] or [B, H, W, C] format
        pil_images = []
        for img in image_np:
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images

    # Handle single image
    return _single_tensor_to_pil(image_np)


def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    """
    # Remove unnecessary dimensions
    if image_np.ndim == 4:
        image_np = np.squeeze(image_np)

    # Convert to uint8 if necessary
    if image_np.dtype != np.uint8:
        image_np = (image_np * 255).astype(np.uint8)

    # Ensure image has a shape [H, W, C] or [H, W] for grayscale
    if image_np.ndim == 3 and image_np.shape[0] in [1, 3, 4]:  # [C, H, W] format
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]
    
    # Handle different shapes
    if image_np.ndim == 2:  # Grayscale image
        return Image.fromarray(image_np, mode='L')
    elif image_np.ndim == 3:
        if image_np.shape[2] == 1:  # Single channel, grayscale
            return Image.fromarray(image_np.squeeze(), mode='L')
        elif image_np.shape[2] == 3:  # RGB
            return Image.fromarray(image_np, mode='RGB')
        elif image_np.shape[2] == 4:  # RGBA
            return Image.fromarray(image_np, mode='RGBA')
    else:
        raise ValueError(f"Unsupported image shape for conversion to PIL: {image_np.shape}")

    raise ValueError(f"Failed to convert tensor with shape {image_np.shape} to PIL image")


def pil_to_tensor(image_pil):
    """
    Convert a PIL image or a list of PIL images to a PyTorch tensor.
    If a list of images is provided, it returns a batch of tensors.
    """
    if isinstance(image_pil, list):
        tensors = [pil_to_single_tensor(img) for img in image_pil]
        return torch.stack(tensors)  # Stack tensors into a batch
    else:
        return pil_to_single_tensor(image_pil)


def pil_to_single_tensor(image_pil):
    """
    Helper function to convert a single PIL image to a PyTorch tensor.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    if image_np.ndim == 2:  # Grayscale image
        image_np = np.expand_dims(image_np, axis=2)
    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # Add batch dimension [1, C, H, W]
    return image_tensor
