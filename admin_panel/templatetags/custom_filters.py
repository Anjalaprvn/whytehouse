from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if dictionary is None:
        return 0
    return dictionary.get(key, 0)

@register.filter
def format_duration(duration):
    """Format duration string to ☀️ X / 🌙 Y format"""
    import re
    
    if not duration:
        return "☀️ 5 / 🌙 4"
    
    # Try to extract numbers from duration string
    # Patterns like "5 Days 4 Nights", "5D/4N", "5 days", etc.
    duration_str = str(duration).lower()
    
    # Look for patterns like "5 days 4 nights" or "5d 4n"
    match = re.search(r'(\d+)\s*(?:days?|d).*?(\d+)\s*(?:nights?|n)', duration_str)
    if match:
        days = match.group(1)
        nights = match.group(2)
        return f"☀️ {days} / 🌙 {nights}"
    
    # Look for just days
    match = re.search(r'(\d+)\s*(?:days?|d)', duration_str)
    if match:
        days = int(match.group(1))
        nights = days - 1 if days > 0 else 0
        return f"☀️ {days} / 🌙 {nights}"
    
    # Default fallback
    return "☀️ 5 / 🌙 4"

@register.filter
def get_days(duration):
    """Extract days from duration string"""
    import re
    if not duration:
        return "5"
    duration_str = str(duration).lower()
    match = re.search(r'(\d+)\s*(?:days?|d)', duration_str)
    if match:
        return match.group(1)
    return "5"

@register.filter
def get_nights(duration):
    """Extract nights from duration string"""
    import re
    if not duration:
        return "4"
    duration_str = str(duration).lower()
    # Look for explicit nights
    match = re.search(r'(\d+)\s*(?:nights?|n)', duration_str)
    if match:
        return match.group(1)
    # If only days found, calculate nights as days-1
    match = re.search(r'(\d+)\s*(?:days?|d)', duration_str)
    if match:
        days = int(match.group(1))
        return str(days - 1 if days > 0 else 0)
    return "4"
