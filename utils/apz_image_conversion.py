import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [B, C, H, W] or [C, H, W].
    Returns a single PIL image if input is a single image, or a list of PIL images if input is a batch.
    """
    # Ensure the tensor is on the CPU and convert to numpy array
    image_np = image_tensor.cpu().numpy()

    # If the input is a single image, add a batch dimension (to unify handling)
    if image_np.ndim == 3:  # [C, H, W]
        image_np = np.expand_dims(image_np, 0)  # Convert to [1, C, H, W]

    # Handle batch of images
    pil_images = []
    for img in image_np:  # img has shape [C, H, W]
        pil_images.append(_single_tensor_to_pil(img))

    # If only one image, return the image itself instead of a list
    if len(pil_images) == 1:
        return pil_images[0]
    else:
        return pil_images

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    Handles tensors of shape [C, H, W] or [H, W, C].
    """
    # If the image is in [C, H, W] format (channel-first), move channels to the last dimension
    if image_np.shape[0] in [1, 3, 4]:  # [C, H, W] format
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]

    # Determine the mode based on the number of channels
    if image_np.shape[-1] == 1:  # Grayscale
        image_np = image_np.squeeze(-1)
        mode = 'L'
    elif image_np.shape[-1] == 3:  # RGB
        mode = 'RGB'
    elif image_np.shape[-1] == 4:  # RGBA
        mode = 'RGBA'
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

    # Convert to uint8 if necessary
    if image_np.dtype != np.uint8:
        image_np = (image_np * 255).astype(np.uint8)

    return Image.fromarray(image_np, mode=mode)

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
        image_np = np.expand_dims(image_np, axis=2)  # Expand dimensions to [H, W, 1]
    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np)  # No need to unsqueeze if handling single images
    return image_tensor
