#!/usr/bin/env python3
"""
Debug the font sizing process to see what's happening.
"""

from utils.apz_markdown_parser import parse_markdown
from utils.apz_font_manager import FontManager
from utils.apz_text_wrapper import wrap_text

def debug_font_sizing():
    """Debug the font sizing process."""
    print("=== Debug Font Sizing ===")
    
    test_text = "Nuovo nome. Stessa missione. WiforAgri diventa 4Agri!"
    print(f"Input text: '{test_text}'")
    print()
    
    # Parse markdown
    parsed_parts = parse_markdown(test_text)
    print(f"Parsed parts: {len(parsed_parts)}")
    
    for i, (text_part, styles) in enumerate(parsed_parts):
        print(f"  Part {i}: '{text_part}' (styles: {styles})")
        print()
    
    # Test with different font sizes
    print("Testing with different font sizes:")
    
    # Initialize font manager with a realistic font
    font_manager = FontManager("Arial", "Arial", "Arial", 100)
    
    # Test with different font sizes
    font_sizes = [79, 60, 40, 30, 20]
    effective_textbox_width = 980
    effective_textbox_height = 1250  # 1350 - 2*50 padding
    line_height_ratio = 1.2
    
    for font_size in font_sizes:
        print(f"\nTesting font size: {font_size}")
        try:
            # Try to load font
            font = font_manager.get_regular_font(font_size)
            line_height = int(font_size * line_height_ratio)
            
            # Wrap text with current font size
            wrapped_lines, total_text_height = wrap_text(parsed_parts, font, 
                                                       effective_textbox_width, line_height, font_manager)
            
            print(f"  Wrapped lines: {len(wrapped_lines)}")
            print(f"  Total height: {total_text_height}")
            print(f"  Fits: {total_text_height <= effective_textbox_height}")
            
            # Show the wrapped lines
            for i, (line, line_parts) in enumerate(wrapped_lines):
                print(f"    Line {i}: '{line}'")
                print(f"      Parts: {len(line_parts)}")
                for j, (chunk, chunk_styles) in enumerate(line_parts):
                    print(f"        Part {j}: '{chunk}' (styles: {chunk_styles})")
            
            if total_text_height <= effective_textbox_height:
                print(f"  ✅ Font size {font_size} fits!")
                break
            else:
                print(f"  ❌ Font size {font_size} doesn't fit")
                
        except Exception as e:
            print(f"  Error with font size {font_size}: {e}")
            continue

if __name__ == "__main__":
    debug_font_sizing()
