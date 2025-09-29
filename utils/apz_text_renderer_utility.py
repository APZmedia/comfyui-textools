# utils/apz_text_renderer_utility.py
from PIL import Image
from .apz_box_utility import BoxUtility
from .apz_twemoji_renderer import TwemojiRenderer

class TextRendererUtility:
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
                print(f"Warning: embedded color rendering failed, falling back to standard fill. Error: {exc}")
        draw.text(position, text, font=font, fill=fill)

    @staticmethod
    def render_text(draw, wrapped_lines, box_start_x, box_start_y, padding, theTextbox_width, theTextbox_height, font_manager, color_utility, alignment, vertical_alignment, line_height_ratio, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if not wrapped_lines:
            return  # If there's no text to render

        # Calculate effective dimensions
        effective_textbox_width, effective_textbox_height = BoxUtility.calculate_effective_dimensions(theTextbox_width, theTextbox_height, padding)

        # Calculate total text height for vertical alignment purposes
        # Use the actual font size from the first line, not a hardcoded value
        font_size = wrapped_lines[0][1][0][1]['size'] if wrapped_lines and wrapped_lines[0][1] else 30
        total_text_height = len(wrapped_lines) * int(font_size * line_height_ratio)

        # Calculate the initial Y position based on vertical alignment
        if vertical_alignment == "top":
            current_y = box_start_y + padding
        elif vertical_alignment == "middle":
            current_y = box_start_y + padding + (effective_textbox_height - total_text_height) // 2
        elif vertical_alignment == "bottom":
            current_y = box_start_y + padding + (effective_textbox_height - total_text_height)

        for line, line_parts in wrapped_lines:
            # Calculate the total width of the line
            line_width = sum(font_manager.get_font_for_style(chunk_styles, wrapped_lines[0][1][0][1]['size']).getbbox(chunk)[2] for chunk, chunk_styles in line_parts)

            # Adjust the X position based on alignment
            if alignment == "left":
                current_x = box_start_x + padding
            elif alignment == "center":
                current_x = box_start_x + padding + (effective_textbox_width - line_width) // 2
            elif alignment == "right":
                current_x = box_start_x + padding + (effective_textbox_width - line_width)

            for chunk, chunk_styles in line_parts:
                # Get font with emoji support
                current_font = font_manager.get_font_for_style(chunk_styles, wrapped_lines[0][1][0][1]['size'], chunk)
                
                # Handle hashtag styling (special color for hashtags)
                if chunk_styles.get('hashtag', False):
                    # Use a different color for hashtags (e.g., blue)
                    hashtag_color = (0, 100, 200)  # Blue color for hashtags
                    current_font_color_rgb = hashtag_color
                else:
                    current_font_color_rgb = color_utility.get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
                
                # Check if this is an emoji that needs special handling
                if font_manager.emoji_support.has_emoji(chunk):
                    # Split the chunk into emoji and non-emoji parts
                    emoji_parts = font_manager.emoji_support.split_text_by_emoji(chunk)
                    chunk_start_x = current_x
                    
                    for emoji_part, is_emoji in emoji_parts:
                        if is_emoji:
                            # Use Twemoji for serverless-compatible emoji rendering
                            # print(f"DEBUG: Rendering emoji '{emoji_part}' (length: {len(emoji_part)}) at size {font_size}")
                            try:
                                twemoji_renderer = TwemojiRenderer(use_svg=False)
                                # Use standard 72x72 size and scale to font_size
                                emoji_img = twemoji_renderer.render_emoji(emoji_part, 72)
                                
                                if emoji_img:
                                    # Scale emoji to match font size
                                    if emoji_img.size != (font_size, font_size):
                                        emoji_img = emoji_img.resize((font_size, font_size), Image.Resampling.LANCZOS)
                                    
                                    # Paste emoji onto the image
                                    emoji_y = int(current_y + font_size - emoji_img.height + 5)
                                    draw._image.paste(emoji_img, (int(current_x), emoji_y), emoji_img)
                                    current_x += font_size
                                else:
                                    # Fallback to regular text rendering if PNG not available
                                    TextRendererUtility._draw_text_with_color_support(
                                        draw, (current_x, current_y), emoji_part, current_font, current_font_color_rgb, font_manager
                                    )
                                    bbox = current_font.getbbox(emoji_part)
                                    current_x += bbox[2] - bbox[0]
                            except Exception as e:
                                print(f"PNG emoji renderer failed: {e}")
                                # Fallback to regular text rendering
                                TextRendererUtility._draw_text_with_color_support(
                                    draw, (current_x, current_y), emoji_part, current_font, current_font_color_rgb, font_manager
                                )
                                bbox = current_font.getbbox(emoji_part)
                                current_x += bbox[2] - bbox[0]
                        else:
                            # Regular text part
                            TextRendererUtility._draw_text_with_color_support(
                                draw, (current_x, current_y), emoji_part, current_font, current_font_color_rgb, font_manager
                            )
                            bbox = current_font.getbbox(emoji_part)
                            current_x += bbox[2] - bbox[0]
                    
                    # Calculate total width for the entire chunk
                    chunk_width = current_x - chunk_start_x
                    continue  # Skip the regular text rendering below
                else:
                    # Regular text rendering
                    TextRendererUtility._draw_text_with_color_support(
                        draw, (current_x, current_y), chunk, current_font, current_font_color_rgb, font_manager
                    )
                    chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                if chunk_styles.get('u', False):  # Underline
                    underline_y = current_y + current_font.getsize(chunk)[1]
                    draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                if chunk_styles.get('s', False):  # Strikethrough
                    strikeout_y = current_y + current_font.getsize(chunk)[1] // 2
                    draw.line((current_x, strikeout_y, current_x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                current_x += chunk_width

            # Move to the next line
            current_y += int(font_size * line_height_ratio)
