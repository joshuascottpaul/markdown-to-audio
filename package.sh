#!/bin/bash
# Package markdown-to-audio for distribution

set -e

VERSION=${1:-"v0.1.0"}
PLATFORMS=("linux-amd64" "linux-arm64" "darwin-amd64" "darwin-arm64")

echo "Packaging markdown-to-audio $VERSION"

# Create dist directory
mkdir -p dist

for platform in "${PLATFORMS[@]}"; do
    echo "Building for $platform..."
    
    # Create platform directory
    platform_dir="dist/markdown-to-audio-$platform"
    mkdir -p "$platform_dir"
    
    # Copy files
    cp md2mp3-openai.py "$platform_dir/"
    cp README.md "$platform_dir/"
    cp LICENSE "$platform_dir/"
    cp requirements.txt "$platform_dir/"
    
    # Create install script
    cat > "$platform_dir/install.sh" << 'EOF'
#!/bin/bash
set -e

INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
mkdir -p "$INSTALL_DIR"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Install Python dependencies
pip3 install -r requirements.txt --user

# Install script
cp md2mp3-openai.py "$INSTALL_DIR/md2mp3"
chmod +x "$INSTALL_DIR/md2mp3"

echo "✓ Installed to $INSTALL_DIR/md2mp3"
echo ""
echo "Make sure $INSTALL_DIR is in your PATH:"
echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
echo ""
echo "Set your OpenAI API key:"
echo "  export OPENAI_API_KEY='your-key-here'"
EOF
    chmod +x "$platform_dir/install.sh"
    
    # Create tarball
    cd dist
    tar -czf "markdown-to-audio-$VERSION-$platform.tar.gz" "markdown-to-audio-$platform"
    rm -rf "markdown-to-audio-$platform"
    cd ..
    
    echo "✓ Created markdown-to-audio-$VERSION-$platform.tar.gz"
done

echo ""
echo "✓ All packages created in dist/"
echo ""
echo "To create a GitHub release:"
echo "  gh release create $VERSION dist/*.tar.gz --title \"$VERSION\" --notes \"Release $VERSION\""
