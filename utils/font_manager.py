from PIL import ImageFont

class FontManager:
    def __init__(self, font_path, font_size, bold_font_path=None, italic_font_path=None):
        self.font_path = font_path
        self.font_size = font_size
        self.bold_font_path = bold_font_path or font_path
        self.italic_font_path = italic_font_path or font_path

    def get_font(self, style=None):
        """
        Returns the appropriate font based on the style.
        """
        if style == "bold":
            return ImageFont.truetype(self.bold_font_path, self.font_size)
        elif style == "italic":
            return ImageFont.truetype(self.italic_font_path, self.font_size)
        else:
            return ImageFont.truetype(self.font_path, self.font_size)
