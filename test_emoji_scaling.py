import unittest

from utils.apz_markdown_renderer_utility import MarkdownRendererUtility
from utils.apz_text_wrapper import wrap_text


class DummyFont:
    """Minimal font stub providing the interface expected by width helpers."""
    def __init__(self, font_size: int):
        self.size = max(font_size, 1)

    def getbbox(self, text: str):
        width = len(text) * max(self.size // 2, 1)
        return (0, 0, width, self.size)

    def getsize(self, text: str):
        width = len(text) * max(self.size // 2, 1)
        return (width, self.size)


class DummyEmojiSupport:
    """Emoji support shim that reports 😀 as an emoji and splits text accordingly."""
    def has_emoji(self, text: str) -> bool:
        return "😀" in text

    def split_text_by_emoji(self, text: str):
        parts = []
        buffer = []
        for char in text:
            if self.has_emoji(char):
                if buffer:
                    parts.append(("".join(buffer), False))
                    buffer = []
                parts.append((char, True))
            else:
                buffer.append(char)
        if buffer:
            parts.append(("".join(buffer), False))
        return parts


class DummyFontManager:
    """Font manager stub that provides DummyFont instances and emoji support."""
    def __init__(self):
        self.emoji_support = DummyEmojiSupport()
        self.max_font_size = 64

    def get_font_for_style(self, styles: dict, font_size: int, text: str = ""):
        return DummyFont(font_size)

    def should_use_embedded_color(self, font) -> bool:
        return False


class EmojiScalingRegressionTests(unittest.TestCase):
    def setUp(self):
        self.font_manager = DummyFontManager()

    def test_measure_text_width_scales_with_font_size(self):
        large_size = 48
        small_size = 24

        large_width = MarkdownRendererUtility._measure_text_width(
            "😀", {}, self.font_manager, large_size
        )
        small_width = MarkdownRendererUtility._measure_text_width(
            "😀", {}, self.font_manager, small_size
        )

        self.assertEqual(large_width, large_size)
        self.assertEqual(small_width, small_size)
        self.assertGreater(large_width, small_width, "Emoji width should scale with requested font size")

    def test_measure_text_width_handles_mixed_text_and_emoji(self):
        font_size = 32
        width = MarkdownRendererUtility._measure_text_width(
            "A😀B", {}, self.font_manager, font_size
        )

        expected_text_width = font_size  # two letters at font_size // 2 each == font_size
        expected_emoji_width = font_size
        self.assertEqual(width, expected_text_width + expected_emoji_width)

    def test_wrap_text_uses_emoji_width_for_line_breaks(self):
        font_size = 30
        dummy_font = DummyFont(font_size)
        text = "😀 😀 😀"
        max_width = font_size + (font_size // 2)  # enough for one emoji plus trailing space

        wrapped_lines, _ = wrap_text(
            parsed_text=[(text, {"size": font_size})],
            font=dummy_font,
            max_width=max_width,
            line_height=int(font_size * 1.2),
            font_manager=self.font_manager,
        )

        self.assertGreaterEqual(len(wrapped_lines), 3, "Each emoji should wrap due to width constraints")
        for line, parts in wrapped_lines:
            self.assertLessEqual(
                len("".join(chunk for chunk, _ in parts).strip()),
                2,
                "Wrapped line should contain at most one emoji plus optional space",
            )


if __name__ == "__main__":
    unittest.main()
