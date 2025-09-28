#!/usr/bin/env python3
"""
Debug script to check text box dimensions and positioning.
"""

def debug_dimensions():
    """Debug the text box dimensions issue."""
    print("=== Debug Text Box Dimensions ===")
    
    # Parameters from ComfyUI interface
    theTextbox_width = 1080
    theTextbox_height = 1350
    padding = 50
    font_size = 100
    line_height_ratio = 1.2
    
    print(f"Text box dimensions: {theTextbox_width} x {theTextbox_height}")
    print(f"Padding: {padding}")
    print(f"Font size: {font_size}")
    print(f"Line height ratio: {line_height_ratio}")
    
    # Calculate effective dimensions
    effective_width = theTextbox_width - 2 * padding
    effective_height = theTextbox_height - 2 * padding
    
    print(f"Effective dimensions: {effective_width} x {effective_height}")
    
    # Calculate line height
    line_height = int(font_size * line_height_ratio)
    print(f"Line height: {line_height}")
    
    # Calculate how many lines can fit
    max_lines = effective_height // line_height
    print(f"Maximum lines that can fit: {max_lines}")
    
    # Check if 2 lines can fit
    total_height_for_2_lines = 2 * line_height
    print(f"Total height for 2 lines: {total_height_for_2_lines}")
    print(f"Can fit 2 lines? {total_height_for_2_lines <= effective_height}")
    
    # Check vertical positioning for middle alignment
    if total_height_for_2_lines <= effective_height:
        # Calculate Y position for middle alignment
        start_y = padding + (effective_height - total_height_for_2_lines) // 2
        line1_y = start_y
        line2_y = start_y + line_height
        
        print(f"Middle alignment:")
        print(f"  Start Y: {start_y}")
        print(f"  Line 1 Y: {line1_y}")
        print(f"  Line 2 Y: {line2_y}")
        print(f"  Line 2 bottom: {line2_y + font_size}")
        print(f"  Text box bottom: {theTextbox_height}")
        print(f"  Line 2 fits? {line2_y + font_size <= theTextbox_height}")
    else:
        print("ERROR: Not enough space for 2 lines!")

if __name__ == "__main__":
    debug_dimensions()
