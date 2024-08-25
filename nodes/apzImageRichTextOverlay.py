from PIL import Image
from ..utils.image_utils import open_image, save_image
from ..utils.text_overlay import add_text_overlay
from ..utils.font_manager import FontManager
from ..utils.color_translator import hex_to_rgb

class APZmediaImageRichTextOverlay:
    def __init__(self, font_path, font_size=30, bold_font_path=None, italic_font_path=None, device="cpu"):
        print("APZmediaImageRichTextOverlay initialized")
        self.device = device
        self.font_manager = FontManager(font_path, font_size, bold_font_path, italic_font_path)

    def add_overlay(self, image_path, text, output_path, font_color="#000000", position=(0, 0), alignment="center", max_width=None):
        # Open the image using the PIL approach
        image = open_image(image_path)

        # Convert the font color from hex to RGB
        font_color_rgb = hex_to_rgb(font_color)

        # Add the text overlay with wrapping logic to the image
        image = add_text_overlay(image, text, self.font_manager, position, font_color_rgb, alignment, max_width)

        # Save the modified image
        save_image(image, output_path)
