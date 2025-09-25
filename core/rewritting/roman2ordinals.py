import re

# French ordinal numbers up to 50
french_ordinals = {
    1: "première",
    2: "seconde",
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

def roman_to_int(roman):
    """Convert Roman numeral to integer"""
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    total = 0
    prev_value = 0

    for char in reversed(roman):
        value = roman_values.get(char, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total

def replace_roman_ordinals(text):
    """
    Replace Roman numeral ordinals (Ire, IIe, IIIe, etc.) with French ordinals
    (première, seconde, troisième, etc.) up to 50
    """
    # Pattern to match Roman numerals followed by 're' or 'e'
    # Updated to include L for 50
    pattern = r'\b([IVXL]+)(re|e)\b'

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

        roman_part = match.group(1)  # The Roman numeral part (I, II, III, etc.)
        suffix = match.group(2)  # The suffix (re or e)

        # Convert Roman numeral to integer
        number = roman_to_int(roman_part)

        # Get the French ordinal
        if number in french_ordinals:
            return french_ordinals[number]
        else:
            # If we don't have the French equivalent, return original
            return match.group(0)

    result = re.sub(pattern, replace_match, text)
    return result


# Test the function
if __name__ == "__main__":
    test_text = "La Ire guerre mondiale, la IIe République, le IIIe siècle, le XXVIIIe arrondissement, le Le siècle."
    print("Original:", test_text)
    print("Replaced:", replace_roman_ordinals(test_text))

    # More test cases including higher numbers
    test_cases = [
        "Ire étape",
        "IIe division",
        "IIIe République",
        "Ve siècle",
        "Xe arrondissement",
        "XXe siècle",
        "XXIe siècle",
        "XXVe anniversaire",
        "XXXe édition",
        "XLe parallèle",
        "XLVe président",
        "Le jour"  # Roman numeral for 50
    ]

    for test in test_cases:
        print(f"{test} → {replace_roman_ordinals(test)}")
