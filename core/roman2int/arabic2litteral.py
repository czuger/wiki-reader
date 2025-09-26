import re

from num2words import num2words


def convert_numbers_to_french(text):
    """
    Converts all Arabic numbers in a text to French literal form.

    Args:
        text (str): Input text containing Arabic numbers

    Returns:
        str: Text with Arabic numbers converted to French literals
    """
    # Pattern to match integers (positive and negative)
    pattern = r'-?\b\d+\b'

    def replace_number(match):
        number = int(match.group())
        try:
            return num2words(number, lang='fr')
        except:
            # If conversion fails, return original number
            return match.group()

    # Replace all numbers with their French literal equivalent
    result = re.sub(pattern, replace_number, text)
    return result


# Test examples
if __name__ == "__main__":
    # Test with your numbers
    test_text1 = "Les années de 2033 à 1786 sont importantes."
    print("Original:", test_text1)
    print("Converted:", convert_numbers_to_french(test_text1))
    print()

    # More test examples
    test_cases = [
        "J'ai 25 ans et je possède 3 voitures.",
        "Le prix est de 150 euros pour 2 personnes.",
        "En 1989, il y avait 1000000 habitants.",
        "Les numéros gagnants sont: 7, 13, 42 et 99.",
        "La température était de -5 degrés."
    ]

    for test in test_cases:
        print("Original:", test)
        print("Converted:", convert_numbers_to_french(test))
        print()
