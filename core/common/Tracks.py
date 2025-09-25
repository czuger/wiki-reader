class TrackReader:
    def __init__(self, file_path: str = "links.txt"):
        self.file_path = file_path
        self.tracks = []
        self._load_tracks()

    def _load_tracks(self):
        """Load tracks from the file, discarding commented lines."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()

                # Skip empty lines and commented lines (starting with #)
                if not line or line.startswith('#'):
                    continue

                # Split by semicolon
                parts = line.split(';')

                if len(parts) == 7:
                    track = Track(*parts)
                    self.tracks.append(track)
                else:
                    print(f"Warning: Line {line_num} has incorrect number of fields: {line}")



class Track:
    def __init__(self, link, artist, album, title, track_id, distant_name, distant_path):
        self.link = link.strip()
        self.artist = artist.strip()
        self.album = album.strip()
        self.title = title.strip()
        self.track_id = track_id.strip()
        self.distant_name = distant_name.strip()
        self.distant_path = distant_path.strip()

    # Getters
    def get_link(self):
        return self.link

    def get_artist(self):
        return self.artist

    def get_album(self):
        return self.album

    def get_title(self):
        return self.title

    def get_track_id(self):
        return self.track_id

    def get_distant_name(self):
        return self.distant_name

    def get_distant_path(self):
        return self.distant_path

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.album})"

    def __repr__(self):
        return f"Track(artist='{self.artist}', title='{self.title}', album='{self.album}')"
