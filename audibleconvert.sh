#!/bin/bash

# Ensure ffmpeg is found
export PATH="/opt/homebrew/bin:$PATH"

# Check if activation_bytes.txt exists
if [ ! -f "activation_bytes.txt" ]; then
    if [ -f "setup.md" ]; then
        cat setup.md
    else
        echo "Error: activation_bytes.txt not found."
        echo "Please create this file with your activation bytes."
    fi
    exit 1
fi

# Read activation bytes from file
activation_bytes=$(cat activation_bytes.txt)

# Check if activation bytes are empty
if [ -z "$activation_bytes" ]; then
    echo "Error: activation_bytes.txt is empty"
    exit 1
fi



# Check if a file was provided
if [ -z "$1" ]; then
  echo "Usage: audibleconvert <file.aax>"
  exit 1
fi

# Extract filename without extension
input_file="$1"
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
