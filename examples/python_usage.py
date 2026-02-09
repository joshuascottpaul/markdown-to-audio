#!/usr/bin/env python3
"""
Example: Use md2mp3-openai.py from Python code
"""

import subprocess
import os
import sys

def convert_markdown_to_audio(
    input_file,
    output_file=None,
    voice="shimmer",
    model="tts-1-hd",
    audio_format="mp3"
):
    """
    Convert markdown to audio using md2mp3-openai.py
    
    Args:
        input_file: Path to markdown file
        output_file: Path to output audio file (optional)
        voice: Voice name (shimmer, alloy, echo, fable, onyx, nova)
        model: TTS model (tts-1, tts-1-hd)
        audio_format: Audio format (mp3, opus, aac, flac, wav, pcm)
    
    Returns:
        True if successful, False otherwise
    """
    
    # Check API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        return False
    
    # Build command
    cmd = ['./md2mp3-openai.py', input_file]
    if output_file:
        cmd.append(output_file)
    cmd.extend([voice, model, audio_format])
    
    # Run conversion
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return False

if __name__ == '__main__':
    # Example usage
    success = convert_markdown_to_audio(
        'tests/test_document.md',
        'test_output.mp3',
        voice='alloy',
        model='tts-1-hd',
        audio_format='mp3'
    )
    
    if success:
        print("✓ Conversion successful")
    else:
        print("✗ Conversion failed")
        sys.exit(1)
