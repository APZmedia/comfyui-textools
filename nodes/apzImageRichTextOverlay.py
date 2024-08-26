# main_class.py

import
from PIL import ImageDraw
from ..utils.apz_text_box_utility import TextBoxUtility
from ..utils.apz_color_utility import ColorUtility
from ..utils.apz_font_loader_utility import FontLoaderUtility
from ..utils.apz_text_renderer_utility import TextRendererUtility
from ..utils.apz_image_conversion import tensor_to_pil, pil_to_single_tensor
from ..utils.apz_font_manager import FontManager

class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu"):
        print("APZmediaImageRichTextOverlay initialized")
        self.device = device

    _alignments = ["left", "right", "center"]
    _vertical_alignments = ["top", "middle", "bottom"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "theText": ("STRING", {"multiline": True, "default": "Hello <b>World</b> <i>This is italic</i>"}),
                "theTextbox_width": ("INT", {"default": 200, "min": 1}),
                "theTextbox_height": ("INT", {"default": 200, "min": 1}),
                "max_font_size": ("INT", {"default": 30, "min": 1, "max": 256, "step": 1}),
                "font": ("STRING", {"default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}),
                "italic_font": ("STRING", {"default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"}),
                "bold_font": ("STRING", {"default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}),
                "alignment": (cls._alignments, {"default": "center"}),
                "vertical_alignment": (cls._vertical_alignments, {"default": "middle"}),
                "font_color": ("STRING", {"default": "#000000"}),
                "italic_font_color": ("STRING", {"default": "#000000"}),
                "bold_font_color": ("STRING", {"default": "#000000"}),
                "box_start_x": ("INT", {"default": 0}),
                "box_start_y": ("INT", {"default": 0}),
                "padding": ("INT", {"default": 50}),
                "line_height_ratio": ("FLOAT", {"default": 1.2, "min": 1.0}),  # Ratio for line height relative to font size
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apz_add_text_overlay"
    CATEGORY = "image/text"

    def apz_add_text_overlay(self, image, theText, theTextbox_width, theTextbox_height, max_font_size, font, italic_font, bold_font, alignment, vertical_alignment, font_color, italic_font_color, bold_font_color, box_start_x, box_start_y, padding, line_height_ratio):
        original_shape = image.shape
        original_dtype = image.dtype

        pil_images = tensor_to_pil(image)
        print(f"Input Tensor Shape: {image.shape}")

        color_utility = ColorUtility()
        font_color_rgb = color_utility.hex_to_rgb(font_color)
        italic_font_color_rgb = color_utility.hex_to_rgb(italic_font_color)
        bold_font_color_rgb = color_utility.hex_to_rgb(bold_font_color)

        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        font_loader = FontLoaderUtility(font_manager, max_font_size)

        processed_images = []
        for idx, image_pil in enumerate(pil_images):
            print(f"Processing Image {idx + 1}/{len(pil_images)}")

            effective_textbox_width = theTextbox_width - 2 * padding
            effective_textbox_height = theTextbox_height - 2 * padding

            font_size, wrapped_lines, total_text_height = font_loader.find_fitting_font_size(theText, effective_textbox_width, effective_textbox_height, line_height_ratio)

            if font_size:
                draw = ImageDraw.Draw(image_pil)
                TextRendererUtility.render_text(
                    draw, wrapped_lines, box_start_x, box_start_y, padding,
                    effective_textbox_width, effective_textbox_height, font_manager,
                    color_utility, alignment, vertical_alignment, line_height_ratio,
                    font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
                )

            processed_image = pil_to_tensor(image_pil, original_dtype)
            print(f"Processed PIL image to tensor shape: {processed_image.shape}")
            processed_images.append(processed_image)

        final_tensor = torch.cat(processed_images, dim=0)  # Concatenate along the batch dimension
        print(f"Final output tensor shape: {final_tensor.shape}")

        return final_tensor,