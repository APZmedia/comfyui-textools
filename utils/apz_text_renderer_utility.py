# utils/apz_text_renderer_utility.py
from ..utils.apz_box_utility import BoxUtility

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
            current_y = box_start_y + (effective_textbox_height - total_text_height) // 2
        elif vertical_alignment == "bottom":
            current_y = box_start_y + effective_textbox_height - total_text_height

        for line, line_parts in wrapped_lines:
            # Calculate the total width of the line
            line_width = sum(font_manager.get_font_for_style(chunk_styles, wrapped_lines[0][1][0][1]['size']).getbbox(chunk)[2] for chunk, chunk_styles in line_parts)

            # Adjust the X position based on alignment
            if alignment == "left":
                current_x = box_start_x + padding
            elif alignment == "center":
                current_x = box_start_x + (effective_textbox_width - line_width) // 2
            elif alignment == "right":
                current_x = box_start_x + effective_textbox_width - line_width  # Subtract padding only once

            for chunk, chunk_styles in line_parts:
                current_font = font_manager.get_font_for_style(chunk_styles, wrapped_lines[0][1][0][1]['size'])
                current_font_color_rgb = color_utility.get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
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
