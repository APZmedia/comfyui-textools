# ComfyUI-textools Project Overview

## Project Purpose
ComfyUI-textools is a collection of custom nodes for ComfyUI that provides advanced text processing capabilities, specifically focused on applying rich text overlays on images with sophisticated styling options.

## Core Functionality
- **Rich Text Overlay**: Apply formatted text (bold, italic, underline, strikethrough) on images
- **Font Management**: Support for custom fonts with different styles
- **Text Layout**: Advanced text wrapping, alignment, and positioning
- **Visual Elements**: Bounding boxes, backgrounds, and styling options

## Project Structure

```
comfyui-textools/
├── nodes/                          # ComfyUI custom nodes
│   └── apzImageRichTextOverlay.py  # Main text overlay node
├── utils/                          # Utility modules
│   ├── apz_box_utility.py          # Bounding box calculations and drawing
│   ├── apz_color_utility.py        # Color conversion utilities
│   ├── apz_font_loader_utility.py  # Font loading and sizing logic
│   ├── apz_font_manager.py         # Font management and caching
│   ├── apz_image_conversion.py     # Tensor/PIL image conversion
│   ├── apz_rich_text_parser.py     # HTML-like tag parsing
│   ├── apz_text_box_utility.py     # Text box positioning
│   ├── apz_text_renderer_utility.py # Text rendering engine
│   └── apz_text_wrapper.py         # Text wrapping algorithms
├── setup.py                        # Package configuration
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

## Key Components

### Main Nodes
- **APZmediaImageRichTextOverlay** (V1)
  - **Location**: `nodes/apzImageRichTextOverlay.py`
  - **Purpose**: Original ComfyUI node for HTML-like rich text overlay functionality
  - **Inputs**: Image, text, styling parameters, positioning
  - **Outputs**: Image with text overlay applied
  - **Status**: Stable, no error handling

- **APZmediaImageRichTextOverlayV2** (V2)
  - **Location**: `nodes/apzImageRichTextOverlayV2.py`
  - **Purpose**: Enhanced version with comprehensive error handling and fallback mechanisms
  - **Inputs**: Image, text, styling parameters, positioning, error indicator toggle
  - **Outputs**: Image with text overlay applied or error indicators
  - **Status**: Enhanced with error handling

- **APZmediaImageMarkdownTextOverlay**
  - **Location**: `nodes/apzImageMarkdownTextOverlay.py`
  - **Purpose**: ComfyUI node for markdown-formatted text overlay functionality
  - **Inputs**: Image, markdown text, parsing mode, styling parameters, positioning
  - **Outputs**: Image with markdown text overlay applied
  - **Status**: Enhanced with error handling

### Utility Architecture
The project follows a modular utility-based architecture:

1. **Text Processing Pipeline**:
   - `apz_rich_text_parser.py` → Parses HTML-like tags
   - `apz_markdown_parser.py` → Parses markdown syntax
   - `apz_text_wrapper.py` → Handles text wrapping
   - `apz_text_renderer_utility.py` → Renders HTML-like text with styles
   - `apz_markdown_renderer_utility.py` → Renders markdown text with styles

2. **Font Management**:
   - `apz_font_manager.py` → Font loading and caching
   - `apz_font_loader_utility.py` → Font sizing and fitting

3. **Visual Elements**:
   - `apz_box_utility.py` → Bounding box calculations
   - `apz_color_utility.py` → Color conversions

4. **Image Processing**:
   - `apz_image_conversion.py` → Tensor/PIL conversions

## Dependencies
- **Pillow**: Image processing and font handling
- **torch**: Tensor operations for ComfyUI compatibility
- **numpy**: Numerical operations
- **colorama**: Terminal color output
- **re**: Regular expressions for text parsing

## Development Status
- ✅ Core text overlay functionality
- ✅ Rich text parsing (bold, italic, underline, strikethrough)
- ✅ Markdown text parsing (bold, italic, underline, strikethrough, headers, lists)
- ✅ Font management with caching
- ✅ Text wrapping and alignment
- ✅ Bounding box visualization
- ✅ Background and styling options
- ✅ ComfyUI integration
- ✅ Modular architecture with reusable utilities
- ✅ Enhanced error handling system (V2 nodes)
- ✅ Fallback mechanisms and visual error indicators
- ✅ Parameter validation and graceful degradation

## Future Development Areas
- Additional text effects (shadows, outlines)
- More font format support
- Animation capabilities
- Performance optimizations
- Additional text styling options 