# Examples

This directory contains example scripts showing how to use markdown-to-audio in different scenarios.

## Batch Conversion (Bash)

`batch_convert.sh` - Convert all markdown files in a directory

```bash
# Use defaults (shimmer voice, HD quality, MP3)
./examples/batch_convert.sh

# Specify voice, model, and format
./examples/batch_convert.sh echo tts-1-hd aac
```

## Python Integration

`python_usage.py` - Use the tool from Python code

```bash
./examples/python_usage.py
```

Or import the function in your own code:

```python
from examples.python_usage import convert_markdown_to_audio

convert_markdown_to_audio(
    'document.md',
    'output.mp3',
    voice='alloy',
    model='tts-1-hd',
    audio_format='mp3'
)
```

## AI Agent Integration

For AI agents and automation systems, see [AI_AGENT_GUIDE.md](../AI_AGENT_GUIDE.md) for:
- Command structure reference
- Voice/format selection guides
- Cost estimation
- Error handling
- Return codes
