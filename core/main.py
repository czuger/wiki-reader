import os
import shutil

from core.converter import TextToSpeechGenerator
from core.reader import extract_text_from_url


def main():
    """Main function"""
    print("Web Article to Speech Converter")
    print("-" * 40)

    shutil.rmtree("audio_cache")
    os.makedirs("audio_cache")

    # Get URL from user
    url = "https://fr.wikipedia.org/wiki/P%C3%A9riode_pr%C3%A9dynastique_%C3%A9gyptienne"

    print(f"\nProcessing URL: {url}")

    # Extract text from webpage
    print("Extracting text from webpage...")
    paragraphs = extract_text_from_url(url)

    tt_sg = TextToSpeechGenerator()

    for p in paragraphs:
        print(f"Extracted {len(p)} characters of text")
        print(p)

        # Convert to speech
        print("Converting text to speech...")
        tt_sg.text_to_speech_file(p)

    print("Done!")

if __name__ == "__main__":
    main()