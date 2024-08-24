from PIL import Image, ImageDraw, ImageFont
import torch
import numpy as np
import os
import re

class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu"):
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

    def parse_rich_text(self, theText):
        tag_re = re.compile(r'<(/?)(b|i|u|s)>')
        parts = []
        current_pos = 0
        styles = {'b': False, 'i': False, 'u': False, 's': False}
        style_stack = []

        for match in tag_re.finditer(theText):
            start, end = match.span()
            tag_type, tag_name = match.groups()

            if start > current_pos:
                parts.append((theText[current_pos:start], styles.copy()))

            if tag_type == '':
                style_stack.append(styles.copy())
                styles[tag_name] = True
            else:
                if style_stack:
                    styles = style_stack.pop()

            current_pos = end

        if current_pos < len(theText):
            parts.append((theText[current_pos:], styles.copy()))

        if not parts:
            parts.append((theText, styles.copy()))

        return parts

    def apz_wrap_text_and_calculate_height(self, parsed_text, font, apz_max_width, line_height):
        wrapped_lines = []
        current_line = ""
        current_styles = {'b': False, 'i': False, 'u': False, 's': False}
        line_parts = []

        for text, styles in parsed_text:
            words = text.split(' ')
            for i, word in enumerate(words):
                if '\n' in word:
                    subwords = word.split('\n')
                    for j, subword in enumerate(subwords):
                        if j > 0:
                            wrapped_lines.append((current_line, line_parts))
                            current_line = ""
                            line_parts = []
                        if current_line:
                            test_line = current_line + ' ' + subword
                        else:
                            test_line = subword
                        w = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]

                        if w <= apz_max_width:
                            current_line = test_line
                            if current_line.strip():
                                line_parts.append((subword, styles))
                            if i < len(words) - 1 or j < len(subwords) - 1:
                                line_parts.append((' ', styles))
                        else:
                            wrapped_lines.append((current_line, line_parts))
                            current_line = subword
                            line_parts = [(subword, styles)]
                            if i < len(words) - 1 or j < len(subwords) - 1:
                                line_parts.append((' ', styles))
                else:
                    if current_line:
                        test_line = current_line + ' ' + word
                    else:
                        test_line = word
                    w = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]

                    if w <= apz_max_width:
                        current_line = test_line
                        if current_line.strip():
                            line_parts.append((word, styles))
                        if i < len(words) - 1:
                            line_parts.append((' ', styles))
                    else:
                        wrapped_lines.append((current_line, line_parts))
                        current_line = word
                        line_parts = [(word, styles)]
                        if i < len(words) - 1:
                            line_parts.append((' ', styles))

            if text.endswith(' '):
                current_line += ' '
                line_parts.append((' ', styles))

        if current_line:
            wrapped_lines.append((current_line, line_parts))

        total_height = len(wrapped_lines) * line_height
        return wrapped_lines, total_height

    def load_font(self, font_path, font_size):
        try:
            return ImageFont.truetype(font_path, font_size)
        except IOError:
            default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            try:
                return ImageFont.truetype(default_font, font_size)
            except IOError:
                raise RuntimeError("Cannot load default font. Ensure the font path is correct.")

    def apz_add_text_overlay(self, image, theText, theTextbox_width, theTextbox_height, max_font_size, font, italic_font, bold_font, alignment, vertical_alignment, font_color, italic_font_color, bold_font_color, box_start_x, box_start_y, padding, line_height_ratio):
        image_tensor = image
        image_np = image_tensor.cpu().numpy()
        image_pil = Image.fromarray((image_np.squeeze(0) * 255).astype(np.uint8))
        font_color_rgb = tuple(int(font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        italic_font_color_rgb = tuple(int(italic_font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        bold_font_color_rgb = tuple(int(bold_font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        apz_effective_textbox_width = theTextbox_width - 2 * padding
        apz_effective_textbox_height = theTextbox_height - 2 * padding

        font_size = max_font_size

        while font_size >= 1:
            apz_loaded_font = self.load_font(font, font_size)
            line_height = int(font_size * line_height_ratio)

            parsed_text = self.parse_rich_text(theText)
            wrapped_lines, apz_total_text_height = self.apz_wrap_text_and_calculate_height(parsed_text, apz_loaded_font, apz_effective_textbox_width, line_height)

            if apz_total_text_height <= apz_effective_textbox_height:
                draw = ImageDraw.Draw(image_pil)

                if vertical_alignment == "top":
                    y = box_start_y + padding
                elif vertical_alignment == "bottom":
                    y = box_start_y + theTextbox_height - apz_total_text_height - padding
                elif vertical_alignment == "middle":
                    y = box_start_y + padding + (apz_effective_textbox_height - apz_total_text_height) // 2

                for line, line_parts in wrapped_lines:
                    if alignment == "left":
                        x = box_start_x + padding
                    elif alignment == "right":
                        x = box_start_x + apz_effective_textbox_width - (apz_loaded_font.getbbox(line)[2] - apz_loaded_font.getbbox(line)[0]) + padding
                    elif alignment == "center":
                        x = box_start_x + padding + (apz_effective_textbox_width - (apz_loaded_font.getbbox(line)[2] - apz_loaded_font.getbbox(line)[0])) // 2

                    for chunk, chunk_styles in line_parts:
                        if chunk_styles['b']:
                            font_style = bold_font
                            current_font_color_rgb = bold_font_color_rgb
                        elif chunk_styles['i']:
                            font_style = italic_font
                            current_font_color_rgb = italic_font_color_rgb
                        else:
                            font_style = font
                            current_font_color_rgb = font_color_rgb

                        if not os.path.exists(font_style):
                            font_style = font

                        apz_loaded_font = self.load_font(font_style, font_size)
                        draw.text((x, y), chunk, fill=current_font_color_rgb, font=apz_loaded_font)
                        chunk_width = apz_loaded_font.getbbox(chunk)[2] - apz_loaded_font.getbbox(chunk)[0]

                        if chunk_styles['u']:
                            underline_y = y + apz_loaded_font.getsize(chunk)[1]
                            draw.line((x, underline_y, x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                        if chunk_styles['s']:
                            strikeout_y = y + apz_loaded_font.getsize(chunk)[1] // 2
                            draw.line((x, strikeout_y, x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                        x += chunk_width

                    y += line_height

                break

            font_size -= 1

        image_tensor_out = torch.tensor(np.array(image_pil).astype(np.float32) / 255.0)
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)
        return (image_tensor_out,)

NODE_CLASS_MAPPINGS = {
    "APZmedia Image Rich Text Overlay": APZmediaImageRichTextOverlay,
}
