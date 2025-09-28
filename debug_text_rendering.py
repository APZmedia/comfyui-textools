#!/usr/bin/env python3
"""
Debug script to test text rendering and see why the last line is missing.
"""

from utils.apz_markdown_parser import parse_markdown
from utils.apz_text_wrapper import wrap_text
from utils.apz_font_manager import FontManager
from PIL import Image, ImageDraw, ImageFont

def debug_text_rendering():
    """Debug the text rendering issue."""
    print("=== Debug Text Rendering ===")
    
    # Test text from the ComfyUI interface
    test_text = "Hello **World** *This is italic* with #hashtags and 😀 emojis"
    print(f"Input text: '{test_text}'")
    print(f"Text length: {len(test_text)}")
    
    # Parse markdown
    parsed_parts = parse_markdown(test_text)
    print(f"\nParsed parts ({len(parsed_parts)}):")
    for i, (text, styles) in enumerate(parsed_parts):
        print(f"  {i}: '{text}' -> {styles}")
    
    # Test font loading
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    # Test text wrapping
    max_width = 1000  # Reasonable width
    line_height = 60
    
    wrapped_lines, total_height = wrap_text(parsed_parts, font, max_width, line_height)
    print(f"\nWrapped lines ({len(wrapped_lines)}):")
    for i, (line_text, line_parts) in enumerate(wrapped_lines):
        print(f"  Line {i}: '{line_text}' ({len(line_parts)} parts)")
        for j, (chunk, styles) in enumerate(line_parts):
            print(f"    Part {j}: '{chunk}' -> {styles}")
    
    print(f"\nTotal height: {total_height}")
    
    # Test if the issue is with the last line
    if wrapped_lines:
        last_line = wrapped_lines[-1]
        print(f"\nLast line: '{last_line[0]}'")
        print(f"Last line parts: {last_line[1]}")

if __name__ == "__main__":
    debug_text_rendering()
