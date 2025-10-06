# ComfyUI Textools - Component Documentation

## Overview
ComfyUI Textools is a comprehensive text processing system for ComfyUI that provides advanced text overlay capabilities with rich formatting, emoji support, hashtag processing, and brand asset integration.

## Architecture

The system follows a modular architecture with three main layers:

1. **Node Layer** - ComfyUI interface nodes
2. **Processing Layer** - Text parsing, rendering, and utilities
3. **Utility Layer** - Core functionality and helpers

---

## Node Components

### Core Text Overlay Nodes

#### 1. APZmediaImageRichTextOverlay (V1)
- **File**: `nodes/apzImageRichTextOverlay.py`
- **Purpose**: Original rich text overlay node with HTML-like formatting
- **Features**:
  - Bold, italic, underline, strikethrough text
  - Custom font support
  - Text positioning and alignment
  - Basic error handling
- **Inputs**: Image, text, fonts, positioning, styling
- **Outputs**: Image with text overlay

#### 2. APZmediaImageRichTextOverlayV2 (V2)
- **File**: `nodes/apzImageRichTextOverlayV2.py`
- **Purpose**: Enhanced rich text overlay with comprehensive features
- **Features**:
  - All V1 features plus:
  - Hashtag support with custom colors
  - Emoji support with PNG rendering
  - Enhanced error handling
  - Visual error indicators
  - URL font support
- **Inputs**: Image, text, fonts, positioning, styling, hashtag/emoji options
- **Outputs**: Image with enhanced text overlay

#### 3. APZmediaImageMarkdownTextOverlay
- **File**: `nodes/apzImageMarkdownTextOverlay.py`
- **Purpose**: Markdown-formatted text overlay
- **Features**:
  - Markdown parsing (basic, headers, extended)
  - Bold, italic, underline, strikethrough
  - Header support (H1-H6)
  - List support
  - Hashtag and emoji support
- **Inputs**: Image, markdown text, parsing mode, fonts, styling
- **Outputs**: Image with markdown text overlay

### Brand-Integrated Nodes

#### 4. APZmediaBrandRichTextOverlay
- **File**: `nodes/apzBrandRichTextOverlay.py`
- **Purpose**: Brand asset integrated rich text overlay
- **Features**:
  - Brand font integration
  - Brand color schemes
  - Brand asset loading
  - Font override support
- **Inputs**: Image, brand assets, text, styling options
- **Outputs**: Image with brand-styled text overlay

#### 5. APZmediaBrandRichTextOverlayV2
- **File**: `nodes/apzBrandRichTextOverlayV2.py`
- **Purpose**: Enhanced brand text overlay with full feature set
- **Features**:
  - All brand features plus:
  - Hashtag support
  - Emoji support
  - Enhanced error handling
  - URL font support
- **Inputs**: Image, brand assets, text, styling, hashtag/emoji options
- **Outputs**: Image with enhanced brand text overlay

#### 6. APZmediaBrandMarkdownTextOverlay
- **File**: `nodes/apzBrandMarkdownTextOverlay.py`
- **Purpose**: Brand-integrated markdown text overlay
- **Features**:
  - Brand styling with markdown
  - Markdown parsing with brand fonts
  - Brand color integration
  - Hashtag and emoji support
- **Inputs**: Image, brand assets, markdown text, parsing mode
- **Outputs**: Image with brand-styled markdown overlay

---

## Utility Components

### Text Processing Pipeline

#### 1. apz_rich_text_parser.py
- **Purpose**: Parses HTML-like rich text tags
- **Features**:
  - `<b>`, `<i>`, `<u>`, `<s>` tag parsing
  - Nested tag support
  - Style attribute extraction
  - Text chunking for rendering
- **Key Classes**: `RichTextParser`
- **Methods**: `parse_rich_text()`, `extract_styles()`

#### 2. apz_markdown_parser.py
- **Purpose**: Parses markdown syntax into renderable format
- **Features**:
  - Header parsing (H1-H6)
  - Bold/italic text parsing
  - List parsing
  - Link parsing
  - Code block parsing
- **Key Classes**: `MarkdownParser`
- **Methods**: `parse_markdown()`, `parse_markdown_with_headers()`, `parse_markdown_extended()`

#### 3. apz_text_wrapper.py
- **Purpose**: Handles text wrapping and line breaking
- **Features**:
  - Word-based wrapping
  - Emoji-aware wrapping
  - Font size consideration
  - Line height calculation
- **Key Functions**: `wrap_text()`, `_get_word_width()`

### Rendering Engine

#### 4. apz_text_renderer_utility.py
- **Purpose**: Core text rendering engine for rich text
- **Features**:
  - Multi-style text rendering
  - Font switching per chunk
  - Color management
  - Emoji PNG integration
  - Hashtag styling
- **Key Classes**: `TextRendererUtility`
- **Methods**: `render_text()`, `_draw_text_with_color_support()`

#### 5. apz_markdown_renderer_utility.py
- **Purpose**: Markdown-specific rendering engine
- **Features**:
  - Header rendering
  - List rendering
  - Markdown-specific styling
  - Emoji and hashtag support
- **Key Classes**: `MarkdownRendererUtility`
- **Methods**: `render_markdown_text()`, `_process_parsed_parts()`

### Font Management

#### 6. apz_font_manager.py
- **Purpose**: Font loading, caching, and management
- **Features**:
  - Font caching system
  - Style-based font selection
  - Emoji font fallback
  - Font size management
- **Key Classes**: `FontManager`
- **Methods**: `get_font_for_style()`, `load_font()`, `get_regular_font()`

#### 7. apz_font_loader_utility.py
- **Purpose**: Font sizing and fitting algorithms
- **Features**:
  - Dynamic font sizing
  - Text fitting algorithms
  - Size optimization
- **Key Classes**: `FontLoaderUtility`
- **Methods**: `find_fitting_font_size()`

#### 8. apz_enhanced_font_loader_utility.py
- **Purpose**: Enhanced font loading with comprehensive error handling
- **Features**:
  - Aggressive scaling fallback
  - Word width checking
  - Comprehensive error handling
  - Multiple text type support
- **Key Classes**: `EnhancedFontLoaderUtility`
- **Methods**: `find_fitting_font_size()`, `_try_aggressive_scaling()`

### Emoji Support System

#### 9. apz_emoji_support.py
- **Purpose**: Emoji detection and font management
- **Features**:
  - Unicode emoji detection
  - Emoji font loading
  - Scale factor calculation
  - Text segmentation
- **Key Classes**: `EmojiSupport`
- **Methods**: `has_emoji()`, `get_emoji_font()`, `split_text_by_emoji()`

#### 10. apz_emoji_png_renderer.py
- **Purpose**: High-quality emoji PNG generation
- **Features**:
  - Super-sampling for crisp rendering
  - Font-based emoji generation
  - PNG caching system
  - Multi-resolution support
- **Key Classes**: `EmojiPNGRenderer`
- **Methods**: `load_emoji_png()`, `_generate_emoji_png()`, `_render_emoji_to_png()`

#### 11. apz_twemoji_renderer.py
- **Purpose**: Twemoji emoji rendering system
- **Features**:
  - Twemoji CDN integration
  - SVG to PNG conversion
  - Emoji downloading and caching
- **Key Classes**: `TwemojiRenderer`
- **Methods**: `load_emoji()`, `render_emoji()`, `download_emoji()`

#### 12. apz_png_emoji_text_renderer.py
- **Purpose**: PNG-based emoji text rendering
- **Features**:
  - PNG emoji integration
  - Text and emoji mixing
  - Position management
- **Key Classes**: `PNGEmojiTextRenderer`
- **Methods**: `render_text_with_png_emojis()`

### Visual Elements

#### 13. apz_box_utility.py
- **Purpose**: Bounding box calculations and drawing
- **Features**:
  - Box coordinate calculation
  - Effective dimension calculation
  - Bounding box drawing
  - Padding management
- **Key Classes**: `BoxUtility`
- **Methods**: `calculate_box_coordinates()`, `draw_bounding_box()`

#### 14. apz_color_utility.py
- **Purpose**: Color conversion and management
- **Features**:
  - HEX to RGB conversion
  - Color validation
  - Style-based color selection
- **Key Classes**: `ColorUtility`
- **Methods**: `hex_to_rgb()`, `get_font_color()`

#### 15. apz_text_box_utility.py
- **Purpose**: Text box positioning and layout
- **Features**:
  - Text box calculations
  - Alignment handling
  - Position management
- **Key Classes**: `TextBoxUtility`
- **Methods**: `calculate_text_position()`, `align_text()`

### Specialized Features

#### 16. apz_hashtag_parser.py
- **Purpose**: Hashtag detection and styling
- **Features**:
  - Hashtag regex matching
  - Color assignment
  - Style application
- **Key Classes**: `HashtagParser`
- **Methods**: `parse_hashtags()`, `apply_hashtag_styles()`

#### 17. apz_url_file_utility.py
- **Purpose**: URL-based file handling
- **Features**:
  - URL file downloading
  - Local caching
  - File cleanup
  - Signed URL support
- **Key Classes**: `URLFileUtility`
- **Methods**: `download_file()`, `get_cached_file()`, `cleanup_old_files()`

#### 18. apz_image_conversion.py
- **Purpose**: Image format conversion
- **Features**:
  - Tensor to PIL conversion
  - PIL to tensor conversion
  - Format handling
- **Key Functions**: `tensor_to_pil()`, `pil_to_tensor()`

#### 19. apz_error_handler_utility.py
- **Purpose**: Error handling and recovery
- **Features**:
  - Error detection
  - Fallback mechanisms
  - Error reporting
- **Key Classes**: `ErrorHandler`
- **Methods**: `handle_error()`, `get_fallback()`

---

## Data Flow

### Text Processing Pipeline

1. **Input**: Raw text (HTML or Markdown)
2. **Parsing**: Text is parsed into structured format with styles
3. **Wrapping**: Text is wrapped to fit within bounds
4. **Font Loading**: Appropriate fonts are loaded and cached
5. **Rendering**: Text is rendered with styles and effects
6. **Integration**: Emojis and hashtags are integrated
7. **Output**: Final image with text overlay

### Emoji Processing Pipeline

1. **Detection**: Emoji characters are detected in text
2. **Font Selection**: Appropriate emoji font is selected
3. **PNG Generation**: High-quality PNG is generated using super-sampling
4. **Caching**: Generated PNG is cached for future use
5. **Positioning**: Emoji is positioned with text baseline
6. **Integration**: Emoji is pasted onto the image

### Brand Asset Integration

1. **Asset Loading**: Brand assets are loaded from provided data
2. **Font Extraction**: Brand fonts are extracted and loaded
3. **Color Application**: Brand colors are applied to text
4. **Style Integration**: Brand styling is applied to text elements
5. **Rendering**: Text is rendered with brand styling

---

## Key Features

### Text Formatting
- **Rich Text**: HTML-like tags (`<b>`, `<i>`, `<u>`, `<s>`)
- **Markdown**: Full markdown support with headers, lists, links
- **Hashtags**: Automatic hashtag detection and styling
- **Emojis**: High-quality emoji rendering with PNG generation

### Font Management
- **Custom Fonts**: Support for regular, italic, and bold fonts
- **URL Fonts**: Download and cache fonts from URLs
- **Font Caching**: Intelligent font caching system
- **Size Optimization**: Automatic font sizing to fit text

### Visual Elements
- **Bounding Boxes**: Optional bounding box drawing
- **Backgrounds**: Text background support
- **Alignment**: Text alignment options
- **Positioning**: Precise text positioning

### Error Handling
- **Fallback Mechanisms**: Graceful degradation on errors
- **Visual Indicators**: Error indicators in output
- **Comprehensive Logging**: Detailed error reporting
- **Recovery**: Automatic error recovery where possible

---

## Dependencies

### Core Dependencies
- **Pillow (PIL)**: Image processing and font handling
- **torch**: Tensor operations for ComfyUI compatibility
- **re**: Regular expressions for text parsing
- **os**: File system operations
- **urllib**: URL handling for font downloads

### Optional Dependencies
- **cairosvg**: SVG to PNG conversion (for Twemoji)
- **requests**: HTTP requests for font downloads

---

## Configuration

### Font Configuration
- Local font paths
- URL-based fonts with signatures
- Font caching directories
- Font size limits

### Emoji Configuration
- Emoji font priorities
- PNG generation settings
- Caching directories
- Quality settings

### Error Handling Configuration
- Error indicator settings
- Fallback mechanisms
- Logging levels
- Recovery options

---

## Performance Considerations

### Caching
- Font caching for performance
- Emoji PNG caching
- URL file caching
- Automatic cleanup of old files

### Optimization
- Super-sampling for emoji quality
- Efficient text wrapping algorithms
- Font size optimization
- Memory management

### Scalability
- Modular architecture
- Efficient resource usage
- Error recovery mechanisms
- Performance monitoring

---

This documentation provides a comprehensive overview of all components in the ComfyUI Textools system, their purposes, features, and interactions. Each component is designed to work together to provide a robust, feature-rich text processing system for ComfyUI.


