import json
from typing import Dict, Any


class Config:
    def __init__(self, config_file_path: str = "config.json") -> None:
        """
        Initialize config from JSON file.

        Parameters
        ----------
        config_file_path : str, optional
            Path to the JSON configuration file, by default "config.json"
        """
        with open(config_file_path, 'r') as f:
            self._config: Dict[str, Any] = json.load(f)

    # OpenAI accessors
    def openai_key(self) -> str:
        """Return OpenAI API key."""
        return self._config['open_ai']['openai_key']

    # Mongo accessors
    def mongo_server(self) -> str:
        """Return MongoDB server address."""
        return self._config['mongo']['server']

    def mongo_user(self) -> str:
        """Return MongoDB username."""
        return self._config['mongo']['user']

    def mongo_pass(self) -> str:
        """Return MongoDB password."""
        return self._config['mongo']['pass']

    def mongo_database(self) -> str:
        """Return MongoDB database name."""
        return self._config['mongo']['database']

    def mongo_url(self) -> str:
        """Return complete MongoDB connection URL."""
        user = self._config['mongo']['user']
        password = self._config['mongo']['pass']
        server = self._config['mongo']['server']
        database = self._config['mongo']['database']
        return f"mongodb://{user}:{password}@{server}/{database}"

    # Flask accessors
    def flask_secret_key(self) -> str:
        """Return Flask secret key."""
        return self._config['flask']['secret_key']
