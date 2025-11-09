# 🚀 Quick Start Guide - PDF Teaching Pattern Extractor

## Your Complete Solution is Ready!

You now have a **production-ready system** for processing PDF collections to extract teaching patterns with both vision and text intelligence. Here's everything you need to get started.

---

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies

```bash
cd /home/user/Fabric/scripts/batch_pdf_processor
pip install -r requirements.txt
```

This installs: `google-generativeai` (for Gemini AI vision/text intelligence)

### Step 2: Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 3: Configure the Key

**Choose ONE method:**

**Option A - Environment Variable (Quick)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B - Config File (Persistent)**
```bash
mkdir -p ~/.config/fabric
cat > ~/.config/fabric/batch_processor_config.json <<EOF
{
  "gemini_api_key": "YOUR-API-KEY-HERE",
  "use_vision": true,
  "pattern": "extract_teaching_content"
}
EOF
```

**Option C - Enter in GUI**
Just launch the GUI and enter it there - it will be saved automatically.

### Step 4: Launch!

```bash
# Interactive launcher
./launch.sh

# Or launch GUI directly
python gui.py

# Or use CLI directly
python batch_processor.py --help
```

---

## 🎯 Your Statistics Use Case - Complete Workflow

Here's the **exact workflow** you described for building a statistics knowledge base:

### Phase 1: Extract Teaching Patterns from PDFs

```bash
# Process your entire statistics textbook collection
python batch_processor.py ~/statistics_textbooks/ \
  -o ~/stats_knowledge_base/extracted/ \
  --pattern extract_teaching_content

# This gives you:
# ✅ Text content from all PDFs
# ✅ Diagram/chart/equation descriptions (via Gemini vision)
# ✅ Teaching patterns identified
# ✅ Concept hierarchies
# ✅ Vector-ready knowledge chunks
```

**Output structure:**
```
stats_knowledge_base/extracted/
├── processing_summary.json
├── textbook1_extracted.txt      # Raw text
├── textbook1_teaching.md        # Structured teaching content
├── textbook1_metadata.json      # Metadata for filtering
├── textbook2_extracted.txt
├── textbook2_teaching.md
└── ...
```

### Phase 2: Build Vector Database

Now you're ready for the vector database step. Here's a **complete working script**:

```python
# scripts/build_vector_db.py
import chromadb
from chromadb.config import Settings
from pathlib import Path
import json

def build_stats_knowledge_base():
    """Build vector database from extracted teaching content"""

    # Initialize ChromaDB
    client = chromadb.PersistentClient(
        path="./stats_vectordb"
    )

    # Create collection
    collection = client.create_collection(
        name="statistics_knowledge",
        metadata={"description": "Statistics textbook knowledge base"}
    )

    # Load extracted teaching content
    extracted_dir = Path("~/stats_knowledge_base/extracted/").expanduser()

    documents = []
    metadatas = []
    ids = []

    for teaching_file in extracted_dir.glob("*_teaching.md"):
        # Read teaching content
        with open(teaching_file) as f:
            content = f.read()

        # Read metadata
        metadata_file = teaching_file.parent / teaching_file.name.replace('_teaching.md', '_metadata.json')
        with open(metadata_file) as f:
            metadata = json.load(f)

        # Add to lists
        documents.append(content)
        metadatas.append(metadata)
        ids.append(teaching_file.stem)

    # Add to vector database
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Added {len(documents)} documents to vector database")
    return collection

if __name__ == "__main__":
    collection = build_stats_knowledge_base()

    # Test query
    results = collection.query(
        query_texts=["regression analysis with Python"],
        n_results=5
    )

    print("\nTest Query Results:")
    for doc in results['documents'][0]:
        print(f"\n{doc[:200]}...")
```

### Phase 3: Query and Generate Teaching Materials

```python
# scripts/generate_teaching_materials.py
import chromadb
import subprocess

def generate_topic_materials(topic, subtopics=None):
    """Generate comprehensive teaching materials for a topic"""

    # Connect to vector database
    client = chromadb.PersistentClient(path="./stats_vectordb")
    collection = client.get_collection("statistics_knowledge")

    # Build query
    if subtopics:
        query = f"{topic}: {', '.join(subtopics)}"
    else:
        query = topic

    # Retrieve relevant content
    results = collection.query(
        query_texts=[query],
        n_results=10
    )

    # Combine context
    context = "\n\n--- SECTION ---\n\n".join(results['documents'][0])

    # Generate teaching pattern using Fabric
    result = subprocess.run(
        ['fabric', '--pattern', 'create_teaching_pattern'],
        input=context,
        capture_output=True,
        text=True
    )

    return result.stdout

# Example: Generate regression teaching materials
regression_materials = generate_topic_materials(
    topic="Regression Analysis",
    subtopics=[
        "linear regression",
        "multiple regression",
        "logistic regression",
        "Python implementation",
        "scikit-learn",
        "statsmodels"
    ]
)

# Save to file
with open("regression_teaching_materials.md", "w") as f:
    f.write(regression_materials)

print("✅ Generated regression teaching materials")
```

### Phase 4: Complete Automation

```bash
#!/bin/bash
# automated_stats_knowledge_pipeline.sh

echo "📚 Statistics Knowledge Base Pipeline"
echo "======================================"

# Step 1: Extract from PDFs
echo "Step 1: Extracting teaching patterns from PDFs..."
python batch_processor.py ~/statistics_textbooks/ \
  -o ~/stats_knowledge_base/extracted/

# Step 2: Build vector database
echo "Step 2: Building vector database..."
python build_vector_db.py

# Step 3: Generate teaching materials for key topics
echo "Step 3: Generating teaching materials..."

TOPICS=(
  "regression:linear regression,multiple regression,Python scikit-learn"
  "time_series:ARIMA,seasonal decomposition,forecasting,statsmodels"
  "hypothesis_testing:t-test,chi-square,ANOVA,p-values"
  "bayesian:prior,posterior,Bayes theorem,PyMC"
  "machine_learning:supervised,unsupervised,classification,regression"
)

for topic_spec in "${TOPICS[@]}"; do
  IFS=':' read -r topic subtopics <<< "$topic_spec"
  echo "  Generating: $topic"

  python -c "
from generate_teaching_materials import generate_topic_materials
materials = generate_topic_materials('$topic', '$subtopics'.split(','))
with open('teaching_${topic}.md', 'w') as f:
    f.write(materials)
"
done

echo "✅ Pipeline complete!"
echo "📊 Generated teaching materials for ${#TOPICS[@]} topics"
echo "📁 Output: ~/stats_knowledge_base/"
```

---

## 🎨 Interface Options

### Option 1: GUI (Easiest)

```bash
python gui.py
```

**Perfect for:**
- Interactive use
- Selecting specific files
- Visual progress tracking
- One-time processing jobs

**Features:**
- 📁 Folder browser
- 📄 Multi-file selector
- 🔑 API key management
- 📊 Real-time progress
- 🎯 Pattern selection
- 👁️ Vision toggle

### Option 2: CLI (Most Powerful)

```bash
# Basic usage
python batch_processor.py input.pdf -o output/

# Batch folder
python batch_processor.py ~/pdfs/ -o ~/output/

# Advanced options
python batch_processor.py ~/pdfs/ \
  -o ~/output/ \
  --pattern extract_teaching_content \
  --workers 5 \
  --gemini-key "YOUR-KEY"
```

**Perfect for:**
- Automation
- Scripting
- Large batches
- Scheduled jobs

**All Options:**
```
-o, --output DIR           Output directory (required)
-p, --pattern NAME         Pattern to use (default: extract_teaching_content)
--no-vision               Disable vision intelligence (faster, text-only)
--sequential              Process one at a time (less RAM)
-w, --workers N           Number of parallel workers (default: 3)
--gemini-key KEY          Gemini API key
```

### Option 3: Direct Fabric Integration

```bash
# Single PDF with teaching pattern
fabric --pattern extract_teaching_content -a textbook.pdf

# Multiple PDFs combined
fabric --pattern create_teaching_pattern \
  -a chapter1.pdf \
  -a chapter2.pdf \
  -a chapter3.pdf \
  -o complete_course.md
```

---

## 📊 What You Get

### For Each PDF Processed:

1. **`{filename}_extracted.txt`**
   - Raw text content
   - Vision descriptions of diagrams/charts/equations
   - Complete content with structure preserved

2. **`{filename}_teaching.md`**
   - Subject domain identified
   - Pedagogical patterns found
   - Concept hierarchies
   - Learning objectives
   - Visual element analysis
   - Teaching strategies
   - Assessment opportunities
   - **Vector-ready knowledge chunks**

3. **`{filename}_metadata.json`**
   - File information
   - Processing settings
   - Vision usage flag
   - Pattern used

4. **`processing_summary.json`**
   - Total files processed
   - Success/failure counts
   - Complete results list

---

## 🔬 Vision Intelligence Examples

### What Gemini Vision Understands:

**Mathematical Equations:**
```
Vision Analysis:
"This diagram shows the linear regression equation: y = mx + b
where m represents the slope and b is the y-intercept.
The visual includes a scatter plot with a fitted line..."
```

**Statistical Diagrams:**
```
Vision Analysis:
"This box plot illustrates the distribution of test scores.
The median (50th percentile) is shown at 75, with the
interquartile range spanning from 65 to 85. Three outliers
are visible below 50..."
```

**Process Flowcharts:**
```
Vision Analysis:
"This flowchart depicts the hypothesis testing process:
1. State null and alternative hypotheses
2. Choose significance level (α)
3. Calculate test statistic
4. Determine p-value
5. Make decision..."
```

### When Vision is Most Valuable:

✅ **Use Vision For:**
- Mathematical textbooks with equations
- Statistical content with graphs/charts
- Diagrams and flowcharts
- Scanned documents
- Image-heavy PDFs

⚡ **Skip Vision For:**
- Text-only documents
- Fast processing needed
- API cost concerns
- Simple text extraction

---

## 💡 Pro Tips

### Tip 1: Optimize Batch Size
```bash
# For large collections, process in batches
find ~/huge_collection -name "*.pdf" | \
  xargs -n 50 python batch_processor.py -o ~/output/batch_{} -w 5
```

### Tip 2: Combine Patterns
```bash
# Extract first, then create teaching materials
python batch_processor.py pdfs/ -o extracted/ -p extract_teaching_content

# Then combine and synthesize
cat extracted/*_teaching.md | \
  fabric --pattern create_teaching_pattern > comprehensive_course.md
```

### Tip 3: Metadata Filtering
```python
# Query with metadata filters
results = collection.query(
    query_texts=["regression"],
    n_results=10,
    where={"source": "Introduction to Statistical Learning"}
)
```

### Tip 4: Scheduled Processing
```bash
# Add to crontab: process new PDFs daily at 2 AM
0 2 * * * cd ~/Fabric/scripts/batch_pdf_processor && \
  python batch_processor.py ~/Dropbox/Statistics_PDFs/ -o ~/knowledge_base/
```

---

## 🎓 Complete Statistics Course Example

Here's your **end-to-end workflow** for creating a comprehensive statistics course:

```bash
#!/bin/bash
# build_statistics_course.sh

TEXTBOOKS="$HOME/statistics_textbooks"
OUTPUT="$HOME/stats_course"

# 1. Extract from all textbooks
echo "📚 Extracting from textbooks..."
python batch_processor.py "$TEXTBOOKS" -o "$OUTPUT/extracted/"

# 2. Build vector database
echo "🗄️ Building knowledge base..."
python build_vector_db.py

# 3. Generate course modules
MODULES=(
  "regression"
  "probability"
  "hypothesis_testing"
  "time_series"
  "bayesian_statistics"
  "machine_learning"
)

for module in "${MODULES[@]}"; do
  echo "📖 Generating module: $module"

  # Query vector database
  python query_knowledge.py "$module" > "$OUTPUT/context_${module}.txt"

  # Generate teaching materials
  cat "$OUTPUT/context_${module}.txt" | \
    fabric --pattern create_teaching_pattern \
    > "$OUTPUT/module_${module}.md"

  # Generate quiz
  cat "$OUTPUT/context_${module}.txt" | \
    fabric --pattern create_quiz \
    > "$OUTPUT/quiz_${module}.md"

  # Generate flashcards
  cat "$OUTPUT/context_${module}.txt" | \
    fabric --pattern create_flash_cards \
    > "$OUTPUT/flashcards_${module}.md"
done

echo "✅ Complete statistics course generated!"
echo "📁 Location: $OUTPUT/"
```

**You get:**
- 6 comprehensive teaching modules
- 6 quiz sets
- 6 flashcard sets
- Searchable vector knowledge base
- All from your PDF collection!

---

## 🚨 Troubleshooting

### "No API key found"
```bash
# Check if set
echo $GEMINI_API_KEY

# Set it
export GEMINI_API_KEY="your-key"

# Or use --no-vision flag
python batch_processor.py input.pdf -o output/ --no-vision
```

### "Fabric not found"
```bash
# Check Fabric installation
which fabric

# If not found, ensure it's in PATH
export PATH="$PATH:$HOME/go/bin"
```

### "Python dependency missing"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### GUI won't start
```bash
# Install tkinter (Ubuntu/Debian)
sudo apt-get install python3-tk

# Then try again
python gui.py
```

---

## 📚 Next Steps

1. **Process your PDFs:**
   ```bash
   python batch_processor.py ~/statistics_textbooks/ -o ~/extracted/
   ```

2. **Build vector database:**
   ```bash
   python build_vector_db.py  # (create this script from example above)
   ```

3. **Query and generate:**
   ```bash
   python generate_teaching_materials.py
   ```

4. **Iterate and refine:**
   - Adjust patterns as needed
   - Experiment with different queries
   - Combine multiple sources

---

## 🎉 You're Ready!

Everything is set up and ready to go:

✅ PDF text extraction (Fabric built-in)
✅ Vision intelligence (Gemini AI)
✅ Teaching pattern extraction (universal pattern)
✅ Batch processing (Python script)
✅ GUI interface (Tkinter)
✅ CLI interface (full-featured)
✅ Vector DB ready output
✅ Comprehensive documentation

**Start processing your PDFs now:**

```bash
cd /home/user/Fabric/scripts/batch_pdf_processor
./launch.sh
```

---

**Questions? Check the full README.md or create an issue!**

Happy Learning! 📖✨
