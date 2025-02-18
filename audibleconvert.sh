#!/bin/bash

# Ensure ffmpeg is found
export PATH="/opt/homebrew/bin:$PATH"

# Check if both file and activation bytes were provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: audibleconvert <file.aax> <activation_bytes>"
  exit 1
fi

# Extract filename without extension
input_file="$1"
activation_bytes="$2"
output_file="${input_file%.aax}.mp3"

# Run the conversion with progress shown
echo "Converting: $input_file -> $output_file"
ffmpeg -activation_bytes "$activation_bytes" -i "$input_file" -c:a libmp3lame -b:a 64k "$output_file"

# Check if conversion succeeded
if [ $? -eq 0 ]; then
  echo "Conversion complete: $output_file"
else
  echo "Error: Conversion failed."
  exit 1
fi
