# Cloud Deployment Guide

Run markdown-to-audio on various cloud platforms.

## GitHub Actions

### Setup

1. Add your OpenAI API key to repository secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add secret: `OPENAI_API_KEY`

2. Use the included workflows:
   - `.github/workflows/convert.yml` - Manual conversion
   - `.github/workflows/batch-convert.yml` - Auto-convert on push

### Manual Conversion

1. Go to Actions tab
2. Select "Convert Markdown to Audio"
3. Click "Run workflow"
4. Choose file, voice, model, format
5. Download artifact when complete

### Automatic Batch Conversion

1. Create `content/` directory in your repo
2. Add markdown files to `content/`
3. Push to GitHub
4. Workflow automatically converts all files
5. Download artifacts from Actions tab

## AWS Lambda

```python
import json
import subprocess
import boto3

def lambda_handler(event, context):
    # Download markdown from S3
    s3 = boto3.client('s3')
    s3.download_file(
        event['bucket'],
        event['markdown_key'],
        '/tmp/input.md'
    )
    
    # Convert
    subprocess.run([
        'python3', 'md2mp3-openai.py',
        '/tmp/input.md',
        '/tmp/output.mp3',
        event.get('voice', 'shimmer'),
        event.get('model', 'tts-1-hd'),
        'mp3'
    ], env={'OPENAI_API_KEY': os.environ['OPENAI_API_KEY']})
    
    # Upload to S3
    s3.upload_file(
        '/tmp/output.mp3',
        event['bucket'],
        event['output_key']
    )
    
    return {'statusCode': 200}
```

**Requirements:**
- Lambda layer with Python dependencies
- ffmpeg layer
- Increase timeout (5+ minutes)
- Increase memory (512MB+)

## Google Cloud Run

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY md2mp3-openai.py .

CMD ["python3", "md2mp3-openai.py"]
```

**Deploy:**
```bash
gcloud run deploy markdown-to-audio \
  --source . \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY \
  --memory 1Gi \
  --timeout 600
```

## Azure Functions

**function.json:**
```json
{
  "bindings": [
    {
      "type": "httpTrigger",
      "direction": "in",
      "name": "req"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

**__init__.py:**
```python
import azure.functions as func
import subprocess
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    markdown_content = req.get_body().decode('utf-8')
    
    with open('/tmp/input.md', 'w') as f:
        f.write(markdown_content)
    
    subprocess.run([
        'python3', 'md2mp3-openai.py',
        '/tmp/input.md',
        '/tmp/output.mp3'
    ], env={'OPENAI_API_KEY': os.environ['OPENAI_API_KEY']})
    
    with open('/tmp/output.mp3', 'rb') as f:
        audio_data = f.read()
    
    return func.HttpResponse(
        audio_data,
        mimetype='audio/mpeg'
    )
```

## Replit

1. Import repository to Replit
2. Add secret: `OPENAI_API_KEY`
3. Run: `pip install -r requirements.txt`
4. Execute: `./md2mp3-openai.py document.md`

## Railway

1. Connect GitHub repo
2. Add environment variable: `OPENAI_API_KEY`
3. Railway auto-detects Python
4. Use as CLI or build API wrapper

## Render

**render.yaml:**
```yaml
services:
  - type: web
    name: markdown-to-audio
    env: python
    buildCommand: pip install -r requirements.txt && apt-get install -y ffmpeg
    startCommand: python3 api_server.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

## Cost Considerations

- **GitHub Actions**: 2000 free minutes/month
- **AWS Lambda**: 1M free requests/month
- **Google Cloud Run**: 2M free requests/month
- **Azure Functions**: 1M free executions/month

**OpenAI API costs remain the same:**
- tts-1: $0.015/1K chars
- tts-1-hd: $0.030/1K chars

## Tips

1. **Timeout**: Set 5-10 minutes for long documents
2. **Memory**: 512MB minimum, 1GB recommended
3. **Storage**: Use temp storage, clean up after
4. **Secrets**: Always use environment variables for API keys
5. **Artifacts**: Store output in S3/GCS/Azure Blob for persistence
