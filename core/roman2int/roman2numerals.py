import re

from core.roman2int.roman2ordinals import roman_to_int

# French cardinal numbers (un, deux, trois, etc.)
french_numerals = {
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "onze",
    12: "douze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
    17: "dix-sept",
    18: "dix-huit",
    19: "dix-neuf",
    20: "vingt",
    21: "vingt et un",
    22: "vingt-deux",
    23: "vingt-trois",
    24: "vingt-quatre",
    25: "vingt-cinq",
    26: "vingt-six",
    27: "vingt-sept",
    28: "vingt-huit",
    29: "vingt-neuf",
    30: "trente",
    31: "trente et un",
    32: "trente-deux",
    33: "trente-trois",
    34: "trente-quatre",
    35: "trente-cinq",
    36: "trente-six",
    37: "trente-sept",
    38: "trente-huit",
    39: "trente-neuf",
    40: "quarante",
    41: "quarante et un",
    42: "quarante-deux",
    43: "quarante-trois",
    44: "quarante-quatre",
    45: "quarante-cinq",
    46: "quarante-six",
    47: "quarante-sept",
    48: "quarante-huit",
    49: "quarante-neuf",
    50: "cinquante"
}


def replace_roman_numerals(text):
    """
    Replace standalone Roman numerals (I, II, III, etc.) with French ordinals
    (première, seconde, troisième, etc.) up to 50
    """
    # Pattern to match standalone Roman numerals
    pattern = r'\b([IVXL]+)\b'

    def replace_match(match):
        # Get the full match and its position
        start_pos = match.start()

        # Don't replace if at the beginning of text
        if start_pos == 0:
            return match.group(0)

        # Check the 3 characters before the match for a period
        check_start = max(0, start_pos - 3)
        preceding_chars = text[check_start:start_pos]

        # If there's a period in the preceding 3 characters, don't replace
        if '.' in preceding_chars:
            return match.group(0)

        roman_part = match.group(1)

        # Only convert if it's a valid Roman numeral
        try:
            # Check if it only contains valid Roman numeral characters
            if all(c in 'IVXL' for c in roman_part):
                number = roman_to_int(roman_part)

                # Make sure it's a positive number and within our range
                if number > 0 and number in french_numerals:
                    return french_numerals[number]
        except:
            pass

        return match.group(0)  # Return original if not convertible

    result = re.sub(pattern, replace_match, text)
    return result


# Test the function
if __name__ == "__main__":
    test_text = "Volume I, Chapitre II, Partie III, le livre V contient des informations."
    print("Original:", test_text)
    print("Replaced:", replace_roman_numerals(test_text))

    # Test cases for standalone Roman numerals
    test_cases = [
        "Volume I",
        "Chapitre II",
        "Partie III",
        "Section IV",
        "Tome V",
        "Livre VI",
        "Annexe VII",
        "Acte VIII",
        "Article IX",
        "Point X",
        "Phase XI",
        "Étape XII",
        "Niveau XV",
        "Série XX",
        "Groupe XXV",
        "Classe XXX",
        "Division XXXV",
        "Secteur XL",
        "Zone XLV",
        "Région L",
        "Le I est important",
        "Numéro II disponible",
        "Option III choisie",
        "La Division XXXV",
    ]

    print("\nTest cases:")
    for test in test_cases:
        result = replace_roman_numerals(test)
        if result != test:
            print(f"{test} → {result}")
        else:
            print(f"{test} → (unchanged)")
