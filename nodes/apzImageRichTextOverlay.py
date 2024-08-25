from PIL import Image, ImageDraw
import torch
import numpy as np

from ..utils.apz_font_manager import FontManager
from ..utils.apz_rich_text_parser import RichTextParser
from ..utils.apz_text_wrapper import TextWrapper
from ..utils.apz_colors_translator import hex_to_rgb
from ..utils.image_tensor_utils import pil_to_tensor, tensor_to_pil  # Import the conversion functions

class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu"):
        print("APZmediaImageRichTextOverlay initialized")
        self.device = device
        self.text_parser = RichTextParser()

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
        # Convert the input tensor to a PIL image
        image_pil = tensor_to_pil(image)

        # Debugging: Print the shape of the image after converting to PIL
        print(f"PIL image size: {image_pil.size}, mode: {image_pil.mode}")

        # Convert hex colors to RGB tuples
        font_color_rgb = hex_to_rgb(font_color)
        italic_font_color_rgb = hex_to_rgb(italic_font_color)
        bold_font_color_rgb = hex_to_rgb(bold_font_color)

        # Calculate effective textbox dimensions
        effective_textbox_width = theTextbox_width - 2 * padding
        effective_textbox_height = theTextbox_height - 2 * padding

        # Initialize FontManager and TextWrapper
        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        text_wrapper = TextWrapper(font_manager)

        # Adjust font size and wrap text until it fits within the textbox
        for font_size in range(max_font_size, 0, -1):
            line_height = int(font_size * line_height_ratio)
            parsed_text = self.text_parser.parse(theText)
            wrapped_lines, total_text_height = text_wrapper.wrap_text(parsed_text, effective_textbox_width, line_height, font_size)

            if total_text_height <= effective_textbox_height:
                self._draw_text(
                    image_pil, wrapped_lines, alignment, vertical_alignment, font_manager, font_size, line_height,
                    font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, box_start_x, box_start_y, padding,
                    effective_textbox_width, effective_textbox_height
                )
                break

        # Convert the modified PIL image back to a tensor
        image_tensor_out = pil_to_tensor(image_pil)

        # Debugging: Print the shape of the final image tensor
        print("Final image tensor shape:", image_tensor_out.shape)

        return image_tensor_out

    def _draw_text(self, image_pil, wrapped_lines, alignment, vertical_alignment, font_manager, font_size, line_height, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, box_start_x, box_start_y, padding, effective_textbox_width, effective_textbox_height):
        draw = ImageDraw.Draw(image_pil)
        y = self._calculate_initial_y(vertical_alignment, box_start_y, padding, effective_textbox_height, len(wrapped_lines) * line_height)

        for line in wrapped_lines:
            x = self._calculate_initial_x(alignment, box_start_x, padding, effective_textbox_width, line, font_manager, font_size)
            for chunk, chunk_styles in line:
                current_font = font_manager.get_font_for_style(chunk_styles, font_size)
                current_font_color_rgb = self._get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
                draw.text((x, y), chunk, fill=current_font_color_rgb, font=current_font)
                chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                if chunk_styles.get('u', False):
                    self._draw_underline(draw, x, y, chunk, current_font, current_font_color_rgb)
                if chunk_styles.get('s', False):
                    self._draw_strikeout(draw, x, y, chunk, current_font, current_font_color_rgb)

                x += chunk_width
            y += line_height

    def _calculate_initial_y(self, vertical_alignment, box_start_y, padding, effective_textbox_height, total_text_height):
        if vertical_alignment == "top":
            return box_start_y + padding
        elif vertical_alignment == "bottom":
            return box_start_y + effective_textbox_height - total_text_height - padding
        else:  # "middle"
            return box_start_y + padding + (effective_textbox_height - total_text_height) // 2

    def _calculate_initial_x(self, alignment, box_start_x, padding, effective_textbox_width, line, font_manager, font_size):
        font = font_manager.load_font(font_manager.font, font_size)
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        if alignment == "left":
            return box_start_x + padding
        elif alignment == "right":
            return box_start_x + effective_textbox_width - line_width + padding
        else:  # "center"
            return box_start_x + padding + (effective_textbox_width - line_width) // 2

    def _get_font_color(self, chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if chunk_styles.get('b', False):
            return bold_font_color_rgb
        elif chunk_styles.get('i', False):
            return italic_font_color_rgb
        else:
            return font_color_rgb

    def _draw_underline(self, draw, x, y, chunk, font, color):
        underline_y = y + font.getsize(chunk)[1]
        draw.line((x, underline_y, x + font.getbbox(chunk)[2] - font.getbbox(chunk)[0], underline_y), fill=color, width=1)

    def _draw_strikeout(self, draw, x, y, chunk, font, color):
        strikeout_y = y + font.getsize(chunk)[1] // 2
        draw.line((x, strikeout_y, x + font.getbbox(chunk)[2] - font.getbbox(chunk)[0], strikeout_y), fill=color, width=1)
s