import unittest

from utils.apz_markdown_renderer_utility import MarkdownRendererUtility
from utils.apz_markdown_parser import parse_markdown


class DummyFont:
    """Lightweight font stub that provides the bbox/size interface used by the renderer."""
    def __init__(self, font_size: int):
        self.font_size = max(font_size, 1)

    def getbbox(self, text: str):
        width = len(text) * max(self.font_size // 2, 1)
        return (0, 0, width, self.font_size)

    def getsize(self, text: str):
        width = len(text) * max(self.font_size // 2, 1)
        return (width, self.font_size)


class DummyEmojiSupport:
    """Emoji support shim that disables emoji-specific behavior for these unit tests."""
    def has_emoji(self, text: str) -> bool:
        return False

    def get_emoji_font(self, font_size: int):
        return None

    def test_emoji_support(self, font) -> bool:
        return False

    def should_use_embedded_color(self, font) -> bool:
        return False

    def is_color_font(self, font) -> bool:
        return False


class DummyFontManager:
    """Font manager stub that supplies dummy font instances to the markdown renderer."""
    def __init__(self):
        self.emoji_support = DummyEmojiSupport()

    def get_font_for_style(self, styles: dict, font_size: int, text: str = ""):
        return DummyFont(font_size)

    def should_use_embedded_color(self, font) -> bool:
        return False


class MarkdownRendererLineBreakTests(unittest.TestCase):
    """Validates markdown renderer behavior for explicit line breaks and spacing."""
    def setUp(self):
        self.font_manager = DummyFontManager()
        self.font_size = 20
        self.max_width = 4096  # Large width to avoid wrapping interfering with tests

    def _line_texts(self, lines):
        """Helper to convert parsed line tuples into plain strings for assertions."""
        return ["".join(part for part, _ in line) for line in lines]

    def test_preserves_blank_line_between_content(self):
        text = "Line 1\n\nLine 3"
        parsed = parse_markdown(text)
        lines = MarkdownRendererUtility._process_parsed_parts(parsed, self.max_width, self.font_manager, self.font_size)

        self.assertEqual(len(lines), 3, "Two text lines plus one blank line should be produced")
        line_texts = self._line_texts(lines)
        self.assertEqual(line_texts[0].strip(), "Line 1")
        self.assertEqual(line_texts[1], "", "Middle blank line should be preserved as an empty render line")
        self.assertEqual(line_texts[2].strip(), "Line 3")

    def test_preserves_leading_and_trailing_blank_lines(self):
        text = "\nHello World\n"
        parsed = parse_markdown(text)
        lines = MarkdownRendererUtility._process_parsed_parts(parsed, self.max_width, self.font_manager, self.font_size)

        self.assertEqual(len(lines), 3, "Blank, content, blank should result in three lines")
        line_texts = self._line_texts(lines)
        self.assertEqual(line_texts[0], "", "Leading newline should become an empty line")
        self.assertEqual(line_texts[1].strip(), "Hello World")
        self.assertEqual(line_texts[2], "", "Trailing newline should become an empty line")

    def test_total_height_counts_blank_lines(self):
        text = "Top\n\nBottom"
        dimensions = MarkdownRendererUtility.calculate_markdown_text_dimensions(
            text=text,
            markdown_mode="basic",
            font_manager=self.font_manager,
            font_size=self.font_size,
            line_height_ratio=1.0,
            max_width=self.max_width,
        )
        expected_lines = 3  # Two content lines and a blank separator line
        expected_height = expected_lines * self.font_size

        self.assertEqual(
            dimensions[1],
            expected_height,
            "Vertical measurements should include preserved blank lines",
        )


if __name__ == "__main__":
    unittest.main()
