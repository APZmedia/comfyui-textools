ComfyUI-textools Bundled Emoji Fonts
====================================

This directory contains bundled emoji fonts for consistent emoji rendering across all platforms.

Current Fonts:
- SegoeUIEmoji.ttf (Windows Segoe UI Emoji - Primary)
- NotoColorEmoji-Regular.ttf (Google's Noto Color Emoji - Fallback)

These fonts provide comprehensive Unicode emoji support including:
- Basic emojis (😀 🎉 🚀 🎨)
- Extended emoji sets
- Regional flag emojis
- Skin tone variations
- Gender variations

The fonts are automatically used by ComfyUI-textools nodes when emoji support is enabled.
They provide consistent emoji rendering across all platforms (Windows, macOS, Linux).

Font Priority:
1. SegoeUIEmoji.ttf (Windows emoji font - most reliable)
2. NotoColorEmoji-Regular.ttf (Google's Noto Color Emoji)
3. System fonts (fallback)

For more information:
- Segoe UI Emoji: Microsoft's Windows emoji font
- Google Fonts: https://fonts.google.com/noto/specimen/Noto+Color+Emoji
- GitHub: https://github.com/googlefonts/noto-emoji
- License: Open Font License (free to distribute)