## Installation

```bash
# Clone the repository
git clone https://github.com/joshuascottpaul/markdown-to-audio.git
cd markdown-to-audio

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Make script executable (if needed)
chmod +x md2mp3-openai.py

# Test it works
./md2mp3-openai.py --help
```

## Quick Start

```bash
# Convert a markdown file to audio
./md2mp3-openai.py document.md

# Preview all available voices
./md2mp3-openai.py --preview

# Use a specific voice
./md2mp3-openai.py document.md output.mp3 echo
```

## System Requirements

- Python 3.7 or higher
- ffmpeg (for concatenating audio chunks)
- pandoc (optional, improves markdown conversion)

### Installing ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)
