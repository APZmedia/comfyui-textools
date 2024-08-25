# font_manager.py
from PIL import ImageFont

class FontManager:
    def __init__(self, font, italic_font, bold_font, max_font_size, default_font=None):
        self.font = font
        self.italic_font = italic_font
        self.bold_font = bold_font
        self.max_font_size = max_font_size
        self.default_font = default_font or "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def load_font(self, font_path, font_size):
        try:
            return ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Warning: Cannot load font at {font_path}. Falling back to default font.")
            try:
                return ImageFont.truetype(self.default_font, font_size)
            except IOError:
                raise RuntimeError("Cannot load default font. Ensure the font path is correct.")

    def get_font_for_style(self, style_flags, font_size):
        bold = style_flags.get('b', False)
        italic = style_flags.get('i', False)

        if bold:
            return self.load_font(self.bold_font, font_size)
        elif italic:
            return self.load_font(self.italic_font, font_size)
        else:
            return self.load_font(self.font, font_size)
