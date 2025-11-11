import os

from core.common.snake_case import snake_case


class TextBackup:
    """Classe pour sauvegarder des textes dans des fichiers.

    Cette classe permet de sauvegarder des versions originales et nettoyées
    de textes dans un répertoire basé sur les informations du track.
    """

    def __init__(self, track_data):
        """Initialise le système de sauvegarde.

        Args :
            track_data : Objet contenant les informations du track
        """
        self.backup_dir = f"cache/texts/{track_data.local_path()}"
        os.makedirs(self.backup_dir, exist_ok=True)

    def save_original(self, i: int, text: str) -> None:
        """Sauvegarde le texte original.

        Args :
            i : Numéro du fichier
            text : Texte à sauvegarder
        """
        filepath = f"{self.backup_dir}/{snake_case(text[:20])}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

    def save_cleaned(self, i: int, text: str) -> None:
        """Sauvegarde le texte nettoyé.

        Args :
            i : Numéro du fichier
            text : Texte nettoyé à sauvegarder
        """
        filepath = f"{self.backup_dir}/{snake_case(text[:20])}_cleaned.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
