import argparse
import os
import shutil
import subprocess
from argparse import ArgumentParser

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from core.common.set_tags import set_local_tag
from core.common.tracks import Track, YamlTrackReader
from core.libs.text_backup import TextBackup
from core.text_to_speech.converter import TextToSpeechGenerator
from core.text_to_speech.reader import extract_text_from_url


def copy_to_remote(local_path: str, remote_server: str, remote_path: str) -> None:
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_server)

    # Create remote directory if it doesn't exist
    remote_dir = os.path.dirname(remote_path)
    ssh.exec_command(f'mkdir -p "{remote_dir}"')

    scp = SCPClient(ssh.get_transport())
    scp.put(local_path, remote_path)

    scp.close()
    ssh.close()


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
    text_backuper = TextBackup(track_data)

    print(f"\nProcessing URL: {url}")

    # Extract text from webpage
    print("Extracting text from webpage...")
    paragraphs = extract_text_from_url(url, track_data)

    backup_paragraph_dir = f"cache/texts/{track_data.local_path()}"
    os.makedirs(backup_paragraph_dir, exist_ok=True)

    tt_sg = TextToSpeechGenerator(working_dir)

    for i, p in enumerate(paragraphs):
        print(f"Extracted {len(p)} characters of text")
        print(p)

        text_backuper.save_cleaned(i, p)

        # Convert to speech
        print("Converting text to speech...")
        tt_sg.text_to_speech_file(p, track_data)


def process_link(args: argparse.Namespace, track_data: Track) -> None:
    working_dir, use_existing_data = working_directory(args, track_data)

    if not use_existing_data:
        download_and_convert(working_dir, track_data)

    print("Concatenating data...")
    subprocess.run(["./scripts/concat.sh", working_dir])

    print("Setting tags data...")
    set_local_tag(track_data)

    print("Pushing file...")
    copy_to_remote(f"{working_dir}/concatenated_file.mp3", track_data.remote_server, track_data.remote_name())


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

    track_reader = YamlTrackReader(file_path="links/rois_france.yaml")
    for track in track_reader.tracks:
        process_link(args, track)

    print("Done!")


if __name__ == "__main__":
    main()
