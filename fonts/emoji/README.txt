ComfyUI-textools Bundled Emoji Fonts
====================================

This directory contains bundled emoji fonts for consistent emoji rendering across all platforms.

Current Fonts:
- NotoColorEmoji-Color.ttf (Google's Noto Color Emoji - Primary, Color)
- SegoeUIEmoji.ttf (Windows Segoe UI Emoji - Fallback, Monochrome)
- NotoColorEmoji-Regular.ttf (Google's Noto Color Emoji - Alternative)

These fonts provide comprehensive Unicode emoji support including:
- Basic emojis (😀 🎉 🚀 🎨)
- Extended emoji sets
- Regional flag emojis
- Skin tone variations
- Gender variations

The fonts are automatically used by ComfyUI-textools nodes when emoji support is enabled.
They provide consistent emoji rendering across all platforms (Windows, macOS, Linux).

Font Priority:
1. NotoColorEmoji-Color.ttf (Color emoji font - serverless compatible)
2. SegoeUIEmoji.ttf (Windows emoji font - monochrome fallback)
3. NotoColorEmoji-Regular.ttf (Google's Noto Color Emoji - alternative)
4. System fonts (fallback)

Special Features:
- NotoColorEmoji uses fixed size 109 with automatic scaling
- Color emoji support for serverless environments
- Cross-platform compatibility

For more information:
- Segoe UI Emoji: Microsoft's Windows emoji font
- Google Fonts: https://fonts.google.com/noto/specimen/Noto+Color+Emoji
- GitHub: https://github.com/googlefonts/noto-emoji
- License: Open Font License (free to distribute)