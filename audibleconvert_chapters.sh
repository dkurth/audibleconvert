#!/bin/bash

# Check if both file and activation bytes were provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: audibleconvert_chapters <file.aax> <activation_bytes>"
    exit 1
fi

input_file="$1"
activation_bytes="$2"

base_name="${input_file%.aax}"

# Extract chapter timestamps
chapter_times=$(ffprobe -i "$input_file" -print_format csv -show_chapters | awk -F',' 'NR>1 {printf "%s,", $2}')
chapter_times=${chapter_times%,}  # Remove trailing comma

if [ -z "$chapter_times" ]; then
    echo "No chapters found in file."
    exit 1
fi

# Convert to individual chapter MP3s
# Update the ffmpeg command to use the passed activation bytes
ffmpeg -activation_bytes "$activation_bytes" -i "$input_file" -f segment -segment_times "$chapter_times" -c:a libmp3lame -b:a 64k "${base_name}_chapter_%02d.mp3"

echo "Chapters extracted as MP3s!"
