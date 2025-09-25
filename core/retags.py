from core.common.set_tags import set_remote_tag
from core.common.tracks import YamlTrackReader


def main():
    """Main function"""
    print("Rewriting tags")
    print("-" * 40)

    track_reader = YamlTrackReader()
    for track in track_reader.tracks:
        set_remote_tag(track)

    print("Done!")


if __name__ == "__main__":
    main()
