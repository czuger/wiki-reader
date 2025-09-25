from cambai import CambAI, ApiException, OutputType

from config.config import Config


# Exemple d'utilisation
def main():
    config = Config("../config.json")

    # Remplacez par votre vraie clé API
    api_key = config.camb_ai_key()

    # Initialiser le client
    client = CambAI(api_key=api_key)

    try:
        voices = client.list_voices()
        print(f"Found {len(voices)} voices:")
        for voice in voices[:5]:  # Print first 5 as an example
            print(f"  - ID: {voice.id}, Name: {voice.voice_name}, Gender: {voice.gender}, Language: {voice.language}")
    except ApiException as e:
        print(f"Could not list voices: {e}")

    # pprint(client.get_target_languages())

    # return

    try:
        print("Generating a new voice and speech...")

        file_path = "my_generated_speech.mp3"

        client.text_to_speech(
            text="""Le Moyen Empire est une période de l'histoire de l'Égypte antique qui suit la Première Période intermédiaire et précède
la Deuxième Période intermédiaire. Il couvre une période allant des environs de 2033 à 1786 avant Jésus-Christ et
connaît deux ou trois dynasties""",
            voice_id=20298,  # Example voice ID
            output_type=OutputType.RAW_BYTES,  # Specify raw bytes for direct saving
            save_to_file=file_path,
            verbose=True,  # For more detailed logging from the SDK
            language=76
        )
        print("Good")

    except ApiException as e:
        print(f"API Exception when calling text_to_voice: {e}\n")


if __name__ == "__main__":
    main()
