import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [B, C, H, W] or [B, H, W, C].
    """
    image_np = image_tensor.cpu().numpy()

    if image_np.ndim == 4:  # [B, C, H, W] or [B, H, W, C] format
        pil_images = []
        for img in image_np:
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images
    elif image_np.ndim == 3:  # Single image case [C, H, W] or [H, W, C]
        return _single_tensor_to_pil(image_np)
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    """
    # Handle [C, H, W] format
    if image_np.ndim == 3 and image_np.shape[0] == 3:  # [C, H, W] for RGB
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]

    # Handle already correct [H, W, C] format
    if image_np.ndim == 3 and image_np.shape[-1] == 3:  # [H, W, C] for RGB
        # Convert the numpy array to a PIL Image
        return Image.fromarray((image_np * 255).astype(np.uint8), mode='RGB')
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")
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
