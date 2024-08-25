def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.
    """
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
