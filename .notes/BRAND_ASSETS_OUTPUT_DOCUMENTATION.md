# Brand Asset Loader Output Documentation

## Overview

The `APZmediaBrandAssetLoader` node provides comprehensive brand asset management with multiple output formats. This documentation explains how to read and use the various output fields from the brand asset loader in other ComfyUI nodes.

## Output Structure

The Brand Asset Loader node provides **23 output fields** organized into different categories:

### 1. Brand Assets Dictionary (Primary Output)
- **Type**: `BRAND_ASSETS`
- **Name**: `brand_assets`
- **Description**: Complete dictionary containing all brand assets and metadata
- **Usage**: Connect to other nodes that need access to all brand assets

### 2. Logo Assets (Images + Masks)
- **logo_vertical_color** (IMAGE): Vertical color logo image
- **logo_vertical_color_mask** (MASK): Alpha mask for vertical color logo
- **logo_vertical_mono** (IMAGE): Vertical monochrome logo image
- **logo_vertical_mono_mask** (MASK): Alpha mask for vertical monochrome logo
- **logo_horizontal_color** (IMAGE): Horizontal color logo image
- **logo_horizontal_color_mask** (MASK): Alpha mask for horizontal color logo
- **logo_horizontal_mono** (IMAGE): Horizontal monochrome logo image
- **logo_horizontal_mono_mask** (MASK): Alpha mask for horizontal monochrome logo
- **logo_icon** (IMAGE): Icon logo image
- **logo_icon_mask** (MASK): Alpha mask for icon logo

### 3. Font Assets (String Paths)
- **font_primary** (STRING): Primary font file path
- **font_primary_bold** (STRING): Primary bold font file path
- **font_primary_italic** (STRING): Primary italic font file path
- **font_secondary** (STRING): Secondary font file path
- **font_secondary_bold** (STRING): Secondary bold font file path
- **font_secondary_italic** (STRING): Secondary italic font file path
- **font_tertiary** (STRING): Tertiary font file path
- **font_tertiary_bold** (STRING): Tertiary bold font file path
- **font_tertiary_italic** (STRING): Tertiary italic font file path

### 4. Brand Metadata
- **color_palette** (STRING): JSON string containing color palette
- **brand_name** (STRING): Name of the brand
- **status_message** (STRING): Status message about asset loading

## Using Brand Assets in Other Nodes

### Method 1: Direct Field Connection

Connect specific output fields directly to other nodes:

```
Brand Asset Loader
├── logo_vertical_color → Logo Placement Node
├── font_primary → Text Node
├── color_palette → Color Processing Node
└── brand_name → Display Node
```

### Method 2: Brand Assets Dictionary

Use the `brand_assets` output with nodes that can read the dictionary:

```
Brand Asset Loader
└── brand_assets → Font Selector Node
                  → Logo Overlay Node
                  → Color Palette Node
```

### Method 3: Global Brand Access

Use the `APZmediaGlobalBrandAccess` node to retrieve assets without direct connections:

```
Global Brand Access Node
├── asset_type: "logo"
├── logo_type: "vertical_color"
└── include_mask: True
```

## Brand Assets Dictionary Structure

The `brand_assets` dictionary contains the following structure:

```python
{
    # Logo assets (torch.Tensor)
    "logo_vertical_color": torch.Tensor,
    "logo_vertical_color_mask": torch.Tensor,
    "logo_vertical_mono": torch.Tensor,
    "logo_vertical_mono_mask": torch.Tensor,
    "logo_horizontal_color": torch.Tensor,
    "logo_horizontal_color_mask": torch.Tensor,
    "logo_horizontal_mono": torch.Tensor,
    "logo_horizontal_mono_mask": torch.Tensor,
    "logo_icon": torch.Tensor,
    "logo_icon_mask": torch.Tensor,
    
    # Font paths (string)
    "font_primary": str,
    "font_primary_bold": str,
    "font_primary_italic": str,
    "font_secondary": str,
    "font_secondary_bold": str,
    "font_secondary_italic": str,
    "font_tertiary": str,
    "font_tertiary_bold": str,
    "font_tertiary_italic": str,
    
    # Brand metadata
    "color_palette": str,  # JSON string
    "brand_name": str,
    "status_message": str
}
```

## Color Palette Format

The `color_palette` field contains a JSON string with the following structure:

```json
[
    {
        "name": "Primary Blue",
        "hex": "#0066CC",
        "id": "primary-blue"
    },
    {
        "name": "Secondary Gray",
        "hex": "#666666",
        "id": "secondary-gray"
    },
    {
        "name": "Accent Orange",
        "hex": "#FF6600",
        "id": "accent-orange"
    }
]
```

## Common Usage Patterns

### 1. Logo Placement Workflow

```
Brand Asset Loader
├── logo_vertical_color → Logo Placement Node (image input)
├── logo_vertical_color_mask → Logo Placement Node (mask input)
└── brand_name → Display Node
```

### 2. Font Selection Workflow

```
Brand Asset Loader
└── brand_assets → Font Selector Node
                  ├── font_type: "primary"
                  ├── font_variant: "bold"
                  └── output: font_path
```

### 3. Color Processing Workflow

```
Brand Asset Loader
├── color_palette → Color Parser Node
└── brand_name → Display Node
```

### 4. Multi-Asset Workflow

```
Brand Asset Loader
├── brand_assets → Font Selector Node
├── logo_vertical_color → Logo Overlay Node
├── color_palette → Color Processing Node
└── brand_name → Display Node
```

## Node Integration Examples

### Font Selector Node Integration

```python
# In your custom node
def process_font(self, brand_assets):
    # Extract font path from brand assets
    font_path = brand_assets.get("font_primary", "")
    if font_path:
        # Use the font path
        return font_path
    return ""
```

### Logo Processing Node Integration

```python
# In your custom node
def process_logo(self, brand_assets):
    # Extract logo and mask
    logo_image = brand_assets.get("logo_vertical_color")
    logo_mask = brand_assets.get("logo_vertical_color_mask")
    
    if logo_image is not None and logo_mask is not None:
        # Process logo with mask
        return self.apply_mask(logo_image, logo_mask)
    return None
```

### Color Palette Processing

```python
import json

# In your custom node
def process_colors(self, brand_assets):
    color_palette_json = brand_assets.get("color_palette", "[]")
    try:
        colors = json.loads(color_palette_json)
        # Process color palette
        return colors
    except json.JSONDecodeError:
        return []
```

## Error Handling

### Checking Asset Availability

```python
def check_asset_availability(self, brand_assets):
    # Check if assets are loaded
    status = brand_assets.get("status_message", "")
    if "Error" in status or "Failed" in status:
        return False
    
    # Check specific asset
    logo = brand_assets.get("logo_vertical_color")
    if logo is None:
        return False
    
    return True
```

### Fallback Values

```python
def get_font_with_fallback(self, brand_assets, font_type, variant):
    # Try to get specific font
    font_key = f"font_{font_type}_{variant}" if variant else f"font_{font_type}"
    font_path = brand_assets.get(font_key, "")
    
    # Fallback to regular variant
    if not font_path and variant != "regular":
        font_path = brand_assets.get(f"font_{font_type}", "")
    
    # Fallback to primary font
    if not font_path and font_type != "primary":
        font_path = brand_assets.get("font_primary", "")
    
    return font_path
```

## Best Practices

### 1. Always Check Asset Availability
- Check `status_message` for loading errors
- Verify asset existence before processing
- Use fallback values when assets are missing

### 2. Use Appropriate Output Types
- Use `IMAGE` outputs for logo processing nodes
- Use `STRING` outputs for font path nodes
- Use `BRAND_ASSETS` for comprehensive asset access

### 3. Handle Empty Assets
- Check for `None` values in image tensors
- Check for empty strings in font paths
- Provide meaningful error messages

### 4. Optimize Performance
- Use specific field connections when possible
- Avoid processing unused assets
- Cache frequently accessed assets

## Troubleshooting

### Common Issues

1. **Empty Assets**: Check if brand assets were loaded successfully
2. **Invalid Paths**: Verify font file paths exist and are accessible
3. **Image Format**: Ensure logo images are in the correct tensor format
4. **Color Palette**: Validate JSON format of color palette

### Debug Information

```python
def debug_brand_assets(self, brand_assets):
    print(f"Brand Name: {brand_assets.get('brand_name', 'Unknown')}")
    print(f"Status: {brand_assets.get('status_message', 'No status')}")
    
    # Check logo availability
    logos = ['logo_vertical_color', 'logo_horizontal_color', 'logo_icon']
    for logo in logos:
        has_logo = brand_assets.get(logo) is not None
        print(f"{logo}: {'Available' if has_logo else 'Missing'}")
    
    # Check font availability
    fonts = ['font_primary', 'font_secondary', 'font_tertiary']
    for font in fonts:
        font_path = brand_assets.get(font, "")
        print(f"{font}: {'Available' if font_path else 'Missing'}")
```

## Conclusion

The Brand Asset Loader provides comprehensive access to all brand assets through multiple output formats. Choose the appropriate method based on your specific use case:

- **Direct field connection** for specific assets
- **Brand assets dictionary** for comprehensive access
- **Global brand access** for flexible asset retrieval

Always implement proper error handling and fallback mechanisms to ensure robust workflows.
