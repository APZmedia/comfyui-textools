# utils/apz_text_renderer_utility.py
from .apz_box_utility import BoxUtility

class TextRendererUtility:
    @staticmethod
    def render_text(draw, wrapped_lines, box_start_x, box_start_y, padding, theTextbox_width, theTextbox_height, font_manager, color_utility, alignment, vertical_alignment, line_height_ratio, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if not wrapped_lines:
            return  # If there's no text to render

        # Calculate effective dimensions
        effective_textbox_width, effective_textbox_height = BoxUtility.calculate_effective_dimensions(theTextbox_width, theTextbox_height, padding)

        # Calculate total text height for vertical alignment purposes
        total_text_height = len(wrapped_lines) * int(wrapped_lines[0][1][0][1]['size'] * line_height_ratio)

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
                
                # Check if we need to scale the emoji (for NotoColorEmoji)
                scale_factor = font_manager.emoji_support.get_emoji_scale_factor(wrapped_lines[0][1][0][1]['size'])
                if scale_factor != 1.0 and font_manager.emoji_support.has_emoji(chunk):
                    # Scale the emoji text
                    from PIL import Image, ImageDraw, ImageFont
                    # Create a temporary image to render the emoji at the correct size
                    temp_img = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
                    temp_draw = ImageDraw.Draw(temp_img)
                    temp_draw.text((0, 0), chunk, fill=current_font_color_rgb, font=current_font)
                    
                    # Get the bounding box of the rendered text
                    bbox = temp_draw.textbbox((0, 0), chunk, font=current_font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # Scale down to the desired size
                    scaled_width = int(text_width * scale_factor)
                    scaled_height = int(text_height * scale_factor)
                    
                    if scaled_width > 0 and scaled_height > 0:
                        # Crop and resize the emoji
                        cropped = temp_img.crop(bbox)
                        scaled_emoji = cropped.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                        
                        # Paste the scaled emoji onto the main image
                        draw._image.paste(scaled_emoji, (int(current_x), int(current_y)), scaled_emoji)
                        chunk_width = scaled_width
                    else:
                        # Fallback to regular text rendering
                        draw.text((current_x, current_y), chunk, fill=current_font_color_rgb, font=current_font)
                        chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]
                else:
                    # Regular text rendering
                    draw.text((current_x, current_y), chunk, fill=current_font_color_rgb, font=current_font)
                    chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                if chunk_styles.get('u', False):  # Underline
                    underline_y = current_y + current_font.getsize(chunk)[1]
                    draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                if chunk_styles.get('s', False):  # Strikethrough
                    strikeout_y = current_y + current_font.getsize(chunk)[1] // 2
                    draw.line((current_x, strikeout_y, current_x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                current_x += chunk_width

            # Move to the next line
            current_y += int(wrapped_lines[0][1][0][1]['size'] * line_height_ratio)
