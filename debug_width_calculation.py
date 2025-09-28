#!/usr/bin/env python3
"""
Debug the width calculation to see why text is breaking incorrectly.
"""

def debug_width_calculation():
    """Debug the width calculation."""
    print("=== Debug Width Calculation ===")
    
    test_text = "Nuovo nome. Stessa missione. WiforAgri diventa 4Agri!"
    words = test_text.split(' ')
    
    print(f"Text: '{test_text}'")
    print(f"Words: {words}")
    print()
    
    # Simulate realistic font width calculations
    # At font size 79, characters are roughly 50-60 pixels wide
    # Let's use realistic estimates based on character count
    max_width = 980  # 1080 - 2*50 padding
    
    print(f"Max width: {max_width}")
    print()
    
    current_line_width = 0
    lines = []
    current_line = []
    
    for i, word in enumerate(words):
        # Realistic width estimates for font size 79
        # Approximate: 50-60 pixels per character for most fonts at size 79
        word_width = len(word) * 55  # Conservative estimate
        
        # Calculate space width if there's a next word
        space_width = 0
        if i < len(words) - 1:
            space_width = 30  # Space is roughly 30 pixels at size 79
        
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

if __name__ == "__main__":
    debug_width_calculation()
