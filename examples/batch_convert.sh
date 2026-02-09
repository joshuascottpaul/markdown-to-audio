#!/bin/bash
# Example: Batch convert all markdown files in a directory

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set"
    exit 1
fi

VOICE="${1:-shimmer}"
MODEL="${2:-tts-1-hd}"
FORMAT="${3:-mp3}"

echo "Converting all .md files with voice: $VOICE, model: $MODEL, format: $FORMAT"

for file in *.md; do
    if [ -f "$file" ]; then
        output="${file%.md}.$FORMAT"
        echo "Converting: $file -> $output"
        ./md2mp3-openai.py "$file" "$output" "$VOICE" "$MODEL" "$FORMAT"
    fi
done

echo "Done!"
