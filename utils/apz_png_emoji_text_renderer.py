# png_emoji_text_renderer.py
import os
import re
from PIL import Image, ImageDraw, ImageFont
from .apz_emoji_png_renderer import EmojiPNGRenderer

class PNGEmojiTextRenderer:
    """
    Text renderer that uses PNG emojis for perfect color emoji support.
    """
    
    def __init__(self):
        self.emoji_png_renderer = EmojiPNGRenderer()
    
    def render_text_with_png_emojis(self, draw, text, font, font_size, x, y, color):
        """
        Render text with PNG emojis embedded.
        """
        current_x = x
        current_y = y
        
        # Split text into emoji and non-emoji parts
        parts = self.emoji_png_renderer.split_text_and_emojis(text)
        
        for text_part, is_emoji in parts:
            if is_emoji:
                # Try to render emoji as PNG
                emoji_img = self.emoji_png_renderer.load_emoji_png(text_part, font_size)
                if emoji_img:
                    # Paste emoji onto the image
                    draw._image.paste(emoji_img, (int(current_x), int(current_y)), emoji_img)
                    current_x += font_size
                else:
                    # Fallback to text rendering
                    draw.text((current_x, current_y), text_part, fill=color, font=font)
                    bbox = font.getbbox(text_part)
                    current_x += bbox[2] - bbox[0]
            else:
                # Render regular text
                draw.text((current_x, current_y), text_part, fill=color, font=font)
                bbox = font.getbbox(text_part)
                current_x += bbox[2] - bbox[0]
    
    def render_rich_text_with_png_emojis(self, draw, text_parts, font_manager, font_size, 
                                       base_color, bold_color, italic_color, hashtag_color):
        """
        Render rich text with PNG emojis.
        """
        current_x = 0
        current_y = 0
        
        for text_part, styles in text_parts:
            # Determine font
            if styles.get('b', False):  # Bold
                font = font_manager.get_bold_font(font_size)
            elif styles.get('i', False):  # Italic
                font = font_manager.get_italic_font(font_size)
            else:
                font = font_manager.get_regular_font(font_size)
            
            # Determine color
            if styles.get('hashtag', False):
                color = hashtag_color
            elif styles.get('b', False):
                color = bold_color
            elif styles.get('i', False):
                color = italic_color
            else:
                color = base_color
            
            # Render the text part with PNG emoji support
            self.render_text_with_png_emojis(draw, text_part, font, font_size, current_x, current_y, color)
            
            # Move to next position
            if self.emoji_png_renderer.has_emoji(text_part):
                current_x += font_size  # Rough estimate for emojis
            else:
                bbox = font.getbbox(text_part)
                current_x += bbox[2] - bbox[0]
