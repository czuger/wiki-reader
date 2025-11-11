import re

from num2words import num2words


def convert_numbers_to_french(text: str) -> str:
    """
    Convertit tous les nombres arabes d'un texte en forme littérale française.

    Args :
        text : Texte contenant des nombres arabes

    Returns :
        Texte avec les nombres convertis en littéral français
    """
    # D'abord, supprimer les espaces dans les grands nombres (30 000 -> 30000)
    text = re.sub(r'(\d+)\s+(\d{3})', r'\1\2', text)

    # Pattern pour matcher les entiers (positifs et négatifs)
    pattern = r'-?\b\d+\b'

    def replace_number(match):
        number = int(match.group())
        return num2words(number, lang='fr')

    # Remplacer tous les nombres par leur équivalent littéral français
    result = re.sub(pattern, replace_number, text)
    return result
