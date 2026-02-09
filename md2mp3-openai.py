#!/usr/bin/env python3
"""
Convert markdown to high-quality MP3 using OpenAI TTS API
"""

import os
import sys
from pathlib import Path

def show_help():
    help_text = """
Usage: ./md2mp3-openai.py [OPTIONS] input.md [output] [voice] [model] [format]

Convert markdown files to high-quality audio using OpenAI TTS.

Options:
  --preview [voice]   Generate sample audio files for all voices (or specific voice)
  --help, -h          Show this help message

Arguments:
  input.md      Markdown file to convert (required)
  output        Output filename (optional, defaults to input with format extension)
  voice         Voice name (optional, default: shimmer)
  model         TTS model (optional, default: tts-1-hd)
  format        Audio format (optional, default: mp3)

Available Voices (choose based on preference):
  shimmer       Female, soft and warm - gentle and calming (default)
  alloy         Neutral, balanced - good for professional content
  echo          Male, clear and expressive - good for narration
  fable         British accent, warm - distinctive and engaging
  onyx          Deep male voice - authoritative tone
  nova          Female, energetic - upbeat and dynamic

Models (quality vs. cost trade-off):
  tts-1         Standard quality - faster generation, half the cost
  tts-1-hd      High definition - best quality, recommended (default)
                Natural prosody, better pronunciation, clearer audio

Audio Formats:
  mp3           MP3 format - general use, widely compatible (default)
                Best for: General listening, podcasts, most devices
  opus          Opus format - internet streaming, low latency, smaller files
                Best for: Web streaming, real-time communication, bandwidth-limited
  aac           AAC format - digital audio compression, preferred by YouTube/iOS/Android
                Best for: Mobile devices, YouTube uploads, Apple ecosystem
  flac          FLAC format - lossless compression, highest quality
                Best for: Archival, audiophile listening, no quality loss
  wav           WAV format - uncompressed, largest files
                Best for: Professional audio editing, maximum compatibility
  pcm           PCM format - raw audio data
                Best for: Audio processing, development, raw format needs

Examples:
  # Basic usage (shimmer voice, HD quality, MP3)
  ./md2mp3-openai.py document.md

  # Preview all voices
  ./md2mp3-openai.py --preview

  # Preview specific voice
  ./md2mp3-openai.py --preview echo

  # Custom output filename
  ./md2mp3-openai.py document.md audio.mp3

  # Different voice (neutral professional)
  ./md2mp3-openai.py document.md output.mp3 alloy

  # Opus format for streaming (smaller file)
  ./md2mp3-openai.py document.md output.opus shimmer tts-1-hd opus

  # AAC format for YouTube/mobile
  ./md2mp3-openai.py document.md output.aac shimmer tts-1-hd aac

  # FLAC format for highest quality
  ./md2mp3-openai.py document.md output.flac shimmer tts-1-hd flac

  # Standard quality MP3 (faster, cheaper)
  ./md2mp3-openai.py document.md output.mp3 shimmer tts-1 mp3

Features:
  - Automatically splits long documents into chunks (4000 char limit per API call)
  - Concatenates chunks seamlessly into single audio file
  - Converts markdown to plain text (removes formatting)
  - Shows character count and estimated cost before generation
  - Supports 6 audio formats (mp3, opus, aac, flac, wav, pcm)
  - Preview mode to test all voices before converting

Format Comparison:
  File Size:  opus < aac < mp3 < flac < wav < pcm
  Quality:    pcm = wav = flac > aac ≈ mp3 > opus
  Streaming:  opus (best) > aac > mp3 > others
  Mobile:     aac (best) > mp3 > opus > others

Notes:
  - Long documents are split into multiple API calls and concatenated
  - Cost is per character: tts-1-hd is $0.030/1K chars, tts-1 is $0.015/1K chars
  - Typical 10-page document (~5000 chars) costs $0.15 (HD) or $0.075 (standard)
  - Quality difference between tts-1 and tts-1-hd is noticeable - HD recommended
  - Format choice doesn't affect API cost, only file size and compatibility
  - For most use cases, MP3 (default) provides best balance of quality and compatibility

Environment:
  OPENAI_API_KEY must be set

Cost:
  tts-1:    $0.015 per 1K characters (~$0.75 per 50K chars)
  tts-1-hd: $0.030 per 1K characters (~$1.50 per 50K chars)
"""
    print(help_text)
    sys.exit(0)

def preview_voices(specific_voice=None):
    """Generate voice samples for preview"""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    voices = [specific_voice] if specific_voice else ['shimmer', 'alloy', 'echo', 'fable', 'onyx', 'nova']
    sample_text = "Hello! This is a sample of my voice. I'm demonstrating the text to speech capabilities of OpenAI's API. Each voice has its own unique character and tone."
    
    print("Generating voice samples...")
    cost = len(voices) * 0.003
    print(f"Cost: ~${cost:.2f} total\n")
    
    for voice in voices:
        output_file = f"voice-sample-{voice}.mp3"
        print(f"Generating {voice}...", end='', flush=True)
        
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=sample_text
        )
        
        response.stream_to_file(output_file)
        print(f" ✓ saved to {output_file}")
    
    print("\n✓ All samples generated!")
    print("\nListen to each sample and pick your favorite voice.")
    print("Then use it with: ./md2mp3-openai.py document.md output.mp3 <voice>")
    sys.exit(0)

def main():
    # Check for preview mode
    if len(sys.argv) > 1 and sys.argv[1] == '--preview':
        specific_voice = sys.argv[2] if len(sys.argv) > 2 else None
        if specific_voice and specific_voice not in ['shimmer', 'alloy', 'echo', 'fable', 'onyx', 'nova']:
            print(f"Error: Unknown voice '{specific_voice}'")
            print("Available: shimmer, alloy, echo, fable, onyx, nova")
            sys.exit(1)
        preview_voices(specific_voice)
    
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        show_help()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    voice = sys.argv[3] if len(sys.argv) > 3 else 'shimmer'
    model = sys.argv[4] if len(sys.argv) > 4 else 'tts-1-hd'
    audio_format = sys.argv[5] if len(sys.argv) > 5 else 'mp3'
    
    # Validate format
    valid_formats = ['mp3', 'opus', 'aac', 'flac', 'wav', 'pcm']
    if audio_format not in valid_formats:
        print(f"Error: Invalid format '{audio_format}'")
        print(f"Valid formats: {', '.join(valid_formats)}")
        sys.exit(1)
    
    # Set default output file if not provided
    if not output_file:
        output_file = input_file.replace('.md', f'.{audio_format}')
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Check if openai package is installed
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed")
        print("Install with: pip3 install openai")
        sys.exit(1)
    
    # Read and convert markdown to plain text
    print(f"Reading {input_file}...")
    try:
        import subprocess
        result = subprocess.run(
            ['pandoc', input_file, '-t', 'plain'],
            capture_output=True,
            text=True,
            check=True
        )
        text = result.stdout
    except subprocess.CalledProcessError:
        # Fallback: just read the file
        with open(input_file, 'r') as f:
            text = f.read()
    
    # Remove excessive whitespace
    text = '\n'.join(line for line in text.split('\n') if line.strip())
    
    char_count = len(text)
    cost_estimate = (char_count / 1000) * (0.030 if model == 'tts-1-hd' else 0.015)
    
    print(f"Converting to audio...")
    print(f"Voice: {voice} | Model: {model} | Format: {audio_format}")
    print(f"Characters: {char_count:,} | Est. cost: ${cost_estimate:.2f}")
    
    # Generate speech
    client = OpenAI(api_key=api_key)
    
    # Split text into chunks if needed (4000 char limit with buffer)
    max_chunk_size = 4000
    chunks = []
    
    if len(text) <= max_chunk_size:
        chunks = [text]
    else:
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            # If single paragraph is too long, split by sentences
            if len(para) > max_chunk_size:
                sentences = para.split('. ')
                for sent in sentences:
                    if len(current_chunk) + len(sent) + 2 <= max_chunk_size:
                        current_chunk += sent + ". "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sent + ". "
            elif len(current_chunk) + len(para) + 2 <= max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    print(f"Generating {len(chunks)} audio chunk(s)...")
    
    # Generate audio for each chunk
    import tempfile
    temp_files = []
    
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}/{len(chunks)}...", end='', flush=True)
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=chunk,
            response_format=audio_format
        )
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_format}')
        response.stream_to_file(temp_file.name)
        temp_files.append(temp_file.name)
        print(" done")
    
    # Concatenate if multiple chunks
    if len(temp_files) == 1:
        import shutil
        shutil.move(temp_files[0], output_file)
    else:
        print("Concatenating audio chunks...")
        import subprocess
        
        # Create concat file list
        concat_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        for tf in temp_files:
            concat_file.write(f"file '{tf}'\n")
        concat_file.close()
        
        # Use ffmpeg to concatenate
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', concat_file.name, '-c', 'copy', output_file, '-y'
        ], capture_output=True, check=True)
        
        # Cleanup
        os.unlink(concat_file.name)
        for tf in temp_files:
            os.unlink(tf)
    
    print(f"✓ Audio saved to: {output_file}")

if __name__ == '__main__':
    main()
