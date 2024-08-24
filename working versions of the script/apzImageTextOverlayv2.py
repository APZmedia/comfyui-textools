from PIL import Image, ImageDraw, ImageFont
import torch
import numpy as np
import os

class apzImageTextOverlay:
    def __init__(self, device="cpu"):
        self.device = device
    _alignments = ["left", "right", "center"]
    _vertical_alignments = ["top", "middle", "bottom"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "theText": ("STRING", {"multiline": True, "default": "Hello"}),
                "theTextbox_width": ("INT", {"default": 200, "min": 1}),  
                "theTextbox_height": ("INT", {"default": 200, "min": 1}),  
                "max_font_size": ("INT", {"default": 30, "min": 1, "max": 256, "step": 1}),  
                "font": ("STRING", {"default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}), 
                "alignment": (cls._alignments, {"default": "center"}),  
                "vertical_alignment": (cls._vertical_alignments, {"default": "middle"}),
                "font_color": ("STRING", {"default": "#000000"}),  
                "box_start_x": ("INT", {"default": 0}),  
                "box_start_y": ("INT", {"default": 0}),
                "padding": ("INT", {"default": 50}),
                "line_height": ("INT", {"default": 20, "min": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apz_add_text_overlay"
    CATEGORY = "image/text"

    def apz_wrap_text_and_calculate_height(self, theText, font, apz_max_width, line_height):
        wrapped_lines = []
        paragraphs = theText.split('\n')
        
        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = words[0] if words else ''
            
            for word in words[1:]:
                test_line = current_line + ' ' + word if current_line else word
                test_line_bbox = font.getbbox(test_line)
                w = test_line_bbox[2] - test_line_bbox[0]
                if w <= apz_max_width:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            
            wrapped_lines.append(current_line)

        total_height = len(wrapped_lines) * line_height
        wrapped_text = '\n'.join(wrapped_lines)
        return wrapped_text, total_height

    def apz_add_text_overlay(self, image, theText, theTextbox_width, theTextbox_height, max_font_size, font, alignment, vertical_alignment, font_color, box_start_x, box_start_y, padding, line_height):
        image_tensor = image
        image_np = image_tensor.cpu().numpy()
        image_pil = Image.fromarray((image_np.squeeze(0) * 255).astype(np.uint8))
        font_color_rgb = tuple(int(font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        apz_effective_textbox_width = theTextbox_width - 2 * padding
        apz_effective_textbox_height = theTextbox_height - 2 * padding

        font_size = max_font_size
        default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        
        if not os.path.exists(font):
            font = default_font

        while font_size >= 1:
            try:
                apz_loaded_font = ImageFont.truetype(font, font_size)
            except IOError:
                apz_loaded_font = ImageFont.truetype(default_font, font_size)

            apz_wrapped_text, apz_total_text_height = self.apz_wrap_text_and_calculate_height(theText, apz_loaded_font, apz_effective_textbox_width, line_height)

            if apz_total_text_height <= apz_effective_textbox_height:
                draw = ImageDraw.Draw(image_pil)
                lines = apz_wrapped_text.split('\n')

                if vertical_alignment == "top":
                    y = box_start_y + padding
                elif vertical_alignment == "bottom":
                    y = box_start_y + theTextbox_height - apz_total_text_height - padding
                elif vertical_alignment == "middle":
                    y = box_start_y + padding + (apz_effective_textbox_height - apz_total_text_height) // 2

                for line in lines:
                    line_bbox = apz_loaded_font.getbbox(line)
                    line_width = line_bbox[2] - line_bbox[0]

                    if alignment == "left":
                        x = box_start_x + padding
                    elif alignment == "right":
                        x = box_start_x + apz_effective_textbox_width - line_width + padding
                    elif alignment == "center":
                        x = box_start_x + padding + (apz_effective_textbox_width - line_width) // 2

                    draw.text((x, y), line, fill=font_color_rgb, font=apz_loaded_font)
                    y += line_height

                break

            font_size -= 1

        image_tensor_out = torch.tensor(np.array(image_pil).astype(np.float32) / 255.0)
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)
        return (image_tensor_out,)

NODE_CLASS_MAPPINGS = {
    "apzImage Text Overlay": apzImageTextOverlay,
}
