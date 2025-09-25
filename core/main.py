import argparse
import os
import shutil
import subprocess
from argparse import ArgumentParser

from core.common.set_tags import set_remote_tag
from core.common.tracks import Track, YamlTrackReader
from core.text_to_speech.converter import TextToSpeechGenerator
from core.text_to_speech.reader import extract_text_from_url


def working_directory(args: argparse.Namespace, track_data: Track) -> tuple[str, bool]:
    """
    Create or handle working directory for track data.

    Returns:
        tuple[str, bool]: Directory path and boolean indicating whether existing data will be used
    """
    dir_path = f"audio_cache/{track_data.local_path()}"

    if os.path.exists(dir_path):
        if hasattr(args, 'erase_existing_data') and args.erase_existing_data:
            # Remove existing directory and recreate it - we won't use existing data
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
            return dir_path, False
        elif hasattr(args, 'use_existing_data') and args.use_existing_data:
            # Directory exists, and we want to use existing data
            return dir_path, True
        else:
            raise RuntimeError(
                f"Directory already exists: {dir_path}. Use the -r option to erase existing data or -u option to use existing data.")
    else:
        # Directory doesn't exist, create it - no existing data to use
        os.makedirs(dir_path)
        return dir_path, False


def download_and_convert(working_dir: str, track_data: Track) -> None:
    # Get URL from user
    url = track_data.link

    print(f"\nProcessing URL: {url}")

    # Extract text from webpage
    print("Extracting text from webpage...")
    paragraphs = extract_text_from_url(url)

    tt_sg = TextToSpeechGenerator(working_dir)

    for p in paragraphs:
        print(f"Extracted {len(p)} characters of text")
        print(p)

        # Convert to speech
        print("Converting text to speech...")
        tt_sg.text_to_speech_file(p)


def process_link(args: argparse.Namespace, track_data: Track) -> None:
    working_dir, use_existing_data = working_directory(args, track_data)

    if not use_existing_data:
        download_and_convert(working_dir, track_data)

    print("Concatenating data...")
    subprocess.run(["./scripts/concat.sh", working_dir])

    print("Pushing file...")
    subprocess.run(["./scripts/push.sh", working_dir, track_data.remote_scp_path()])

    print("Setting tags data...")
    set_remote_tag(track_data)


def main():
    """Main function"""
    parser = ArgumentParser()
    parser.add_argument('-r', '--erase-existing-data', action='store_true',
                        help='Erase already converted data.')

    parser.add_argument('-u', '--use-existing-data', action='store_true',
                        help='Use already converted data.')

    args = parser.parse_args()

    print("Web Article to Speech Converter")
    print("-" * 40)

    track_reader = YamlTrackReader()
    for track in track_reader.tracks:
        process_link(args, track)

    print("Done!")


if __name__ == "__main__":
    main()
