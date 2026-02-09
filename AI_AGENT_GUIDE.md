# AI Agent Integration Guide

This tool is designed to be easily used by AI agents and automation systems.

## Quick Reference for AI Agents

### Basic Command Structure
```bash
./md2mp3-openai.py <input.md> [output] [voice] [model] [format]
```

### Common Use Cases

**Convert markdown to audio (defaults):**
```bash
./md2mp3-openai.py document.md
# Output: document.mp3 (shimmer voice, HD quality)
```

**Preview voices:**
```bash
./md2mp3-openai.py --preview
# Generates: voice-sample-{shimmer,alloy,echo,fable,onyx,nova}.mp3
```

**Specify output format:**
```bash
./md2mp3-openai.py input.md output.mp3 shimmer tts-1-hd mp3
```

### Voice Selection Guide

| Voice | Gender | Tone | Best For |
|-------|--------|------|----------|
| shimmer | Female | Soft, warm | Calming content, meditation |
| alloy | Neutral | Balanced | Professional, technical docs |
| echo | Male | Clear, expressive | Narration, storytelling |
| fable | Male | British, warm | Engaging content |
| onyx | Male | Deep, authoritative | News, formal content |
| nova | Female | Energetic | Dynamic, upbeat content |

### Format Selection Guide

| Format | Size | Quality | Use Case |
|--------|------|---------|----------|
| mp3 | Medium | Good | General purpose (default) |
| opus | Small | Good | Web streaming, bandwidth-limited |
| aac | Small | Good | Mobile, YouTube |
| flac | Large | Lossless | Archival, audiophile |
| wav | Largest | Lossless | Professional editing |
| pcm | Largest | Raw | Audio processing |

### Cost Estimation

- **tts-1**: $0.015 per 1K characters
- **tts-1-hd**: $0.030 per 1K characters (recommended)

Example: 5000 character document = ~$0.15 (HD) or ~$0.075 (standard)

### Error Handling

The script will exit with error messages for:
- Missing OPENAI_API_KEY environment variable
- File not found
- Invalid voice name
- Invalid format
- Missing openai package

### Environment Setup

```bash
export OPENAI_API_KEY='sk-...'
pip install openai
```

### Return Codes

- `0`: Success
- `1`: Error (check stderr for details)

### Output Behavior

- Progress messages go to stdout
- Errors go to stderr
- Audio file written to specified path
- Temporary files automatically cleaned up

### Automation Example

```bash
#!/bin/bash
# Batch convert all markdown files

for file in *.md; do
    echo "Converting $file..."
    ./md2mp3-openai.py "$file" "${file%.md}.mp3" alloy tts-1-hd mp3
done
```

### Python API Usage

```python
import subprocess
import os

os.environ['OPENAI_API_KEY'] = 'sk-...'

result = subprocess.run([
    './md2mp3-openai.py',
    'input.md',
    'output.mp3',
    'shimmer',
    'tts-1-hd',
    'mp3'
], capture_output=True, text=True)

if result.returncode == 0:
    print("Success:", result.stdout)
else:
    print("Error:", result.stderr)
```

### Dependencies Check

```bash
# Check if dependencies are available
command -v ffmpeg >/dev/null 2>&1 || echo "ffmpeg not installed"
command -v pandoc >/dev/null 2>&1 || echo "pandoc not installed (optional)"
python3 -c "import openai" 2>/dev/null || echo "openai package not installed"
```

### File Size Expectations

- Short document (1K chars): ~50-100 KB (mp3)
- Medium document (10K chars): ~500 KB - 1 MB (mp3)
- Long document (50K chars): ~2-5 MB (mp3)

### Processing Time

- ~2-5 seconds per 1000 characters
- Longer documents split into chunks (processed sequentially)
- Network speed affects generation time

### Limitations

- Max 4000 characters per API call (automatically chunked)
- Requires internet connection
- API rate limits apply (check OpenAI docs)
- ffmpeg required for multi-chunk concatenation
