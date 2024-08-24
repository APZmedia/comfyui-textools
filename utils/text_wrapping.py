# rich_text_overlay/utils/text_wrapping.py

def wrap_text_and_calculate_height(parsed_text, font, max_width, line_height):
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
