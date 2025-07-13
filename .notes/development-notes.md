# Development Notes

## Code Architecture Patterns

### 1. Utility-Based Design
The project follows a utility-based architecture where each utility class has a single responsibility:
- **Separation of Concerns**: Each utility handles one specific aspect (fonts, colors, text parsing, etc.)
- **Modularity**: Easy to test and modify individual components
- **Reusability**: Utilities can be used across different nodes

### 2. Font Management Pattern
```python
# Font caching for performance
self.font_cache = {}
def load_font(self, font_path, font_size):
    if (font_path, font_size) not in self.font_cache:
        font = ImageFont.truetype(font_path, font_size)
        self.font_cache[(font_path, font_size)] = font
    return self.font_cache[(font_path, font_size)]
```

### 3. Rich Text Parsing Pattern
Uses regex-based parsing with style stack management:
```python
tag_re = re.compile(r'<(/?)(b|i|u|s)>')
style_stack = []  # Maintains style hierarchy
```

### 4. Error Handling Pattern
Comprehensive fallback system with multiple strategies:
```python
# Enhanced font loader with error handling
font_size, wrapped_lines, total_height, warnings = font_loader.find_fitting_font_size(
    text, width, height, line_ratio, text_type
)

# Error handler with fallback strategies
error_handler = ErrorHandlerUtility()
fallback_text, fallback_size, error_msg = error_handler.handle_text_overflow_error(
    text, box_width, box_height, font_size, warnings
)

# Enhanced font scaling fallback
success, scaled_font_size, processed_text, scaling_msg = error_handler.handle_font_scaling_fallback(
    text, box_width, box_height, original_font_size, font_manager, line_ratio, text_type
)
```

## Key Technical Decisions

### 1. Image Format Handling
- **Input**: ComfyUI tensors (torch.Tensor)
- **Processing**: Convert to PIL for text operations
- **Output**: Convert back to tensors for ComfyUI compatibility

### 2. Font Path Management
- Default paths point to system fonts (Linux DejaVu)
- Windows compatibility needs font path adjustments
- Consider using relative paths or font discovery

### 3. Color System
- Uses hex color strings for user input
- Converts to RGB tuples for PIL operations
- Supports alpha channel for transparency

## Development Guidelines

### 1. Adding New Text Styles
To add a new text style (e.g., outline, shadow):

1. **Update Parser** (`apz_rich_text_parser.py`):
   ```python
   tag_re = re.compile(r'<(/?)(b|i|u|s|outline|shadow)>')
   ```

2. **Update Font Manager** (`apz_font_manager.py`):
   ```python
   def get_font_for_style(self, style, font_size):
       if style.get('outline', False):
           return self.get_outline_font(font_size)
   ```

3. **Update Renderer** (`apz_text_renderer_utility.py`):
   ```python
   # Add rendering logic for new style
   ```

### 2. Adding New Node Parameters
When adding new parameters to the main node:

1. **Update INPUT_TYPES**:
   ```python
   "new_parameter": ("STRING", {"default": "default_value"}),
   ```

2. **Update Method Signature**:
   ```python
   def apz_add_text_overlay(self, ..., new_parameter):
   ```

3. **Update Documentation** in README.md

### 3. Performance Considerations
- **Font Caching**: Already implemented, prevents repeated font loading
- **Batch Processing**: Handles multiple images in tensor batches
- **Memory Management**: Consider clearing font cache for large font sets

## Common Issues and Solutions

### 1. Font Path Issues
**Problem**: Font files not found on different operating systems
**Solution**: 
- Use font discovery libraries
- Provide fallback fonts
- Allow relative paths
- **Enhanced**: Automatic system font detection and fallback

### 2. Text Overflow
**Problem**: Text doesn't fit in specified box
**Solution**: 
- Implement font size reduction algorithm
- Add text truncation options
- Provide overflow indicators
- **Enhanced**: Multi-strategy fallback with visual error indicators
- **Enhanced**: Progressive font scaling (down to 2px)
- **Enhanced**: Intelligent text truncation strategies

### 3. Word Too Long
**Problem**: Individual words exceed container width
**Solution**:
- Word hyphenation
- Font size reduction
- Text truncation
- **Enhanced**: Automatic word breaking and hyphenation
- **Enhanced**: Progressive font scaling for long words
- **Enhanced**: Word truncation with ellipsis

### 4. Color Format Issues
**Problem**: Invalid color strings
**Solution**: 
- Add color validation in ColorUtility
- Provide color picker in ComfyUI
- Support named colors
- **Enhanced**: Comprehensive color validation and fallback

## Testing Strategy

### 1. Unit Tests Needed
- Text parsing with various tag combinations
- Font loading and caching
- Color conversion utilities
- Text wrapping algorithms
- Error handling scenarios
- Fallback mechanism validation
- Word length validation

### 2. Integration Tests
- End-to-end text overlay functionality
- Different image formats and sizes
- Various font combinations
- Error recovery scenarios
- Fallback text rendering
- Cross-platform font compatibility

### 3. Performance Tests
- Large text processing
- Multiple font sizes
- Batch image processing
- Error handling overhead
- Fallback mechanism performance
- Memory usage under error conditions

## Future Enhancements

### 1. Text Effects
- **Drop Shadows**: Add shadow rendering
- **Outlines**: Text outline effects
- **Gradients**: Gradient text colors
- **Animations**: Text animation support

### 2. Font Features
- **Variable Fonts**: Support for variable font technology
- **Font Fallbacks**: Automatic font substitution
- **Web Fonts**: Download and cache web fonts

### 3. Layout Improvements
- **Text Flow**: Around objects, in shapes
- **Advanced Alignment**: Justified text, vertical text
- **Text Paths**: Text along curves

### 4. Performance Optimizations
- **GPU Acceleration**: Use GPU for text rendering
- **Parallel Processing**: Multi-threaded text processing
- **Memory Optimization**: Better memory management for large images

## Debugging Tips

### 1. Enable Debug Output
```python
# Add debug prints in utilities
print(f"Debug: Processing text '{text}' with styles {styles}")
```

### 2. Visual Debugging
- Use bounding box visualization
- Add text position indicators
- Show font loading status

### 3. Common Debug Points
- Font loading failures
- Text parsing errors
- Color conversion issues
- Image format problems 