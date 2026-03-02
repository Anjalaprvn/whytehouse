from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if dictionary is None:
        return 0
    return dictionary.get(key, 0)

@register.filter
def format_duration(value):
    """
    Format duration values like '5D/4N', '3D/2N', etc. to readable format
    Converts duration strings to 'X days Y nights' format or returns as is if format doesn't match
    """
    if not value:
        return ""
    
    # Handle string inputs that might represent duration
    duration_str = str(value).strip()
    
    # Match patterns like "5D/4N", "3D/2N", etc.
    match = re.match(r'^(\d+)D[/-](\d+)N$', duration_str.upper())
    if match:
        days = match.group(1)
        nights = match.group(2)
        return f"{days}D / {nights}N"
    
    # If it doesn't match the expected pattern, return the original value
    return duration_str
