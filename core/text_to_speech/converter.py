import os

from openai import OpenAI

from config.config import Config


class TextToSpeechGenerator:
    INSTRUCTIONS = """
        Effet vocal : Calme, posé et rassurant ; projeter une autorité tranquille et de la confiance.
        Ton : Sincère, empathique et délicatement autoritaire — exprimer des excuses authentiques tout en transmettant la compétence.
        Rythme : Régulier et modéré ; suffisamment posé pour communiquer l'attention, mais assez efficace pour démontrer le professionnalisme.
        Émotion : Empathie et compréhension véritables ; parler avec chaleur."""

    def __init__(self, working_dir: str):
        """Initialize the TTS generator with OpenAI client and iterator"""
        # Initialize OpenAI client
        config = Config()
        self.client = OpenAI(api_key=config.openai_key())

        # Initialize iterator for file naming
        self.file_iterator = 0

        # Create audio directory if it doesn't exist
        self.audio_dir = working_dir
        os.makedirs(self.audio_dir, exist_ok=True)

    def _generate_filename(self):
        """Generate filename using iterator and increment it"""
        filename = f"audio_{self.file_iterator:04d}.mp3"
        self.file_iterator += 1
        return filename

    def text_to_speech_file(self, text):
        """Convert text to speech using OpenAI TTS and save to file"""
        # Generate filename using iterator
        audio_filename = self._generate_filename()
        audio_path = os.path.join(self.audio_dir, audio_filename)

        print(f"Generating audio as: {audio_filename}")

        # Use the streaming response method
        with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="onyx",
                input=text,
                instructions=self.INSTRUCTIONS,
        ) as response:
            response.stream_to_file(audio_path)

        print(f"Audio saved to: {audio_path}")
        return audio_path

    def reset_iterator(self):
        """Reset the file iterator to 0"""
        self.file_iterator = 0

    def get_current_iterator_value(self):
        """Get the current iterator value"""
        return self.file_iterator
