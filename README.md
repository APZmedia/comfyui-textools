# ComfyUI-textools

**ComfyUI-textools** is a collection of custom nodes designed for use with ComfyUI. These nodes enhance text processing capabilities, including applying rich text overlays on images with comprehensive error handling and fallback mechanisms.

## Overview

ComfyUI-textools includes several custom nodes, such as:

- **APZmedia Image Rich Text Overlay**: A node for overlaying rich text on images with support for bold, italic, underline, and strike-through styles using HTML-like tags.
- **APZmedia Image Rich Text Overlay V2**: Enhanced version with comprehensive error handling, fallback mechanisms, visual error indicators, hashtag support, and emoji support.
- **APZmedia Image Markdown Text Overlay**: A node for overlaying markdown-formatted text on images with support for bold, italic, underline, strikethrough, headers, lists, hashtags, and emojis.

## Features

### URL Support for Fonts
All text overlay nodes now support both local file paths and signed URLs for font files:

- **Local Paths**: Works exactly as before with local font files
- **Signed URLs**: Automatically downloads fonts from URLs and caches them locally
- **Mixed Usage**: You can use local paths for some fonts and URLs for others
- **Automatic Caching**: Downloaded fonts are cached to avoid re-downloading
- **Cleanup**: Old cached files are automatically cleaned up
- **No Input Changes**: No changes needed to node inputs or structure

**Examples:**
```
Local paths:
font: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

Signed URLs:
font: "https://your-cdn.com/fonts/regular.ttf?signature=abc123"

Mixed usage:
font: "/local/path/regular.ttf"
italic_font: "https://cdn.com/italic.ttf?signature=xyz"
```

### APZmedia Image Rich Text Overlay
- **Rich Text Support**: Allows the addition of bold, italic, underline, and strike-through text on images.
- **Customizable Fonts**: Supports different fonts for regular, bold, and italic text from local paths or signed URLs.
- **URL Support**: Automatically downloads fonts from signed URLs and caches them locally for optimal performance.
- **Alignment Options**: Supports text alignment (left, right, center) and vertical alignment (top, middle, bottom).
- **Text Wrapping**: Automatically wraps text within a defined box area.

### APZmedia Image Rich Text Overlay V2
- **All V1 Features**: Includes all features from the original rich text overlay.
- **Enhanced Error Handling**: Comprehensive fallback mechanisms for font loading and text overflow issues.
- **Progressive Font Scaling**: Automatically scales font sizes from maximum down to 2px when text doesn't fit.
- **Intelligent Text Truncation**: Smart text truncation strategies when scaling fails.
- **Visual Error Indicators**: Shows error messages directly on images when problems occur (optional).
- **Parameter Validation**: Validates input parameters and provides helpful warnings.
- **Graceful Degradation**: Continues to work even when encountering errors.
- **Error Indicator Toggle**: Option to show or hide visual error indicators.
- **Console Feedback**: Reports scaling actions and fallback strategies used.
- **Hashtag Support**: Automatic detection and styling of hashtags (#hashtag) with special blue coloring.
- **Emoji Support**: Full Unicode emoji support with automatic font fallback system.
- **Enhanced Text Processing**: Advanced parsing that handles hashtags, emojis, and formatting simultaneously.

### APZmedia Image Markdown Text Overlay
- **Markdown Support**: Supports standard markdown syntax including **bold**, *italic*, __underline__, ~~strikethrough~~, headers (# ## ###), and lists.
- **Multiple Modes**: Three parsing modes - basic (text styling only), with_headers (includes header support), and extended (includes lists and code blocks).
- **Customizable Fonts**: Same font customization options as the rich text overlay.
- **Alignment Options**: Same alignment and positioning options as the rich text overlay.
- **Text Wrapping**: Advanced text wrapping that respects markdown formatting.
- **Enhanced Error Handling**: Same comprehensive error handling and font scaling as V2 rich text overlay.
- **Progressive Font Scaling**: Automatically scales font sizes when markdown text doesn't fit.
- **Smart Fallback Strategies**: Intelligent text processing and truncation when needed.
- **Hashtag Support**: Automatic detection and styling of hashtags (#hashtag) with special blue coloring.
- **Emoji Support**: Full Unicode emoji support with automatic font fallback system.
- **Enhanced Text Processing**: Advanced parsing that handles hashtags, emojis, and formatting simultaneously.
- **Emoji Font Fallback**: Automatically detects and uses system emoji fonts (Windows Segoe UI Emoji, macOS Apple Color Emoji, Linux Noto Color Emoji).
- **Hashtag Detection**: Extracts and reports found hashtags for further processing.
- **Emoji Detection**: Identifies and reports emoji characters in text.
- **Processing Information**: Returns detailed information about text processing and feature detection.
- **Cross-Platform Emoji Support**: Works across Windows, macOS, and Linux with appropriate emoji fonts.

## Input Types

### APZmedia Image Rich Text Overlay
- **image (IMAGE)**: The image to which the text will be applied.
- **theText (STRING)**: The rich text string to overlay on the image, with support for HTML-like tags (e.g., `<b>`, `<i>`, etc.).
- **theTextbox_width (INT)**: Width of the text box.
- **theTextbox_height (INT)**: Height of the text box.
- **max_font_size (INT)**: Maximum font size to use.
- **font (STRING)**: Path to the font file.
- **italic_font (STRING)**: Path to the italic font file.
- **bold_font (STRING)**: Path to the bold font file.
- **alignment (STRING)**: Horizontal text alignment (left, right, center).
- **vertical_alignment (STRING)**: Vertical text alignment (top, middle, bottom).
- **font_color (STRING)**: Color of the font.
- **italic_font_color (STRING)**: Color of the italic font.
- **bold_font_color (STRING)**: Color of the bold font.
- **box_start_x (INT)**: X-coordinate for the text box's starting position.
- **box_start_y (INT)**: Y-coordinate for the text box's starting position.
- **padding (INT)**: Padding inside the text box.
- **line_height_ratio (FLOAT)**: Ratio for line height relative to font size.

### APZmedia Image Rich Text Overlay V2
- **All V1 Parameters**: Includes all parameters from the original rich text overlay.
- **show_error_indicators (STRING)**: Show visual error indicators (true/false). When enabled, displays error messages directly on the image when text cannot be rendered properly.
- **hashtag_color (STRING)**: Color for hashtags (default: blue).
- **enable_hashtag_support (STRING)**: Enable hashtag support (true/false).
- **enable_emoji_support (STRING)**: Enable emoji support (true/false).

### APZmedia Image Markdown Text Overlay
- **image (IMAGE)**: The image to which the text will be applied.
- **theText (STRING)**: The markdown text string to overlay on the image.
- **markdown_mode (STRING)**: Markdown parsing mode (basic, with_headers, extended).
- **theTextbox_width (INT)**: Width of the text box.
- **theTextbox_height (INT)**: Height of the text box.
- **max_font_size (INT)**: Maximum font size to use.
- **font (STRING)**: Path to the font file.
- **italic_font (STRING)**: Path to the italic font file.
- **bold_font (STRING)**: Path to the bold font file.
- **alignment (STRING)**: Horizontal text alignment (left, right, center).
- **vertical_alignment (STRING)**: Vertical text alignment (top, middle, bottom).
- **font_color (STRING)**: Color of the font.
- **italic_font_color (STRING)**: Color of the italic font.
- **bold_font_color (STRING)**: Color of the bold font.
- **box_start_x (INT)**: X-coordinate for the text box's starting position.
- **box_start_y (INT)**: Y-coordinate for the text box's starting position.
- **padding (INT)**: Padding inside the text box.
- **line_height_ratio (FLOAT)**: Ratio for line height relative to font size.
- **hashtag_color (STRING)**: Color for hashtags (default: blue).
- **enable_hashtag_support (STRING)**: Enable hashtag support (true/false).
- **enable_emoji_support (STRING)**: Enable emoji support (true/false).

## Output Types

### APZmedia Image Rich Text Overlay
- **image (IMAGE)**: The image with the applied text overlay.

### APZmedia Image Rich Text Overlay V2
- **image (IMAGE)**: The image with the applied text overlay (with error handling).
- **hashtags_found (STRING)**: Comma-separated list of hashtags found in the text.
- **emojis_found (STRING)**: Comma-separated list of emojis found in the text.
- **processing_info (STRING)**: Detailed information about text processing and feature detection.

### APZmedia Image Markdown Text Overlay
- **image (IMAGE)**: The image with the applied markdown text overlay.
- **hashtags_found (STRING)**: Comma-separated list of hashtags found in the text.
- **emojis_found (STRING)**: Comma-separated list of emojis found in the text.
- **processing_info (STRING)**: Detailed information about text processing and feature detection.

## How It Works

### APZmedia Image Rich Text Overlay
1. **Text Wrapping**: Automatically wraps the provided text within the specified width and height.
2. **Rich Text Processing**: Processes tags like `<b>` for bold and `<i>` for italic, applying the appropriate styles.
3. **Text Overlay**: Draws the text onto the image with the specified alignment and font settings.
4. **Text Box**: Draws a box around the text with the specified padding and line height ratio.
5. **Output**: Returns the image with the text overlay applied.

### APZmedia Image Rich Text Overlay V2
1. **Parameter Validation**: Validates all input parameters and provides warnings for invalid values.
2. **Enhanced Text Wrapping**: Advanced text wrapping with comprehensive error handling.
3. **Rich Text Processing**: Same processing as V1 with enhanced error recovery.
4. **Progressive Font Scaling**: Automatically reduces font size from maximum down to 2px when text doesn't fit.
5. **Intelligent Text Truncation**: Applies smart truncation strategies (100 → 50 → 25 characters) when scaling fails.
6. **Error Handling**: Provides fallback mechanisms for font loading and text overflow issues.
7. **Visual Error Indicators**: Shows error messages on images when problems occur (optional).
8. **Console Feedback**: Reports scaling actions and fallback strategies used.
9. **Graceful Degradation**: Continues to work even when encountering errors.
10. **Output**: Returns the image with the text overlay applied, scaled text, or error indicators.

### APZmedia Image Markdown Text Overlay
1. **Markdown Parsing**: Parses markdown syntax based on the selected mode (basic, with_headers, extended).
2. **Text Wrapping**: Advanced text wrapping that respects markdown formatting and word boundaries.
3. **Style Application**: Applies appropriate fonts and colors based on markdown formatting.
4. **Progressive Font Scaling**: Same automatic font scaling as V2 rich text overlay.
5. **Intelligent Text Truncation**: Smart truncation strategies when markdown text doesn't fit.
6. **Layout Rendering**: Renders text with proper alignment and positioning while maintaining markdown structure.
7. **Error Handling**: Comprehensive error handling with fallback mechanisms.
8. **Output**: Returns the image with the markdown text overlay applied, scaled text, or error indicators.

## Error Handling & Fallback Mechanisms

ComfyUI-textools includes comprehensive error handling to ensure your text overlays always work, even in challenging scenarios.

### Progressive Font Scaling

When text doesn't fit in the specified dimensions, the system automatically scales down the font size:

1. **Normal Scaling**: Reduces font size from maximum to minimum (6px) in 1px increments
2. **Aggressive Scaling**: Goes below minimum to very small sizes (down to 2px)
3. **Text Truncation**: Applies smart truncation strategies when scaling fails
4. **Error Indicators**: Shows visual error messages when all strategies fail

### Scaling Strategies

```
Original Font Size (e.g., 30px)
    ↓
Progressive Reduction (29px, 28px, 27px...)
    ↓
Minimum Size (6px)
    ↓
Aggressive Scaling (5px, 4px, 3px, 2px)
    ↓
Text Truncation (100 → 50 → 25 characters)
    ↓
Error Message ("Text overflow")
```

### Console Feedback

The system provides detailed console feedback about scaling actions:

```
Warning: Text overflow detected at font size 30
Font scaling fallback: Font scaled to 12 (Reduced by 18)
```

### Error Indicator Options

- **Enabled**: Shows red error boxes with messages on the image
- **Disabled**: Uses fallback text without visual indicators
- **Console Warnings**: Always provides feedback in the console

## Hashtag and Emoji Support

The enhanced text overlay supports modern text features:

### Hashtag Support
- **Automatic Detection**: Detects hashtags in the format `#hashtag`
- **Special Styling**: Hashtags are rendered in bold with a distinctive blue color
- **Extraction**: Returns found hashtags for further processing
- **Integration**: Works with all text modes (rich text, markdown)

### Emoji Support
- **Unicode Emojis**: Full support for Unicode emoji characters (😀 🎉 🚀 🎨)
- **Bundled Fonts**: Includes emoji fonts with the project for consistent rendering
- **Font Priority System**: 
  1. **Bundled Fonts** (fonts/emoji/) - Consistent across all platforms
  2. **System Fonts** - Windows Segoe UI Emoji, macOS Apple Color Emoji, Linux Noto
  3. **Default Font** - Last resort fallback
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy Setup**: Add emoji fonts to `fonts/emoji/` directory for enhanced support
- **Automatic Color Glyphs**: Detects Pillow builds that support embedded color glyph rendering and uses palette-aware drawing to keep emoji colors intact.
- **Graceful Degradation**: When embedded color glyphs are unavailable, the node logs a warning and automatically falls back to monochrome rendering or PNG emoji assets so that workflows continue to function.

### Example Usage
```
Text: "Hello #world! 😀 This is **bold** text with emojis 🎉"

Features detected:
- Hashtags: #world
- Emojis: 😀, 🎉
- Formatting: **bold**
```

### Bundled Emoji Fonts

ComfyUI-textools includes a bundled emoji font system for consistent emoji rendering:

#### **Font Directory Structure**
```
fonts/
└── emoji/
    ├── NotoColorEmoji.ttf    # Google's Noto Color Emoji (recommended)
    ├── Twemoji.woff2        # Twitter's Twemoji font
    └── README.txt           # Setup instructions
```

#### **Adding Emoji Fonts**
1. **Download Noto Color Emoji** from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Color+Emoji)
2. **Save as** `NotoColorEmoji.ttf` in the `fonts/emoji/` directory
3. **Restart ComfyUI** - the nodes will automatically use the bundled font

#### **Benefits of Bundled Fonts**
- **Consistent Rendering**: Emojis look the same across Windows, macOS, and Linux
- **No Dependencies**: No need to install system emoji fonts
- **Reliable Support**: Emojis work even on systems without emoji fonts
- **Version Control**: Specific emoji font versions for predictable results

#### **Font Priority System**
The emoji support system uses fonts in this order:
1. **Bundled fonts** (fonts/emoji/) - Highest priority
2. **System emoji fonts** - Platform-specific fallback
3. **Default fonts** - Last resort

#### **Emoji Scaling Behavior**
- Emoji glyphs are sized based on the resolved text font size, ensuring consistent proportions when switching between default and custom fonts.
- When the active emoji font only supports a fixed render size (e.g., Noto Color Emoji), the renderer automatically rescales output to match the requested point size before compositing.
- PNG-based emoji fallbacks are rendered at the same pixel dimensions as text glyphs so mixed text/emoji lines align correctly.
- Word wrapping and layout calculations use the same emoji-aware width measurements as the renderer, preventing layout drift when varying font sizes or switching to custom fonts.

## Markdown Syntax Support

The markdown text overlay supports the following syntax:

### Basic Mode
- `**text**` - Bold text
- `*text*` - Italic text
- `__text__` - Underlined text
- `~~text~~` - Strikethrough text

### With Headers Mode
- All basic mode features
- `# Header 1` - Large header (rendered as bold)
- `## Header 2` - Medium header (rendered as bold)
- `### Header 3` - Small header (rendered as bold)

### Extended Mode
- All with_headers mode features
- `- item` or `* item` - List items (rendered with bullet points)
- `1. item` - Numbered list items
- `` `code` `` - Inline code (rendered as bold)

## Node Comparison & Usage Recommendations

### Node Feature Comparison

| Feature | Rich Text V1 | Rich Text V2 | Markdown |
|---------|--------------|--------------|----------|
| Basic Functionality | ✅ | ✅ | ✅ |
| Error Handling | ❌ | ✅ | ✅ |
| Progressive Font Scaling | ❌ | ✅ | ✅ |
| Visual Error Indicators | ❌ | ✅ | ❌ |
| Parameter Validation | ❌ | ✅ | ✅ |
| Console Feedback | ❌ | ✅ | ✅ |
| Hashtag Support | ❌ | ✅ | ✅ |
| Emoji Support | ❌ | ✅ | ✅ |
| Advanced Text Processing | ❌ | ✅ | ✅ |
| Backward Compatibility | ✅ | ✅ | ✅ |

### Usage Recommendations

#### **For New Projects**
- **Rich Text V2**: **RECOMMENDED** for modern applications with hashtag and emoji support
- **Markdown**: Use when you prefer markdown syntax over HTML-like tags

#### **For Existing Projects**
- **Rich Text V1**: Keep using for stability, migrate to V2 when needed
- **Rich Text V2**: Use for new features, hashtag/emoji support, or when encountering text overflow issues
- **Markdown**: Migrate to for markdown formatting with hashtag and emoji support

#### **For Production Use**
- **Rich Text V2**: **RECOMMENDED** for modern applications with hashtag and emoji support
- **Markdown**: Use for content that benefits from markdown formatting with hashtag and emoji support

#### **For Testing & Development**
- **Rich Text V1**: Use as baseline for comparison
- **Rich Text V2**: Use for enhanced features, error handling, hashtag and emoji support
- **Markdown**: Use for markdown-specific content testing with hashtag and emoji support

## Troubleshooting

### Common Issues & Solutions

#### **Text Not Rendering**
- **Problem**: Text appears too small or doesn't show
- **Solution**: Check console for scaling messages. The system automatically scales down font sizes when needed.

#### **Font Loading Errors**
- **Problem**: Font files not found
- **Solution**: Use system font paths or enable error indicators to see fallback behavior.

#### **Text Overflow**
- **Problem**: Text doesn't fit in specified box
- **Solution**: The system automatically handles this with progressive scaling and truncation.

#### **Performance Issues**
- **Problem**: Slow rendering with large text
- **Solution**: Use V2 nodes which include optimized error handling and caching.

### Console Messages

The system provides helpful console feedback:

```
# Normal operation
APZmediaImageRichTextOverlayV2 initialized with enhanced error handling

# Warning messages
Warning: Text overflow detected at font size 30
Warning: Word 'supercalifragilisticexpialidocious' is too long

# Scaling feedback
Font scaling fallback: Font scaled to 12 (Reduced by 18)
Markdown font scaling fallback: Text truncated to 50 chars

# Error indicators
Text overflow - all scaling strategies failed
```

### Getting Help

- **Check Console**: Always check console output for detailed feedback
- **Enable Error Indicators**: Use `show_error_indicators = true` to see visual error messages
- **Try Different Nodes**: Use V2 nodes for enhanced error handling
- **Adjust Parameters**: Reduce font size or increase text box dimensions if needed
