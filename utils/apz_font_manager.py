from PIL import ImageFont

class FontManager:
    def __init__(self, font, italic_font, bold_font, max_font_size):
        self.font = font
        self.italic_font = italic_font
        self.bold_font = bold_font
        self.max_font_size = max_font_size

    def load_font(self, font_path, font_size):
        try:
            return ImageFont.truetype(font_path, font_size)
        except IOError:
            default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            try:
                return ImageFont.truetype(default_font, font_size)
            except IOError:
                raise RuntimeError("Cannot load default font. Ensure the font path is correct.")

    def get_font_for_style(self, style_flags, font_size):
        if style_flags['b']:
            return self.load_font(self.bold_font, font_size)
        elif style_flags['i']:
            return self.load_font(self.italic_font, font_size)
        else:
            return self.load_font(self.font, font_size)
