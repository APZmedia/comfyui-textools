#!/usr/bin/env python3
"""
Create a comprehensive test text with all markdown features, emojis, and formatting cases.
"""

def create_comprehensive_test_text():
    """Create a comprehensive test text with all features."""
    
    test_text = """# Welcome to APZmedia Text Tools! 🎉

This is a **comprehensive test** of all markdown features and emoji support. Let's see how well our text rendering handles various scenarios:

## Text Formatting Examples

Here we have *italic text* and **bold text** working together. We can also use __underline__ and ~~strikethrough~~ formatting.

### Hashtag Support
Our system supports #hashtags automatically with blue styling. You can use multiple #hashtags in the same text like #texttools #comfyui #markdown.

### Emoji Integration
Emojis work seamlessly with text: Hello 😀 World! We support single emojis like 🎨 and multiple emojis together: 😀😀😀. Even complex emojis like 🚀 work perfectly.

## Lists and Enumerations

### Unordered Lists
- First item with **bold text**
- Second item with *italic text*
- Third item with #hashtag
- Fourth item with 😀 emoji
- Fifth item with **bold** and *italic* combined

### Ordered Lists
1. First numbered item
2. Second item with **bold formatting**
3. Third item with #hashtag support
4. Fourth item with 😀 emoji
5. Fifth item with mixed formatting: **bold** *italic* #hashtag 😀

## Complex Scenarios

### Mixed Formatting
This paragraph contains **bold text**, *italic text*, __underline__, ~~strikethrough~~, #hashtags, and 😀 emojis all in one sentence.

### Line Breaks and Spacing
This is the first line.
This is the second line with **bold text**.

This is a new paragraph with *italic text* and #hashtag support.

### Edge Cases
- Empty lines above and below
- Multiple spaces:    four    spaces
- Special characters: @#$%^&*()
- Unicode characters: café, naïve, résumé
- Numbers: 123, 456.789, 1,000,000

## Final Test
This is the final paragraph with **bold**, *italic*, __underline__, ~~strikethrough~~, #hashtag, and 😀 emoji all working together perfectly! 🎉"""

    return test_text

def main():
    """Main function to display the test text."""
    print("=== Comprehensive Test Text ===")
    print()
    
    test_text = create_comprehensive_test_text()
    print(test_text)
    print()
    
    print("=== Text Statistics ===")
    print(f"Total characters: {len(test_text)}")
    print(f"Total lines: {len(test_text.split(chr(10)))}")
    print(f"Contains hashtags: {'#' in test_text}")
    print(f"Contains emojis: {any(ord(char) > 127 for char in test_text)}")
    print(f"Contains bold: {'**' in test_text}")
    print(f"Contains italic: {'*' in test_text}")
    print(f"Contains underline: {'__' in test_text}")
    print(f"Contains strikethrough: {'~~' in test_text}")
    print(f"Contains headers: {'#' in test_text}")
    print(f"Contains lists: {'-' in test_text or any(line.strip().startswith(str(i) + '.') for i in range(1, 10) for line in test_text.split(chr(10)))}")

if __name__ == "__main__":
    main()
