import unittest

from core.roman2int.arabic2litteral import convert_numbers_to_french


class TestConvertNumbersToFrench(unittest.TestCase):
    """Tests pour la fonction convert_numbers_to_french."""

    def test_annees_multiples(self):
        """Teste la conversion de plusieurs années."""
        text = "Les années de 2033 à 1786 sont importantes."
        result = convert_numbers_to_french(text)
        self.assertIn("deux mille trente-trois", result)
        self.assertIn("mille sept cent quatre-vingt-six", result)

    def test_age_et_quantite(self):
        """Teste l'âge et la quantité de voitures."""
        text = "J'ai 25 ans et je possède 3 voitures."
        result = convert_numbers_to_french(text)
        self.assertIn("vingt-cinq", result)
        self.assertIn("trois", result)

    def test_prix_et_personnes(self):
        """Teste le prix et le nombre de personnes."""
        text = "Le prix est de 150 euros pour 2 personnes."
        result = convert_numbers_to_french(text)
        self.assertIn("cent cinquante", result)
        self.assertIn("deux", result)

    def test_annee_et_grand_nombre(self):
        """Teste une année et un grand nombre."""
        text = "En 1989, il y avait 1000000 habitants."
        result = convert_numbers_to_french(text)
        self.assertIn("mille neuf cent quatre-vingt-neuf", result)
        self.assertIn("un million", result)

        # Test also number with space
        text = "Il y avait 30 000 hommes"
        result = convert_numbers_to_french(text)
        self.assertIn("Il y avait trente mille hommes", result)

    def test_numeros_multiples(self):
        """Teste plusieurs numéros dans une liste."""
        text = "Les numéros gagnants sont: 7, 13, 42 et 99."
        result = convert_numbers_to_french(text)
        self.assertIn("sept", result)
        self.assertIn("treize", result)
        self.assertIn("quarante-deux", result)
        self.assertIn("quatre-vingt-dix-neuf", result)

    def test_nombre_negatif(self):
        """Teste un nombre négatif."""
        text = "La température était de -5 degrés."
        result = convert_numbers_to_french(text)
        self.assertIn("moins cinq", result)

    def test_texte_sans_nombre(self):
        """Teste qu'un texte sans nombre reste inchangé."""
        text = "Ceci est un texte sans chiffre."
        self.assertEqual(convert_numbers_to_french(text), text)


if __name__ == "__main__":
    unittest.main()
