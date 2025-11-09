#!/bin/bash
# Launcher script for PDF Batch Processor
# Detects environment and launches appropriate interface

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║   Fabric PDF Teaching Pattern Extractor          ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check dependencies
if ! python3 -c "import google.generativeai" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Dependencies not installed.${NC}"
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Check Fabric
if ! command -v fabric &> /dev/null; then
    echo -e "${YELLOW}❌ Fabric CLI not found. Please install Fabric first.${NC}"
    exit 1
fi

# Check for Gemini API key
if [ -z "$GEMINI_API_KEY" ]; then
    CONFIG_FILE="$HOME/.config/fabric/batch_processor_config.json"
    if [ -f "$CONFIG_FILE" ]; then
        HAS_KEY=$(python3 -c "import json; print('gemini_api_key' in json.load(open('$CONFIG_FILE')))" 2>/dev/null || echo "False")
        if [ "$HAS_KEY" = "False" ]; then
            echo -e "${YELLOW}⚠️  No Gemini API key found.${NC}"
            echo "You can:"
            echo "  1. Set GEMINI_API_KEY environment variable"
            echo "  2. Enter it in the GUI"
            echo "  3. Use --no-vision flag for text-only processing"
            echo ""
        fi
    else
        echo -e "${YELLOW}ℹ️  No API key configured yet. You can add it in the GUI.${NC}"
        echo ""
    fi
fi

# Menu
echo "Select interface:"
echo "  1) GUI (Graphical Interface) - Recommended"
echo "  2) CLI (Command Line)"
echo "  3) Help & Examples"
echo ""
read -p "Choice [1-3]: " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 Launching GUI...${NC}"
        python3 gui.py
        ;;
    2)
        echo -e "${GREEN}📋 CLI Mode${NC}"
        echo ""
        echo "Usage: python3 batch_processor.py <input> -o <output> [options]"
        echo ""
        echo "Examples:"
        echo "  # Process a folder"
        echo "  python3 batch_processor.py ~/pdfs/ -o ~/output/"
        echo ""
        echo "  # Process specific files"
        echo "  python3 batch_processor.py file1.pdf -o ~/output/"
        echo ""
        echo "  # Disable vision (text-only)"
        echo "  python3 batch_processor.py ~/pdfs/ -o ~/output/ --no-vision"
        echo ""
        echo "For full help:"
        python3 batch_processor.py --help
        ;;
    3)
        echo -e "${GREEN}📖 Opening README...${NC}"
        if command -v less &> /dev/null; then
            less README.md
        elif command -v more &> /dev/null; then
            more README.md
        else
            cat README.md
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
