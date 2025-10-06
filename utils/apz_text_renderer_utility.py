# utils/apz_text_renderer_utility.py
from PIL import Image
from .apz_box_utility import BoxUtility
from .apz_twemoji_renderer import TwemojiRenderer
from .apz_emoji_png_renderer import EmojiPNGRenderer

class TextRendererUtility:
    # Cache for emoji dimensions to avoid recalculation
    _emoji_dimensions_cache = {}
    # Cache for processed emoji images to avoid reprocessing
    _emoji_images_cache = {}
    
    @staticmethod
    def _get_emoji_rendered_width(emoji_segment, chunk_size, emoji_png_renderer):
        """
        Get the actual width that an emoji will occupy when rendered.
        Uses caching to avoid recalculation for the same emoji and size.
        """
        # Create cache key based on emoji and size
        cache_key = f"{emoji_segment}_{chunk_size}"
        
        # Check cache first
        if cache_key in TextRendererUtility._emoji_dimensions_cache:
            return TextRendererUtility._emoji_dimensions_cache[cache_key]
        
        emoji_img = emoji_png_renderer.load_emoji_png(emoji_segment, chunk_size)
        if not emoji_img:
            width = int(chunk_size * 0.8)  # Fallback width
            TextRendererUtility._emoji_dimensions_cache[cache_key] = width
            return width
        
        # Apply the same cropping logic as the renderer to remove padding
        import numpy as np
        emoji_array = np.array(emoji_img)
        
        # Find content boundaries with more aggressive padding removal
        if emoji_array.shape[2] == 4:  # RGBA
            alpha_channel = emoji_array[:, :, 3]
            # Use a higher threshold to be more aggressive about removing padding
            content_pixels = alpha_channel > 10  # Threshold for transparency
        else:  # RGB
            # For RGB images, look for non-white pixels (assuming white is background)
            content_pixels = np.any(emoji_array < 250, axis=2)
        
        if np.any(content_pixels):
            content_rows = np.any(content_pixels, axis=1)
            content_cols = np.any(content_pixels, axis=0)
            
            # Find the first and last rows/columns with content
            content_top = np.argmax(content_rows) if np.any(content_rows) else 0
            content_bottom = len(content_rows) - np.argmax(content_rows[::-1]) if np.any(content_rows) else emoji_img.height
            content_left = np.argmax(content_cols) if np.any(content_cols) else 0
            content_right = len(content_cols) - np.argmax(content_cols[::-1]) if np.any(content_cols) else emoji_img.width
            
            content_width = content_right - content_left
            
            # Ensure we have a reasonable minimum width
            if content_width > 0:
                width = max(content_width, 4)  # Minimum 4px width
            else:
                width = int(chunk_size * 0.8)
        else:
            width = int(chunk_size * 0.8)
        
        # Cache the result
        TextRendererUtility._emoji_dimensions_cache[cache_key] = width
        return width

    @staticmethod
    def _get_processed_emoji_image(emoji_segment, chunk_size, emoji_png_renderer):
        """
        Get a processed emoji image with padding removed.
        Uses caching to avoid reprocessing the same emoji and size.
        """
        # Create cache key based on emoji and size
        cache_key = f"{emoji_segment}_{chunk_size}"
        
        # Check cache first
        if cache_key in TextRendererUtility._emoji_images_cache:
            return TextRendererUtility._emoji_images_cache[cache_key]
        
        emoji_img = emoji_png_renderer.load_emoji_png(emoji_segment, chunk_size)
        if not emoji_img:
            TextRendererUtility._emoji_images_cache[cache_key] = None
            return None
        
        # Apply the same cropping logic as the renderer to remove padding
        import numpy as np
        emoji_array = np.array(emoji_img)
        
        # Find content boundaries with more aggressive padding removal
        if emoji_array.shape[2] == 4:  # RGBA
            alpha_channel = emoji_array[:, :, 3]
            # Use a higher threshold to be more aggressive about removing padding
            content_pixels = alpha_channel > 10  # Threshold for transparency
        else:  # RGB
            # For RGB images, look for non-white pixels (assuming white is background)
            content_pixels = np.any(emoji_array < 250, axis=2)
        
        if np.any(content_pixels):
            content_rows = np.any(content_pixels, axis=1)
            content_cols = np.any(content_pixels, axis=0)
            
            # Find the first and last rows/columns with content
            content_top = np.argmax(content_rows) if np.any(content_rows) else 0
            content_bottom = len(content_rows) - np.argmax(content_rows[::-1]) if np.any(content_rows) else emoji_img.height
            content_left = np.argmax(content_cols) if np.any(content_cols) else 0
            content_right = len(content_cols) - np.argmax(content_cols[::-1]) if np.any(content_cols) else emoji_img.width
            
            # Crop to content area to remove padding
            if content_right > content_left and content_bottom > content_top:
                emoji_img = emoji_img.crop((content_left, content_top, content_right, content_bottom))
        
        # Cache the processed image
        TextRendererUtility._emoji_images_cache[cache_key] = emoji_img
        return emoji_img

    @staticmethod
    def clear_emoji_cache():
        """
        Clear the emoji caches to free memory.
        Call this when you want to reset the cache.
        """
        TextRendererUtility._emoji_dimensions_cache.clear()
        TextRendererUtility._emoji_images_cache.clear()

    @staticmethod
    def _draw_text_with_color_support(draw, position, text, font, fill, font_manager):
        use_embedded_color = font_manager.should_use_embedded_color(font)
        if use_embedded_color:
            try:
                draw.text(position, text, font=font, embedded_color=True)
                return
            except TypeError:
                pass
            except Exception as exc:
                # Debug logging removed for performance
                pass
        draw.text(position, text, font=font, fill=fill)

    @staticmethod
    def _measure_chunk_width(text, styles, font_manager, chunk_size):
        """
        Measure the width of a text chunk, with emoji-aware handling.
        This must match the actual rendering logic exactly.
        """
        if not text:
            return 0

        local_styles = styles if isinstance(styles, dict) else {}
        emoji_support = getattr(font_manager, "emoji_support", None)

        # For spaces, use a simple and consistent measurement
        if text == ' ':
            try:
                measure_font = font_manager.get_font_for_style(local_styles, chunk_size, text)
                bbox = measure_font.getbbox(text)
                space_width = bbox[2] - bbox[0]
                # Ensure space width is reasonable and consistent
                return max(space_width, 2)  # Minimum 2px for space
            except Exception:
                # Fallback for space width
                return max(chunk_size // 4, 2)  # Minimum 2px

        if emoji_support and emoji_support.has_emoji(text):
            total_width = 0
            for segment, is_emoji in emoji_support.split_text_by_emoji(text):
                if not segment:
                    continue
                if is_emoji:
                    # Use the helper function to ensure consistency with rendering
                    from .apz_emoji_png_renderer import EmojiPNGRenderer
                    emoji_png_renderer = EmojiPNGRenderer()
                    emoji_width = TextRendererUtility._get_emoji_rendered_width(segment, chunk_size, emoji_png_renderer)
                    total_width += emoji_width
                else:
                    segment_font = font_manager.get_font_for_style(local_styles, chunk_size, segment)
                    bbox = segment_font.getbbox(segment)
                    total_width += bbox[2] - bbox[0]
            return total_width

        measure_font = font_manager.get_font_for_style(local_styles, chunk_size, text)
        bbox = measure_font.getbbox(text)
        return bbox[2] - bbox[0]

    @staticmethod
    def render_text(draw, wrapped_lines, box_start_x, box_start_y, padding, theTextbox_width, theTextbox_height, font_manager, color_utility, alignment, vertical_alignment, line_height_ratio, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, hashtag_color_rgb=None, show_debug_boxes=False):
        if not wrapped_lines:
            return

        effective_textbox_width, effective_textbox_height = BoxUtility.calculate_effective_dimensions(
            theTextbox_width, theTextbox_height, padding
        )

        processed_lines = []
        total_text_height = 0

        for _, line_parts in wrapped_lines:
            chunk_infos = []
            max_chunk_size = 0
            line_width = 0

            for chunk, chunk_styles in line_parts:
                styles_dict = chunk_styles if isinstance(chunk_styles, dict) else {}
                chunk_size = styles_dict.get("size", font_manager.max_font_size if hasattr(font_manager, "max_font_size") else 16)
                chunk_width = TextRendererUtility._measure_chunk_width(chunk, styles_dict, font_manager, chunk_size)

                chunk_infos.append((chunk, styles_dict, chunk_size, chunk_width))
                max_chunk_size = max(max_chunk_size, chunk_size)
                line_width += chunk_width

            if max_chunk_size == 0:
                max_chunk_size = font_manager.max_font_size if hasattr(font_manager, "max_font_size") else 16

            line_height = int(max_chunk_size * line_height_ratio)
            total_text_height += line_height
            processed_lines.append({
                "chunks": chunk_infos,
                "line_width": line_width,
                "line_height": line_height,
                "line_size": max_chunk_size,
            })

        if vertical_alignment == "middle":
            current_y = box_start_y + padding + max((effective_textbox_height - total_text_height) // 2, 0)
        elif vertical_alignment == "bottom":
            current_y = box_start_y + padding + max(effective_textbox_height - total_text_height, 0)
        else:
            current_y = box_start_y + padding

        emoji_png_renderer = EmojiPNGRenderer()

        for line_data in processed_lines:
            line_height = line_data["line_height"]
            line_width = line_data["line_width"]

            if current_y + line_height > box_start_y + theTextbox_height - padding:
                break

            if alignment == "center":
                current_x = box_start_x + padding + max((effective_textbox_width - line_width) // 2, 0)
            elif alignment == "right":
                current_x = box_start_x + padding + max(effective_textbox_width - line_width, 0)
            else:
                current_x = box_start_x + padding

            for chunk, styles_dict, chunk_size, chunk_width in line_data["chunks"]:
                if not chunk:
                    continue

                # Debug box removed for clean rendering

                current_font = font_manager.get_font_for_style(styles_dict, chunk_size, chunk)
                
                # Log font usage for rendering
                font_name = getattr(current_font, 'path', 'Unknown') if hasattr(current_font, 'path') else 'PIL Default'
                # Debug logging removed for performance

                if styles_dict.get("hashtag", False):
                    if hashtag_color_rgb:
                        current_font_color_rgb = hashtag_color_rgb
                        print(f"🏷️ Hashtag detected: '{chunk}' using color: {hashtag_color_rgb}")
                    else:
                        current_font_color_rgb = (0, 100, 200)  # Default blue
                        print(f"🏷️ Hashtag detected: '{chunk}' using default blue color")
                else:
                    current_font_color_rgb = color_utility.get_font_color(
                        styles_dict, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
                    )

                if chunk_width > 0 and font_manager.emoji_support.has_emoji(chunk):
                    # Handle multiple consecutive emojis by splitting them individually
                    emoji_segments = font_manager.emoji_support.split_text_by_emoji(chunk)
                    current_x_offset = current_x
                    
                    for emoji_segment, is_emoji in emoji_segments:
                        if not emoji_segment:
                            continue
                        
                        # Debug boxes removed for clean rendering
                            
                        if is_emoji:
                            # Render each emoji individually using cached processed image
                            emoji_img = TextRendererUtility._get_processed_emoji_image(emoji_segment, chunk_size, emoji_png_renderer)
                            if emoji_img:
                                # Position emoji to align with text baseline
                                text_baseline = current_y + chunk_size
                                emoji_y = text_baseline - emoji_img.height
                                emoji_y = max(current_y, emoji_y)
                                
                                # Position emoji without extra spacing
                                draw._image.paste(emoji_img, (int(current_x_offset), emoji_y), emoji_img)
                                
                                # Debug box removed for clean rendering
                                
                                # Move x position using the calculated width (same as measurement)
                                emoji_width = TextRendererUtility._get_emoji_rendered_width(emoji_segment, chunk_size, emoji_png_renderer)
                                current_x_offset += emoji_width
                            else:
                                # Fallback to font rendering for this emoji
                                TextRendererUtility._draw_text_with_color_support(
                                    draw, (current_x_offset, current_y), emoji_segment, current_font, current_font_color_rgb, font_manager
                                )
                                
                                # Debug box removed for clean rendering
                                
                                # Estimate width for positioning
                                current_x_offset += chunk_size
                        else:
                            # Position non-emoji text without extra spacing
                            
                            # Render non-emoji text
                            TextRendererUtility._draw_text_with_color_support(
                                draw, (current_x_offset, current_y), emoji_segment, current_font, current_font_color_rgb, font_manager
                            )
                            
                            # Debug box removed for clean rendering
                            
                            # Measure and advance position
                            segment_width = TextRendererUtility._measure_chunk_width(emoji_segment, styles_dict, font_manager, chunk_size)
                            current_x_offset += segment_width
                    
                    # Update current_x to the final position
                    current_x = current_x_offset
                else:
                    # Position text chunk without extra spacing
                    
                    TextRendererUtility._draw_text_with_color_support(
                        draw, (current_x, current_y), chunk, current_font, current_font_color_rgb, font_manager
                    )
                    
                    # Debug box removed for clean rendering

                if chunk_width > 0 and chunk.strip():
                    if styles_dict.get("u", False):
                        underline_y = current_y + current_font.getsize(chunk)[1]
                        draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                    if styles_dict.get("s", False):
                        strikeout_y = current_y + current_font.getsize(chunk)[1] // 2
                        draw.line((current_x, strikeout_y, current_x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                # Advance position after text chunk (only for non-emoji chunks)
                if not (chunk_width > 0 and font_manager.emoji_support.has_emoji(chunk)):
                    current_x += chunk_width

            current_y += line_height
