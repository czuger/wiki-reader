#!/bin/sh

cd "$1" || exit
ffmpeg -i concatenated_file.mp3 -metadata artist="$3" -metadata album="$4" -metadata title="$5" -metadata track="$6" -metadata tracknumber="$6" -c copy temp.mp3 && mv temp.mp3 "$2"
