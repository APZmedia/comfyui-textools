# Emoji Fonts for ComfyUI-textools

This directory contains emoji fonts bundled with ComfyUI-textools to ensure consistent emoji rendering across all platforms.

## Fonts Included

### Noto Color Emoji
- **File**: `NotoColorEmoji.ttf`
- **Source**: Google's Noto Color Emoji font
- **License**: Open Font License
- **Coverage**: Comprehensive Unicode emoji support

### Twemoji
- **File**: `Twemoji.woff2`
- **Source**: Twitter's Twemoji font
- **License**: CC-BY 4.0
- **Coverage**: Twitter's emoji set

## Usage

The ComfyUI-textools nodes automatically detect and use these bundled fonts before falling back to system fonts. This ensures:

1. **Consistent Rendering**: Emojis look the same across Windows, macOS, and Linux
2. **No Dependencies**: No need to install system emoji fonts
3. **Reliable Support**: Emojis work even on systems without emoji fonts

## Font Priority

The emoji support system uses fonts in this order:

1. **Bundled Noto Color Emoji** (primary)
2. **Bundled Twemoji** (fallback)
3. **System emoji fonts** (Windows Segoe UI Emoji, macOS Apple Color Emoji, Linux Noto)
4. **Default font** (last resort)

## Adding New Fonts

To add additional emoji fonts:

1. Place the font file in this directory
2. Update `utils/apz_emoji_support.py` to include the new font in the `_get_emoji_font_paths()` method
3. Test the font with the emoji support system

## License

These fonts are included under their respective open-source licenses:
- Noto Color Emoji: Open Font License
- Twemoji: CC-BY 4.0

For full license details, see the individual font files or their source repositories.
