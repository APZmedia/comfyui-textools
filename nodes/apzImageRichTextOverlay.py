# apzImageRichTextOverlay.py
from PIL import ImageDraw
import torch
import numpy as np
from ..utils.apz_image_conversion import tensor_to_pil, pil_to_tensor
from ..utils.apz_rich_text_parser import parse_rich_text
from ..utils.apz_text_wrapper import wrap_text
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
        image_pil = tensor_to_pil(image)
        font_color_rgb = tuple(int(font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        italic_font_color_rgb = tuple(int(italic_font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        bold_font_color_rgb = tuple(int(bold_font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        effective_textbox_width = theTextbox_width - 2 * padding
        effective_textbox_height = theTextbox_height - 2 * padding

        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        font_size = max_font_size

        while font_size >= 1:
            loaded_font = font_manager.load_font(font, font_size)
            line_height = int(font_size * line_height_ratio)
            parsed_text = parse_rich_text(theText)
            wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, effective_textbox_width, line_height)

            if total_text_height <= effective_textbox_height:
                draw = ImageDraw.Draw(image_pil)
                y = self._calculate_initial_y(vertical_alignment, box_start_y, padding, effective_textbox_height, total_text_height)

                for line, line_parts in wrapped_lines:
                    x = self._calculate_initial_x(alignment, box_start_x, padding, effective_textbox_width, line, loaded_font)
                    for chunk, chunk_styles in line_parts:
                        current_font = font_manager.get_font_for_style(chunk_styles, font_size)
                        current_font_color_rgb = self._get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
                        draw.text((x, y), chunk, fill=current_font_color_rgb, font=current_font)
                        chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                        if chunk_styles.get('u', False):
                            underline_y = y + current_font.getsize(chunk)[1]
                            draw.line((x, underline_y, x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                        if chunk_styles.get('s', False):
                            strikeout_y = y + current_font.getsize(chunk)[1] // 2
                            draw.line((x, strikeout_y, x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                        x += chunk_width

                    y += line_height

                break

            font_size -= 1

        image_tensor_out = pil_to_tensor(image_pil)
        return (image_tensor_out,)

    def _calculate_initial_y(self, vertical_alignment, box_start_y, padding, effective_textbox_height, total_text_height):
        if vertical_alignment == "top":
            return box_start_y + padding
        elif vertical_alignment == "bottom":
            return box_start_y + effective_textbox_height - total_text_height - padding
        else:  # "middle"
            return box_start_y + padding + (effective_textbox_height - total_text_height) // 2

    def _calculate_initial_x(self, alignment, box_start_x, padding, effective_textbox_width, line, font):
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
