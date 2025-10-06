"""
ComfyUI Text Tools - Utilities Package
This module provides utility functions and classes for text processing, font management, and image manipulation.
"""

# Import core utility modules that don't require external dependencies
try:
    from .apz_box_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_color_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_enhanced_font_loader_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_error_handler_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_font_loader_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_font_manager import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_image_conversion import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_markdown_parser import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_markdown_renderer_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_rich_text_parser import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_text_box_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_text_renderer_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_text_wrapper import *
except ImportError as e:
    # Debug logging removed for performance
    pass

try:
    from .apz_url_file_utility import *
except ImportError as e:
    # Debug logging removed for performance
    pass

# Make specific classes and functions available for import
try:
    from .apz_error_handler_utility import ErrorHandlerUtility as apz_error_handler
except ImportError:
    apz_error_handler = None

try:
    from .apz_font_manager import FontManager as apz_font_manager
except ImportError:
    apz_font_manager = None

try:
    from .apz_rich_text_parser import RichTextParser as apz_rich_text_parser
except ImportError:
    apz_rich_text_parser = None

try:
    from .apz_markdown_parser import MarkdownParser as apz_markdown_parser
except ImportError:
    apz_markdown_parser = None

try:
    from .apz_image_conversion import ImageConversionUtility as apz_image_conversion
except ImportError:
    apz_image_conversion = None

try:
    from .apz_text_wrapper import TextWrapper as apz_text_wrapper
except ImportError:
    apz_text_wrapper = None

try:
    from .apz_text_renderer_utility import TextRendererUtility as apz_text_renderer_utility
except ImportError:
    apz_text_renderer_utility = None

try:
    from .apz_url_file_utility import URLFileUtility as apz_url_file_utility, get_local_file_path
except ImportError:
    apz_url_file_utility = None
    get_local_file_path = None

__all__ = [
    'apz_error_handler',
    'apz_font_manager', 
    'apz_rich_text_parser',
    'apz_markdown_parser',
    'apz_image_conversion',
    'apz_text_wrapper',
    'apz_text_renderer_utility',
    'apz_url_file_utility',
    'get_local_file_path',
    'ErrorHandlerUtility',
    'FontManager',
    'RichTextParser',
    'MarkdownParser',
    'ImageConversionUtility',
    'TextWrapper',
    'TextRendererUtility',
    'URLFileUtility'
]
