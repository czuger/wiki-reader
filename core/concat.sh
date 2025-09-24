#!/bin/bash

# Navigate to audio_cache directory
cd audio_cache

# Remove any existing filelist
rm -f filelist.txt

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
ffmpeg -f concat -safe 0 -i filelist.txt -c copy ../combined_audio.mp3

# Clean up
rm filelist.txt

echo "Done! Combined file saved as combined_audio.mp3 in parent directory"
