from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK
from mutagen.mp3 import MP3

from core.common.tracks import Track


def set_local_tag(track_data: Track) -> None:
    local_path = track_data.local_tmp_path()  # or whatever method gets local path

    audio = MP3(local_path, ID3=ID3)

    if audio.tags is None:
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=track_data.title))
    audio.tags.add(TPE1(encoding=3, text=track_data.artist))
    audio.tags.add(TALB(encoding=3, text=track_data.album))
    audio.tags.add(TRCK(encoding=3, text=str(track_data.track_id)))

    audio.save()
