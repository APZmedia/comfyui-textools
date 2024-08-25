from PIL import Image, ImageDraw
import torch
import numpy as np

from utils.font_manager import FontManager
from utils.rich_text_parser import RichTextParser
from utils.text_wrapper import TextWrapper
from utils.image_helpers import hex_to_rgb, convert_to_tensor

class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu"):
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
        image_tensor = image
        image_np = image_tensor.cpu().numpy()
        image_pil = Image.fromarray((image_np.squeeze(0) * 255).astype(np.uint8))

        font_color_rgb = hex_to_rgb(font_color)
        italic_font_color_rgb = hex_to_rgb(italic_font_color)
        bold_font_color_rgb = hex_to_rgb(bold_font_color)

        effective_textbox_width = theTextbox_width - 2 * padding
        effective_textbox_height = theTextbox_height - 2 * padding

        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        text_wrapper = TextWrapper(font_manager)

        for font_size in range(max_font_size, 0, -1):
            line_height = int(font_size * line_height_ratio)
            parsed_text = self.text_parser.parse(theText)
            wrapped_lines, total_text_height = text_wrapper.wrap_text(parsed_text, effective_textbox_width, line_height, font_size)

            if total_text_height <= effective_textbox_height:
                self._draw_text(image_pil, wrapped_lines, alignment, vertical_alignment, font_manager, font_size, line_height, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, box_start_x, box_start_y, padding, effective_textbox_width)
                break

        return convert_to_tensor(image_pil)

    def _draw_text(self, image_pil, wrapped_lines, alignment, vertical_alignment, font_manager, font_size, line_height, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, box_start_x, box_start_y, padding, effective_textbox_width):
        draw = ImageDraw.Draw(image_pil)
        y = self._calculate_initial_y(vertical_alignment, box_start_y, padding, effective_textbox_height, len(wrapped_lines) * line_height)

        for line, line_parts in wrapped_lines:
            x = self._calculate_initial_x(alignment, box_start_x, padding, effective_textbox_width, line, font_manager, font_size)
            for chunk, chunk_styles in line_parts:
                current_font = font_manager.get_font_for_style(chunk_styles, font_size)
                current_font_color_rgb = self._get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
                draw.text((x, y), chunk, fill=current_font_color_rgb, font=current_font)
                chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                if chunk_styles['u']:
                    self._draw_underline(draw, x, y, chunk, current_font, current_font_color_rgb)
                if chunk_styles['s']:
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
        if chunk_styles['b']:
            return bold_font_color_rgb
        elif chunk_styles['i']:
            return italic_font_color_rgb
        else:
            return font_color_rgb

    def _draw_underline(self, draw, x, y, chunk, font, color):
        underline_y = y + font.getsize(chunk)[1]
        draw.line((x, underline_y, x + font.getbbox(chunk)[2] - font.getbbox(chunk)[0], underline_y), fill=color, width=1)

    def _draw_strikeout(self, draw, x, y, chunk, font, color):
        strikeout_y = y + font.getsize(chunk)[1] // 2
        draw.line((x, strikeout_y, x + font.getbbox(chunk)[2] - font.getbbox(chunk)[0], strikeout_y), fill=color, width=1)

NODE_CLASS_MAPPINGS = {
    "APZmedia Image Rich Text Overlay": APZmediaImageRichTextOverlay,
}
