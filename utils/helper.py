from datetime import datetime

def parse_date(date_str):
    """Convert string to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None

def format_date(date_obj):
    """Format date for display"""
    if not date_obj:
        return "No date"
    return date_obj.strftime("%Y-%m-%d")