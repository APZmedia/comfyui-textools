# utils/apz_text_renderer_utility.py
from .apz_box_utility import BoxUtility
from .apz_emoji_png_renderer import EmojiPNGRenderer

class TextRendererUtility:
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
    def _measure_chunk_width(text, styles, font_manager, font_size):
        """
        Measure the width of a text chunk, with emoji-aware handling.
        """
        if not text:
            return 0

        local_styles = styles if isinstance(styles, dict) else {}
        emoji_support = getattr(font_manager, "emoji_support", None)

        if emoji_support and emoji_support.has_emoji(text):
            total_width = 0
            for segment, is_emoji in emoji_support.split_text_by_emoji(text):
                if not segment:
                    continue
                if is_emoji:
                    total_width += font_size * max(len(segment), 1)
                else:
                    segment_font = font_manager.get_font_for_style(local_styles, font_size, segment)
                    bbox = segment_font.getbbox(segment)
                    total_width += bbox[2] - bbox[0]
            return total_width

        measure_font = font_manager.get_font_for_style(local_styles, font_size, text)
        bbox = measure_font.getbbox(text)
        return bbox[2] - bbox[0]

    @staticmethod
    def render_text(draw, wrapped_lines, box_start_x, box_start_y, padding, theTextbox_width, theTextbox_height, font_manager, color_utility, alignment, vertical_alignment, line_height_ratio, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb):
        if not wrapped_lines:
            return

        effective_textbox_width, effective_textbox_height = BoxUtility.calculate_effective_dimensions(
            theTextbox_width, theTextbox_height, padding
        )

        processed_lines = []
        total_text_height = 0

        for _, line_parts in wrapped_lines:
            chunk_infos = []
            max_chunk_size = 0
            line_width = 0

            for chunk, chunk_styles in line_parts:
                styles_dict = chunk_styles if isinstance(chunk_styles, dict) else {}
                chunk_size = styles_dict.get("size", font_manager.max_font_size if hasattr(font_manager, "max_font_size") else 16)
                chunk_width = TextRendererUtility._measure_chunk_width(chunk, styles_dict, font_manager, chunk_size)

                chunk_infos.append((chunk, styles_dict, chunk_size, chunk_width))
                max_chunk_size = max(max_chunk_size, chunk_size)
                line_width += chunk_width

            if max_chunk_size == 0:
                max_chunk_size = font_manager.max_font_size if hasattr(font_manager, "max_font_size") else 16

            line_height = int(max_chunk_size * line_height_ratio)
            total_text_height += line_height
            processed_lines.append({
                "chunks": chunk_infos,
                "line_width": line_width,
                "line_height": line_height,
                "line_size": max_chunk_size,
            })

        if vertical_alignment == "middle":
            current_y = box_start_y + padding + max((effective_textbox_height - total_text_height) // 2, 0)
        elif vertical_alignment == "bottom":
            current_y = box_start_y + padding + max(effective_textbox_height - total_text_height, 0)
        else:
            current_y = box_start_y + padding

        emoji_png_renderer = EmojiPNGRenderer()

        for line_data in processed_lines:
            line_height = line_data["line_height"]
            line_width = line_data["line_width"]

            if current_y + line_height > box_start_y + theTextbox_height - padding:
                break

            if alignment == "center":
                current_x = box_start_x + padding + max((effective_textbox_width - line_width) // 2, 0)
            elif alignment == "right":
                current_x = box_start_x + padding + max(effective_textbox_width - line_width, 0)
            else:
                current_x = box_start_x + padding

            for chunk, styles_dict, chunk_size, chunk_width in line_data["chunks"]:
                if not chunk:
                    continue

                current_font = font_manager.get_font_for_style(styles_dict, chunk_size, chunk)

                if styles_dict.get("hashtag", False):
                    current_font_color_rgb = (0, 100, 200)
                else:
                    current_font_color_rgb = color_utility.get_font_color(
                        styles_dict, font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
                    )

                if chunk_width > 0 and font_manager.emoji_support.has_emoji(chunk):
                    emoji_img = emoji_png_renderer.load_emoji_png(chunk, chunk_size)
                    if emoji_img:
                        emoji_y = int(current_y + chunk_size - emoji_img.height + 5)
                        draw._image.paste(emoji_img, (int(current_x), emoji_y), emoji_img)
                    else:
                        TextRendererUtility._draw_text_with_color_support(
                            draw, (current_x, current_y), chunk, current_font, current_font_color_rgb, font_manager
                        )
                else:
                    TextRendererUtility._draw_text_with_color_support(
                        draw, (current_x, current_y), chunk, current_font, current_font_color_rgb, font_manager
                    )

                if chunk_width > 0 and chunk.strip():
                    if styles_dict.get("u", False):
                        underline_y = current_y + current_font.getsize(chunk)[1]
                        draw.line((current_x, underline_y, current_x + chunk_width, underline_y), fill=current_font_color_rgb, width=1)
                    if styles_dict.get("s", False):
                        strikeout_y = current_y + current_font.getsize(chunk)[1] // 2
                        draw.line((current_x, strikeout_y, current_x + chunk_width, strikeout_y), fill=current_font_color_rgb, width=1)

                current_x += chunk_width

            current_y += line_height
