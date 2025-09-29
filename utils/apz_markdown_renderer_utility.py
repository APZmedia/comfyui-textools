# markdown_renderer_utility.py
from PIL import Image, ImageDraw
from .apz_font_manager import FontManager
from .apz_color_utility import ColorUtility
from .apz_markdown_parser import parse_markdown, parse_markdown_with_headers, parse_markdown_extended

class MarkdownRendererUtility:
    """
    Utility class for rendering markdown text with proper styling and layout.
    """
    
    @staticmethod
    def _draw_text_with_color_support(draw, position, text, font, fill, font_manager):
        use_embedded_color = font_manager.should_use_embedded_color(font)
        if use_embedded_color:
            try:
                draw.text(position, text, font=font, embedded_color=True)
                return
            except TypeError:
                pass
            except Exception as exc:
                print(f"Warning: embedded color rendering failed, falling back to standard fill. Error: {exc}")
        draw.text(position, text, font=font, fill=fill)

    @staticmethod
    def _measure_text_width(text, styles, font_manager, font_size):
        """
        Compute the render width for a text chunk, accounting for emojis that may require PNG rendering.
        """
        if not text:
            return 0

        emoji_support = getattr(font_manager, "emoji_support", None)
        if emoji_support and emoji_support.has_emoji(text):
            total_width = 0
            for segment, is_emoji in emoji_support.split_text_by_emoji(text):
                if not segment:
                    continue
                if is_emoji:
                    total_width += font_size * len(segment)
                else:
                    segment_font = font_manager.get_font_for_style(styles, font_size, segment)
                    bbox = segment_font.getbbox(segment)
                    total_width += bbox[2] - bbox[0]
            return total_width

        measure_font = font_manager.get_font_for_style(styles, font_size, text)
        bbox = measure_font.getbbox(text)
        return bbox[2] - bbox[0]
    
    @staticmethod
    def render_markdown_text(draw, text, markdown_mode, box_left, box_top, padding, 
                           box_width, box_height, font_manager, color_utility, 
                           alignment, vertical_alignment, line_height_ratio,
                           font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, 
                           font_size):
        """
        Render markdown text with proper styling and layout.
        
        Args:
            draw: PIL ImageDraw object
            text: Markdown text to render
            markdown_mode: Mode of markdown parsing ("basic", "with_headers", "extended")
            box_left, box_top: Top-left corner of text box
            padding: Internal padding
            box_width, box_height: Dimensions of text box
            font_manager: FontManager instance
            color_utility: ColorUtility instance
            alignment: Horizontal alignment ("left", "center", "right")
            vertical_alignment: Vertical alignment ("top", "middle", "bottom")
            line_height_ratio: Line height multiplier
            font_color_rgb, italic_font_color_rgb, bold_font_color_rgb: Color tuples
            font_size: Base font size
        """
        # Parse markdown based on mode
        if markdown_mode == "basic":
            parsed_parts = parse_markdown(text)
        elif markdown_mode == "with_headers":
            parsed_parts = parse_markdown_with_headers(text)
        elif markdown_mode == "extended":
            parsed_parts = parse_markdown_extended(text)
        else:
            parsed_parts = parse_markdown(text)
        
        # Process parsed parts into renderable lines
        renderable_lines = MarkdownRendererUtility._process_parsed_parts(
            parsed_parts, box_width - 2 * padding, font_manager, font_size
        )
        
        # Calculate total height needed
        line_height = font_size * line_height_ratio
        total_height = len(renderable_lines) * line_height
        
        # Calculate starting Y position based on vertical alignment
        if vertical_alignment == "middle":
            start_y = box_top + (box_height - total_height) // 2
        elif vertical_alignment == "bottom":
            start_y = box_top + box_height - total_height - padding
        else:  # top
            start_y = box_top + padding
        
        # Render each line
        current_y = start_y
        for line in renderable_lines:
            if current_y + font_size > box_top + box_height - padding:
                break  # Stop if we exceed box height
                
            MarkdownRendererUtility._render_line(
                draw, line, box_left, current_y, padding, box_width,
                font_manager, color_utility, alignment, font_size,
                font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
            )
            current_y += line_height
    
    @staticmethod
    def _process_parsed_parts(parsed_parts, max_width, font_manager, font_size):
        """
        Process parsed markdown parts into renderable lines with proper wrapping.
        
        Args:
            parsed_parts: List of (text, styles) tuples from markdown parser
            max_width: Maximum width for text wrapping
            font_manager: FontManager instance
            font_size: Base font size
            
        Returns:
            List of renderable lines, where each line is a list of (text, styles) tuples
        """
        lines = []
        current_line = []
        current_line_width = 0

        for text_part, styles in parsed_parts:
            segments = text_part.split('\n')
            text_part_ends_with_newline = text_part.endswith('\n')

            for segment_index, segment in enumerate(segments):
                words = segment.split(' ') if segment else []

                for i, word in enumerate(words):
                    if not word:
                        continue

                    font = font_manager.get_font_for_style(styles, font_size, word)
                    bbox = font.getbbox(word)
                    word_width = bbox[2] - bbox[0]

                    space_width = 0
                    if i < len(words) - 1:
                        space_bbox = font.getbbox(' ')
                        space_width = space_bbox[2] - space_bbox[0]

                    if current_line_width + word_width + space_width <= max_width:
                        current_line.append((word, styles))
                        current_line_width += word_width

                        if i < len(words) - 1:
                            current_line.append((' ', styles))
                            current_line_width += space_width
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = [(word, styles)]
                        current_line_width = word_width

                        if i < len(words) - 1:
                            current_line.append((' ', styles))
                            current_line_width += space_width

                newline_requested = segment_index < len(segments) - 1 or (
                    segment_index == len(segments) - 1 and text_part_ends_with_newline
                )

                if newline_requested:
                    lines.append(current_line)
                    current_line = []
                    current_line_width = 0

        if current_line:
            lines.append(current_line)

        if not lines:
            lines.append([])

        return lines
    
    @staticmethod
    def _render_line(draw, line, box_left, y, padding, box_width, font_manager,
                    color_utility, alignment, font_size, font_color_rgb,
                    italic_font_color_rgb, bold_font_color_rgb):
        """
        Render a single line of markdown text.
        """
        # Calculate total line width
        total_line_width = 0
        for text_part, styles in line:
            measure_font = font_manager.get_font_for_style(styles, font_size)
            bbox = measure_font.getbbox(text_part)
            total_line_width += bbox[2] - bbox[0]

        # Calculate starting X position based on alignment
        if alignment == "center":
            x = box_left + (box_width - total_line_width) // 2
        elif alignment == "right":
            x = box_left + box_width - total_line_width - padding
        else:  # left
            x = box_left + padding

        current_x = x
        for text_part, styles in line:
            # Skip empty text parts
            if not text_part:
                continue
                
            current_font = font_manager.get_font_for_style(styles, font_size, text_part)

            if styles.get("hashtag", False):
                color = (0, 100, 200)
            elif styles.get("b", False):
                color = bold_font_color_rgb
            elif styles.get("i", False):
                color = italic_font_color_rgb
            else:
                color = font_color_rgb

            chunk_width = None

            if font_manager.emoji_support.has_emoji(text_part):
                # Split the text part into individual emojis if it contains multiple emojis
                emoji_parts = font_manager.emoji_support.split_text_by_emoji(text_part)
                
                for emoji_part, is_emoji in emoji_parts:
                    if is_emoji:
                        # Try to use PNG emoji renderer first
                        try:
                            from .apz_emoji_png_renderer import EmojiPNGRenderer
                            emoji_png_renderer = EmojiPNGRenderer()
                            emoji_img = emoji_png_renderer.load_emoji_png(emoji_part, font_size)
                            
                            if emoji_img:
                                # Scale emoji to match font size
                                if emoji_img.size != (font_size, font_size):
                                    emoji_img = emoji_img.resize((font_size, font_size), Image.Resampling.LANCZOS)
                                
                                # Calculate proper Y position to align with text baseline
                                # Position emoji slightly lower to align better with text
                                emoji_y = int(y + font_size - emoji_img.height + 5)
                                # Paste emoji PNG onto the image
                                draw._image.paste(emoji_img, (int(current_x), emoji_y), emoji_img)
                                current_x += font_size  # Move to next position
                            else:
                                # Fallback to regular text rendering
                                MarkdownRendererUtility._draw_text_with_color_support(
                                    draw, (current_x, y), emoji_part, current_font, color, font_manager
                                )
                                bbox = current_font.getbbox(emoji_part)
                                current_x += bbox[2] - bbox[0]
                        except Exception as e:
                            print(f"PNG emoji renderer failed: {e}")
                            # Fallback to regular text rendering
                            MarkdownRendererUtility._draw_text_with_color_support(
                                draw, (current_x, y), emoji_part, current_font, color, font_manager
                            )
                            bbox = current_font.getbbox(emoji_part)
                            current_x += bbox[2] - bbox[0]
                    else:
                        # Regular text part
                        MarkdownRendererUtility._draw_text_with_color_support(
                            draw, (current_x, y), emoji_part, current_font, color, font_manager
                        )
                        bbox = current_font.getbbox(emoji_part)
                        current_x += bbox[2] - bbox[0]
                
                # Calculate total width for the entire text part
                chunk_width = current_x - (box_left + padding if alignment == "left" else 
                                         box_left + padding + (box_width - line_width) // 2 if alignment == "center" else 
                                         box_left + padding + (box_width - line_width))
            else:
                bbox = current_font.getbbox(text_part)
                MarkdownRendererUtility._draw_text_with_color_support(
                    draw, (current_x, y), text_part, current_font, color, font_manager
                )
                chunk_width = bbox[2] - bbox[0]

            if chunk_width is None:
                chunk_width = 0

            if styles.get("u", False):
                underline_y = y + current_font.getsize(text_part)[1]
                draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=color, width=1)
            if styles.get("s", False):
                strikeout_y = y + current_font.getsize(text_part)[1] // 2
                draw.line((current_x, strikeout_y, current_x + chunk_width, strikeout_y), fill=color, width=1)

            current_x += chunk_width

    @staticmethod
    def calculate_markdown_text_dimensions(text, markdown_mode, font_manager,
                                         font_size, line_height_ratio, max_width=None):
        """
        Calculate the dimensions needed to render markdown text.
        
        Args:
            text: Markdown text to measure
            markdown_mode: Mode of markdown parsing
            font_manager: FontManager instance
            font_size: Base font size
            line_height_ratio: Line height multiplier
            max_width: Maximum width for wrapping (None for no wrapping)
            
        Returns:
            Tuple of (width, height) in pixels
        """
        # Parse markdown
        if markdown_mode == "basic":
            parsed_parts = parse_markdown(text)
        elif markdown_mode == "with_headers":
            parsed_parts = parse_markdown_with_headers(text)
        elif markdown_mode == "extended":
            parsed_parts = parse_markdown_extended(text)
        else:
            parsed_parts = parse_markdown(text)
        
        # Process into lines
        if max_width:
            lines = MarkdownRendererUtility._process_parsed_parts(
                parsed_parts, max_width, font_manager, font_size
            )
        else:
            # No wrapping - treat as single line
            lines = [parsed_parts]
        
        # Calculate dimensions
        line_height = font_size * line_height_ratio
        height = len(lines) * line_height
        
        # Calculate maximum line width
        max_line_width = 0
        for line in lines:
            line_width = 0
            for text_part, styles in line:
                font = font_manager.get_font_for_style(styles, font_size)
                bbox = font.getbbox(text_part)
                line_width += bbox[2] - bbox[0]
            max_line_width = max(max_line_width, line_width)
        
        return max_line_width, height
