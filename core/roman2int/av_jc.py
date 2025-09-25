def replace_av_jc(text):
    """
    Replace "av. J.-C." with "avant Jésus-Christ"
    """
    import re

    # Pattern to match various forms of "av. J.-C."
    # Handles variations in spacing and punctuation
    patterns = [
        r'\bav\.\s*J\.-C\.',
        r'\bav\.\s*J\.C\.',
        r'\bav\s*J\.-C\.',
        r'\bav\s*J\.C\.',
    ]

    result = text
    for pattern in patterns:
        result = re.sub(pattern, 'avant Jésus-Christ', result, flags=re.IGNORECASE)

    return result