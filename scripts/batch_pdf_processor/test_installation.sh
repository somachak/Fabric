#!/bin/bash
# Installation Test Script
# Verifies all components are working

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Batch PDF Processor - Installation Test              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() {
    echo -e "${GREEN}✓${NC} $1"
}

fail() {
    echo -e "${RED}✗${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Python version
echo "Testing Python installation..."
if python3 --version &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    pass "Python installed: $PYTHON_VERSION"
else
    fail "Python 3 not found"
    exit 1
fi

echo ""

# Test 2: Python dependencies
echo "Testing Python dependencies..."
python3 -c "
import sys
try:
    import google.generativeai
    print('✓ google.generativeai installed')
except ImportError:
    print('✗ google.generativeai not installed')
    sys.exit(1)

try:
    from batch_processor import FabricBatchProcessor
    print('✓ batch_processor module working')
except ImportError as e:
    print(f'✗ batch_processor import failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    pass "All Python dependencies OK"
else
    fail "Python dependencies missing"
    echo ""
    echo "Run: pip install -r requirements.txt"
    exit 1
fi

echo ""

# Test 3: Fabric CLI
echo "Testing Fabric CLI..."
if command -v fabric &> /dev/null; then
    FABRIC_VERSION=$(fabric --version 2>&1 || echo "unknown")
    pass "Fabric CLI found"
else
    fail "Fabric CLI not found in PATH"
    echo ""
    echo "To build Fabric:"
    echo "  cd /home/user/Fabric"
    echo "  go build ./cmd/fabric"
    echo "  export PATH=\$PATH:/home/user/Fabric"
    echo ""
    warn "Batch processor will work but cannot call fabric commands"
fi

echo ""

# Test 4: Pattern exists
echo "Testing Fabric patterns..."
PATTERN_FILE="$HOME/.config/fabric/patterns/extract_teaching_content/system.md"
if [ -f "$PATTERN_FILE" ]; then
    pass "extract_teaching_content pattern found"
elif [ -f "/home/user/Fabric/data/patterns/extract_teaching_content/system.md" ]; then
    pass "extract_teaching_content pattern exists in repo"
    warn "Run 'fabric --setup' to install patterns"
else
    fail "extract_teaching_content pattern not found"
fi

echo ""

# Test 5: Optional components
echo "Testing optional components..."

# tkinter
if python3 -c "import tkinter" 2>/dev/null; then
    pass "tkinter available (GUI will work)"
else
    warn "tkinter not available (GUI won't work)"
    echo "  Install with: sudo apt-get install python3-tk"
fi

# ChromaDB
if python3 -c "import chromadb" 2>/dev/null; then
    pass "ChromaDB installed (vector DB examples will work)"
else
    warn "ChromaDB not installed (optional)"
    echo "  Install when needed: pip install chromadb"
fi

echo ""

# Test 6: Configuration
echo "Testing configuration..."
CONFIG_DIR="$HOME/.config/fabric"
if [ -d "$CONFIG_DIR" ]; then
    pass "Config directory exists: $CONFIG_DIR"
else
    warn "Config directory doesn't exist (will be created on first use)"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    pass "GEMINI_API_KEY environment variable set"
else
    warn "GEMINI_API_KEY not set (needed for vision intelligence)"
    echo "  Set with: export GEMINI_API_KEY='your-key'"
fi

echo ""

# Summary
echo "╔════════════════════════════════════════════════════════╗"
echo "║  Test Summary                                          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

echo "Core Components:"
pass "Python 3 installed"
pass "Python dependencies installed"

if command -v fabric &> /dev/null; then
    pass "Fabric CLI available"
    echo ""
    echo -e "${GREEN}✅ Ready to process PDFs!${NC}"
    echo ""
    echo "Quick start:"
    echo "  python batch_processor.py input.pdf -o output/"
else
    warn "Fabric CLI not built yet"
    echo ""
    echo -e "${YELLOW}⚠️  Almost ready!${NC}"
    echo ""
    echo "Next step: Build Fabric CLI"
    echo "  cd /home/user/Fabric"
    echo "  go build ./cmd/fabric"
    echo "  export PATH=\$PATH:/home/user/Fabric"
fi

echo ""
echo "Optional Features:"
if python3 -c "import tkinter" 2>/dev/null; then
    pass "GUI available"
else
    echo "  - GUI: Install tkinter"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    pass "Vision intelligence configured"
else
    echo "  - Vision: Set GEMINI_API_KEY"
fi

if python3 -c "import chromadb" 2>/dev/null; then
    pass "Vector DB support available"
else
    echo "  - Vector DB: pip install chromadb"
fi

echo ""
echo "For full test report, see: INSTALLATION_TEST_REPORT.md"
