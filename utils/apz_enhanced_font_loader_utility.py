# enhanced_font_loader_utility.py

from .apz_rich_text_parser import parse_rich_text
from .apz_markdown_parser import parse_markdown, parse_markdown_with_headers, parse_markdown_extended
from .apz_text_wrapper import wrap_text
from .apz_markdown_renderer_utility import MarkdownRendererUtility
import logging

class EnhancedFontLoaderUtility:
    """
    Enhanced font loader utility with comprehensive fallback error handling.
    Handles cases where font sizes are too large or words don't fit in wrapping boxes.
    """
    
    def __init__(self, font_manager, max_font_size):
        self.font_manager = font_manager
        self.max_font_size = max_font_size
        self.min_font_size = 6  # Minimum readable font size
        self.logger = logging.getLogger(__name__)

    def find_fitting_font_size(self, theText, effective_textbox_width, effective_textbox_height, 
                              line_height_ratio, text_type="rich_text"):
        """
        Find the largest font size that fits the text in the specified dimensions.
        Includes comprehensive fallback handling for edge cases.
        
        Args:
            theText: Text to fit
            effective_textbox_width: Available width for text
            effective_textbox_height: Available height for text
            line_height_ratio: Line height multiplier
            text_type: Type of text ("rich_text", "markdown_basic", "markdown_headers", "markdown_extended")
            
        Returns:
            Tuple of (font_size, wrapped_lines, total_text_height, warnings)
        """
        warnings = []
        
        # Validate input parameters
        if effective_textbox_width <= 0 or effective_textbox_height <= 0:
            warnings.append("Invalid text box dimensions")
            return self._get_fallback_result(warnings)
        
        if not theText or not theText.strip():
            warnings.append("Empty text provided")
            return self._get_fallback_result(warnings)
        
        # Parse text based on type
        try:
            if text_type == "rich_text":
                parsed_text = parse_rich_text(theText)
            elif text_type == "markdown_basic":
                parsed_text = parse_markdown(theText)
            elif text_type == "markdown_headers":
                parsed_text = parse_markdown_with_headers(theText)
            elif text_type == "markdown_extended":
                parsed_text = parse_markdown_extended(theText)
            else:
                parsed_text = parse_rich_text(theText)  # Default fallback
        except Exception as e:
            warnings.append(f"Text parsing failed: {str(e)}")
            return self._get_fallback_result(warnings)
        
        # Check for extremely long words that might not fit even at minimum font size
        longest_word = self._find_longest_word(parsed_text)
        if longest_word:
            min_font = self.font_manager.get_regular_font(self.min_font_size)
            longest_word_width = min_font.getbbox(longest_word)[2] - min_font.getbbox(longest_word)[0]
            if longest_word_width > effective_textbox_width:
                warnings.append(f"Word '{longest_word}' is too long to fit even at minimum font size")
                return self._get_fallback_result(warnings, longest_word)
        
        # Try to find fitting font size with aggressive scaling
        font_size = self.max_font_size
        while font_size >= self.min_font_size:
            try:
                # Use regular font as a baseline for size fitting
                loaded_font = self.font_manager.get_regular_font(font_size)
                line_height = int(font_size * line_height_ratio)
                
                # Wrap text with current font size
                wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, 
                                                           effective_textbox_width, line_height, self.font_manager)
                
                # Attach font size to the style dictionary in wrapped_lines
                for line, line_parts in wrapped_lines:
                    for chunk, chunk_styles in line_parts:
                        chunk_styles['size'] = font_size

                # Compute render lines with markdown renderer to account for preserved newlines
                if text_type.startswith("markdown"):
                    render_lines = MarkdownRendererUtility._process_parsed_parts(
                        parse_markdown(theText) if text_type == "markdown_basic"
                        else parse_markdown_with_headers(theText) if text_type == "markdown_headers"
                        else parse_markdown_extended(theText),
                        effective_textbox_width,
                        self.font_manager,
                        font_size,
                    )
                else:
                    render_lines = []
                    for aggregated_line, aggregated_parts in wrapped_lines:
                        render_lines.append(aggregated_parts)

                logical_line_count = len(render_lines)
                total_text_height = logical_line_count * line_height
                
                # Check if text fits
                if total_text_height <= effective_textbox_height:
                    # Check if any individual words are too wide
                    word_warnings = self._check_word_widths(render_lines, font_size, effective_textbox_width)
                    warnings.extend(word_warnings)
                    
                    return font_size, wrapped_lines, total_text_height, warnings
                    
            except Exception as e:
                import traceback
                warnings.append(f"Error at font size {font_size}: {str(e)}")
                # # Debug logging removed for performance  # Uncomment for debugging
                font_size -= 1
                continue
                
            font_size -= 1
        
        # If we get here, no font size worked - try aggressive scaling
        return self._try_aggressive_scaling(theText, effective_textbox_width, effective_textbox_height, 
                                          line_height_ratio, text_type, warnings)
    
    def _try_aggressive_scaling(self, theText, effective_textbox_width, effective_textbox_height, 
                               line_height_ratio, text_type, warnings):
        """
        Try aggressive font scaling when normal scaling fails.
        This includes text truncation and very small font sizes.
        """
        warnings.append("Normal font scaling failed, trying aggressive scaling")
        
        # Try with very small font sizes (below minimum)
        for font_size in range(self.min_font_size - 1, 2, -1):
            try:
                # Parse text again
                if text_type == "rich_text":
                    parsed_text = parse_rich_text(theText)
                elif text_type == "markdown_basic":
                    parsed_text = parse_markdown(theText)
                elif text_type == "markdown_headers":
                    parsed_text = parse_markdown_with_headers(theText)
                elif text_type == "markdown_extended":
                    parsed_text = parse_markdown_extended(theText)
                else:
                    parsed_text = parse_rich_text(theText)
                
                loaded_font = self.font_manager.get_regular_font(font_size)
                line_height = int(font_size * line_height_ratio)
                
                wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, 
                                                           effective_textbox_width, line_height, self.font_manager)
                
                # Attach font size
                for line, line_parts in wrapped_lines:
                    for chunk, chunk_styles in line_parts:
                        chunk_styles['size'] = font_size
                
                if total_text_height <= effective_textbox_height:
                    warnings.append(f"Text fits with aggressive scaling at font size {font_size}")
                    return font_size, wrapped_lines, total_text_height, warnings
                    
            except Exception as e:
                continue
        
        # If aggressive scaling fails, try text truncation
        return self._try_text_truncation(theText, effective_textbox_width, effective_textbox_height, 
                                        line_height_ratio, text_type, warnings)
    
    def _try_text_truncation(self, theText, effective_textbox_width, effective_textbox_height, 
                            line_height_ratio, text_type, warnings):
        """
        Try text truncation when all scaling methods fail.
        """
        warnings.append("All scaling methods failed, trying text truncation")
        
        # Try different truncation strategies
        truncation_strategies = [
            (theText[:100] + "..." if len(theText) > 100 else theText, "truncated to 100 chars"),
            (theText[:50] + "..." if len(theText) > 50 else theText, "truncated to 50 chars"),
            (theText[:25] + "..." if len(theText) > 25 else theText, "truncated to 25 chars"),
            ("Text overflow", "replaced with error message")
        ]
        
        for truncated_text, strategy in truncation_strategies:
            try:
                # Parse truncated text
                if text_type == "rich_text":
                    parsed_text = parse_rich_text(truncated_text)
                elif text_type == "markdown_basic":
                    parsed_text = parse_markdown(truncated_text)
                elif text_type == "markdown_headers":
                    parsed_text = parse_markdown_with_headers(truncated_text)
                elif text_type == "markdown_extended":
                    parsed_text = parse_markdown_extended(truncated_text)
                else:
                    parsed_text = parse_rich_text(truncated_text)
                
                # Try with minimum font size
                font_size = self.min_font_size
                loaded_font = self.font_manager.get_regular_font(font_size)
                line_height = int(font_size * line_height_ratio)
                
                wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, 
                                                           effective_textbox_width, line_height, self.font_manager)
                
                # Attach font size
                for line, line_parts in wrapped_lines:
                    for chunk, chunk_styles in line_parts:
                        chunk_styles['size'] = font_size
                
                if total_text_height <= effective_textbox_height:
                    warnings.append(f"Text fits after {strategy}")
                    return font_size, wrapped_lines, total_text_height, warnings
                    
            except Exception as e:
                continue
        
        # Final fallback
        warnings.append("All fallback strategies failed")
        return self._get_fallback_result(warnings)
    
    def _find_longest_word(self, parsed_text):
        """Find the longest word in the parsed text."""
        longest_word = ""
        for text, styles in parsed_text:
            words = text.split()
            for word in words:
                if len(word) > len(longest_word):
                    longest_word = word
        return longest_word
    
    def _check_word_widths(self, wrapped_lines, font_size, max_width):
        """Check if any individual words are too wide for the container."""
        warnings = []
        for line in wrapped_lines:
            for chunk, chunk_styles in line:
                if chunk.strip():  # Skip spaces
                    # Get appropriate font for this chunk
                    if chunk_styles.get('b', False):
                        font = self.font_manager.get_bold_font(font_size)
                    elif chunk_styles.get('i', False):
                        font = self.font_manager.get_italic_font(font_size)
                    else:
                        font = self.font_manager.get_regular_font(font_size)
                    
                    word_width = font.getbbox(chunk)[2] - font.getbbox(chunk)[0]
                    if word_width > max_width:
                        warnings.append(f"Word '{chunk}' ({word_width}px) exceeds container width ({max_width}px) at font size {font_size}")
        
        return warnings
    
    def _get_fallback_result(self, warnings, problematic_word=None):
        """Generate a fallback result when text cannot be properly fitted."""
        fallback_font_size = self.min_font_size
        
        try:
            # Create a fallback text that will definitely fit
            if problematic_word:
                fallback_text = f"Text too long: {problematic_word[:10]}..."
            else:
                fallback_text = "Text overflow"
            
            # Parse as simple text
            parsed_text = [(fallback_text, {'b': False, 'i': False, 'u': False, 's': False})]
            
            # Use minimum font size
            loaded_font = self.font_manager.get_regular_font(fallback_font_size)
            line_height = int(fallback_font_size * 1.2)
            
            # Force wrap to single line if needed
            wrapped_lines, total_text_height = wrap_text(parsed_text, loaded_font, 1000, line_height, self.font_manager)
            
            # Attach font size
            for line, line_parts in wrapped_lines:
                for chunk, chunk_styles in line_parts:
                    chunk_styles['size'] = fallback_font_size
            
            warnings.append(f"Using fallback font size: {fallback_font_size}")
            return fallback_font_size, wrapped_lines, total_text_height, warnings
            
        except Exception as e:
            warnings.append(f"Fallback generation failed: {str(e)}")
            return None, None, None, warnings
    
    def get_text_dimensions(self, theText, font_size, text_type="rich_text"):
        """
        Calculate the dimensions needed to render text at a specific font size.
        
        Args:
            theText: Text to measure
            font_size: Font size to use
            text_type: Type of text parsing
            
        Returns:
            Tuple of (width, height) in pixels
        """
        try:
            # Parse text
            if text_type == "rich_text":
                parsed_text = parse_rich_text(theText)
            elif text_type == "markdown_basic":
                parsed_text = parse_markdown(theText)
            elif text_type == "markdown_headers":
                parsed_text = parse_markdown_with_headers(theText)
            elif text_type == "markdown_extended":
                parsed_text = parse_markdown_extended(theText)
            else:
                parsed_text = parse_rich_text(theText)
            
            # Use regular font for measurement
            font = self.font_manager.get_regular_font(font_size)
            line_height = int(font_size * 1.2)
            
            # Wrap text with very large width to get natural dimensions
            wrapped_lines, total_height = wrap_text(parsed_text, font, 10000, line_height, self.font_manager)
            
            # Calculate maximum line width
            max_width = 0
            for line, line_parts in wrapped_lines:
                line_width = 0
                for chunk, chunk_styles in line_parts:
                    # Get appropriate font for this chunk
                    if chunk_styles.get('b', False):
                        chunk_font = self.font_manager.get_bold_font(font_size)
                    elif chunk_styles.get('i', False):
                        chunk_font = self.font_manager.get_italic_font(font_size)
                    else:
                        chunk_font = self.font_manager.get_regular_font(font_size)
                    
                    chunk_width = chunk_font.getbbox(chunk)[2] - chunk_font.getbbox(chunk)[0]
                    line_width += chunk_width
                
                max_width = max(max_width, line_width)
            
            return max_width, total_height
            
        except Exception as e:
            self.logger.error(f"Error calculating text dimensions: {str(e)}")
            return 0, 0
    
    def suggest_font_size(self, theText, target_width, target_height, text_type="rich_text"):
        """
        Suggest an appropriate font size based on target dimensions.
        
        Args:
            theText: Text to analyze
            target_width: Target width
            target_height: Target height
            text_type: Type of text parsing
            
        Returns:
            Suggested font size or None if no good suggestion
        """
        # Start with a reasonable font size
        test_sizes = [24, 20, 16, 14, 12, 10, 8, 6]
        
        for size in test_sizes:
            width, height = self.get_text_dimensions(theText, size, text_type)
            if width <= target_width and height <= target_height:
                return size
        
        return None
