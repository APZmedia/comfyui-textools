# text_wrapper.py
def wrap_text(parsed_text, font, max_width, line_height):
    wrapped_lines = []
    current_line = ""
    line_parts = []

    for text, styles in parsed_text:
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
                    w = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]

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
                w = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]

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
