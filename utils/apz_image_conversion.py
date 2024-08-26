import torch
import numpy as np
from PIL import Image

import torch
import numpy as np
from PIL import Image
from PIL import Image
import torch

def tensor_to_pil(image_tensor):
    """
    Converts a PyTorch tensor with shape [B, H, W, C] to a list of PIL images.
    """
    # Log the initial shape and dtype of the input tensor
    print(f"Initial tensor shape: {image_tensor.shape}, dtype: {image_tensor.dtype}")
    
    # Ensure the tensor is in the correct format
    if image_tensor.dtype != torch.uint8:
        print("Converting tensor to uint8 format and scaling pixel values to [0, 255].")
        image_tensor = (image_tensor * 255).type(torch.uint8)  # Convert to uint8 if needed
    else:
        print("Tensor is already in uint8 format.")

    # Iterate over the batch dimension and convert each image
    pil_images = []
    for i in range(image_tensor.size(0)):
        print(f"Processing image {i+1}/{image_tensor.size(0)}...")
        
        # Extract the individual image from the batch and convert to [H, W, C]
        img_np = image_tensor[i].cpu().numpy()  # Convert to NumPy array
        print(f"Converted tensor to NumPy array with shape: {img_np.shape}")

        pil_image = Image.fromarray(img_np)
        print(f"Converted NumPy array to PIL image with mode: {pil_image.mode}, size: {pil_image.size}")
        
        pil_images.append(pil_image)
    
    print(f"Total {len(pil_images)} images converted to PIL format.")
    
    return pil_images


def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    Handles tensors of shape [C, H, W] or [H, W, C].
    """
    print(f"Original image shape: {image_np.shape}")  # Debugging

    # Convert float images in [0, 1] range to uint8 images in [0, 255] range
    if image_np.dtype in [np.float32, np.float64]:
        print("Converting to uint8 format.")  # Debugging
        image_np = (image_np * 255).astype(np.uint8)

    # Handle different channel configurations
    if image_np.ndim == 3 and image_np.shape[0] in [1, 3, 4]:  # [C, H, W] format
        print("Transposing from [C, H, W] to [H, W, C].")  # Debugging
        image_np = np.moveaxis(image_np, 0, -1)  # Convert to [H, W, C]

    # Determine the correct mode for PIL image
    if image_np.ndim == 3 and image_np.shape[-1] == 1:  # Grayscale
        mode = 'L'
        image_np = image_np.squeeze(-1)  # Remove the channel dimension for grayscale
    elif image_np.ndim == 3 and image_np.shape[-1] == 3:  # RGB
        mode = 'RGB'
    elif image_np.ndim == 3 and image_np.shape[-1] == 4:  # RGBA
        mode = 'RGBA'
    else:
        raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

    print(f"Before PIL Conversion: Data is in {image_np.dtype} format, mode: {mode}.")  # Debugging
    return Image.fromarray(image_np, mode=mode)

def pil_to_tensor(image_pil, original_dtype=None):
    """
    Convert a list of PIL images back to a PyTorch tensor with shape [B, C, H, W].
    Ensures the tensor has the same dtype as the original if provided.
    """
    if isinstance(image_pil, list):
        tensors = [pil_to_single_tensor(img, original_dtype) for img in image_pil]
        return torch.cat(tensors)  # Concatenate tensors along the batch dimension
    else:
        return pil_to_single_tensor(image_pil, original_dtype)

def pil_to_single_tensor(image_pil, original_dtype=None):
    """
    Convert a single PIL image to a torch tensor.
    The resulting tensor will have the shape (3, H, W) for RGB images and will be cast back to original dtype if provided.
    """
    image_pil = image_pil.convert("RGB")  # Ensure the image is in RGB mode
    image_array = np.array(image_pil)  # Convert to numpy array
    tensor = torch.from_numpy(image_array).permute(2, 0, 1).float() / 255.0  # Convert to tensor and normalize
    tensor = tensor.unsqueeze(0)  # Add a batch dimension

    # Convert back to original dtype if necessary
    if original_dtype is not None:
        if original_dtype == torch.uint8:
            tensor = (tensor * 255).to(original_dtype)
        else:
            tensor = tensor.to(original_dtype)

    return tensor
