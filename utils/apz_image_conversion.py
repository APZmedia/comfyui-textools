import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Convert a PyTorch tensor with shape [B, H, W, C] to a list of PIL images.
    """
    # Ensure the tensor is on the CPU and convert to numpy array
    image_np = image_tensor.cpu().numpy()

    print(f"Input Tensor Shape: {image_tensor.shape}  # This should show the input shape, e.g., [10, 512, 512, 3]")

    # The input is expected to always be a 4D tensor [B, H, W, C]
    if image_np.ndim == 4:  # [B, H, W, C] batch of images
        pil_images = []
        for img in image_np:  # img has shape [H, W, C]
            pil_images.append(_single_tensor_to_pil(img))
        print(f"Converted {len(pil_images)} images to PIL format.  # This should confirm the number of images processed")
        return pil_images
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def _single_tensor_to_pil(image_np):
    """
    Helper function to convert a single image tensor (numpy array) to a PIL image.
    Handles tensors of shape [H, W, C].
    """
    # Ensure the image data is in the format [H, W, C]
    if image_np.ndim == 3 and image_np.shape[-1] in [1, 3, 4]:  # [H, W, C] format
        # Convert grayscale to RGB by repeating the single channel if needed
        if image_np.shape[-1] == 1:
            image_np = np.repeat(image_np, 3, axis=-1)  # This should convert grayscale to RGB if needed

        # Convert to uint8 if necessary
        if image_np.dtype != np.uint8:
            image_np = (image_np * 255).astype(np.uint8)  # This should scale values to [0, 255] and convert to uint8

        # Determine the mode based on the number of channels
        if image_np.shape[-1] == 3:  # RGB
            mode = 'RGB'
        elif image_np.shape[-1] == 4:  # RGBA
            mode = 'RGBA'
        else:
            raise ValueError(f"Unsupported channel configuration: {image_np.shape}")

        print(f"Converted image shape for PIL: {image_np.shape}  # This should show the shape [H, W, C] for PIL conversion")
        return Image.fromarray(image_np, mode=mode)
    else:
        raise ValueError(f"Unsupported image shape for conversion: {image_np.shape}")

def pil_to_tensor(image_pil):
    """
    Convert a list of PIL images back to a PyTorch tensor with shape [B, C, H, W].
    """
    if isinstance(image_pil, list):
        tensors = [pil_to_single_tensor(img) for img in image_pil]
        tensor_stack = torch.stack(tensors)  # Stack tensors into a batch
        print(f"Stacked tensor shape: {tensor_stack.shape}  # This should show the shape [B, C, H, W] after stacking")
        return tensor_stack
    else:
        return pil_to_single_tensor(image_pil)

def pil_to_single_tensor(image_pil):
    """
    Helper function to convert a single PIL image to a PyTorch tensor.
    """
    image_np = np.array(image_pil).astype(np.float32) / 255.0

    if image_np.ndim == 2:  # Grayscale image, expand dims to [H, W, 1]
        image_np = np.expand_dims(image_np, axis=-1)  # This should add channel dimension for grayscale images

    image_np = np.transpose(image_np, (2, 0, 1))  # Convert [H, W, C] to [C, H, W]
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # Add batch dimension [1, C, H, W]
    print(f"Converted PIL image to tensor shape: {image_tensor.shape}  # This should show the shape [1, C, H, W] for the tensor")
    return image_tensor
