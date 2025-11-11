import re

from core.roman2int.roman2int import roman_to_int

french_ordinals = {
    1: "premier",
    2: "deuxième",
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
    2: "deuxième"  # second → seconde
}


def find_if_sentence_is_feminine(phrase: str) -> bool:
    """
    Détecte si une phrase française est au féminin.

    Cette fonction analyse l'article défini au début de la phrase
    pour déterminer si le genre est féminin (La).

    Args :
        phrase : La phrase française à analyser

    Returns :
        True si la phrase est au féminin (commence par "La"), False sinon
    """
    # Convertir en minuscules pour la comparaison et séparer les mots
    phrase_lower = phrase.lower().strip()
    premier_mot = phrase_lower.split()[0]

    # Vérifier l'article défini
    if premier_mot == "la":
        return True
    else:
        return False


def get_french_ordinal(number: int, feminine: bool) -> str:
    """
    Obtient l'ordinal français pour un nombre donné.

    Cette fonction retourne la forme ordinale d'un nombre en français,
    avec possibilité d'obtenir la forme féminine si elle diffère de la forme masculine.

    Args :
        number : Le nombre à convertir en ordinal
        feminine : True pour la forme féminine, False pour la forme masculine

    Returns :
        L'ordinal en français (ex : "premier", "première", "deuxième")
    """
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

        # If there's a « in the preceding 3 characters, don't replace
        if '«' in preceding_chars:
            return match.group(0)  # Return original

        # Get the number (either Roman or Arabic)
        if match.group(1).isdigit():  # Arabic numeral
            number = int(match.group(1))
        else:  # Roman numeral
            number = roman_to_int(match.group(1))

        # Determine gender based on suffix
        suffix = match.group(2).lower()
        is_feminine = suffix in ['re', 'ère']  # 're' and 'ère' are feminine, 'er' and 'e' are masculine

        if not is_feminine and find_if_sentence_is_feminine(text):
            is_feminine = True

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
