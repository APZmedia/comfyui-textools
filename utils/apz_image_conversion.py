import torch
import numpy as np
from PIL import Image

def tensor_to_pil(image_tensor):
    """
    Converts a PyTorch tensor with shape [B, H, W, C] or [B, C, H, W] to a list of PIL images.
    Assumes the tensor contains pixel values in the range [0, 1] for floating-point types
    and [0, 255] for uint8 types.
    """
    # Ensure the tensor is on the CPU and in the correct format
    if image_tensor.is_floating_point():
        image_tensor = (image_tensor * 255).type(torch.uint8)

    image_tensor = image_tensor.cpu()  # Ensure the tensor is on the CPU
    
    # Convert the tensor to [B, H, W, C] format if it's in [B, C, H, W]
    if image_tensor.shape[1] == 3 or image_tensor.shape[1] == 4:
        image_tensor = image_tensor.permute(0, 2, 3, 1)

    pil_images = []
    for img in image_tensor:
        img_np = img.numpy()  # Convert to NumPy array
        print(f"Shape of img_np: {img_np.shape}")  # Print the shape of the NumPy array to the console
        img_np = img_np.astype(np.uint8)  # Convert to uint8 if necessary
        pil_image = Image.fromarray(img_np,'RGB')  # Convert to PIL Image
        pil_images.append(pil_image)

    return pil_images

def pil_to_tensor(image_pil):
    """
    Converts a list of PIL images to a PyTorch tensor with shape [B, C, H, W].
    The resulting tensor will contain pixel values in the range [0, 1].
    """
    if not isinstance(image_pil, list):
        image_pil = [image_pil]

    tensors = []
    for img in image_pil:
        img_np = np.array(img)  # Convert PIL image to NumPy array
        img_np = np.expand_dims(img_np, axis=0)
        print(f"Shape of img_np in pil to tensor: {img_np.shape}")  # Print the shape of the NumPy array to the console
        tensor = torch.from_numpy(img_np).float() / 255.0  # Convert to tensor and normalize to [0, 1]
        tensors.append(tensor)

    return torch.stack(tensors)  # Stack the list into a batch tensor with shape [B, C, H, W]
