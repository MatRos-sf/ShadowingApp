from utils.tools import format_time


def test_format_time():
    """Test formatting time"""
    formatted_time = format_time(125)
    assert formatted_time == "02:05"
