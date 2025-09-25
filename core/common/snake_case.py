import re
import unicodedata


def snake_case(text):
    """Convert string to snake_case, handling accented characters"""
    # Remove accents and convert to ASCII
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')

    # Handle acronyms and convert camelCase/PascalCase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    # Handle numbers and remaining uppercase letters
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    # Replace spaces, hyphens, and other separators with underscores
    s3 = re.sub(r'[-\s]+', '_', s2)
    # Remove multiple underscores and convert to lowercase
    return re.sub(r'_+', '_', s3).lower().strip('_')
