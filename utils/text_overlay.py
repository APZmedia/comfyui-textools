from PIL import ImageDraw

def add_text_overlay(image, text, font_manager, position, font_color, alignment="center", max_width=None, line_height_ratio=1.2):
    """
    Adds a wrapped text overlay to the given PIL image.
    """
    draw = ImageDraw.Draw(image)
    font = font_manager.get_font()
    text_wrapper = TextWrapper(font_manager)

    # Wrap the text
    wrapped_lines, total_text_height = text_wrapper.wrap_text(text, max_width, font.size, line_height_ratio)

    # Calculate the starting Y position based on vertical alignment
    y = position[1]
    if alignment == "center":
        y = (image.height - total_text_height) // 2

    # Draw each line of text
    for line in wrapped_lines:
        text_width, text_height = draw.textsize(line, font=font)
        x = position[0]
        if alignment == "center":
            x = (image.width - text_width) // 2

        draw.text((x, y), line, fill=font_color, font=font)
        y += text_height * line_height_ratio

    return image
