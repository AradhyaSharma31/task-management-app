from datetime import datetime

def format_date(date_str):
    """
    Convert a string (YYYY-MM-DD) to a datetime.date object.
    Returns None if input is invalid.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"⚠️ Invalid date format: {date_str}. Use YYYY-MM-DD.")
        return None

def format_datetime(dt):
    """
    Format a datetime object as a string for display.
    """
    if not dt:
        return "N/A"
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except (AttributeError, TypeError):
        return "N/A"

def safe_strftime(dt, format_str="%Y-%m-%d"):
    """
    Safely format datetime/date objects, handling None and string types.
    """
    if not dt:
        return "N/A"
    try:
        if isinstance(dt, str):
            return dt
        return dt.strftime(format_str)
    except (AttributeError, TypeError):
        return str(dt) if dt else "N/A"