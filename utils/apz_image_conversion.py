import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [B, C, H, W].
    """
    # Ensure the tensor is on the CPU and convert to numpy array
    image_np = image_tensor.cpu().numpy()

    # Handle batch of images
    if image_np.ndim == 4:  # [B, C, H, W] format
        pil_images = []
        for img in image_np:
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    """
    # Check if the image is in [C, H, W] format
    if image_np.shape[0] == 3:  # Assume [C, H, W] format for RGB
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

    # Convert the numpy array to a PIL Image
    return Image.fromarray((image_np * 255).astype(np.uint8), mode='RGB')

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
