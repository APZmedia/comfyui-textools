# text_wrapper.py
def _get_word_width(word, font, font_manager=None):
    """Get the width of a word, handling emojis correctly."""
    # For all text (including emojis), use normal font metrics
    # The PNG rendering will happen in the final renderer
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
                # Calculate word width
                word_width = _get_word_width(word, font, font_manager)
                
                # Calculate space width if there's a next word
                space_width = 0
                if i < len(words) - 1:
                    space_width = _get_word_width(' ', font, font_manager)
                
                # Check if word AND space fit on current line
                current_line_width = _get_word_width(current_line, font, font_manager) if current_line else 0
                if current_line_width + word_width + space_width <= max_width:
                    # Word and space fit, add word to current line
                    if current_line:
                        current_line += ' ' + word
                    else:
                        current_line = word
                    line_parts.append((word, styles))
                    
                    # Add space if there's a next word
                    if i < len(words) - 1:
                        line_parts.append((' ', styles))
                else:
                    # Word doesn't fit, start new line
                    if current_line:
                        wrapped_lines.append((current_line, line_parts))
                    current_line = word
                    line_parts = [(word, styles)]
                    
                    # Add space if there's a next word
                    if i < len(words) - 1:
                        line_parts.append((' ', styles))

        if text.endswith(' '):
            current_line += ' '
            line_parts.append((' ', styles))

    if current_line:
        wrapped_lines.append((current_line, line_parts))

    total_height = len(wrapped_lines) * line_height
    return wrapped_lines, total_height
