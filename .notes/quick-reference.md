# Quick Reference Guide

## Common Tasks

### 1. Adding a New Text Style

```python
# 1. Update parser regex
tag_re = re.compile(r'<(/?)(b|i|u|s|newstyle)>')

# 2. Add to style dictionary
styles = {'b': False, 'i': False, 'u': False, 's': False, 'newstyle': False}

# 3. Update font manager
def get_font_for_style(self, style, font_size):
    if style.get('newstyle', False):
        return self.get_newstyle_font(font_size)
    # ... existing code

# 4. Update renderer
def render_text_with_style(draw, text, style, font, color):
    if style.get('newstyle', False):
        # Add new style rendering logic
        pass
```

### 2. Adding a New Node Parameter

```python
# 1. Add to INPUT_TYPES
"new_param": ("STRING", {"default": "default_value"}),

# 2. Update method signature
def apz_add_text_overlay(self, ..., new_param):

# 3. Use in method body
# Process new_param as needed
```

### 3. Font Path for Different OS

```python
# Windows
"C:/Windows/Fonts/arial.ttf"

# Linux
"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# macOS
"/System/Library/Fonts/Arial.ttf"

# Automatic system detection
error_handler = ErrorHandlerUtility()
system_fonts = error_handler.get_system_font_paths()
```

## Code Snippets

### Color Conversion
```python
# Hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# RGB to Hex
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)
```

### Font Loading with Error Handling
```python
def load_font_safe(font_path, font_size):
    try:
        return ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"Font not found: {font_path}")
        # Fallback to default font
        return ImageFont.load_default()
```

### Text Wrapping
```python
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
```

## Troubleshooting

### Font Issues
**Problem**: Font not loading
```python
# Debug font loading
print(f"Font path: {font_path}")
print(f"Font exists: {os.path.exists(font_path)}")
```

**Solution**: Use enhanced error handling
```python
error_handler = ErrorHandlerUtility()
success, font_path_used, error_msg = error_handler.handle_font_loading_error(font_path)
if not success:
    print(f"Font error: {error_msg}")
```

### Color Issues
**Problem**: Invalid color format
```python
# Validate color format
def is_valid_hex_color(color):
    import re
    pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    return bool(re.match(pattern, color))
```

### Text Overflow Issues
**Problem**: Text doesn't fit in container
```python
# Enhanced error handling with progressive scaling
font_loader = EnhancedFontLoaderUtility(font_manager, max_font_size)
font_size, wrapped_lines, total_height, warnings = font_loader.find_fitting_font_size(
    text, width, height, line_ratio, text_type
)

# Enhanced font scaling fallback
error_handler = ErrorHandlerUtility()
success, scaled_size, processed_text, msg = error_handler.handle_font_scaling_fallback(
    text, box_width, box_height, original_size, font_manager, line_ratio, text_type
)

# Handle warnings
if warnings:
    for warning in warnings:
        print(f"Warning: {warning}")
```

### Performance Issues
**Problem**: Slow text rendering
```python
# Enable font caching
font_cache = {}
def get_cached_font(font_path, size):
    key = (font_path, size)
    if key not in font_cache:
        font_cache[key] = ImageFont.truetype(font_path, size)
    return font_cache[key]
```

## Common Patterns

### Batch Processing
```python
def process_batch(images, text, params):
    results = []
    for image in images:
        result = process_single_image(image, text, params)
        results.append(result)
    return torch.cat(results, dim=0)
```

### Parameter Validation
```python
def validate_params(params):
    if params['max_font_size'] < 1:
        raise ValueError("Font size must be positive")
    if not is_valid_hex_color(params['font_color']):
        raise ValueError("Invalid color format")
```

### Error Recovery
```python
def safe_text_rendering(draw, text, font, color, fallback_color=(0,0,0)):
    try:
        draw.text((x, y), text, font=font, fill=color)
    except Exception as e:
        print(f"Text rendering failed: {e}")
        draw.text((x, y), text, font=font, fill=fallback_color)
```

## Development Commands

### Testing
```bash
# Run basic tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=utils tests/

# Performance test
python -m pytest tests/test_performance.py -v
```

### Installation
```bash
# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt

# Check for missing dependencies
pip check
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Debugging Tips

### Enable Debug Output
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"Processing text: {text}")
logger.info(f"Font loaded: {font_path}")
logger.warning(f"Fallback to default font")
```

### Visual Debugging
```python
# Draw debug rectangles
def draw_debug_box(draw, x, y, w, h, color=(255,0,0)):
    draw.rectangle([x, y, x+w, y+h], outline=color, width=2)

# Show text boundaries
def draw_text_bounds(draw, text, font, x, y, color=(0,255,0)):
    bbox = font.getbbox(text)
    draw.rectangle(bbox, outline=color, width=1)
```

### Memory Profiling
```python
import tracemalloc
tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
tracemalloc.stop()
```

## Quick Fixes

### Fix Font Path Issues
```python
# Add to font manager
def get_system_font_path(self):
    import platform
    if platform.system() == "Windows":
        return "C:/Windows/Fonts/arial.ttf"
    elif platform.system() == "Linux":
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    else:  # macOS
        return "/System/Library/Fonts/Arial.ttf"
```

### Fix Color Issues
```python
# Add to color utility
def normalize_color(self, color):
    if color.startswith('#'):
        return color
    elif color in ['red', 'blue', 'green']:
        return {'red': '#FF0000', 'blue': '#0000FF', 'green': '#00FF00'}[color]
    else:
        return '#000000'  # Default to black
```

### Fix Performance Issues
```python
# Add cache size limit
MAX_CACHE_SIZE = 100
if len(self.font_cache) > MAX_CACHE_SIZE:
    # Remove oldest entries
    oldest_keys = list(self.font_cache.keys())[:10]
    for key in oldest_keys:
        del self.font_cache[key]
```

### Font Scaling Strategies
```python
# Progressive font scaling
scaling_strategies = [
    (original_size - 2, "Reduced by 2"),
    (original_size - 4, "Reduced by 4"),
    (original_size - 6, "Reduced by 6"),
    (6, "Minimum readable"),
    (4, "Very small"),
    (2, "Tiny")
]

# Text truncation strategies
truncation_strategies = [
    (text[:100] + "...", "100 chars"),
    (text[:50] + "...", "50 chars"),
    (text[:25] + "...", "25 chars"),
    ("Text overflow", "error message")
]
``` 