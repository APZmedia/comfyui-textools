# text_wrapper.py
def _get_word_width(word, font, font_manager=None):
    """Get the width of a word, handling emojis correctly."""
    if not word:
        return 0

    base_font_size = getattr(font, "size", None)
    if base_font_size is None:
        try:
            base_font_size = font.font.size  # type: ignore[attr-defined]
        except Exception:
            base_font_size = 16

    # For spaces, use a simple and consistent measurement
    if word == ' ':
        try:
            if font_manager:
                measure_font = font_manager.get_font_for_style({}, base_font_size, word)
                bbox = measure_font.getbbox(word)
                space_width = bbox[2] - bbox[0]
                # Ensure space width is reasonable and consistent
                return max(space_width, 2)  # Minimum 2px for space
            else:
                bbox = font.getbbox(word)
                space_width = bbox[2] - bbox[0]
                return max(space_width, 2)  # Minimum 2px for space
        except Exception:
            # Fallback for space width
            return max(base_font_size // 4, 2)  # Minimum 2px

    if font_manager:
        emoji_support = getattr(font_manager, "emoji_support", None)
        if emoji_support and emoji_support.has_emoji(word):
            total_width = 0
            for segment, is_emoji in emoji_support.split_text_by_emoji(word):
                if not segment:
                    continue
                if is_emoji:
                    # Use the helper function to ensure consistency with rendering
                    from .apz_emoji_png_renderer import EmojiPNGRenderer
                    from .apz_text_renderer_utility import TextRendererUtility
                    emoji_png_renderer = EmojiPNGRenderer()
                    emoji_width = TextRendererUtility._get_emoji_rendered_width(segment, base_font_size, emoji_png_renderer)
                    total_width += emoji_width
                else:
                    try:
                        measure_font = font_manager.get_font_for_style({}, base_font_size, segment)
                        bbox = measure_font.getbbox(segment)
                        total_width += bbox[2] - bbox[0]
                    except Exception:
                        bbox = font.getbbox(segment)
                        total_width += bbox[2] - bbox[0]
            if total_width > 0:
                return total_width

    bbox = font.getbbox(word)
    return bbox[2] - bbox[0]


def _clone_styles(styles):
    return styles.copy() if isinstance(styles, dict) else {}
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
                            line_parts.append((subword, _clone_styles(styles)))
                        if i < len(words) - 1 or j < len(subwords) - 1:
                            line_parts.append((' ', _clone_styles(styles)))
                    else:
                        wrapped_lines.append((current_line, line_parts))
                        current_line = subword
                        line_parts = [(subword, _clone_styles(styles))]
                        if i < len(words) - 1 or j < len(subwords) - 1:
                            line_parts.append((' ', _clone_styles(styles)))
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
                    line_parts.append((word, _clone_styles(styles)))
                    
                    # Add space if there's a next word
                    if i < len(words) - 1:
                        line_parts.append((' ', _clone_styles(styles)))
                else:
                    # Word doesn't fit, start new line
                    if current_line:
                        wrapped_lines.append((current_line, line_parts))
                    current_line = word
                    line_parts = [(word, _clone_styles(styles))]
                    
                    # Add space if there's a next word
                    if i < len(words) - 1:
                        line_parts.append((' ', _clone_styles(styles)))

        if text.endswith(' '):
            current_line += ' '
            line_parts.append((' ', _clone_styles(styles)))

    if current_line:
        wrapped_lines.append((current_line, line_parts))

    total_height = len(wrapped_lines) * line_height
    return wrapped_lines, total_height
