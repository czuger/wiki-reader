import re


def convert_date_ranges_to_tuples(text: str) -> str:
    """
    Replaces dates in format (year-year) with (year, year).

    Handles dates with or without spaces around the hyphen.

    Args:
        text: The text containing dates to reformat

    Returns:
        The text with reformatted dates

    Example:
        >>> convert_date_ranges_to_tuples("Philippe III (1245-1285)")
        'Philippe III (1245, 1285)'
        >>> convert_date_ranges_to_tuples("Philippe III (1245 - 1285)")
        'Philippe III (1245, 1285)'
    """
    # Search for pattern: opening parenthesis, 4 digits, optional spaces, hyphen, optional spaces, 4 digits, closing parenthesis
    # Replace with the two years separated by a comma and a space
    result = re.sub(r'\((\d{4})\s*-\s*(\d{4})\)', r'(\1, \2)', text)
    return result
