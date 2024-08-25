# color_utility.py

class ColorUtility:
    @staticmethod
    def hex_to_rgb(hex_color):
        return tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def get_font_color(chunk_styles, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if chunk_styles.get('b', False):
            return bold_font_color_rgb
        elif chunk_styles.get('i', False):
            return italic_font_color_rgb
        else:
            return font_color_rgb
