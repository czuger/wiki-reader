import yaml

from core.common.snake_case import snake_case


class YamlTrackReader:
    def __init__(self, file_path: str = "links.yaml"):
        self.file_path = file_path
        self.tracks = []
        self.globals = {}
        self._load_tracks()

    def _load_tracks(self):
        """Load tracks from the YAML file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        # Load global settings
        self.globals = data.get('globals', {})

        # Load tracks
        tracks_data = data.get('tracks', [])
        for track_data in tracks_data:
            # Merge global settings with track-specific data
            merged_data = {**self.globals, **track_data}

            track = Track(
                link=merged_data.get('link', ''),
                artist=merged_data.get('artist', ''),
                album=merged_data.get('album', ''),
                title=merged_data.get('title', ''),
                track_id=merged_data.get('track_id', ''),
                remote_server=merged_data.get('remote_server', ''),
                distant_path=merged_data.get('remote_path', '')  # Note: YAML uses 'remote_path'
            )
            self.tracks.append(track)


class Track:
    def __init__(self, link, artist, album, title, track_id, remote_server, distant_path):
        self.link = str(link).strip()
        self.artist = str(artist).strip()
        self.album = str(album).strip()
        self.title = str(title).strip()
        self.track_id = str(track_id).strip()
        self.distant_name = snake_case(title)
        self.remote_server = str(remote_server).strip()
        self.distant_path = str(distant_path).strip()

    def remote_name(self):
        return f"{self.distant_path}/{self.distant_name}.mp3"

    def remote_scp_path(self):
        return f"{self.remote_server}:{self.remote_name()}"

    def local_path(self):
        return snake_case(self.title)

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.album})"

    def __repr__(self):
        return f"Track(artist='{self.artist}', title='{self.title}', album='{self.album}')"
