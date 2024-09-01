# font_manager.py
from PIL import ImageFont 

class FontManager:
    def __init__(self, regular_font_path, italic_font_path, bold_font_path, max_font_size):
        self.regular_font_path = regular_font_path
        self.italic_font_path = italic_font_path
        self.bold_font_path = bold_font_path
        self.max_font_size = max_font_size

        # Print statements to confirm paths
        print(f"Initialized FontManager with Regular Font: {regular_font_path}")
        print(f"Italic Font: {italic_font_path}")
        print(f"Bold Font: {bold_font_path}")

        # Dictionary to cache loaded fonts
        self.font_cache = {}

        

    def load_font(self, font_path, font_size):
        # Load font from cache if available
        if (font_path, font_size) not in self.font_cache:
            print(f"Loading font from path: {font_path} with size: {font_size}")
            font = ImageFont.truetype(font_path, font_size)
            self.font_cache[(font_path, font_size)] = font
        return self.font_cache[(font_path, font_size)]
    

    def get_regular_font(self, font_size):
        return self.load_font(self.regular_font_path, font_size)

    def get_italic_font(self, font_size):
        return self.load_font(self.italic_font_path, font_size)

    def get_bold_font(self, font_size):
        return self.load_font(self.bold_font_path, font_size)

    def get_font_for_style(self, style, font_size):
        if style.get('b', False):
            # print(f"Selected Bold Font for style '{style}' with size: {font_size}")
            return self.get_bold_font(font_size)
        elif style.get('i', False):
            # print(f"Selected Italic Font for style '{style}' with size: {font_size}")
            return self.get_italic_font(font_size)
        else:
            # print(f"Selected Regular Font for style '{style}' with size: {font_size}")
            return self.get_regular_font(font_size)
