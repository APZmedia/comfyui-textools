#!/usr/bin/env python3
"""
Debug the specific line breaking issue.
"""

from utils.apz_markdown_parser import parse_markdown
from utils.apz_font_manager import FontManager

def debug_line_breaking():
    """Debug the line breaking issue."""
    print("=== Debug Line Breaking ===")
    
    test_text = "Nuovo nome. Stessa missione. WiforAgri diventa 4Agri!"
    print(f"Input text: '{test_text}'")
    print()
    
    # Initialize font manager
    font_manager = FontManager("Arial", "Arial", "Arial", 100)
    
    # Parse markdown
    parsed_parts = parse_markdown(test_text)
    print(f"Parsed parts: {len(parsed_parts)}")
    
    for i, (text_part, styles) in enumerate(parsed_parts):
        print(f"  Part {i}: '{text_part}' (styles: {styles})")
        print(f"    Length: {len(text_part)}")
        print(f"    Words: {text_part.split(' ')}")
        print()
    
    # Test the renderer logic with a specific width
    print("Testing renderer logic with width 500:")
    from utils.apz_markdown_renderer_utility import MarkdownRendererUtility
    
    try:
        lines = MarkdownRendererUtility._process_parsed_parts(
            parsed_parts, 500, font_manager, 20
        )
        print(f"Rendered lines: {len(lines)}")
        
        for i, line in enumerate(lines):
            print(f"  Line {i}: {len(line)} chunks")
            for j, (chunk, chunk_styles) in enumerate(line):
                print(f"    Chunk {j}: '{chunk}' (styles: {chunk_styles})")
                
    except Exception as e:
        print(f"Error in rendering: {e}")

if __name__ == "__main__":
    debug_line_breaking()
