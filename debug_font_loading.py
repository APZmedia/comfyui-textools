#!/usr/bin/env python3
"""
Debug font loading to see if the issue is with font loading.
"""

from PIL import ImageFont
import os

def debug_font_loading():
    """Debug font loading."""
    print("=== Debug Font Loading ===")
    
    # Try to load a system font
    try:
        # Try to load a system font
        font = ImageFont.load_default()
        print(f"Default font loaded: {font}")
        
        # Test text width calculation
        test_text = "Nuovo nome. Stessa missione. WiforAgri diventa 4Agri!"
        words = test_text.split(' ')
        
        print(f"Text: '{test_text}'")
        print(f"Words: {words}")
        print()
        
        max_width = 980
        current_line_width = 0
        lines = []
        current_line = []
        
        for i, word in enumerate(words):
            # Calculate word width using the actual font
            bbox = font.getbbox(word)
            word_width = bbox[2] - bbox[0]
            
            # Calculate space width if there's a next word
            space_width = 0
            if i < len(words) - 1:
                space_bbox = font.getbbox(' ')
                space_width = space_bbox[2] - space_bbox[0]
            
            print(f"Word {i}: '{word}' (width: {word_width}, space: {space_width})")
            print(f"  Current line width: {current_line_width}")
            print(f"  Total needed: {current_line_width + word_width + space_width}")
            print(f"  Fits: {current_line_width + word_width + space_width <= max_width}")
            
            # Check if word AND space fit on current line
            if current_line_width + word_width + space_width <= max_width:
                # Word and space fit, add word to current line
                current_line.append(word)
                current_line_width += word_width
                print(f"  -> Added to current line")
                
                # Add space if there's a next word
                if i < len(words) - 1:
                    current_line.append(' ')
                    current_line_width += space_width
                    print(f"  -> Added space")
            else:
                # Word doesn't fit, start new line
                if current_line:
                    lines.append(current_line)
                    print(f"  -> Started new line (previous line: {current_line})")
                current_line = [word]
                current_line_width = word_width
                print(f"  -> New line with word: {current_line}")
                
                # Add space if there's a next word
                if i < len(words) - 1:
                    current_line.append(' ')
                    current_line_width += space_width
                    print(f"  -> Added space to new line")
            
            print()
        
        # Add the last line
        if current_line:
            lines.append(current_line)
        
        print("Final lines:")
        for i, line in enumerate(lines):
            line_text = ' '.join(line)
            print(f"  Line {i}: '{line_text}'")
            print(f"    Length: {len(line_text)}")
            print(f"    Chunks: {len(line)}")
            
    except Exception as e:
        print(f"Error loading font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_font_loading()
