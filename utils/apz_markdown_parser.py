# markdown_parser.py
import re

def parse_markdown(theText):
    """
    Parse markdown text and convert to style dictionary format.
    Supports: **bold**, *italic*, __underline__, ~~strikethrough~~
    """
    # Define markdown patterns and their corresponding styles
    patterns = [
        (r'\*\*(.*?)\*\*', 'b'),      # **bold**
        (r'\*(.*?)\*', 'i'),          # *italic*
        (r'__(.*?)__', 'u'),          # __underline__
        (r'~~(.*?)~~', 's'),          # ~~strikethrough~~
    ]
    
    parts = []
    current_pos = 0
    styles = {'b': False, 'i': False, 'u': False, 's': False}
    style_stack = []
    
    # Find all markdown patterns in the text
    matches = []
    for pattern, style_type in patterns:
        for match in re.finditer(pattern, theText):
            matches.append((match.start(), match.end(), match.group(1), style_type))
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Process matches in order
    for start, end, content, style_type in matches:
        # Add text before this match
        if start > current_pos:
            parts.append((theText[current_pos:start], styles.copy()))
        
        # Push current styles to stack and apply new style
        style_stack.append(styles.copy())
        styles[style_type] = True
        
        # Add the styled content
        parts.append((content, styles.copy()))
        
        # Pop styles back
        if style_stack:
            styles = style_stack.pop()
        
        current_pos = end
    
    # Add remaining text
    if current_pos < len(theText):
        parts.append((theText[current_pos:], styles.copy()))
    
    # If no parts were created, return the original text with no styles
    if not parts:
        parts.append((theText, styles.copy()))
    
    return parts

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