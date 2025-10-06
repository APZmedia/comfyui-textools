# markdown_renderer_utility.py
from PIL import Image, ImageDraw
from .apz_font_manager import FontManager
from .apz_color_utility import ColorUtility
from .apz_markdown_parser import parse_markdown, parse_markdown_with_headers, parse_markdown_extended
from .apz_emoji_png_renderer import EmojiPNGRenderer

class MarkdownRendererUtility:
    """
    Utility class for rendering markdown text with proper styling and layout.
    """
    
    @staticmethod
    def _clone_styles(styles):
        return styles.copy() if isinstance(styles, dict) else {}
    
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
                # Debug logging removed for performance
                pass
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
                    # Use the same helper function as the main renderer for consistency
                    from .apz_emoji_png_renderer import EmojiPNGRenderer
                    from .apz_text_renderer_utility import TextRendererUtility
                    emoji_png_renderer = EmojiPNGRenderer()
                    emoji_width = TextRendererUtility._get_emoji_rendered_width(segment, font_size, emoji_png_renderer)
                    total_width += emoji_width
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
                           font_size, hashtag_color_rgb=None):
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

        effective_box_width = max(box_width - 2 * padding, 0)
        effective_box_height = max(box_height - 2 * padding, 0)

        line_sizes = []
        line_heights = []
        for line in renderable_lines:
            chunk_sizes = [styles.get("size", font_size) for _, styles in line if styles is not None]
            line_size = max(chunk_sizes) if chunk_sizes else font_size
            line_sizes.append(line_size)
            line_heights.append(int(line_size * line_height_ratio))

        total_height = sum(line_heights)

        if vertical_alignment == "middle":
            start_y = box_top + padding + max((effective_box_height - total_height) // 2, 0)
        elif vertical_alignment == "bottom":
            start_y = box_top + box_height - padding - total_height
        else:  # top
            start_y = box_top + padding

        current_y = start_y
        for idx, line in enumerate(renderable_lines):
            line_height = line_heights[idx]
            if current_y + line_height > box_top + box_height - padding:
                break  # Stop if we exceed box height

            MarkdownRendererUtility._render_line(
                draw, line, box_left, current_y, padding, box_width,
                font_manager, color_utility, alignment, line_sizes[idx],
                font_color_rgb, italic_font_color_rgb, bold_font_color_rgb, hashtag_color_rgb
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

                    style_dict = MarkdownRendererUtility._clone_styles(styles)
                    word_width = MarkdownRendererUtility._measure_text_width(word, style_dict, font_manager, font_size)

                    space_width = 0
                    if i < len(words) - 1:
                        space_width = MarkdownRendererUtility._measure_text_width(' ', style_dict, font_manager, font_size)

                    if current_line_width + word_width + space_width <= max_width:
                        current_line.append((word, style_dict))
                        current_line_width += word_width

                        if i < len(words) - 1:
                            current_line.append((' ', MarkdownRendererUtility._clone_styles(styles)))
                            current_line_width += space_width
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = [(word, style_dict)]
                        current_line_width = word_width

                        if i < len(words) - 1:
                            current_line.append((' ', MarkdownRendererUtility._clone_styles(styles)))
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
                    italic_font_color_rgb, bold_font_color_rgb, hashtag_color_rgb=None):
        """
        Render a single line of markdown text.
        """
        emoji_png_renderer = EmojiPNGRenderer()

        total_line_width = 0
        for text_part, styles in line:
            style_dict = styles if isinstance(styles, dict) else {}
            chunk_size = style_dict.get("size", font_size)
            total_line_width += MarkdownRendererUtility._measure_text_width(
                text_part, style_dict, font_manager, chunk_size
            )

        if alignment == "center":
            x = box_left + max((box_width - total_line_width) // 2, 0)
        elif alignment == "right":
            x = box_left + max(box_width - total_line_width - padding, 0)
        else:  # left
            x = box_left + padding

        current_x = x
        for text_part, styles in line:
            if not text_part:
                continue

            style_dict = styles if isinstance(styles, dict) else {}
            chunk_size = style_dict.get("size", font_size)
            chunk_width = MarkdownRendererUtility._measure_text_width(
                text_part, style_dict, font_manager, chunk_size
            )
            current_font = font_manager.get_font_for_style(style_dict, chunk_size, text_part)

            if style_dict.get("hashtag", False):
                if hashtag_color_rgb:
                    color = hashtag_color_rgb
                else:
                    color = (0, 100, 200)  # Default blue
            elif style_dict.get("b", False):
                color = bold_font_color_rgb
            elif style_dict.get("i", False):
                color = italic_font_color_rgb
            else:
                color = font_color_rgb

            if chunk_width > 0 and font_manager.emoji_support.has_emoji(text_part):
                # Handle multiple consecutive emojis by splitting them individually
                emoji_segments = font_manager.emoji_support.split_text_by_emoji(text_part)
                current_x_offset = current_x
                
                for emoji_segment, is_emoji in emoji_segments:
                    if not emoji_segment:
                        continue
                        
                    if is_emoji:
                        # Use exact text size for emojis to prevent size mismatch
                        emoji_size = chunk_size  # Match text size exactly
                        emoji_img = emoji_png_renderer.load_emoji_png(emoji_segment, emoji_size)
                        if emoji_img:
                            # Emoji-specific positioning strategy
                            # Different emojis need different alignment approaches
                            
                            # Get emoji characteristics for smart positioning
                            emoji_char = emoji_segment[0] if emoji_segment else '?'
                            emoji_unicode = ord(emoji_char)
                            
                            # Define emoji-specific boundary box with generous padding
                            # Give more space for emojis that tend to extend beyond their boundaries
                            base_padding = max(4, chunk_size // 8)  # 12.5% padding or minimum 4px
                            
                            # Emoji-specific padding adjustments
                            if emoji_unicode in [0x2744, 0x1F331, 0x1F338, 0x2B50]:  # ❄️🌱🌸⭐
                                # Nature/weather emojis that extend upward
                                emoji_padding_top = base_padding * 2
                                emoji_padding_bottom = base_padding
                            elif emoji_unicode in [0x1F600, 0x1F601, 0x1F602]:  # 😀😁😂
                                # Face emojis that are more centered
                                emoji_padding_top = base_padding
                                emoji_padding_bottom = base_padding
                            else:
                                # Default padding for other emojis
                                emoji_padding_top = base_padding
                                emoji_padding_bottom = base_padding
                            
                            # Create generous boundary box
                            emoji_box_top = y - emoji_padding_top
                            emoji_box_bottom = y + chunk_size + emoji_padding_bottom
                            emoji_box_height = emoji_box_bottom - emoji_box_top
                            
                            # Smart centering: position emoji to align with text baseline
                            # Calculate where text baseline would be
                            text_baseline_y = y + (chunk_size * 3 // 4)  # Assume baseline is 3/4 down the line
                            
                            # Position emoji so its bottom aligns with text baseline
                            emoji_y = text_baseline_y - emoji_img.height
                            
                            # Ensure emoji stays within the generous boundary box
                            emoji_y = max(emoji_box_top, min(emoji_y, emoji_box_bottom - emoji_img.height))
                            
                            # Debug logging removed for performance
                            # Debug logging removed for performance
                            # Debug logging removed for performance
                            # Debug logging removed for performance
                            
                            emoji_x = max(0, min(int(current_x_offset), box_left + box_width - emoji_img.width))
                            
                            # Validate emoji position before rendering
                            if (emoji_x >= 0 and emoji_y >= emoji_box_top and 
                                emoji_x + emoji_img.width <= box_left + box_width and
                                emoji_y + emoji_img.height <= emoji_box_bottom):
                                # Debug logging removed for performance
                                # Debug logging removed for performance
                                draw._image.paste(emoji_img, (emoji_x, emoji_y), emoji_img)
                                # Move x position for next emoji
                                current_x_offset += emoji_img.width
                            else:
                                # Debug logging removed for performance
                                MarkdownRendererUtility._draw_text_with_color_support(
                                    draw, (current_x_offset, y), emoji_segment, current_font, color, font_manager
                                )
                                # Estimate width for positioning
                                current_x_offset += chunk_size
                        else:
                            # Fallback to font rendering for this emoji
                            MarkdownRendererUtility._draw_text_with_color_support(
                                draw, (current_x_offset, y), emoji_segment, current_font, color, font_manager
                            )
                            # Estimate width for positioning
                            current_x_offset += chunk_size
                    else:
                        # Render non-emoji text
                        MarkdownRendererUtility._draw_text_with_color_support(
                            draw, (current_x_offset, y), emoji_segment, current_font, color, font_manager
                        )
                        # Measure and advance position
                        segment_width = MarkdownRendererUtility._measure_text_width(emoji_segment, styles, font_manager, chunk_size)
                        current_x_offset += segment_width
                
                # Update current_x to the final position
                current_x = current_x_offset
            else:
                MarkdownRendererUtility._draw_text_with_color_support(
                    draw, (current_x, y), text_part, current_font, color, font_manager
                )

            if chunk_width > 0 and text_part.strip():
                if style_dict.get("u", False):
                    underline_y = y + current_font.getsize(text_part)[1]
                    draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=color, width=1)
                if style_dict.get("s", False):
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
