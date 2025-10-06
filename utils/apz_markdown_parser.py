# markdown_parser.py
import re
from .apz_hashtag_parser import parse_hashtags
from .apz_emoji_support import create_emoji_support

def parse_markdown(theText):
    """
    Parse markdown text and convert to style dictionary format.
    Supports: **bold**, *italic*, __underline__, ~~strikethrough~~, #hashtags, and emojis
    """
    # First, handle hashtags
    hashtag_parts = parse_hashtags(theText)
    
    # Define markdown patterns and their corresponding styles
    patterns = [
        (r'\*\*(.*?)\*\*', 'b'),      # **bold**
        (r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)', 'i'),  # *italic* (not **bold**)
        (r'__(.*?)__', 'u'),          # __underline__
        (r'~~(.*?)~~', 's'),          # ~~strikethrough~~
    ]
    
    # Process each part for markdown formatting
    final_parts = []
    for text_part, styles in hashtag_parts:
        if styles.get('hashtag', False):
            # Hashtags are already processed, add as-is
            final_parts.append((text_part, styles))
        else:
            # Process for markdown formatting
            parts = []
            current_pos = 0
            style_stack = []
            current_styles = styles.copy()
            
            # Find all markdown patterns in this text part
            matches = []
            for pattern, style_type in patterns:
                for match in re.finditer(pattern, text_part):
                    matches.append((match.start(), match.end(), match.group(1), style_type))
            
            # Sort matches by position
            matches.sort(key=lambda x: x[0])
            
            # Process matches in order, avoiding overlaps
            processed_ranges = set()
            
            for start, end, content, style_type in matches:
                # Skip if this range overlaps with already processed ranges
                if any(start < processed_end and end > processed_start 
                       for processed_start, processed_end in processed_ranges):
                    continue
                
                # Add text before this match
                if start > current_pos:
                    before_text = text_part[current_pos:start]
                    if before_text:  # Add all text, including spaces
                        parts.append((before_text, current_styles.copy()))
                
                # Push current styles to stack and apply new style
                style_stack.append(current_styles.copy())
                current_styles[style_type] = True
                
                # Add the styled content
                if content:  # Add all content, including spaces
                    parts.append((content, current_styles.copy()))
                
                # Pop styles back
                if style_stack:
                    current_styles = style_stack.pop()
                
                # Mark this range as processed
                processed_ranges.add((start, end))
                current_pos = end
            
            # Add remaining text
            if current_pos < len(text_part):
                parts.append((text_part[current_pos:], current_styles.copy()))
            
            # If no parts were created, add the original text
            if not parts:
                parts.append((text_part, current_styles.copy()))
            
            final_parts.extend(parts)
    
    return final_parts

def parse_markdown_with_headers(theText):
    """
    Parse markdown text including headers (# ## ### etc.)
    Headers are treated as bold text for rendering purposes.
    """
    # First, handle headers by converting them to bold
    header_pattern = r'^(#{1,6})\s+(.+)$'
    lines = theText.split('\n')
    processed_lines = []
    
    for line in lines:
        header_match = re.match(header_pattern, line.strip())
        if header_match:
            level, content = header_match.groups()
            # Convert header to bold text
            processed_lines.append(f"**{content}**")
        else:
            processed_lines.append(line)
    
    # Join lines back and parse markdown
    processed_text = '\n'.join(processed_lines)
    return parse_markdown(processed_text)

def parse_markdown_extended(theText):
    """
    Extended markdown parser with additional features:
    - Headers (# ## ###)
    - Lists (- item, * item, 1. item)
    - Code blocks (`code`)
    """
    # Handle headers
    header_pattern = r'^(#{1,6})\s+(.+)$'
    lines = theText.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append(line)
            continue
            
        # Handle headers
        header_match = re.match(header_pattern, line)
        if header_match:
            level, content = header_match.groups()
            processed_lines.append(f"**{content}**")
            continue
        
        # Handle list items
        list_match = re.match(r'^([-*]|\d+\.)\s+(.+)$', line)
        if list_match:
            marker, content = list_match.groups()
            processed_lines.append(f"• {content}")
            continue
        
        # Handle inline code
        line = re.sub(r'`([^`]+)`', r'**\1**', line)  # Convert inline code to bold
        
        processed_lines.append(line)
    
    # Join lines back and parse markdown
    processed_text = '\n'.join(processed_lines)
    return parse_markdown(processed_text) 
