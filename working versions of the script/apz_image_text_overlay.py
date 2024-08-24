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
                "apz_image": ("IMAGE",),
                "apz_text": ("STRING", {"multiline": True, "default": "Hello"}),
                "apz_textbox_width": ("INT", {"default": 200, "min": 1}),  
                "apz_textbox_height": ("INT", {"default": 200, "min": 1}),  
                "apz_max_font_size": ("INT", {"default": 30, "min": 1, "max": 256, "step": 1}),  
                "apz_font": ("STRING", {"default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}), 
                "apz_alignment": (cls._alignments, {"default": "center"}),  
                "apz_vertical_alignment": (cls._vertical_alignments, {"default": "middle"}),
                "apz_color": ("STRING", {"default": "#000000"}),  
                "apz_start_x": ("INT", {"default": 0}),  
                "apz_start_y": ("INT", {"default": 0}),
                "apz_padding": ("INT", {"default": 50}),
                "apz_line_height": ("INT", {"default": 20, "min": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apz_add_text_overlay"
    CATEGORY = "image/text"

    def apz_wrap_text_and_calculate_height(self, apz_text, apz_font, apz_max_width, apz_line_height):
        wrapped_lines = []
        # Split the input text by newline characters to respect manual line breaks
        paragraphs = apz_text.split('\n')
        
        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = words[0] if words else ''
            
            for word in words[1:]:
                # Test if adding a new word exceeds the max width
                test_line = current_line + ' ' + word if current_line else word
                test_line_bbox = apz_font.getbbox(test_line)
                w = test_line_bbox[2] - test_line_bbox[0]  # Right - Left for width
                if w <= apz_max_width:
                    current_line = test_line
                else:
                    # If the current line plus the new word exceeds max width, wrap it
                    wrapped_lines.append(current_line)
                    current_line = word
            
            # Don't forget to add the last line of the paragraph
            wrapped_lines.append(current_line)

        # Calculate the total height considering the custom line height
        total_height = len(wrapped_lines) * apz_line_height

        wrapped_text = '\n'.join(wrapped_lines)
        return wrapped_text, total_height


    def apz_add_text_overlay(self, apz_image, apz_text, apz_textbox_width, apz_textbox_height, apz_max_font_size, apz_font, apz_alignment, apz_vertical_alignment, apz_color, apz_start_x, apz_start_y, apz_padding, apz_line_height):
        apz_image_tensor = apz_image
        apz_image_np = apz_image_tensor.cpu().numpy()
        apz_image_pil = Image.fromarray((apz_image_np.squeeze(0) * 255).astype(np.uint8))
        apz_color_rgb = tuple(int(apz_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        apz_effective_textbox_width = apz_textbox_width - 2 * apz_padding  # Adjust for padding
        apz_effective_textbox_height = apz_textbox_height - 2 * apz_padding

        apz_font_size = apz_max_font_size
        default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        
        if not os.path.exists(apz_font):
            apz_font = default_font

        while apz_font_size >= 1:
            try:
                apz_loaded_font = ImageFont.truetype(apz_font, apz_font_size)
            except IOError:
                apz_loaded_font = ImageFont.truetype(default_font, apz_font_size)

            apz_wrapped_text, apz_total_text_height = self.apz_wrap_text_and_calculate_height(apz_text, apz_loaded_font, apz_effective_textbox_width, apz_line_height)

            if apz_total_text_height <= apz_effective_textbox_height:
                draw = ImageDraw.Draw(apz_image_pil)
                lines = apz_wrapped_text.split('\n')

                if apz_vertical_alignment == "top":
                    y = apz_start_y + apz_padding
                elif apz_vertical_alignment == "bottom":
                    y = apz_start_y + apz_effective_textbox_height - apz_total_text_height + apz_padding
                elif apz_vertical_alignment == "middle":
                    y = apz_start_y + apz_padding + (apz_effective_textbox_height - apz_total_text_height) // 2

                for line in lines:
                    line_bbox = apz_loaded_font.getbbox(line)
                    line_width = line_bbox[2] - line_bbox[0]

                    if apz_alignment == "left":
                        x = apz_start_x + apz_padding
                    elif apz_alignment == "right":
                        x = apz_start_x + apz_effective_textbox_width - line_width + apz_padding
                    elif apz_alignment == "center":
                        x = apz_start_x + apz_padding + (apz_effective_textbox_width - line_width) // 2

                    draw.text((x, y), line, fill=apz_color_rgb, font=apz_loaded_font)
                    y += apz_line_height  # Use custom line height for spacing

                break  # Break the loop if text fits within the specified dimensions

            apz_font_size -= 1  # Decrease font size and try again

        apz_image_tensor_out = torch.tensor(np.array(apz_image_pil).astype(np.float32) / 255.0)
        apz_image_tensor_out = torch.unsqueeze(apz_image_tensor_out, 0)
        return (apz_image_tensor_out,)

NODE_CLASS_MAPPINGS = {
    "apzImage Text Overlay": apzImageTextOverlay,
}
