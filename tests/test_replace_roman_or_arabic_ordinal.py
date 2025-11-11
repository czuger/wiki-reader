import unittest

from core.roman2int.roman2ordinals import replace_roman_or_arabic_ordinals


class TestReplaceRomanOrArabicOrdinals(unittest.TestCase):
    """Tests pour la fonction replace_roman_or_arabic_ordinals.

    Vérifie la conversion correcte des ordinaux romains en leur forme littérale.
    """

    def test_basic_feminine_ordinals(self) -> None:
        """Teste les ordinaux romains féminins de base."""
        test_cases = [
            ("La Ire étape", "La première étape"),
            ("La IIe division", "La deuxième division"),
            ("La IIIe République", "La troisième République"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = replace_roman_or_arabic_ordinals(input_text)
                self.assertEqual(result, expected)

    def test_single_digit_ordinals(self) -> None:
        """Teste les ordinaux romains à un chiffre."""
        test_cases = [
            ("Le Ve siècle", "Le cinquième siècle"),
            ("Le Xe arrondissement", "Le dixième arrondissement"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = replace_roman_or_arabic_ordinals(input_text)
                self.assertEqual(result, expected)

    def test_two_digit_ordinals(self) -> None:
        """Teste les ordinaux romains à deux chiffres."""
        test_cases = [
            ("Le XXe siècle", "Le vingtième siècle"),
            ("Le XXIe siècle", "Le vingt et unième siècle"),
            ("Le XXVe anniversaire", "Le vingt-cinquième anniversaire"),
            ("La XXXe édition", "La trentième édition"),
            ("Le XLe parallèle", "Le quarantième parallèle"),
            ("Le XLVe président", "Le quarante-cinquième président"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = replace_roman_or_arabic_ordinals(input_text)
                self.assertEqual(result, expected)

    def test_complex_sentence(self) -> None:
        """Teste une phrase contenant plusieurs ordinaux."""
        input_text = "La Ire guerre mondiale, la IIe République, le IIIe siècle, le XXVIIIe arrondissement, le Le siècle."
        result = replace_roman_or_arabic_ordinals(input_text)

        self.assertIn("première", result)
        self.assertIn("deuxième", result)
        self.assertIn("troisième", result)
        self.assertIn("vingt-huitième", result)

    def test_masculine_gender(self) -> None:
        """Teste le mode masculin avec le paramètre feminine=False."""
        input_text = "Le Ier jour"
        result = replace_roman_or_arabic_ordinals(input_text, feminine=False)

        self.assertEqual(result, "Le premier jour")

    def test_no_ordinal(self) -> None:
        """Teste un texte sans ordinal romain."""
        input_text = "Le jour"
        result = replace_roman_or_arabic_ordinals(input_text)

        self.assertEqual(result, input_text)

    def test_edge_case_first_ordinal(self) -> None:
        """Teste spécifiquement le premier ordinal."""
        input_text = "Le Ie président"
        result = replace_roman_or_arabic_ordinals(input_text)

        self.assertIn("premier", result)


if __name__ == "__main__":
    unittest.main()
