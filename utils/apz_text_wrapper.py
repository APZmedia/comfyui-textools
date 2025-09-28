# text_wrapper.py
def _get_word_width(word, font, font_manager=None):
    """Get the width of a word, handling emojis correctly."""
    if font_manager and font_manager.emoji_support.has_emoji(word):
        # For emojis, use the font size as width (since we're using PNG emojis)
        return font.getbbox('M')[2] - font.getbbox('M')[0]  # Use 'M' as reference
    else:
        # For regular text, use normal font metrics
        return font.getbbox(word)[2] - font.getbbox(word)[0]

def wrap_text(parsed_text, font, max_width, line_height, font_manager=None):
    wrapped_lines = []
    current_line = ""
    line_parts = []

    for text, styles in parsed_text:
        # Split by spaces but preserve the spaces
        words = text.split(' ')
        for i, word in enumerate(words):
            if '\n' in word:
                subwords = word.split('\n')
                for j, subword in enumerate(subwords):
                    if j > 0:
                        wrapped_lines.append((current_line, line_parts))
                        current_line = ""
                        line_parts = []
                    if current_line:
                        test_line = current_line + ' ' + subword
                    else:
                        test_line = subword
                    w = _get_word_width(test_line, font, font_manager)

                    if w <= max_width:
                        current_line = test_line
                        if current_line.strip():
                            line_parts.append((subword, styles))
                        if i < len(words) - 1 or j < len(subwords) - 1:
                            line_parts.append((' ', styles))
                    else:
                        wrapped_lines.append((current_line, line_parts))
                        current_line = subword
                        line_parts = [(subword, styles)]
                        if i < len(words) - 1 or j < len(subwords) - 1:
                            line_parts.append((' ', styles))
            else:
                if current_line:
                    test_line = current_line + ' ' + word
                else:
                    test_line = word
                w = _get_word_width(test_line, font, font_manager)

                if w <= max_width:
                    current_line = test_line
                    if current_line.strip():
                        line_parts.append((word, styles))
                    if i < len(words) - 1:
                        line_parts.append((' ', styles))
                else:
                    wrapped_lines.append((current_line, line_parts))
                    current_line = word
                    line_parts = [(word, styles)]
                    if i < len(words) - 1:
                        line_parts.append((' ', styles))

        if text.endswith(' '):
            current_line += ' '
            line_parts.append((' ', styles))

    if current_line:
        wrapped_lines.append((current_line, line_parts))

    total_height = len(wrapped_lines) * line_height
    return wrapped_lines, total_height
