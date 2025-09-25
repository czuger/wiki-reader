#!/bin/bash

# Navigate to audio_cache directory
cd "$1" || exit

# Remove any existing filelist
rm -f filelist.txt
rm -f concatenated_file.mp3

# Create filelist automatically from all MP3s in audio_cache directory
for file in *.mp3; do
    if [ -f "$file" ]; then
        echo "file '$file'" >> filelist.txt
        echo "Added: $file"
    fi
done

# Check if any MP3 files were found
if [ ! -f filelist.txt ] || [ ! -s filelist.txt ]; then
    echo "No MP3 files found in audio_cache directory"
    exit 1
fi

echo "Files to be joined:"
cat filelist.txt

# Join all MP3 files
echo "Joining files..."
ffmpeg -v quiet -f concat -safe 0 -i filelist.txt -c copy concatenated_file.mp3

# Clean up
rm filelist.txt

echo "Done! Combined file saved as concatenated_file.mp3 in  directory"
