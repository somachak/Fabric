#!/bin/bash

# HR Compensation Visual Explainer Demo Script
# This script demonstrates the HR compensation visualization capabilities

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  💰 HR Compensation Visual Explainer - Demo Script       ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if fabric is installed
if ! command -v fabric &> /dev/null; then
    echo -e "${YELLOW}Error: fabric command not found${NC}"
    echo "Please install fabric first: https://github.com/danielmiessler/fabric"
    exit 1
fi

# Check if the pattern exists
if [ ! -d "$HOME/.config/fabric/patterns/create_hr_compensation_visual" ]; then
    echo -e "${YELLOW}Warning: Pattern not found. Running update...${NC}"
    fabric --updatepatterns
fi

echo -e "${GREEN}✓ Fabric is installed${NC}"
echo ""

# Demo scenarios
echo -e "${BLUE}Choose a demo scenario:${NC}"
echo "1. Explain RSUs (Restricted Stock Units)"
echo "2. 4-Year Vesting with 1-Year Cliff"
echo "3. Compare Two Job Offers"
echo "4. Stock Options (ISO vs NSO)"
echo "5. Total Compensation Breakdown"
echo "6. Custom Question"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}Running Demo 1: RSUs Explanation${NC}"
        echo ""
        echo "Explain RSUs (Restricted Stock Units) with a visual analogy" | \
            fabric --pattern create_hr_compensation_visual
        ;;
    2)
        echo -e "${GREEN}Running Demo 2: Vesting Timeline${NC}"
        echo ""
        echo "Explain 4-year vesting with 1-year cliff using a visual timeline" | \
            fabric --pattern create_hr_compensation_visual
        ;;
    3)
        echo -e "${GREEN}Running Demo 3: Offer Comparison${NC}"
        echo ""
        cat << 'EOF' | fabric --pattern create_hr_compensation_visual
Compare these two job offers and show me which is better:

Offer A (Startup):
- $150,000 base salary
- 10,000 stock options at $1 strike price
- Current company valuation: $10/share
- 4-year vesting, 1-year cliff

Offer B (Big Tech):
- $200,000 base salary
- $50,000/year RSUs (4-year vesting)
- No cliff
- Public company stock

Show me total compensation over 4 years with scenarios.
EOF
        ;;
    4)
        echo -e "${GREEN}Running Demo 4: ISO vs NSO${NC}"
        echo ""
        echo "Explain the difference between ISO and NSO stock options. Include tax implications and when to use each." | \
            fabric --pattern create_hr_compensation_visual
        ;;
    5)
        echo -e "${GREEN}Running Demo 5: Total Compensation${NC}"
        echo ""
        cat << 'EOF' | fabric --pattern create_hr_compensation_visual
Break down total compensation for a Senior Software Engineer:

- Base Salary: $180,000
- Annual Bonus Target: 15% ($27,000)
- RSU Grant: $100,000/year over 4 years
- 401k Match: 6% of salary
- Health Benefits: $15,000/year value
- Other perks: $10,000/year

Show me the full breakdown visually.
EOF
        ;;
    6)
        echo -e "${GREEN}Enter your custom question:${NC}"
        read -p "> " custom_question
        echo ""
        echo "$custom_question" | fabric --pattern create_hr_compensation_visual
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Demo completed!${NC}"
echo ""
echo "💡 Tips:"
echo "  - Save output to file: add '-o output.md' to the command"
echo "  - Try different models: add '--model gpt-4-turbo'"
echo "  - Use the Streamlit UI for interactive experience:"
echo "    cd scripts/python_ui && streamlit run streamlit.py"
echo ""
