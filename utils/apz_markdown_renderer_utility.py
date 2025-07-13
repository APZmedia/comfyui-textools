# markdown_renderer_utility.py
from PIL import ImageDraw
from .apz_font_manager import FontManager
from .apz_color_utility import ColorUtility
from .apz_markdown_parser import parse_markdown, parse_markdown_with_headers, parse_markdown_extended

class MarkdownRendererUtility:
    """
    Utility class for rendering markdown text with proper styling and layout.
    """
    
    @staticmethod
    def render_markdown_text(draw, text, markdown_mode, box_left, box_top, padding, 
                           box_width, box_height, font_manager, color_utility, 
                           alignment, vertical_alignment, line_height_ratio,
                           font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, 
                           font_size):
        """
        Render markdown text with proper styling and layout.
        
        Args:
            draw: PIL ImageDraw object
            text: Markdown text to render
            markdown_mode: Mode of markdown parsing ("basic", "with_headers", "extended")
            box_left, box_top: Top-left corner of text box
            padding: Internal padding
            box_width, box_height: Dimensions of text box
            font_manager: FontManager instance
            color_utility: ColorUtility instance
            alignment: Horizontal alignment ("left", "center", "right")
            vertical_alignment: Vertical alignment ("top", "middle", "bottom")
            line_height_ratio: Line height multiplier
            font_color_rgb, italic_font_color_rgb, bold_font_color_rgb: Color tuples
            font_size: Base font size
        """
        # Parse markdown based on mode
        if markdown_mode == "basic":
            parsed_parts = parse_markdown(text)
        elif markdown_mode == "with_headers":
            parsed_parts = parse_markdown_with_headers(text)
        elif markdown_mode == "extended":
            parsed_parts = parse_markdown_extended(text)
        else:
            parsed_parts = parse_markdown(text)
        
        # Process parsed parts into renderable lines
        renderable_lines = MarkdownRendererUtility._process_parsed_parts(
            parsed_parts, box_width - 2 * padding, font_manager, font_size
        )
        
        # Calculate total height needed
        line_height = font_size * line_height_ratio
        total_height = len(renderable_lines) * line_height
        
        # Calculate starting Y position based on vertical alignment
        if vertical_alignment == "middle":
            start_y = box_top + (box_height - total_height) // 2
        elif vertical_alignment == "bottom":
            start_y = box_top + box_height - total_height - padding
        else:  # top
            start_y = box_top + padding
        
        # Render each line
        current_y = start_y
        for line in renderable_lines:
            if current_y + line_height > box_top + box_height - padding:
                break  # Stop if we exceed box height
                
            MarkdownRendererUtility._render_line(
                draw, line, box_left, current_y, padding, box_width,
                font_manager, color_utility, alignment, font_size,
                font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
            )
            current_y += line_height
    
    @staticmethod
    def _process_parsed_parts(parsed_parts, max_width, font_manager, font_size):
        """
        Process parsed markdown parts into renderable lines with proper wrapping.
        
        Args:
            parsed_parts: List of (text, styles) tuples from markdown parser
            max_width: Maximum width for text wrapping
            font_manager: FontManager instance
            font_size: Base font size
            
        Returns:
            List of renderable lines, where each line is a list of (text, styles) tuples
        """
        lines = []
        current_line = []
        current_line_width = 0
        
        for text_part, styles in parsed_parts:
            # Split text into words for wrapping
            words = text_part.split()
            
            for word in words:
                # Get font for this word
                font = font_manager.get_font_for_style(styles, font_size)
                
                # Calculate word width (add space if not first word in line)
                word_with_space = f" {word}" if current_line else word
                bbox = font.getbbox(word_with_space)
                word_width = bbox[2] - bbox[0]
                
                # Check if word fits on current line
                if current_line_width + word_width <= max_width:
                    # Add word to current line
                    current_line.append((word, styles))
                    current_line_width += word_width
                else:
                    # Start new line
                    if current_line:
                        lines.append(current_line)
                    current_line = [(word, styles)]
                    current_line_width = font.getbbox(word)[2] - font.getbbox(word)[0]
        
        # Add the last line
        if current_line:
            lines.append(current_line)
        
        return lines
    
    @staticmethod
    def _render_line(draw, line, box_left, y, padding, box_width, font_manager, 
                    color_utility, alignment, font_size, font_color_rgb, 
                    italic_font_color_rgb, bold_font_color_rgb):
        """
        Render a single line of markdown text.
        
        Args:
            draw: PIL ImageDraw object
            line: List of (text, styles) tuples for this line
            box_left, y: Position to render the line
            padding: Internal padding
            box_width: Width of text box
            font_manager: FontManager instance
            color_utility: ColorUtility instance
            alignment: Horizontal alignment
            font_size: Base font size
            font_color_rgb, italic_font_color_rgb, bold_font_color_rgb: Color tuples
        """
        # Calculate total line width
        total_line_width = 0
        for text_part, styles in line:
            font = font_manager.get_font_for_style(styles, font_size)
            bbox = font.getbbox(text_part)
            total_line_width += bbox[2] - bbox[0]
        
        # Calculate starting X position based on alignment
        if alignment == "center":
            x = box_left + (box_width - total_line_width) // 2
        elif alignment == "right":
            x = box_left + box_width - total_line_width - padding
        else:  # left
            x = box_left + padding
        
        # Render each text part in the line
        current_x = x
        for text_part, styles in line:
            # Get font and color for this text part
            font = font_manager.get_font_for_style(styles, font_size)
            
            if styles.get('b', False):
                color = bold_font_color_rgb
            elif styles.get('i', False):
                color = italic_font_color_rgb
            else:
                color = font_color_rgb
            
            # Draw the text
            draw.text((current_x, y), text_part, font=font, fill=color)
            
            # Move to next position
            bbox = font.getbbox(text_part)
            current_x += bbox[2] - bbox[0]
    
    @staticmethod
    def calculate_markdown_text_dimensions(text, markdown_mode, font_manager, 
                                         font_size, line_height_ratio, max_width=None):
        """
        Calculate the dimensions needed to render markdown text.
        
        Args:
            text: Markdown text to measure
            markdown_mode: Mode of markdown parsing
            font_manager: FontManager instance
            font_size: Base font size
            line_height_ratio: Line height multiplier
            max_width: Maximum width for wrapping (None for no wrapping)
            
        Returns:
            Tuple of (width, height) in pixels
        """
        # Parse markdown
        if markdown_mode == "basic":
            parsed_parts = parse_markdown(text)
        elif markdown_mode == "with_headers":
            parsed_parts = parse_markdown_with_headers(text)
        elif markdown_mode == "extended":
            parsed_parts = parse_markdown_extended(text)
        else:
            parsed_parts = parse_markdown(text)
        
        # Process into lines
        if max_width:
            lines = MarkdownRendererUtility._process_parsed_parts(
                parsed_parts, max_width, font_manager, font_size
            )
        else:
            # No wrapping - treat as single line
            lines = [parsed_parts]
        
        # Calculate dimensions
        line_height = font_size * line_height_ratio
        height = len(lines) * line_height
        
        # Calculate maximum line width
        max_line_width = 0
        for line in lines:
            line_width = 0
            for text_part, styles in line:
                font = font_manager.get_font_for_style(styles, font_size)
                bbox = font.getbbox(text_part)
                line_width += bbox[2] - bbox[0]
            max_line_width = max(max_line_width, line_width)
        
        return max_line_width, height 