# Markdown to Audio

Convert markdown files to high-quality audio using OpenAI's Text-to-Speech API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 6 natural-sounding voices (shimmer, alloy, echo, fable, onyx, nova)
- Multiple audio formats (MP3, Opus, AAC, FLAC, WAV, PCM)
- Automatic text chunking for long documents
- Voice preview mode
- Cost estimation before generation
- Markdown to plain text conversion

## Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

Quick install:
```bash
git clone https://github.com/joshuascottpaul/markdown-to-audio.git
cd markdown-to-audio
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key-here'
```

## For AI Agents

See [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for integration details and automation examples.

Machine-readable spec: [tool-spec.json](tool-spec.json)

## Cloud Deployment

Run on GitHub Actions, AWS Lambda, Google Cloud Run, and more.

See [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) for setup instructions.

## Requirements

- Python 3.7+
- OpenAI API key
- ffmpeg (for concatenating audio chunks)
- pandoc (optional, for better markdown conversion)

## Setup

Set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Basic usage:
```bash
./md2mp3-openai.py document.md
```

Preview all voices:
```bash
./md2mp3-openai.py --preview
```

Custom voice and format:
```bash
./md2mp3-openai.py document.md output.mp3 alloy tts-1-hd mp3
```

## Available Voices

- **shimmer** - Female, soft and warm (default)
- **alloy** - Neutral, balanced
- **echo** - Male, clear and expressive
- **fable** - British accent, warm
- **onyx** - Deep male voice
- **nova** - Female, energetic

## Audio Formats

- **mp3** - General use, widely compatible (default)
- **opus** - Internet streaming, smaller files
- **aac** - Mobile devices, YouTube
- **flac** - Lossless, highest quality
- **wav** - Uncompressed, professional editing
- **pcm** - Raw audio data

## Cost

- tts-1: $0.015 per 1K characters
- tts-1-hd: $0.030 per 1K characters (recommended)

## Examples

```bash
# Basic conversion
./md2mp3-openai.py article.md

# Different voice
./md2mp3-openai.py article.md output.mp3 echo

# AAC format for mobile
./md2mp3-openai.py article.md output.aac shimmer tts-1-hd aac

# Standard quality (cheaper)
./md2mp3-openai.py article.md output.mp3 shimmer tts-1 mp3
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Issues

Found a bug or have a feature request? [Open an issue](https://github.com/joshuascottpaul/markdown-to-audio/issues).

## License

MIT
