# API Reference

## Main Node: APZmediaImageRichTextOverlay

### Class Definition
```python
class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu")
```

### Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image` | IMAGE | - | Input image tensor |
| `theText` | STRING | "Hello <b>World</b> <i>This is italic</i>" | Rich text with HTML-like tags |
| `theTextbox_width` | INT | 200 | Width of text box |
| `theTextbox_height` | INT | 200 | Height of text box |
| `max_font_size` | INT | 30 | Maximum font size (1-256) |
| `font` | STRING | "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" | Regular font path |
| `italic_font` | STRING | "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf" | Italic font path |
| `bold_font` | STRING | "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" | Bold font path |
| `alignment` | STRING | "center" | Horizontal alignment (left/right/center) |
| `vertical_alignment` | STRING | "middle" | Vertical alignment (top/middle/bottom) |
| `font_color` | STRING | "#000000" | Regular text color (hex) |
| `italic_font_color` | STRING | "#000000" | Italic text color (hex) |
| `bold_font_color` | STRING | "#000000" | Bold text color (hex) |
| `box_start_x` | INT | 0 | X coordinate of text box |
| `box_start_y` | INT | 0 | Y coordinate of text box |
| `padding` | INT | 50 | Internal padding of text box |
| `line_height_ratio` | FLOAT | 1.2 | Line height multiplier |
| `show_bounding_box` | STRING | "false" | Show bounding box (true/false) |
| `bounding_box_color` | STRING | "#FF0000" | Bounding box color (hex) |
| `line_width` | INT | 3 | Bounding box line width (1-10) |
| `line_opacity` | FLOAT | 1.0 | Bounding box opacity (0.0-1.0) |
| `box_background_color` | STRING | "#FFFFFF" | Background color (hex) |
| `box_opacity` | FLOAT | 1.0 | Background opacity (0.0-1.0) |

### Output
- `image` (IMAGE): Image with text overlay applied

## Utility Classes

### ColorUtility

#### Methods
```python
def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]
```
Converts hex color string to RGB tuple.

**Parameters:**
- `hex_color` (str): Hex color string (e.g., "#FF0000")

**Returns:**
- `tuple[int, int, int]`: RGB values (0-255)

### FontManager

#### Constructor
```python
def __init__(self, regular_font_path: str, italic_font_path: str, bold_font_path: str, max_font_size: int)
```

#### Methods
```python
def load_font(self, font_path: str, font_size: int) -> ImageFont.FreeTypeFont
```
Loads and caches a font.

```python
def get_regular_font(self, font_size: int) -> ImageFont.FreeTypeFont
```
Gets regular font with specified size.

```python
def get_italic_font(self, font_size: int) -> ImageFont.FreeTypeFont
```
Gets italic font with specified size.

```python
def get_bold_font(self, font_size: int) -> ImageFont.FreeTypeFont
```
Gets bold font with specified size.

```python
def get_font_for_style(self, style: dict, font_size: int) -> ImageFont.FreeTypeFont
```
Gets appropriate font based on style dictionary.

### FontLoaderUtility

#### Constructor
```python
def __init__(self, font_manager: FontManager, max_font_size: int)
```

#### Methods
```python
def find_fitting_font_size(self, text: str, max_width: int, max_height: int, line_height_ratio: float) -> tuple[int, list, int]
```
Finds the largest font size that fits text in specified dimensions.

**Returns:**
- `tuple[int, list, int]`: (font_size, wrapped_lines, total_height)

### TextRendererUtility

#### Methods
```python
@staticmethod
def render_text(draw: ImageDraw.Draw, wrapped_lines: list, box_left: int, box_top: int, padding: int, box_width: int, box_height: int, font_manager: FontManager, color_utility: ColorUtility, alignment: str, vertical_alignment: str, line_height_ratio: float, font_color_rgb: tuple, italic_font_color_rgb: tuple, bold_font_color_rgb: tuple)
```
Renders text with specified styles and positioning.

### BoxUtility

#### Static Methods
```python
@staticmethod
def calculate_box_coordinates(start_x: int, start_y: int, width: int, height: int) -> tuple[int, int, int, int]
```
Calculates box coordinates (left, top, right, bottom).

```python
@staticmethod
def calculate_effective_box_coordinates(start_x: int, start_y: int, width: int, height: int, padding: int) -> tuple[int, int, int, int]
```
Calculates effective box coordinates with padding.

```python
@staticmethod
def draw_bounding_box(draw: ImageDraw.Draw, left: int, top: int, right: int, bottom: int, line_color: tuple, background_color: tuple, line_width: int)
```
Draws bounding box with specified colors and width.

### Image Conversion Utilities

#### Functions
```python
def tensor_to_pil(tensor: torch.Tensor) -> list[PIL.Image.Image]
```
Converts torch tensor to list of PIL images.

```python
def pil_to_tensor(pil_image: PIL.Image.Image) -> torch.Tensor
```
Converts PIL image to torch tensor.

### Rich Text Parser

#### Functions
```python
def parse_rich_text(theText: str) -> list[tuple[str, dict]]
```
Parses rich text with HTML-like tags.

**Parameters:**
- `theText` (str): Text with HTML-like tags

**Returns:**
- `list[tuple[str, dict]]`: List of (text, style_dict) tuples

**Supported Tags:**
- `<b>` / `</b>`: Bold text
- `<i>` / `</i>`: Italic text
- `<u>` / `</u>`: Underlined text
- `<s>` / `</s>`: Strikethrough text

## Data Types

### Style Dictionary
```python
{
    'b': bool,  # Bold
    'i': bool,  # Italic
    'u': bool,  # Underline
    's': bool   # Strikethrough
}
```

### Color Formats
- **Hex**: "#RRGGBB" or "#RRGGBBAA" (with alpha)
- **RGB**: (r, g, b) tuple with values 0-255
- **RGBA**: (r, g, b, a) tuple with values 0-255

### Alignment Options
- **Horizontal**: "left", "center", "right"
- **Vertical**: "top", "middle", "bottom"

## Error Handling

### Common Exceptions
1. **FontNotFoundError**: Font file not found
2. **ValueError**: Invalid color format
3. **OSError**: File system errors
4. **RuntimeError**: Text overflow or rendering issues

### Error Recovery
- Font loading failures fall back to system default
- Invalid colors default to black (#000000)
- Text overflow triggers font size reduction 