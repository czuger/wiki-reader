import subprocess

from core.common.tracks import Track


def set_remote_tag(track_data: Track) -> None:
    remote_path = track_data.remote_name()
    temp_path = "/tmp/temp.mp3"

    # First command: ffmpeg with metadata
    ffmpeg_cmd = [
        "ssh", track_data.remote_server,
        f'ffmpeg -i "{remote_path}" -metadata "artist={track_data.artist}" -metadata "album={track_data.album}" '
        f'-metadata "title={track_data.title}" -metadata "track={track_data.track_id}" '
        f'-metadata "tracknumber={track_data.track_id}" -c copy {temp_path}'
    ]

    # Second command: move temp file
    mv_cmd = [
        "ssh", track_data.remote_server,
        f'mv {temp_path} "{remote_path}"'
    ]

    try:
        # Run ffmpeg
        result1 = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print("FFmpeg completed successfully")

        # Move file back
        result2 = subprocess.run(mv_cmd, check=True, capture_output=True, text=True)
        print("Tags set successfully on remote server")

    except subprocess.CalledProcessError as e:
        print(f"Error setting tags on remote server: {e}")
        print(f"stderr: {e.stderr}")
        # Cleanup temp file if it exists
        cleanup_cmd = ["ssh", track_data.remote_server, f"rm -f {temp_path}"]
        subprocess.run(cleanup_cmd, capture_output=True)
