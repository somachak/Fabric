#!/bin/bash

# Launch script for Statistical HR Analytics Platform

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  📊 Statistical HR Compensation Analytics Platform         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if in correct directory
if [ ! -f "statistical_hr_app.py" ]; then
    echo -e "${YELLOW}Changing to statistical_hr_analytics directory...${NC}"
    cd "$(dirname "$0")"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check dependencies
echo ""
echo -e "${BLUE}Checking dependencies...${NC}"

if python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${GREEN}✓ Streamlit installed${NC}"
else
    echo -e "${YELLOW}⚠ Streamlit not found${NC}"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for fabric
if command -v fabric &> /dev/null; then
    echo -e "${GREEN}✓ Fabric installed${NC}"
else
    echo -e "${YELLOW}⚠ Fabric not found${NC}"
    echo "Please install Fabric: https://github.com/danielmiessler/fabric"
fi

# Check for pattern
PATTERN_PATH="$HOME/.config/fabric/patterns/apply_statistics_to_hr_compensation"
if [ -d "$PATTERN_PATH" ]; then
    echo -e "${GREEN}✓ Statistical pattern found${NC}"
else
    echo -e "${YELLOW}⚠ Pattern not found at: $PATTERN_PATH${NC}"
    echo "Copying pattern..."
    mkdir -p "$HOME/.config/fabric/patterns"
    cp -r ../../data/patterns/apply_statistics_to_hr_compensation "$HOME/.config/fabric/patterns/"
    echo -e "${GREEN}✓ Pattern installed${NC}"
fi

# Check for knowledge base
KB_PATH="$HOME/statistics_knowledge_base"
if [ -d "$KB_PATH" ]; then
    KB_COUNT=$(find "$KB_PATH" -name "*_teaching.md" 2>/dev/null | wc -l)
    if [ "$KB_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✓ Knowledge base found ($KB_COUNT files)${NC}"
    else
        echo -e "${YELLOW}⚠ Knowledge base empty${NC}"
        echo "  Process your PDFs first:"
        echo "  cd scripts/batch_pdf_processor"
        echo "  python3 batch_processor.py /path/to/pdfs -o ~/statistics_knowledge_base"
    fi
else
    echo -e "${YELLOW}⚠ Knowledge base not found${NC}"
    echo "  Expected location: $KB_PATH"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🚀 Launching Statistical HR Analytics Platform...${NC}"
echo ""
echo -e "${BLUE}Access the app at: http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Launch Streamlit
streamlit run statistical_hr_app.py
