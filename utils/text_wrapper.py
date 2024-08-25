class TextWrapper:
    def __init__(self, font_manager):
        self.font_manager = font_manager

    def wrap_text(self, parsed_text, apz_max_width, line_height, font_size):
        wrapped_lines, current_line, line_parts = [], "", []

        for text, styles in parsed_text:
            words = text.split(' ')
            for word in words:
                current_line, line_parts = self._handle_word_wrap(current_line, line_parts, word, styles, apz_max_width, font_size)

            if text.endswith(' '):
                current_line += ' '
                line_parts.append((' ', styles))

        if current_line:
            wrapped_lines.append((current_line, line_parts))

        total_height = len(wrapped_lines) * line_height
        return wrapped_lines, total_height

    def _handle_word_wrap(self, current_line, line_parts, word, styles, apz_max_width, font_size):
        font = self.font_manager.get_font_for_style(styles, font_size)
        subwords = word.split('\n')
        for subword in subwords:
            test_line = f"{current_line} {subword}".strip()
            if font.getbbox(test_line)[2] - font.getbbox(test_line)[0] <= apz_max_width:
                current_line = test_line
                line_parts.append((subword, styles))
            else:
                return current_line, line_parts

        return current_line, line_parts
