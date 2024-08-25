import torch
import numpy as np
from PIL import Image

def pil_to_tensor(image_pil):
    """
    Convert a PIL image to a PyTorch tensor.
    The tensor will have shape [C, H, W] where C is the number of channels.
    """
    # Convert PIL image to numpy array
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    
    # Handle grayscale images (2D array)
    if image_np.ndim == 2:
        image_np = np.expand_dims(image_np, axis=2)  # Add channel dimension [H, W] -> [H, W, 1]
    
    # Transpose array from [H, W, C] to [C, H, W]
    image_np = np.transpose(image_np, (2, 0, 1))
    
    # Convert numpy array to tensor
    image_tensor = torch.from_numpy(image_np)
    return image_tensor

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, H, W, C] or [H, W, C].
    We'll first check the dimensions and reorder if necessary.
    """
    # Debugging: Print the initial shape of the tensor
    print(f"Tensor shape before conversion: {image_tensor.shape}")

    if len(image_tensor.shape) == 4:
        # Assuming the tensor is in [1, H, W, C] format, we need to reorder to [1, C, H, W]
        image_tensor = image_tensor.permute(0, 3, 1, 2).squeeze(0)  # Permute and remove batch dimension
    elif len(image_tensor.shape) == 3:
        # Assuming the tensor is in [H, W, C] format, we need to reorder to [C, H, W]
        image_tensor = image_tensor.permute(2, 0, 1)

    # Now image_tensor should be in [C, H, W] format
    # Check for grayscale images
    if image_tensor.shape[0] == 1:  # Grayscale image
        image_tensor = image_tensor.repeat(3, 1, 1)  # Convert to RGB by repeating channels

    # Convert to numpy array
    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()

    # Debugging: Print final shape before conversion to PIL
    print("Numpy array shape before converting to PIL:", image_np.shape)

    # Convert numpy array back to PIL Image
    image_pil = Image.fromarray((image_np * 255).astype(np.uint8))

    return image_pil
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, C, H, W] or [C, H, W].
    """
    # Debugging: Print the initial shape of the tensor
    print(f"Tensor shape before conversion: {image_tensor.shape}")

    if len(image_tensor.shape) == 4:
        image_tensor = image_tensor.squeeze(0)  # Remove batch dimension

    # Check for unexpected shapes
    if image_tensor.shape[0] == 1:  # Grayscale image
        image_tensor = image_tensor.repeat(3, 1, 1)  # Convert to RGB by repeating channels

    elif image_tensor.shape[0] != 3:  # If not RGB or Grayscale, handle it
        raise ValueError(f"Unexpected number of channels: {image_tensor.shape[0]}")

    # Ensure the tensor is [C, H, W], then convert to [H, W, C]
    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()

    # Debugging: Print the final shape of the numpy array before converting to PIL
    print("Numpy array shape before converting to PIL:", image_np.shape)

    # Convert numpy array back to PIL Image
    image_pil = Image.fromarray((image_np * 255).astype(np.uint8))

    return image_pil

    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, C, H, W] or [C, H, W].
    """
    # Debugging: Print the initial shape of the tensor
    print(f"Tensor shape before conversion: {image_tensor.shape}")

    if len(image_tensor.shape) == 4:
        image_tensor = image_tensor.squeeze(0)  # Remove batch dimension

    # Debugging: Check for grayscale images and other shapes
    if image_tensor.shape[0] == 1:  # Grayscale image
        image_tensor = image_tensor.repeat(3, 1, 1)  # Convert to RGB by repeating channels

    elif image_tensor.shape[0] == 3:  # RGB image
        pass  # No change needed

    else:
        print(f"Unexpected shape encountered: {image_tensor.shape}")
        # Attempt to reshape if the shape is incorrect
        if image_tensor.shape[1] == 1 and image_tensor.shape[0] > 1:
            image_tensor = image_tensor.squeeze(0)
        elif image_tensor.shape[0] == 1 and image_tensor.shape[1] == 1:
            # Handle the case (1, 1, H, W) or similar
            image_tensor = image_tensor.squeeze(0).squeeze(0)

    # Reorder dimensions from [C, H, W] to [H, W, C]
    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()

    # Scale the numpy array to [0, 255] and convert to uint8
    image_np = (image_np * 255).astype(np.uint8)

    # Debugging: Print final shape before conversion to PIL
    print("Numpy array shape before converting to PIL:", image_np.shape)

    # Convert numpy array back to PIL Image
    image_pil = Image.fromarray(image_np)
    return image_pil