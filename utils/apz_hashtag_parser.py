# hashtag_parser.py
import re

def parse_hashtags(text):
    """
    Parse hashtags in text and return enhanced text with hashtag styling.
    
    Args:
        text: Input text that may contain hashtags
        
    Returns:
        List of (text, styles) tuples with hashtag styling applied
    """
    # Pattern to match hashtags: # followed by word characters
    hashtag_pattern = r'#(\w+)'
    
    parts = []
    current_pos = 0
    base_styles = {'b': False, 'i': False, 'u': False, 's': False, 'hashtag': False}
    
    # Find all hashtag matches
    matches = []
    for match in re.finditer(hashtag_pattern, text):
        matches.append((match.start(), match.end(), match.group(0), match.group(1)))
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Process matches in order
    for start, end, full_hashtag, hashtag_content in matches:
        # Add text before this hashtag
        if start > current_pos:
            parts.append((text[current_pos:start], base_styles.copy()))
        
        # Create hashtag styles (bold + special hashtag flag)
        hashtag_styles = base_styles.copy()
        hashtag_styles['hashtag'] = True
        hashtag_styles['b'] = True  # Make hashtags bold
        
        # Add the hashtag with special styling
        parts.append((full_hashtag, hashtag_styles))
        
        current_pos = end
    
    # Add remaining text
    if current_pos < len(text):
        parts.append((text[current_pos:], base_styles.copy()))
    
    # If no parts were created, return the original text with no styles
    if not parts:
        parts.append((text, base_styles.copy()))
    
    return parts

def extract_hashtags(text):
    """
    Extract all hashtags from text.
    
    Args:
        text: Input text
        
    Returns:
        List of hashtag strings (without #)
    """
    hashtag_pattern = r'#(\w+)'
    matches = re.findall(hashtag_pattern, text)
    return matches

def has_hashtags(text):
    """
    Check if text contains hashtags.
    
    Args:
        text: Input text
        
    Returns:
        Boolean indicating if hashtags are present
    """
    return bool(re.search(r'#\w+', text))

def count_hashtags(text):
    """
    Count the number of hashtags in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of hashtags found
    """
    return len(re.findall(r'#\w+', text))
