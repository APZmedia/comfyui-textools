from PIL import Image

def open_image(image_path):
    """
    Opens an image file and returns it as a PIL Image.
    """
    return Image.open(image_path)

def save_image(image, path):
    """
    Saves a PIL image to the specified path.
    """
    image.save(path, format="PNG")
