from PIL import ImageFont

class FontManager:
    def __init__(self, font, italic_font, bold_font, max_font_size, default_font=None):
        self.font = font
        self.italic_font = italic_font
        self.bold_font = bold_font
        self.max_font_size = max_font_size
        self.default_font = default_font or "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        self.font_cache = {}  # Cache to store loaded fonts

    def load_font(self, font_path, font_size):
        """
        Loads the font from the given path. Falls back to a default font if the font cannot be loaded.
        Caches the font after loading it for the first time.
        """
        cache_key = (font_path, font_size)
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Warning: Cannot load font at {font_path}. Falling back to default font.")
            try:
                font = ImageFont.truetype(self.default_font, font_size)
            except IOError:
                raise RuntimeError("Cannot load default font. Ensure the font path is correct.")

        # Cache the loaded font
        self.font_cache[cache_key] = font
        return font

    def get_font_for_style(self, style_flags, font_size):
        """
        Returns the appropriate font based on the style flags (bold, italic).
        Caches fonts to avoid reloading them.
        """
        bold = style_flags.get('b', False)
        italic = style_flags.get('i', False)

        if bold:
            return self.load_font(self.bold_font, font_size)
        elif italic:
            return self.load_font(self.italic_font, font_size)
        else:
            return self.load_font(self.font, font_size)
