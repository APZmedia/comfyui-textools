import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor with shape [B, C, H, W] or [B, H, W, C] to a list of PIL images.
    """
    image_np = image_tensor.cpu().numpy()
    print(f"Input Tensor Shape: {image_tensor.shape}")  # Debugging: Show the shape of the input tensor

    if image_np.ndim == 4:  # Handle batch of images
        pil_images = []
        for img in image_np:
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    Handles tensors of shape [C, H, W] or [H, W, C].
    """
    print(f"Original image shape: {image_np.shape}")  # Debugging

    # Convert float images in [0, 1] range to uint8 images in [0, 255] range
    if image_np.dtype == np.float32 or image_np.dtype == np.float64:
        print("Converting to uint8 format.")  # Debugging
        image_np = (image_np * 255).astype(np.uint8)

    if image_np.ndim == 3 and image_np.shape[0] in [1, 3, 4]:  # [C, H, W] format
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]

    if image_np.ndim == 3 and image_np.shape[-1] in [1, 3, 4]:  # [H, W, C] format
        mode = 'L' if image_np.shape[-1] == 1 else 'RGB' if image_np.shape[-1] == 3 else 'RGBA'
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

    print(f"Before PIL Conversion: Data is in {image_np.dtype} format.")  # Debugging
    return Image.fromarray(image_np, mode=mode)

def pil_to_tensor(image_pil):
    """
    Convert a list of PIL images back to a PyTorch tensor with shape [B, C, H, W].
    """
    if isinstance(image_pil, list):
        tensors = [pil_to_single_tensor(img) for img in image_pil]
        return torch.cat(tensors)  # Concatenate tensors along the batch dimension
    else:
        return pil_to_single_tensor(image_pil)

def pil_to_single_tensor(image_pil):
    """
    Convert a single PIL image to a torch tensor.
    The resulting tensor will have the shape (3, H, W) for RGB images.
    """
    image_pil = image_pil.convert("RGB")  # Ensure the image is in RGB mode
    image_array = np.array(image_pil)  # Convert to numpy array
    tensor = torch.from_numpy(image_array).permute(2, 0, 1).float() / 255.0  # Convert to tensor and normalize
    return tensor.unsqueeze(0)  # Add a batch dimension
    