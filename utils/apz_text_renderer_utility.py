from ..utils.apz_text_box_utility import TextBoxUtility
from ..utils.apz_color_utility import ColorUtility
from PIL import ImageDraw

class TextRendererUtility:
    @staticmethod
    def render_text(draw, wrapped_lines, box_start_x, box_start_y, padding, effective_textbox_width, effective_textbox_height, font_manager, color_utility, alignment, vertical_alignment, line_height_ratio, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if not wrapped_lines:
            return  # If there's no text to render

        # Assuming the first font size is correct for all lines
        font_size = wrapped_lines[0][1][0][1]['size']

        # Calculate the initial Y position based on vertical alignment
        y = TextBoxUtility.calculate_initial_y(vertical_alignment, box_start_y, padding, effective_textbox_height, len(wrapped_lines) * int(font_size * line_height_ratio))

        for line, line_parts in wrapped_lines:
            # Use the first part of the line to get the default font for alignment calculations
            default_font = font_manager.get_font_for_style(line_parts[0][1], font_size)
            
            # Calculate the initial X position based on horizontal alignment
            x = TextBoxUtility.calculate_initial_x(alignment, box_start_x, padding, effective_textbox_width, line, default_font)

            for chunk, chunk_styles in line_parts:
                current_font = font_manager.get_font_for_style(chunk_styles, font_size)
                current_font_color_rgb = color_utility.get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb)
                draw.text((x, y), chunk, fill=current_font_color_rgb, font=current_font)
                chunk_width = current_font.getbbox(chunk)[2] - current_font.getbbox(chunk)[0]

                if chunk_styles.get('u', False):  # Underline
                    underline_y = y + current_font.getsize(chunk)[1]
                    draw.line((x, underline_y, x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                if chunk_styles.get('s', False):  # Strikethrough
                    strikeout_y = y + current_font.getsize(chunk)[1] // 2
                    draw.line((x, strikeout_y, x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                x += chunk_width

            # Move to the next line
            y += int(font_size * line_height_ratio)
