import argparse
import os
import shutil
import subprocess

from core.common.Tracks import Track, TrackReader
from core.text_to_speech.converter import TextToSpeechGenerator
from core.text_to_speech.reader import extract_text_from_url

def process_link(track_data: Track) -> None:
    shutil.rmtree("audio_cache")
    os.makedirs("audio_cache")

    # Get URL from user
    url = track_data.link

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

    print("Concatenating data...")
    subprocess.run(["./scripts/concat.sh", "audio_cache"])

    print("Setting tags data...")
    subprocess.run(["./scripts/set_tags.sh", "audio_cache", track_data.distant_name, track_data.album, track_data.artist, track_data.title, track_data.track_id])

    print("Pushing file...")
    subprocess.run(["./scripts/push.sh", "audio_cache", track_data.distant_name, track_data.distant_path])


def main():
    """Main function"""

    print("Web Article to Speech Converter")
    print("-" * 40)

    track_reader = TrackReader()
    for track in track_reader.tracks:
        process_link(track)

    print("Done!")

if __name__ == "__main__":
    main()