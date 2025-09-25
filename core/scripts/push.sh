#!/bin/sh

cd "$1" || exit

pwd

scp "concatenated_file.mp3" "$2"