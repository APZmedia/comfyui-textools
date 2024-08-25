import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a list of PIL images.
    Handles tensors of shape [B, H, W, C] (batch of images).
    """
    image_np = image_tensor.cpu().numpy()
    print(f"Input Tensor Shape: {image_tensor.shape}")

    # Handle the expected 4D tensor [B, H, W, C] format
    if image_np.ndim == 4:  # [B, H, W, C] format
        pil_images = []
        for img in image_np:
            pil_images.append(_single_tensor_to_pil(img))
        return pil_images
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    Handles tensors of shape [H, W, C].
    """
    # Ensure image_np is in the format [H, W, C] and check if it is in float32
    if image_np.ndim == 3 and image_np.shape[-1] in [1, 3, 4]:
        print(f"Converted image shape for PIL: {image_np.shape}")
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

    # Convert to uint8 if necessary
    if image_np.dtype != np.uint8:
        print("Converting to uint8 format.")
        image_np = (image_np * 255).astype(np.uint8)

    # Determine the mode based on the number of channels
    if image_np.shape[-1] == 1:  # Grayscale
        image_np = image_np.squeeze(-1)
        mode = 'L'
    elif image_np.shape[-1] == 3:  # RGB
        mode = 'RGB'
    elif image_np.shape[-1] == 4:  # RGBA
        mode = 'RGBA'
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape[-1]}")

    return Image.fromarray(image_np, mode=mode)

def pil_to_tensor(image_pil):
    """
    Convert a list of PIL images back to a PyTorch tensor with shape [B, C, H, W].
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
    image_tensor = torch.from_numpy(image_np)  # Return tensor with shape [C, H, W]

    # Check the data type after converting to tensor
    if image_tensor.dtype == torch.uint8:
        print("After NumPy to Tensor: Data is in uint8 format.")
    elif image_tensor.dtype == torch.float32:
        print("After NumPy to Tensor: Data is in float32 format.")
    else:
        print(f"After NumPy to Tensor: Data is in a different format: {image_tensor.dtype}")

    return image_tensor.unsqueeze(0)  # Add batch dimension [1, C, H, W]
