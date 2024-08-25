import re

class RichTextParser:
    def __init__(self):
        self.tag_re = re.compile(r'<(/?)(b|i|u|s)>')

    def parse(self, text):
        parts, current_pos, styles, style_stack = [], 0, {'b': False, 'i': False, 'u': False, 's': False}, []

        for match in self.tag_re.finditer(text):
            start, end = match.span()
            tag_type, tag_name = match.groups()

            if start > current_pos:
                parts.append((text[current_pos:start], styles.copy()))

            if tag_type == '':
                style_stack.append(styles.copy())
                styles[tag_name] = True
            else:
                if style_stack:
                    styles = style_stack.pop()

            current_pos = end

        if current_pos < len(text):
            parts.append((text[current_pos:], styles.copy()))

        if not parts:
            parts.append((text, styles.copy()))

        return parts
