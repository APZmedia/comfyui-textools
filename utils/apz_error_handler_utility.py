# error_handler_utility.py
import logging
from PIL import ImageDraw, ImageFont
from .apz_color_utility import ColorUtility

class ErrorHandlerUtility:
    """
    Utility class for handling errors in text overlay nodes.
    Provides fallback mechanisms and user-friendly error messages.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.color_utility = ColorUtility()
    
    def handle_font_loading_error(self, font_path, fallback_font_path=None):
        """
        Handle font loading errors with fallback options.
        
        Args:
            font_path: Original font path that failed
            fallback_font_path: Optional fallback font path
            
        Returns:
            Tuple of (success, font_path_used, error_message)
        """
        try:
            # Try to load the original font
            font = ImageFont.truetype(font_path, 12)
            return True, font_path, None
        except Exception as e:
            error_msg = f"Failed to load font '{font_path}': {str(e)}"
            self.logger.warning(error_msg)
            
            # Try fallback font if provided
            if fallback_font_path:
                try:
                    font = ImageFont.truetype(fallback_font_path, 12)
                    return True, fallback_font_path, f"{error_msg} Using fallback font."
                except Exception as e2:
                    error_msg += f" Fallback font also failed: {str(e2)}"
            
            # Use system default font as last resort
            try:
                font = ImageFont.load_default()
                return True, "system_default", f"{error_msg} Using system default font."
            except Exception as e3:
                return False, None, f"{error_msg} System default font also failed: {str(e3)}"
    
    def handle_text_overflow_error(self, text, box_width, box_height, font_size, warnings=None):
        """
        Handle text overflow errors with intelligent fallback strategies.
        
        Args:
            text: Text that caused overflow
            box_width: Available width
            box_height: Available height
            font_size: Font size that caused overflow
            warnings: List of warnings from font loader
            
        Returns:
            Tuple of (fallback_text, fallback_font_size, error_message)
        """
        error_msg = f"Text overflow detected at font size {font_size}"
        if warnings:
            error_msg += f". Warnings: {', '.join(warnings)}"
        
        # Strategy 1: Progressive font size reduction
        for reduction in [2, 4, 6, 8, 10]:
            test_font_size = max(2, font_size - reduction)
            if test_font_size >= 2:  # Don't go below 2px
                return text, test_font_size, f"{error_msg} Reduced font size to {test_font_size}."
        
        # Strategy 2: Truncate text with ellipsis
        if len(text) > 50:
            fallback_text = text[:47] + "..."
            fallback_font_size = max(2, font_size - 2)
            return fallback_text, fallback_font_size, f"{error_msg} Text truncated."
        
        # Strategy 3: Use minimum font size
        fallback_font_size = 2
        return text, fallback_font_size, f"{error_msg} Using minimum font size."
    
    def handle_font_scaling_fallback(self, text, box_width, box_height, original_font_size, 
                                   font_manager, line_height_ratio, text_type="rich_text"):
        """
        Comprehensive font scaling fallback that tries multiple strategies.
        
        Args:
            text: Text to render
            box_width: Available width
            box_height: Available height
            original_font_size: Original font size that failed
            font_manager: Font manager instance
            line_height_ratio: Line height multiplier
            text_type: Type of text parsing
            
        Returns:
            Tuple of (success, font_size, processed_text, error_message)
        """
        from .apz_enhanced_font_loader_utility import EnhancedFontLoaderUtility
        
        # Create enhanced font loader for scaling
        font_loader = EnhancedFontLoaderUtility(font_manager, original_font_size)
        
        # Try progressive scaling
        scaling_strategies = [
            (original_font_size - 2, "Reduced by 2"),
            (original_font_size - 4, "Reduced by 4"),
            (original_font_size - 6, "Reduced by 6"),
            (original_font_size - 8, "Reduced by 8"),
            (original_font_size - 10, "Reduced by 10"),
            (6, "Minimum readable size"),
            (4, "Very small size"),
            (2, "Tiny size")
        ]
        
        for font_size, strategy in scaling_strategies:
            if font_size < 2:
                continue
                
            try:
                # Test if this font size works
                test_font = font_manager.get_regular_font(font_size)
                line_height = int(font_size * line_height_ratio)
                
                # Simple test - check if a single line fits
                test_text = text[:50] if len(text) > 50 else text
                bbox = test_font.getbbox(test_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                if text_width <= box_width and text_height <= box_height:
                    return True, font_size, text, f"Font scaled to {font_size} ({strategy})"
                    
            except Exception as e:
                continue
        
        # If scaling fails, try text truncation
        truncation_strategies = [
            (text[:100] + "..." if len(text) > 100 else text, "100 chars"),
            (text[:50] + "..." if len(text) > 50 else text, "50 chars"),
            (text[:25] + "..." if len(text) > 25 else text, "25 chars"),
            ("Text overflow", "error message")
        ]
        
        for truncated_text, strategy in truncation_strategies:
            try:
                test_font = font_manager.get_regular_font(2)  # Use minimum size
                bbox = test_font.getbbox(truncated_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                if text_width <= box_width and text_height <= box_height:
                    return True, 2, truncated_text, f"Text truncated to {strategy}"
                    
            except Exception as e:
                continue
        
        return False, 2, "Text overflow", "All scaling strategies failed"
    
    def handle_word_too_long_error(self, word, max_width, font_size):
        """
        Handle cases where individual words are too long to fit.
        
        Args:
            word: Word that's too long
            max_width: Maximum available width
            font_size: Current font size
            
        Returns:
            Tuple of (processed_word, new_font_size, error_message)
        """
        error_msg = f"Word '{word}' is too long for container width {max_width}px"
        
        # Strategy 1: Break long word with hyphens
        if len(word) > 20:
            # Simple hyphenation (in a real implementation, you might use a proper hyphenation library)
            mid_point = len(word) // 2
            processed_word = word[:mid_point] + "-" + word[mid_point:]
            return processed_word, font_size, f"{error_msg}. Word hyphenated."
        
        # Strategy 2: Use smaller font
        new_font_size = max(6, font_size - 2)
        return word, new_font_size, f"{error_msg}. Using smaller font size."
    
    def draw_error_indicator(self, draw, x, y, width, height, error_message):
        """
        Draw a visual error indicator on the image.
        
        Args:
            draw: PIL ImageDraw object
            x, y: Position to draw the indicator
            width, height: Size of the error area
            error_message: Error message to display
        """
        try:
            # Draw error background
            error_color = (255, 200, 200, 180)  # Light red with transparency
            draw.rectangle([x, y, x + width, y + height], fill=error_color)
            
            # Draw error border
            border_color = (255, 0, 0, 255)  # Red border
            draw.rectangle([x, y, x + width, y + height], outline=border_color, width=2)
            
            # Draw error text
            try:
                error_font = ImageFont.load_default()
                # Truncate error message if too long
                if len(error_message) > 50:
                    display_text = error_message[:47] + "..."
                else:
                    display_text = error_message
                
                # Calculate text position
                bbox = error_font.getbbox(display_text)
                text_width = bbox[2] - bbox[0]
                text_x = x + (width - text_width) // 2
                text_y = y + (height - 12) // 2
                
                draw.text((text_x, text_y), display_text, font=error_font, fill=(255, 0, 0, 255))
                
            except Exception as e:
                # If text drawing fails, just draw a simple error symbol
                draw.text((x + 5, y + 5), "ERROR", fill=(255, 0, 0, 255))
                
        except Exception as e:
            self.logger.error(f"Failed to draw error indicator: {str(e)}")
    
    def create_fallback_text(self, original_text, error_type, max_length=30):
        """
        Create fallback text when original text cannot be rendered.
        
        Args:
            original_text: Original text that failed
            error_type: Type of error ("overflow", "font", "parsing")
            max_length: Maximum length of fallback text
            
        Returns:
            Fallback text string
        """
        if error_type == "overflow":
            if len(original_text) > max_length:
                return f"Text overflow: {original_text[:max_length-10]}..."
            else:
                return f"Text overflow: {original_text}"
        elif error_type == "font":
            return "Font loading error"
        elif error_type == "parsing":
            return "Text parsing error"
        else:
            return "Rendering error"
    
    def log_error_with_context(self, error, context):
        """
        Log errors with detailed context information.
        
        Args:
            error: Exception or error message
            context: Dictionary with context information
        """
        error_msg = f"Error: {str(error)}"
        if context:
            context_str = ", ".join([f"{k}={v}" for k, v in context.items()])
            error_msg += f" Context: {context_str}"
        
        self.logger.error(error_msg)
    
    def validate_text_box_dimensions(self, width, height, min_width=10, min_height=10):
        """
        Validate text box dimensions.
        
        Args:
            width: Box width
            height: Box height
            min_width: Minimum allowed width
            min_height: Minimum allowed height
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if width < min_width:
            return False, f"Text box width ({width}) is too small. Minimum: {min_width}"
        if height < min_height:
            return False, f"Text box height ({height}) is too small. Minimum: {min_height}"
        if width > 10000:
            return False, f"Text box width ({width}) is too large. Maximum: 10000"
        if height > 10000:
            return False, f"Text box height ({height}) is too large. Maximum: 10000"
        
        return True, None
    
    def validate_font_size(self, font_size, min_size=1, max_size=256):
        """
        Validate font size.
        
        Args:
            font_size: Font size to validate
            min_size: Minimum allowed font size
            max_size: Maximum allowed font size
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if font_size < min_size:
            return False, f"Font size ({font_size}) is too small. Minimum: {min_size}"
        if font_size > max_size:
            return False, f"Font size ({font_size}) is too large. Maximum: {max_size}"
        
        return True, None
    
    def get_system_font_paths(self):
        """
        Get common system font paths for fallback.
        
        Returns:
            Dictionary of platform-specific font paths
        """
        import platform
        import os
        
        system = platform.system()
        
        if system == "Windows":
            return {
                "regular": "C:/Windows/Fonts/arial.ttf",
                "bold": "C:/Windows/Fonts/arialbd.ttf",
                "italic": "C:/Windows/Fonts/ariali.ttf"
            }
        elif system == "Linux":
            return {
                "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "italic": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"
            }
        elif system == "Darwin":  # macOS
            return {
                "regular": "/System/Library/Fonts/Arial.ttf",
                "bold": "/System/Library/Fonts/Arial Bold.ttf",
                "italic": "/System/Library/Fonts/Arial Italic.ttf"
            }
        else:
            return {
                "regular": None,
                "bold": None,
                "italic": None
            } 
