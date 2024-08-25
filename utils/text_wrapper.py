from PIL import ImageFont

class TextWrapper:
    def __init__(self, font_manager):
        self.font_manager = font_manager

    def wrap_text(self, text, max_width, font_size, line_height_ratio=1.2):
        """
        Wraps the text to fit within the specified width.
        Returns the wrapped lines and total height of the text block.
        """
        font = self.font_manager.get_font()
        lines = []
        words = text.split()

        current_line = []
        current_width = 0
        total_text_height = 0

        for word in words:
            word_width, _ = font.getsize(word + ' ')
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                total_text_height += int(font_size * line_height_ratio)
                current_line = [word]
                current_width = word_width

        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
            total_text_height += int(font_size * line_height_ratio)

        return lines, total_text_height
