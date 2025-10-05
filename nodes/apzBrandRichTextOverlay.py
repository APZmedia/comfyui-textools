import torch
from PIL import ImageDraw
from ..utils.apz_color_utility import ColorUtility
from ..utils.apz_font_loader_utility import FontLoaderUtility
from ..utils.apz_text_renderer_utility import TextRendererUtility
from ..utils.apz_image_conversion import tensor_to_pil, pil_to_tensor
from ..utils.apz_font_manager import FontManager
from ..utils.apz_box_utility import BoxUtility
import json

class APZmediaBrandRichTextOverlay:
    def __init__(self, device="cpu"):
        print("APZmediaBrandRichTextOverlay initialized")
        self.device = device

    _alignments = ["left", "right", "center"]
    _vertical_alignments = ["top", "middle", "bottom"]
    _font_types = ["primary", "secondary", "tertiary"]
    _font_variants = ["regular", "bold", "italic"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "brand_assets": ("BRAND_ASSETS",),
                "theText": ("STRING", {"multiline": True, "default": "Hello <b>World</b> <i>This is italic</i>"}),
                "theTextbox_width": ("INT", {"default": 200, "min": 1}),
                "theTextbox_height": ("INT", {"default": 200, "min": 1}),
                "max_font_size": ("INT", {"default": 30, "min": 1, "max": 256, "step": 1}),
                "font_type": (cls._font_types, {"default": "primary"}),
                "font_variant": (cls._font_variants, {"default": "regular"}),
                "alignment": (cls._alignments, {"default": "center"}),
                "vertical_alignment": (cls._vertical_alignments, {"default": "middle"}),
                "font_color": ("STRING", {"default": "#000000"}),
                "italic_font_color": ("STRING", {"default": "#000000"}),
                "bold_font_color": ("STRING", {"default": "#000000"}),
                "box_start_x": ("INT", {"default": 0}),
                "box_start_y": ("INT", {"default": 0}),
                "padding": ("INT", {"default": 50}),
                "line_height_ratio": ("FLOAT", {"default": 1.2, "min": 1.0}),
                "show_bounding_box": (["false", "true"], {"default": "false"}),
                "bounding_box_color": ("STRING", {"default": "#FF0000"}),
                "line_width": ("INT", {"default": 3, "min": 1, "max": 10}),
                "line_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "box_background_color": ("STRING", {"default": "#FFFFFF"}),
                "box_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
            },
            "optional": {
                "font_override_regular": ("STRING", {"default": ""}),
                "font_override_italic": ("STRING", {"default": ""}),
                "font_override_bold": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apz_add_brand_text_overlay"
    CATEGORY = "APZmedia/Brand Text"

    def apz_add_brand_text_overlay(self, image, brand_assets, theText, theTextbox_width, theTextbox_height, max_font_size, font_type, font_variant, alignment, vertical_alignment, font_color, italic_font_color, bold_font_color, box_start_x, box_start_y, padding, line_height_ratio, show_bounding_box, bounding_box_color, line_width, line_opacity, box_background_color, box_opacity, font_override_regular="", font_override_italic="", font_override_bold=""):
        print(f"📝 APZmediaBrandRichTextOverlay processing:")
        print(f"   Text: '{theText[:50]}{'...' if len(theText) > 50 else ''}'")
        print(f"   Font type: {font_type}, Variant: {font_variant}")
        print(f"   Box size: {theTextbox_width}x{theTextbox_height}, Max font size: {max_font_size}")
        
        # Extract brand information
        brand_name = brand_assets.get("brand_name", "Unknown Brand")
        status_message = brand_assets.get("status_message", "")
        print(f"   Brand: {brand_name}")
        print(f"   Status: {status_message}")
        
        # Get font paths from brand assets with overrides
        regular_font_path = self._get_font_path(brand_assets, font_type, "regular", font_override_regular)
        italic_font_path = self._get_font_path(brand_assets, font_type, "italic", font_override_italic)
        bold_font_path = self._get_font_path(brand_assets, font_type, "bold", font_override_bold)
        
        print(f"   Font paths - Regular: {regular_font_path or 'Default'}, Italic: {italic_font_path or 'Default'}, Bold: {bold_font_path or 'Default'}")
        
        pil_images = tensor_to_pil(image)
        color_utility = ColorUtility()

        font_color_rgb = color_utility.hex_to_rgb(font_color)
        italic_font_color_rgb = color_utility.hex_to_rgb(italic_font_color)
        bold_font_color_rgb = color_utility.hex_to_rgb(bold_font_color)

        font_manager = FontManager(regular_font_path, italic_font_path, bold_font_path, max_font_size)
        font_loader = FontLoaderUtility(font_manager, max_font_size)

        processed_images = []
        for idx, image_pil in enumerate(pil_images):
            # Calculate box coordinates
            box_left, box_top, box_right, box_bottom = BoxUtility.calculate_box_coordinates(box_start_x, box_start_y, theTextbox_width, theTextbox_height)

            # Calculate the effective box coordinates considering padding
            effective_box_left, effective_box_top, effective_box_right, effective_box_bottom = BoxUtility.calculate_effective_box_coordinates(box_start_x, box_start_y, theTextbox_width, theTextbox_height, padding)

            draw = ImageDraw.Draw(image_pil, "RGBA")

            # Draw the bounding box if the option is enabled
            if show_bounding_box == "true":
                effective_box_rgb = color_utility.hex_to_rgb(bounding_box_color) + (int(line_opacity * 255),)
                box_background_rgb = color_utility.hex_to_rgb(box_background_color) + (int(box_opacity * 255),)
                BoxUtility.draw_bounding_box(draw, effective_box_left, effective_box_top, effective_box_right, effective_box_bottom, effective_box_rgb, box_background_rgb, line_width)
                
            # Find the font size and wrap the lines
            font_size, wrapped_lines, total_text_height = font_loader.find_fitting_font_size(theText, theTextbox_width - 2 * padding, theTextbox_height - 2 * padding, line_height_ratio)

            if font_size:
                TextRendererUtility.render_text(
                    draw, wrapped_lines, box_left, box_top, padding,
                    box_right - box_left, box_bottom - box_top, font_manager,
                    color_utility, alignment, vertical_alignment, line_height_ratio,
                    font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
                )

            processed_image = pil_to_tensor(image_pil)
            processed_images.append(processed_image)

        final_tensor = torch.cat(processed_images, dim=0)
        return final_tensor,

    def _get_font_path(self, brand_assets, font_type, variant, override_path):
        """Get font path from brand assets with override support"""
        if override_path and override_path.strip():
            print(f"   Using override font for {font_type}_{variant}: {override_path}")
            return override_path.strip()
        
        # Build the font key
        if variant == "regular":
            font_key = f"font_{font_type}"
        else:
            font_key = f"font_{font_type}_{variant}"
        
        font_path = brand_assets.get(font_key, "")
        if font_path:
            print(f"   Using brand font {font_key}: {font_path}")
        else:
            print(f"   Brand font {font_key} not found, will use default")
        
        return font_path
