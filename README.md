# ComfyUI-textools

**ComfyUI-textools** is a collection of custom nodes designed for use with ComfyUI. These nodes enhance text processing capabilities, including applying rich text overlays on images and cleaning file names for safe and consistent file management.

## Overview

ComfyUI-textools includes several custom nodes, such as:

- **APZmedia Image Rich Text Overlay**: A node for overlaying rich text on images with support for bold, italic, underline, and strike-through styles.

## Features

### APZmedia Image Rich Text Overlay
- **Rich Text Support**: Allows the addition of bold, italic, underline, and strike-through text on images.
- **Customizable Fonts**: Supports different fonts for regular, bold, and italic text from a specific url so you can use your already installed fonts.
- **Alignment Options**: Supports text alignment (left, right, center) and vertical alignment (top, middle, bottom).
- **Text Wrapping**: Automatically wraps text within a defined box area.

## Input Types

### APZmedia Image Rich Text Overlay
- **image (IMAGE)**: The image to which the text will be applied.
- **theText (STRING)**: The rich text string to overlay on the image, with support for HTML-like tags (e.g., `<b>`, `<i>`, etc.).
- **theTextbox_width (INT)**: Width of the text box.
- **theTextbox_height (INT)**: Height of the text box.
- **max_font_size (INT)**: Maximum font size to use.
- **font (STRING)**: Path to the font file.
- **italic_font (STRING)**: Path to the italic font file.
- **bold_font (STRING)**: Path to the bold font file.
- **alignment (STRING)**: Horizontal text alignment (left, right, center).
- **vertical_alignment (STRING)**: Vertical text alignment (top, middle, bottom).
- **font_color (STRING)**: Color of the font.
- **italic_font_color (STRING)**: Color of the italic font.
- **bold_font_color (STRING)**: Color of the bold font.
- **box_start_x (INT)**: X-coordinate for the text box's starting position.
- **box_start_y (INT)**: Y-coordinate for the text box's starting position.
- **padding (INT)**: Padding inside the text box.
- **line_height_ratio (FLOAT)**: Ratio for line height relative to font size.

## Output Types

### APZmedia Image Rich Text Overlay
- **image (IMAGE)**: The image with the applied text overlay.

## How It Works

### APZmedia Image Rich Text Overlay
1. **Text Wrapping**: Automatically wraps the provided text within the specified width and height.
2. **Rich Text Processing**: Processes tags like `<b>` for bold and `<i>` for italic, applying the appropriate styles.
3. **Text Overlay**: Draws the text onto the image with the specified alignment and font settings.
4. **Text Box**: Draws a box around the text with the specified padding and line height ratio.
5.  **Output**: Returns the image with the text overlay applied.

