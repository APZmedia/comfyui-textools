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
    print(f"Converted image shape for PIL: {image_np.shape}")
    
    # Ensure data is in [H, W, C] and float32
    if image_np.ndim == 3 and image_np.shape[-1] in [1, 3, 4]:
        pass  # Valid shape
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
        return torch.cat(tensors)  # Concatenate tensors along the batch dimension
    else:
        return pil_to_single_tensor(image_pil)

def pil_to_single_tensor(image_pil):
    """
    Helper function to convert a single PIL image to a PyTorch tensor.
    """
    # Convert PIL image to NumPy array
    image_np = np.array(image_pil)
    print('Original Data Type:', image_np.dtype)

    # Convert image data to float32 if it's not already in the correct format
    if image_np.dtype == np.float32 or image_np.dtype == np.float64:
        print("Converting float data to uint8.")
        image_np = (image_np * 255).astype(np.uint8)
    elif image_np.dtype == np.uint8:
        print("Data is already in uint8 format.")
    else:
        print(f"Unexpected data type: {image_np.dtype}, converting to float32.")
        image_np = image_np.astype(np.float32)

    # Ensure grayscale images have a channel dimension
    if image_np.ndim == 2:  # Grayscale image [H, W]
        image_np = np.expand_dims(image_np, axis=2)  # Expand dimensions to [H, W, 1]

    # Convert [H, W, C] to [C, H, W] format
    image_np = np.transpose(image_np, (2, 0, 1))
    print(f"Shape after transpose (C, H, W): {image_np.shape}")

    # Convert NumPy array to PyTorch tensor
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # Add batch dimension [1, C, H, W]
    print(f"Converted PIL image to tensor shape: {image_tensor.shape}")

    return image_tensor
    