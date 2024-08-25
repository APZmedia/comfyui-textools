# rich_text_parser.py
import re

def parse_rich_text(theText):
    tag_re = re.compile(r'<(/?)(b|i|u|s)>')
    parts = []
    current_pos = 0
    styles = {'b': False, 'i': False, 'u': False, 's': False}
    style_stack = []

    for match in tag_re.finditer(theText):
        start, end = match.span()
        tag_type, tag_name = match.groups()

        if start > current_pos:
            parts.append((theText[current_pos:start], styles.copy()))

        if tag_type == '':
            style_stack.append(styles.copy())
            styles[tag_name] = True
        else:
            if style_stack:
                styles = style_stack.pop()

        current_pos = end

    if current_pos < len(theText):
        parts.append((theText[current_pos:], styles.copy()))

    if not parts:
        parts.append((theText, styles.copy()))

    return parts
