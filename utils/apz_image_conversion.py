import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [B, H, W, C].
    """
    image_np = image_tensor.cpu().numpy()

    # We expect the input tensor to be in [B, H, W, C] format
    if image_np.ndim == 4:  # Batch of images [B, H, W, C]
        pil_images = []
        for img in image_np:  # img has shape [H, W, C]
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images
    elif image_np.ndim == 3:  # Single image case [H, W, C]
        return [_single_tensor_to_pil(image_np)]
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    """
    image_np = np.squeeze(image_np)  # Remove unnecessary dimensions

    if image_np.ndim == 3 and image_np.shape[-1] == 3:  # [H, W, C] format for RGB
        mode = 'RGB'
    elif image_np.ndim == 3 and image_np.shape[-1] == 4:  # [H, W, C] format for RGBA
        mode = 'RGBA'
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape[-1]}")

    if image_np.dtype != np.uint8:
        image_np = (image_np * 255).astype(np.uint8)

    return Image.fromarray(image_np, mode=mode)

def pil_to_tensor(image_pil):
    """
    Convert a PIL image or a list of PIL images back to a PyTorch tensor.
    If a list of images is provided, it returns a batch of tensors with shape [B, C, H, W].
    """
    if isinstance(image_pil, list):
        tensors = [pil_to_single_tensor(img) for img in image_pil]
        return torch.cat(tensors, dim=0)  # Concatenate along batch dimension
    else:
        return pil_to_single_tensor(image_pil)

def pil_to_single_tensor(image_pil):
    """
    Helper function to convert a single PIL image to a PyTorch tensor.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    if image_np.ndim == 2:  # Grayscale image
        image_np = np.expand_dims(image_np, axis=2)  # Expand dimensions to [H, W, 1]
    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # Add batch dimension [1, C, H, W]
    return image_tensor
