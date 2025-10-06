try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
from PIL import ImageDraw
from ..utils.apz_color_utility import ColorUtility
from ..utils.apz_enhanced_font_loader_utility import EnhancedFontLoaderUtility
from ..utils.apz_error_handler_utility import ErrorHandlerUtility
from ..utils.apz_text_renderer_utility import TextRendererUtility
from ..utils.apz_image_conversion import tensor_to_pil, pil_to_tensor
from ..utils.apz_font_manager import FontManager
from ..utils.apz_box_utility import BoxUtility
from ..utils.apz_markdown_parser import parse_markdown, parse_markdown_with_headers, parse_markdown_extended
from ..utils.apz_markdown_renderer_utility import MarkdownRendererUtility
from ..utils.apz_hashtag_parser import parse_hashtags, extract_hashtags, has_hashtags, count_hashtags
from ..utils.apz_emoji_support import create_emoji_support

class APZmediaImageMarkdownTextOverlay:
    def __init__(self, device="cpu"):
        print("APZmediaImageMarkdownTextOverlay initialized")
        self.device = device

    _alignments = ["left", "right", "center"]
    _vertical_alignments = ["top", "middle", "bottom"]
    _markdown_modes = ["basic", "with_headers", "extended"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "theText": ("STRING", {"multiline": True, "default": "Hello **World** *This is italic* with #hashtags and 😀 emojis"}),
                "markdown_mode": (cls._markdown_modes, {"default": "basic"}),
                "theTextbox_width": ("INT", {"default": 200, "min": 1}),
                "theTextbox_height": ("INT", {"default": 200, "min": 1}),
                "max_font_size": ("INT", {"default": 30, "min": 1, "max": 256, "step": 1}),
                "font": ("STRING", {"default": ""}),
                "italic_font": ("STRING", {"default": ""}),
                "bold_font": ("STRING", {"default": ""}),
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
                "hashtag_color": ("STRING", {"default": "#0066CC"}),  # Color for hashtags
                "enable_hashtag_support": (["false", "true"], {"default": "true"}),  # Enable hashtag support
                "enable_emoji_support": (["false", "true"], {"default": "true"}),  # Enable emoji support
                "custom_emoji_font_url": ("STRING", {"default": "", "multiline": False}),  # Optional custom emoji font URL
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "hashtags_found", "emojis_found", "processing_info")
    FUNCTION = "apz_add_markdown_text_overlay"
    CATEGORY = "APZmedia/Text"

    def apz_add_markdown_text_overlay(self, image, theText, markdown_mode, theTextbox_width, theTextbox_height, max_font_size, font, italic_font, bold_font, alignment, vertical_alignment, font_color, italic_font_color, bold_font_color, box_start_x, box_start_y, padding, line_height_ratio, show_bounding_box, bounding_box_color, line_width, line_opacity, box_background_color, box_opacity, hashtag_color, enable_hashtag_support, enable_emoji_support, custom_emoji_font_url):
        print(f"📝 APZmediaImageMarkdownTextOverlay processing:")
        print(f"   Text: '{theText[:50]}{'...' if len(theText) > 50 else ''}'")
        print(f"   Markdown mode: {markdown_mode}")
        print(f"   Font paths - Regular: {font or 'Default'}, Italic: {italic_font or 'Default'}, Bold: {bold_font or 'Default'}")
        print(f"   Box size: {theTextbox_width}x{theTextbox_height}, Max font size: {max_font_size}")
        print(f"   Features - Hashtags: {enable_hashtag_support}, Emojis: {enable_emoji_support}")
        
        pil_images = tensor_to_pil(image)
        color_utility = ColorUtility()

        font_color_rgb = color_utility.hex_to_rgb(font_color)
        italic_font_color_rgb = color_utility.hex_to_rgb(italic_font_color)
        bold_font_color_rgb = color_utility.hex_to_rgb(bold_font_color)
        hashtag_color_rgb = color_utility.hex_to_rgb(hashtag_color)
        
        # Initialize emoji support with custom URL if provided
        custom_url = custom_emoji_font_url.strip() if custom_emoji_font_url else None
        emoji_support = create_emoji_support(custom_url)
        
        # Analyze text for hashtags and emojis
        hashtags_found = []
        emojis_found = []
        processing_info = []
        
        if enable_hashtag_support == "true" and has_hashtags(theText):
            hashtags_found = extract_hashtags(theText)
            processing_info.append(f"Found {len(hashtags_found)} hashtags: {', '.join(hashtags_found)}")
        
        if enable_emoji_support == "true" and emoji_support.has_emoji(theText):
            emojis_found = emoji_support.extract_emojis(theText)
            processing_info.append(f"Found {len(emojis_found)} emojis: {', '.join(emojis_found)}")

        # Initialize error handler
        error_handler = ErrorHandlerUtility()
        
        # Validate parameters
        is_valid_dimensions, dim_error = error_handler.validate_text_box_dimensions(theTextbox_width, theTextbox_height)
        if not is_valid_dimensions:
            print(f"Warning: {dim_error}")
        
        is_valid_font_size, font_error = error_handler.validate_font_size(max_font_size)
        if not is_valid_font_size:
            print(f"Warning: {font_error}")
            max_font_size = min(max_font_size, 256)
        
        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        font_loader = EnhancedFontLoaderUtility(font_manager, max_font_size)

        # Convert markdown to plain text for font sizing calculations
        # This is a simplified approach - in a more sophisticated implementation,
        # you might want to handle different font sizes for different markdown elements
        processed_text = theText
        # Remove markdown syntax for sizing calculations
        processed_text = processed_text.replace('**', '').replace('*', '').replace('__', '').replace('~~', '')
        # Remove headers
        import re
        processed_text = re.sub(r'^#{1,6}\s+', '', processed_text, flags=re.MULTILINE)
        # Remove list markers
        processed_text = re.sub(r'^[-*]\s+', '', processed_text, flags=re.MULTILINE)
        processed_text = re.sub(r'^\d+\.\s+', '', processed_text, flags=re.MULTILINE)

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
                
            # Find the font size and wrap the lines using the original text with enhanced error handling
            text_type_map = {
                "basic": "markdown_basic",
                "with_headers": "markdown_headers", 
                "extended": "markdown_extended"
            }
            text_type = text_type_map.get(markdown_mode, "markdown_basic")
            
            font_size, wrapped_lines, total_text_height, warnings = font_loader.find_fitting_font_size(
                theText, theTextbox_width - 2 * padding, theTextbox_height - 2 * padding, 
                line_height_ratio, text_type
            )

            # Log warnings if any
            if warnings:
                for warning in warnings:
                    print(f"Warning: {warning}")

            if font_size:
                # Use standard markdown rendering with emoji support
                MarkdownRendererUtility.render_markdown_text(
                    draw, theText, markdown_mode, box_left, box_top, padding,
                    box_right - box_left, box_bottom - box_top, font_manager,
                    color_utility, alignment, vertical_alignment, line_height_ratio,
                    font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, font_size, hashtag_color_rgb
                )
            else:
                # Handle case where no font size works - try enhanced scaling fallback
                success, fallback_font_size, fallback_text, scaling_message = error_handler.handle_font_scaling_fallback(
                    theText, theTextbox_width - 2 * padding, theTextbox_height - 2 * padding,
                    max_font_size, font_manager, line_height_ratio, text_type
                )
                
                if success:
                    # Use the scaled font size and text
                    print(f"Markdown font scaling fallback: {scaling_message}")
                    fallback_font = font_manager.get_regular_font(fallback_font_size)
                    
                    # Calculate text position
                    bbox = fallback_font.getbbox(fallback_text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # Position text based on alignment
                    if alignment == "center":
                        x = box_left + (box_right - box_left - text_width) // 2
                    elif alignment == "right":
                        x = box_right - text_width - padding
                    else:  # left
                        x = box_left + padding
                    
                    if vertical_alignment == "middle":
                        y = box_top + (box_bottom - box_top - text_height) // 2
                    elif vertical_alignment == "bottom":
                        y = box_bottom - text_height - padding
                    else:  # top
                        y = box_top + padding
                    
                    draw.text((x, y), fallback_text, font=fallback_font, fill=font_color_rgb)
                    
                else:
                    # All scaling strategies failed - show error indicator
                    error_handler.draw_error_indicator(
                        draw, effective_box_left, effective_box_top, 
                        effective_box_right - effective_box_left, 
                        effective_box_bottom - effective_box_top,
                        "Markdown text overflow - all scaling strategies failed"
                    )

            processed_image = pil_to_tensor(image_pil)
            processed_images.append(processed_image)

        if TORCH_AVAILABLE:
            final_tensor = torch.cat(processed_images, dim=0)
        else:
            # If torch is not available, return the first processed image
            final_tensor = processed_images[0] if processed_images else None
        
        # Prepare return information
        hashtags_str = ", ".join(hashtags_found) if hashtags_found else "None"
        emojis_str = ", ".join(emojis_found) if emojis_found else "None"
        info_str = " | ".join(processing_info) if processing_info else "No issues detected"
        
        return (final_tensor, hashtags_str, emojis_str, info_str) 
