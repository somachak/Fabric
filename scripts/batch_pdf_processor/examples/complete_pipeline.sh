#!/bin/bash
# Complete Pipeline: From PDFs to Teaching Materials
# This script demonstrates the full workflow from PDF extraction to final teaching materials

set -e  # Exit on error

# ============================================================================
# Configuration
# ============================================================================

INPUT_PDFS="${1:-$HOME/statistics_textbooks}"
OUTPUT_BASE="${2:-$HOME/stats_course}"
TOPICS=(
    "regression:linear regression,multiple regression,Python scikit-learn"
    "probability:distributions,bayes theorem,random variables"
    "hypothesis_testing:t-test,chi-square,ANOVA,p-values"
    "time_series:ARIMA,seasonal decomposition,forecasting"
    "bayesian:prior,posterior,conjugate priors,PyMC"
)

# ============================================================================
# Colors for output
# ============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================================
# Helper functions
# ============================================================================

log_step() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

# ============================================================================
# Main Pipeline
# ============================================================================

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Complete Teaching Material Generation Pipeline          ║"
echo "║  From PDFs → Vector DB → Teaching Materials              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo "Configuration:"
echo "  Input PDFs: $INPUT_PDFS"
echo "  Output Base: $OUTPUT_BASE"
echo "  Topics: ${#TOPICS[@]}"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# ============================================================================
# Step 1: Extract Teaching Patterns from PDFs
# ============================================================================

log_step "Step 1: Extracting Teaching Patterns from PDFs"

EXTRACTED_DIR="$OUTPUT_BASE/extracted"
mkdir -p "$EXTRACTED_DIR"

if [ ! -d "$INPUT_PDFS" ]; then
    log_error "Input directory not found: $INPUT_PDFS"
    exit 1
fi

# Count PDFs
PDF_COUNT=$(find "$INPUT_PDFS" -name "*.pdf" -type f | wc -l)
log_warning "Found $PDF_COUNT PDF files"

if [ $PDF_COUNT -eq 0 ]; then
    log_error "No PDF files found in $INPUT_PDFS"
    exit 1
fi

# Run batch processor
cd "$(dirname "$0")/.."  # Go to batch_pdf_processor directory

python batch_processor.py \
    "$INPUT_PDFS" \
    -o "$EXTRACTED_DIR" \
    --pattern extract_teaching_content

log_success "Extracted teaching patterns from $PDF_COUNT PDFs"

# ============================================================================
# Step 2: Build Vector Database
# ============================================================================

log_step "Step 2: Building Vector Database"

VECTORDB_PATH="$OUTPUT_BASE/vectordb"

python examples/build_vector_db.py \
    "$EXTRACTED_DIR" \
    --db-path "$VECTORDB_PATH" \
    --collection teaching_knowledge \
    --no-test

log_success "Vector database created at $VECTORDB_PATH"

# ============================================================================
# Step 3: Generate Teaching Materials for Each Topic
# ============================================================================

log_step "Step 3: Generating Teaching Materials"

MATERIALS_DIR="$OUTPUT_BASE/teaching_materials"
mkdir -p "$MATERIALS_DIR"

topic_count=0

for topic_spec in "${TOPICS[@]}"; do
    # Parse topic:subtopics
    IFS=':' read -r topic subtopics <<< "$topic_spec"
    topic_count=$((topic_count + 1))

    echo ""
    echo "[$topic_count/${#TOPICS[@]}] Processing: $topic"

    # Generate teaching materials
    python examples/query_and_generate.py \
        "$topic" \
        --subtopics ${subtopics//,/ } \
        --db-path "$VECTORDB_PATH" \
        --pattern create_teaching_pattern \
        --output "$MATERIALS_DIR/${topic}.md" \
        > /dev/null

    log_success "Generated: ${topic}.md"

    # Also generate quiz
    python examples/query_and_generate.py \
        "$topic" \
        --subtopics ${subtopics//,/ } \
        --db-path "$VECTORDB_PATH" \
        --pattern create_quiz \
        --output "$MATERIALS_DIR/${topic}_quiz.md" \
        > /dev/null

    log_success "Generated: ${topic}_quiz.md"

    # Also generate flashcards
    python examples/query_and_generate.py \
        "$topic" \
        --subtopics ${subtopics//,/ } \
        --db-path "$VECTORDB_PATH" \
        --pattern create_flash_cards \
        --output "$MATERIALS_DIR/${topic}_flashcards.md" \
        > /dev/null

    log_success "Generated: ${topic}_flashcards.md"
done

# ============================================================================
# Step 4: Create Index/Summary
# ============================================================================

log_step "Step 4: Creating Course Index"

INDEX_FILE="$MATERIALS_DIR/INDEX.md"

cat > "$INDEX_FILE" <<EOF
# Statistics Course Materials

Generated from $PDF_COUNT PDF textbooks on $(date)

## Course Modules

EOF

for topic_spec in "${TOPICS[@]}"; do
    IFS=':' read -r topic subtopics <<< "$topic_spec"
    topic_title=$(echo "$topic" | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($i,1,1)),$i)}1')

    cat >> "$INDEX_FILE" <<EOF
### $topic_title

- [Teaching Materials](./${topic}.md)
- [Quiz](./${topic}_quiz.md)
- [Flashcards](./${topic}_flashcards.md)

EOF
done

cat >> "$INDEX_FILE" <<EOF

## Source Materials

- Total PDFs Processed: $PDF_COUNT
- Extraction Location: \`$EXTRACTED_DIR\`
- Vector Database: \`$VECTORDB_PATH\`

## How to Use

1. Review teaching materials for each module
2. Use quizzes for assessment
3. Use flashcards for memorization and review
4. Query the vector database for additional topics:
   \`\`\`bash
   python examples/query_and_generate.py "your topic" --output custom_topic.md
   \`\`\`

EOF

log_success "Created course index"

# ============================================================================
# Final Summary
# ============================================================================

echo ""
log_step "Pipeline Complete! ✨"

echo ""
echo "📊 Summary:"
echo "  ✓ Processed: $PDF_COUNT PDFs"
echo "  ✓ Generated: ${#TOPICS[@]} teaching modules"
echo "  ✓ Generated: ${#TOPICS[@]} quizzes"
echo "  ✓ Generated: ${#TOPICS[@]} flashcard sets"
echo ""
echo "📁 Output Structure:"
echo "  $OUTPUT_BASE/"
echo "  ├── extracted/           # Raw extracted content"
echo "  ├── vectordb/           # Vector database"
echo "  └── teaching_materials/ # Final course materials"
echo ""
echo "📚 Course Materials:"
echo "  Open: $INDEX_FILE"
echo ""
echo "💡 Next Steps:"
echo "  1. Review generated materials in: $MATERIALS_DIR"
echo "  2. Query vector DB for additional topics"
echo "  3. Customize and refine as needed"
echo ""

# Open index in default viewer (optional)
if command -v xdg-open &> /dev/null; then
    read -p "Open course index? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "$INDEX_FILE" 2>/dev/null || true
    fi
elif command -v open &> /dev/null; then
    read -p "Open course index? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$INDEX_FILE" 2>/dev/null || true
    fi
fi

log_success "Pipeline complete! 🎉"
