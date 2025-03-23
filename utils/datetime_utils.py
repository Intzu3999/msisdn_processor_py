from datetime import datetime

def date_with_time():
    """Returns the current date and time formatted as YYYY-MM-DD_HH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
