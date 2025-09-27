# rich_text_parser.py
import re
from .apz_hashtag_parser import parse_hashtags

def parse_rich_text(theText):
    """
    Parse rich text with HTML-like tags, hashtags, and emojis.
    Supports: <b>, <i>, <u>, <s> tags, #hashtags, and emojis
    """
    # First, handle hashtags
    hashtag_parts = parse_hashtags(theText)
    
    # Process each part for HTML-like tags
    final_parts = []
    for text_part, styles in hashtag_parts:
        if styles.get('hashtag', False):
            # Hashtags are already processed, add as-is
            final_parts.append((text_part, styles))
        else:
            # Process for HTML-like tags
            tag_re = re.compile(r'<(/?)(b|i|u|s)>')
            parts = []
            current_pos = 0
            current_styles = styles.copy()
            style_stack = []

            for match in tag_re.finditer(text_part):
                start, end = match.span()
                tag_type, tag_name = match.groups()

                if start > current_pos:
                    parts.append((text_part[current_pos:start], current_styles.copy()))

                if tag_type == '':
                    style_stack.append(current_styles.copy())
                    current_styles[tag_name] = True
                else:
                    if style_stack:
                        current_styles = style_stack.pop()

                current_pos = end

            if current_pos < len(text_part):
                parts.append((text_part[current_pos:], current_styles.copy()))

            if not parts:
                parts.append((text_part, current_styles.copy()))
            
            final_parts.extend(parts)
    
    return final_parts
