# font_loader_utility.py

from ..utils.apz_rich_text_parser import parse_rich_text
from ..utils.apz_text_wrapper import wrap_text

class FontLoaderUtility:
    def __init__(self, font_manager, max_font_size):
        self.font_manager = font_manager
        self.max_font_size = max_font_size

    def find_fitting_font_size(self, theText, effective_textbox_width, effective_textbox_height, line_height_ratio):
        font_size = self.max_font_size
        while font_size >= 1:
            # Use regular font as a baseline for size fitting
            loaded_font = self.font_manager.get_regular_font(font_size)
            line_height = int(font_size * line_height_ratio)
            parsed_text = parse_rich_text(theText)
            wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, effective_textbox_width, line_height)

            # Attach font size to the style dictionary in wrapped_lines
            for line, line_parts in wrapped_lines:
                for chunk, chunk_styles in line_parts:
                    chunk_styles['size'] = font_size

            if total_text_height <= effective_textbox_height:
                return font_size, wrapped_lines, total_text_height
            font_size -= 1
        return None, None, None  # Fallback if no fitting size is found