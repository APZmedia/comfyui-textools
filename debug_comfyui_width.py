#!/usr/bin/env python3
"""
Debug script to test with ComfyUI interface dimensions.
"""

from utils.apz_markdown_parser import parse_markdown
from utils.apz_text_wrapper import wrap_text
from PIL import ImageFont

def debug_comfyui_dimensions():
    """Debug with ComfyUI interface dimensions."""
    print("=== Debug ComfyUI Interface Dimensions ===")
    
    # ComfyUI interface dimensions
    theTextbox_width = 1080
    padding = 50
    effective_width = theTextbox_width - 2 * padding  # 980px
    
    print(f"Text box width: {theTextbox_width}px")
    print(f"Padding: {padding}px")
    print(f"Effective width: {effective_width}px")
    
    # Test text
    text_with_emoji = "Hello **World** *This is italic* with #hashtags and 😀 emojis"
    text_without_emoji = "Hello **World** *This is italic* with #hashtags and emojis"
    
    # Parse both texts
    parsed_with_emoji = parse_markdown(text_with_emoji)
    parsed_without_emoji = parse_markdown(text_without_emoji)
    
    # Test font loading (using default font size 100 from interface)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    print(f"\nFont size: 100")
    
    # Test wrapping with ComfyUI dimensions
    print(f"\n--- Testing with ComfyUI effective width: {effective_width}px ---")
    
    # Test with emoji
    wrapped_with_emoji, height_with_emoji = wrap_text(parsed_with_emoji, font, effective_width, 120)
    print(f"With emoji: {len(wrapped_with_emoji)} lines, height: {height_with_emoji}px")
    for i, (line, parts) in enumerate(wrapped_with_emoji):
        print(f"  Line {i}: '{line}'")
    
    # Test without emoji
    wrapped_without_emoji, height_without_emoji = wrap_text(parsed_without_emoji, font, effective_width, 120)
    print(f"Without emoji: {len(wrapped_without_emoji)} lines, height: {height_without_emoji}px")
    for i, (line, parts) in enumerate(wrapped_without_emoji):
        print(f"  Line {i}: '{line}'")
    
    # Check if the issue is with the emoji width calculation
    print(f"\n--- Emoji Width Analysis ---")
    emoji_text = "😀"
    emoji_bbox = font.getbbox(emoji_text)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    print(f"Emoji '{emoji_text}' width: {emoji_width}px")
    
    # Test if the emoji is causing the line to exceed the width
    test_line = "and 😀 emojis"
    line_bbox = font.getbbox(test_line)
    line_width = line_bbox[2] - line_bbox[0]
    print(f"Line '{test_line}' width: {line_width}px")
    print(f"Fits in {effective_width}px? {line_width <= effective_width}")

if __name__ == "__main__":
    debug_comfyui_dimensions()
