import torch
import numpy as np
from PIL import Image

def pil_to_tensor(image_pil):
    """
    Convert a PIL image to a PyTorch tensor.
    The tensor will have shape [C, H, W] where C is the number of channels.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0
    if image_np.ndim == 2:  # Grayscale image
        image_np = np.expand_dims(image_np, axis=2)
    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)
    return image_tensor

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor to a PIL image.
    The tensor is expected to have shape [1, C, H, W] or [C, H, W].
    """

    # Handle the batch dimension if present
    if len(image_tensor.shape) == 4:
        image_tensor = image_tensor.squeeze(0)  # Remove batch dimension

    # Convert grayscale to RGB by repeating the channel if necessary
    if image_tensor.shape[0] == 1:
        image_tensor = image_tensor.repeat(3, 1, 1)

    # Reorder dimensions from [C, H, W] to [H, W, C]
    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()

    # Scale the numpy array to [0, 255] and convert to uint8
    image_np = (image_np * 255).astype(np.uint8)

    # Convert numpy array back to PIL Image
    image_pil = Image.fromarray(image_np)
    return image_pil