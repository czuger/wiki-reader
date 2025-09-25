import re

from core.roman2int.roman2int import roman_to_int

french_ordinals = {
    1: "premier",
    2: "second",
    3: "troisième",
    4: "quatrième",
    5: "cinquième",
    6: "sixième",
    7: "septième",
    8: "huitième",
    9: "neuvième",
    10: "dixième",
    11: "onzième",
    12: "douzième",
    13: "treizième",
    14: "quatorzième",
    15: "quinzième",
    16: "seizième",
    17: "dix-septième",
    18: "dix-huitième",
    19: "dix-neuvième",
    20: "vingtième",
    21: "vingt et unième",
    22: "vingt-deuxième",
    23: "vingt-troisième",
    24: "vingt-quatrième",
    25: "vingt-cinquième",
    26: "vingt-sixième",
    27: "vingt-septième",
    28: "vingt-huitième",
    29: "vingt-neuvième",
    30: "trentième",
    31: "trente et unième",
    32: "trente-deuxième",
    33: "trente-troisième",
    34: "trente-quatrième",
    35: "trente-cinquième",
    36: "trente-sixième",
    37: "trente-septième",
    38: "trente-huitième",
    39: "trente-neuvième",
    40: "quarantième",
    41: "quarante et unième",
    42: "quarante-deuxième",
    43: "quarante-troisième",
    44: "quarante-quatrième",
    45: "quarante-cinquième",
    46: "quarante-sixième",
    47: "quarante-septième",
    48: "quarante-huitième",
    49: "quarante-neuvième",
    50: "cinquantième"
}

# Only the differences for feminine ordinals
feminine_ordinal_differences = {
    1: "première",  # premier → première
    2: "seconde"  # second → seconde
}


def get_french_ordinal(number, feminine=True):
    """Get French ordinal, with option for feminine form"""
    base_form = french_ordinals.get(number)
    if base_form and feminine and number in feminine_ordinal_differences:
        return feminine_ordinal_differences[number]
    return base_form


def replace_roman_or_arabic_ordinals(text, feminine=True):
    """
    Replace Roman numeral ordinals (Ire, IIe, IIIe, etc.) and Arabic numeral ordinals (14e, 15e, etc.)
    with French ordinals (première, seconde, troisième, etc.) up to 50
    """

    def replace_match(match):
        # Get the full match and its position
        start_pos = match.start()

        # Don't replace if at the beginning of text
        if start_pos == 0:
            return match.group(0)  # Return original

        # Check the 3 characters before the match for a period
        check_start = max(0, start_pos - 3)
        preceding_chars = text[check_start:start_pos]

        # If there's a period in the preceding 3 characters, don't replace
        if '.' in preceding_chars:
            return match.group(0)  # Return original

        # Get the number (either Roman or Arabic)
        if match.group(1).isdigit():  # Arabic numeral
            number = int(match.group(1))
        else:  # Roman numeral
            number = roman_to_int(match.group(1))

        # Determine gender based on suffix
        suffix = match.group(2).lower()
        is_feminine = suffix in ['re', 'ère']  # 're' and 'ère' are feminine, 'er' and 'e' are masculine

        # Get the French ordinal
        if number in french_ordinals:
            return get_french_ordinal(number, is_feminine)
        else:
            # If we don't have the French equivalent, return original
            return match.group(0)

    # Pattern to match Roman numerals followed by 're', 'ère', 'er', or 'e'
    roman_pattern = r'\b([IVXL]+)(re|ère|er|e)\b'

    # Pattern to match Arabic numerals followed by 're', 'ère', 'er', or 'e'
    arabic_pattern = r'\b(\d+)(re|ère|er|e)\b'

    # First replace Roman numerals
    result = re.sub(roman_pattern, replace_match, text)

    # Then replace Arabic numerals
    result = re.sub(arabic_pattern, replace_match, result)

    return result


# Test the function
if __name__ == "__main__":
    test_text = "La Ire guerre mondiale, la IIe République, le IIIe siècle, le XXVIIIe arrondissement, le Le siècle."
    print("Original:", test_text)
    print("Replaced:", replace_roman_or_arabic_ordinals(test_text))

    # More test cases including higher numbers
    test_cases = [
        "La Ire étape",
        "La IIe division",
        "La IIIe République",
        "Le Ve siècle",
        "Le Xe arrondissement",
        "Le XXe siècle",
        "Le XXIe siècle",
        "Le XXVe anniversaire",
        "La XXXe édition",
        "Le XLe parallèle",
        "Le XLVe président",
        "Le Ie président",
        "Le jour"  # Roman numeral for 50
    ]

    for test in test_cases:
        print(f"{test} → {replace_roman_or_arabic_ordinals(test)}")

    result = replace_roman_or_arabic_ordinals("Le Ire jour", feminine=False)
    print(f"Le Ire jour → {result}")
