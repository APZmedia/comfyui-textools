#!/usr/bin/env python3
"""
Comprehensive Emoji PNG Library Builder
Generates high-quality emoji PNGs at multiple resolutions for serverless environments.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import unicodedata

class EmojiLibraryBuilder:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = self.script_dir
        self.emoji_dir = os.path.join(self.project_root, "fonts", "emoji", "png")
        
        # Resolution ladder for optimal quality
        self.resolutions = [
            ("tiny", 16),
            ("small", 32), 
            ("medium", 64),
            ("large", 128),
            ("xlarge", 256)
        ]
        
        # Essential emojis for common use cases
        self.essential_emojis = [
            "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃",
            "😉", "😊", "😇", "🥰", "😍", "🤩", "😘", "😗", "😚", "😙",
            "😋", "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔",
            "🤐", "🤨", "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "🤥",
            "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕", "🤢", "🤮", "🤧",
            "🥵", "🥶", "🥴", "😵", "🤯", "🤠", "🥳", "😎", "🤓", "🧐",
            "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔",
            "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "☮️",
            "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐",
            "⛎", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐",
            "♑", "♒", "♓", "🆔", "⚛️", "🉑", "☢️", "☣️", "📴", "📳",
            "🈶", "🈚", "🈸", "🈺", "🈷️", "✴️", "🆚", "💮", "🉐", "㊙️",
            "㊗️", "🈴", "🈵", "🈹", "🈲", "🅰️", "🅱️", "🆎", "🆑", "🅾️",
            "🆘", "❌", "⭕", "🛑", "⛔", "📛", "🚫", "💯", "💢", "♨️",
            "🚷", "🚯", "🚳", "🚱", "🔞", "📵", "🚭", "❗", "❕", "❓",
            "❔", "‼️", "⁉️", "🔅", "🔆", "〽️", "⚠️", "🚸", "🔱", "⚜️",
            "🔰", "♻️", "✅", "🈯", "💹", "❇️", "✳️", "❎", "🌐", "💠",
            "Ⓜ️", "🌀", "💤", "🏧", "🚾", "♿", "🅿️", "🈳", "🈂️", "🛂",
            "🛃", "🛄", "🛅", "🚹", "🚺", "🚼", "🚻", "🚮", "🎦", "📶",
            "🈁", "🔣", "ℹ️", "🔤", "🔡", "🔠", "🆖", "🆗", "🆙", "🆒",
            "🆕", "🆓", "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣",
            "8️⃣", "9️⃣", "🔟", "🔢", "#️⃣", "*️⃣", "⏏️", "▶️", "⏸️", "⏯️",
            "⏹️", "⏺️", "⏭️", "⏮️", "⏩", "⏪", "⏫", "⏬", "◀️", "🔼",
            "🔽", "➡️", "⬅️", "⬆️", "⬇️", "↗️", "↘️", "↙️", "↖️", "↕️",
            "↔️", "↩️", "↪️", "⤴️", "⤵️", "🔃", "🔄", "🔙", "🔚", "🔛",
            "🔜", "🔝", "🛐", "⚛️", "🕉️", "✡️", "☸️", "☯️", "✝️", "☦️",
            "☪️", "☮️", "🕎", "🔯", "♈", "♉", "♊", "♋", "♌", "♍",
            "♎", "♏", "♐", "♑", "♒", "♓", "⛎", "🔀", "🔁", "🔂",
            "🔃", "🔄", "🔅", "🔆", "🔇", "🔈", "🔉", "🔊", "📢", "📣",
            "📯", "🔔", "🔕", "🎵", "🎶", "💤", "💢", "💬", "💭", "🗨️",
            "🗯️", "💭", "🃏", "🀄", "🎴", "🎭", "🖼️", "🎨", "👓", "🕶️",
            "🥽", "🥼", "🦺", "👔", "👕", "👖", "🧣", "🧤", "🧥", "🧦",
            "👗", "👘", "🥻", "🩱", "🩲", "🩳", "👙", "👚", "👛", "👜",
            "👝", "🎒", "🦯", "👞", "👟", "🥾", "🥿", "👠", "👡", "🩰",
            "👢", "🩱", "🩲", "🩳", "👙", "👚", "👛", "👜", "👝", "🎒",
            "🦯", "👞", "👟", "🥾", "🥿", "👠", "👡", "🩰", "👢", "🦺",
            "🥽", "🕶️", "👓", "🎭", "🖼️", "🎨", "🃏", "🀄", "🎴", "🎵",
            "🎶", "🔕", "🔔", "📯", "📣", "📢", "🔊", "🔉", "🔈", "🔇",
            "🔆", "🔅", "🔄", "🔃", "🔂", "🔁", "🔀", "♓", "♒", "♑",
            "♐", "♏", "♎", "♍", "♌", "♋", "♊", "♉", "♈", "🔯",
            "🕎", "☮️", "☦️", "✝️", "☯️", "☸️", "✡️", "🕉️", "⚛️", "🛐",
            "🔝", "🔜", "🔛", "🔚", "🔙", "🔄", "🔃", "⤵️", "⤴️", "↪️",
            "↩️", "↔️", "↕️", "↖️", "↙️", "↘️", "↗️", "⬇️", "⬆️", "⬅️",
            "➡️", "🔽", "🔼", "◀️", "⏬", "⏫", "⏪", "⏩", "⏮️", "⏭️",
            "⏺️", "⏹️", "⏯️", "⏸️", "▶️", "⏏️", "*️⃣", "#️⃣", "🔢", "🔟",
            "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣", "0️⃣",
            "🆓", "🆕", "🆒", "🆙", "🆗", "🆖", "🔠", "🔡", "🔤", "ℹ️",
            "🔣", "🈁", "📶", "🎦", "🚮", "🚻", "🚼", "🚺", "🚹", "🛅",
            "🛄", "🛃", "🛂", "🈂️", "🈳", "🅿️", "♿", "🚾", "🏧", "💤",
            "🌀", "Ⓜ️", "💠", "🌐", "❎", "✳️", "❇️", "💹", "🈯", "✅",
            "♻️", "🔰", "⚜️", "🔱", "🚸", "⚠️", "〽️", "🔆", "🔅", "⁉️",
            "‼️", "❔", "❓", "❕", "❗", "🚭", "📵", "🔞", "🚱", "🚳",
            "🚯", "🚷", "♨️", "💢", "💯", "🚫", "📛", "⛔", "🛑", "⭕",
            "❌", "🆘", "🅾️", "🆑", "🆎", "🅱️", "🅰️", "🈲", "🈹", "🈵",
            "🈴", "㊗️", "㊙️", "🉐", "💮", "🆚", "✴️", "🈷️", "🈺", "🈸",
            "🈚", "🈶", "📳", "📴", "☣️", "☢️", "🉑", "⚛️", "🆔", "♓",
            "♒", "♑", "♐", "♏", "♎", "♍", "♌", "♋", "♊", "♉", "♈", "⛎",
            "🛐", "☦️", "☯️", "🕎", "✡️", "☸️", "🕉️", "☪️", "✝️", "☮️",
            "💟", "💝", "💘", "💖", "💗", "💓", "💞", "💕", "❣️", "💔",
            "🤎", "🤍", "🖤", "💜", "💙", "💚", "💛", "🧡", "❤️", "🧐",
            "🤓", "😎", "🥳", "🤠", "🤯", "😵", "🥴", "🥶", "🥵", "🤧",
            "🤮", "🤢", "🤕", "🤒", "😷", "😴", "🤤", "😪", "😔", "🤥",
            "😬", "🙄", "😒", "😏", "😶", "😑", "😐", "🤨", "🤫", "🤭",
            "🤗", "🤑", "😝", "🤪", "😜", "😛", "😋", "😙", "😚", "😗",
            "😘", "🤩", "😍", "🥰", "😇", "😊", "😉", "🙃", "🙂", "😂",
            "🤣", "😅", "😆", "😁", "😄", "😃", "😀"
        ]
        
        # Additional common emojis
        self.common_emojis = [
            "⭐", "🌟", "💫", "✨", "🔥", "💥", "💢", "💦", "💨", "💤",
            "🌍", "🌎", "🌏", "🌐", "🗺️", "🏔️", "⛰️", "🌋", "🗻", "🏕️",
            "🏖️", "🏜️", "🏝️", "🏞️", "🏟️", "🏛️", "🏗️", "🧱", "🏘️", "🏚️",
            "🏠", "🏡", "🏢", "🏣", "🏤", "🏥", "🏦", "🏧", "🏨", "🏩",
            "🏪", "🏫", "🏬", "🏭", "🏮", "🏯", "🏰", "💒", "🗼", "🗽",
            "⛪", "🕌", "🛕", "🕍", "⛩️", "🕋", "⛲", "⛺", "🌉", "🌁",
            "🚧", "🚨", "🚥", "🚦", "🚧", "⚓", "⛵", "🛥️", "🚤", "⛴️",
            "🛳️", "🚢", "✈️", "🛩️", "🛫", "🛬", "🪂", "💺", "🚁", "🚟",
            "🚠", "🚡", "🛰️", "🚀", "🛸", "🛎️", "🧳", "⌛", "⏳", "⏰",
            "⏲️", "⏱️", "🕰️", "🕛", "🕧", "🕐", "🕜", "🕑", "🕝", "🕒",
            "🕞", "🕓", "🕟", "🕔", "🕠", "🕕", "🕡", "🕖", "🕢", "🕗",
            "🕣", "🕘", "🕤", "🕙", "🕥", "🕚", "🕦", "🌑", "🌒", "🌓",
            "🌔", "🌕", "🌖", "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "🌝",
            "🌞", "⭐", "🌟", "💫", "✨", "☄️", "☀️", "🌤️", "⛅", "🌥️",
            "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "☃️", "⛄", "🌬️",
            "💨", "💧", "💦", "☔", "☂️", "🌊", "🌫️", "🌪️", "🔥", "💥",
            "💢", "💫", "💨", "💤", "💦", "💧", "🌊", "🌪️", "🌫️", "🌬️",
            "🌨️", "🌩️", "⛈️", "🌧️", "🌦️", "☁️", "🌥️", "⛅", "🌤️", "☀️",
            "🌞", "🌝", "🌜", "🌛", "🌚", "🌙", "🌘", "🌗", "🌖", "🌕",
            "🌔", "🌓", "🌒", "🌑", "🕦", "🕥", "🕤", "🕣", "🕢", "🕡",
            "🕠", "🕟", "🕞", "🕝", "🕜", "🕧", "🕛", "🕰️", "⏱️", "⏲️",
            "⏰", "⏳", "⌛", "🧳", "🛎️", "🛸", "🚀", "🛰️", "🚡", "🚠",
            "🚟", "🚁", "💺", "🪂", "🛬", "🛫", "🛩️", "✈️", "🚢", "🛳️",
            "⛴️", "🚤", "🛥️", "⛵", "⚓", "🚦", "🚥", "🚨", "🚧", "🌁",
            "🌉", "⛺", "⛲", "🕋", "⛩️", "🕍", "🛕", "🕌", "⛪", "🗽",
            "🗼", "🏰", "🏯", "🏮", "🏭", "🏬", "🏫", "🏪", "🏩", "🏨",
            "🏧", "🏦", "🏥", "🏤", "🏣", "🏢", "🏡", "🏠", "🏚️", "🏘️",
            "🧱", "🏗️", "🏛️", "🏟️", "🏞️", "🏝️", "🏜️", "🏖️", "🏕️", "🗻",
            "🌋", "⛰️", "🏔️", "🗺️", "🌐", "🌏", "🌎", "🌍"
        ]
        
        # Combine all emojis
        self.all_emojis = list(set(self.essential_emojis + self.common_emojis))
        print(f"Total emojis to process: {len(self.all_emojis)}")
        
    def get_emoji_fonts(self):
        """Get available emoji fonts in order of preference."""
        fonts = []
        
        # Try system fonts first
        system_fonts = [
            "Segoe UI Emoji",      # Windows
            "Apple Color Emoji",   # macOS
            "Noto Color Emoji",    # Linux
            "Twemoji",             # Alternative
        ]
        
        for font_name in system_fonts:
            try:
                # Test if font exists
                ImageFont.truetype(font_name, 16)
                fonts.append(("system", font_name))
                print(f"✅ Found system font: {font_name}")
            except OSError:
                continue
        
        # Try bundled fonts
        bundled_fonts_dir = os.path.join(self.project_root, "fonts", "emoji")
        bundled_font_paths = [
            os.path.join(bundled_fonts_dir, "NotoColorEmoji-Color.ttf"),
            os.path.join(bundled_fonts_dir, "NotoColorEmoji-Regular.ttf"),
            os.path.join(bundled_fonts_dir, "SegoeUIEmoji.ttf"),
        ]
        
        for font_path in bundled_font_paths:
            if os.path.exists(font_path):
                try:
                    ImageFont.truetype(font_path, 16)
                    fonts.append(("bundled", font_path))
                    print(f"✅ Found bundled font: {os.path.basename(font_path)}")
                except OSError:
                    continue
        
        if not fonts:
            print("❌ No emoji fonts found!")
            return []
        
        return fonts
    
    def render_emoji_to_png(self, emoji_char, font, size, scale_factor=1.0):
        """Render emoji to PNG with proper scaling and centering."""
        try:
            # Create image with transparent background
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box
            bbox = font.getbbox(emoji_char)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            # Apply scale factor if needed
            if scale_factor != 1.0:
                # Create larger image for scaling
                scaled_size = int(size * scale_factor)
                scaled_img = Image.new("RGBA", (scaled_size, scaled_size), (0, 0, 0, 0))
                scaled_draw = ImageDraw.Draw(scaled_img)
                
                # Draw at scaled position
                scaled_x = int(x * scale_factor)
                scaled_y = int(y * scale_factor)
                
                try:
                    scaled_draw.text((scaled_x, scaled_y), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    # Fallback for fonts without embedded color support
                    scaled_draw.text((scaled_x, scaled_y), emoji_char, font=font, fill=(0, 0, 0, 255))
                
                # Scale down to target size
                img = scaled_img.resize((size, size), Image.Resampling.LANCZOS)
            else:
                # Draw directly at target size
                try:
                    # Try embedded color first (for color emoji fonts)
                    draw.text((x, y), emoji_char, font=font, embedded_color=True)
                except (TypeError, OSError) as e:
                    # Fallback for fonts without embedded color support
                    try:
                        draw.text((x, y), emoji_char, font=font, fill=(0, 0, 0, 255))
                    except Exception as e2:
                        print(f"Failed to render {emoji_char} with font: {e2}")
                        return None
            
            return img
            
        except Exception as e:
            print(f"Error rendering {emoji_char}: {e}")
            return None
    
    def generate_emoji_pngs(self, emoji_char):
        """Generate PNGs for a single emoji at all resolutions."""
        # Handle multi-character emojis (like ⏺️ which is ⏺ + variation selector)
        if len(emoji_char) > 1:
            # Use the first character for filename
            first_char = emoji_char[0]
            unicode_codepoint = ord(first_char)
        else:
            unicode_codepoint = ord(emoji_char)
        
        base_filename = f"{unicode_codepoint:x}"
        
        print(f"Generating PNGs for {emoji_char} (U+{unicode_codepoint:04X})")
        
        # Get available fonts
        fonts = self.get_emoji_fonts()
        if not fonts:
            print(f"❌ No fonts available for {emoji_char}")
            return False
        
        # Use the first available font
        font_type, font_path = fonts[0]
        print(f"Using font: {font_path}")
        
        success_count = 0
        
        for res_name, res_size in self.resolutions:
            try:
                # Try to load font at target size
                if font_type == "system":
                    font = ImageFont.truetype(font_path, res_size)
                    scale_factor = 1.0
                else:
                    try:
                        font = ImageFont.truetype(font_path, res_size)
                        scale_factor = 1.0
                    except OSError:
                        # NotoColorEmoji has size limitations
                        if "NotoColorEmoji" in font_path:
                            base_size = 109
                            font = ImageFont.truetype(font_path, base_size)
                            scale_factor = res_size / base_size
                        else:
                            raise
                
                # Render emoji
                img = self.render_emoji_to_png(emoji_char, font, res_size, scale_factor)
                
                if img:
                    # Save resolution-specific PNG
                    res_path = os.path.join(self.emoji_dir, f"{base_filename}_{res_name}.png")
                    img.save(res_path)
                    print(f"  ✅ {res_name} ({res_size}px) -> {res_path}")
                    success_count += 1
                    
                    # Save base PNG (use large resolution as base)
                    if res_name == "large":
                        base_path = os.path.join(self.emoji_dir, f"{base_filename}.png")
                        img.save(base_path)
                        print(f"  ✅ base -> {base_path}")
                else:
                    print(f"  ❌ Failed to render {res_name} ({res_size}px)")
                    
            except Exception as e:
                print(f"  ❌ Error generating {res_name} ({res_size}px): {e}")
        
        return success_count > 0
    
    def build_library(self):
        """Build the complete emoji PNG library."""
        print("🚀 Building Emoji PNG Library")
        print("=" * 50)
        
        # Create emoji directory
        os.makedirs(self.emoji_dir, exist_ok=True)
        print(f"📁 Emoji directory: {self.emoji_dir}")
        
        # Check available fonts
        fonts = self.get_emoji_fonts()
        if not fonts:
            print("❌ No emoji fonts found! Cannot build library.")
            return False
        
        print(f"📝 Processing {len(self.all_emojis)} emojis...")
        
        success_count = 0
        failed_emojis = []
        
        for i, emoji in enumerate(self.all_emojis, 1):
            print(f"\n[{i}/{len(self.all_emojis)}] Processing: {emoji}")
            
            if self.generate_emoji_pngs(emoji):
                success_count += 1
            else:
                failed_emojis.append(emoji)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 BUILD SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully processed: {success_count}/{len(self.all_emojis)} emojis")
        print(f"❌ Failed: {len(failed_emojis)} emojis")
        
        if failed_emojis:
            print(f"\nFailed emojis: {', '.join(failed_emojis[:10])}")
            if len(failed_emojis) > 10:
                print(f"... and {len(failed_emojis) - 10} more")
        
        # Calculate total files
        total_files = success_count * len(self.resolutions) + success_count  # +1 for base files
        print(f"📁 Total PNG files generated: {total_files}")
        
        return success_count > 0

def main():
    """Main function to build the emoji library."""
    builder = EmojiLibraryBuilder()
    success = builder.build_library()
    
    if success:
        print("\n🎉 Emoji library built successfully!")
        print("The PNG library is now ready for serverless environments.")
    else:
        print("\n❌ Failed to build emoji library.")
        sys.exit(1)

if __name__ == "__main__":
    main()
