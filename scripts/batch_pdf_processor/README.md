# 📚 Batch PDF Teaching Pattern Extractor

A comprehensive system for extracting teaching patterns, concepts, and knowledge from PDF documents using both vision and text intelligence.

## 🌟 Features

- **🎯 Multi-PDF Processing**: Process individual files, selected files, or entire folders
- **👁️ Vision Intelligence**: Analyze diagrams, charts, equations, and visual elements using Gemini AI
- **📝 Text Extraction**: Extract and analyze textual content with pedagogical structure
- **🖥️ Multiple Interfaces**:
  - Simple GUI for easy file selection
  - Powerful CLI for automation and scripting
  - Batch processing with parallel execution
- **📊 Comprehensive Analysis**: Extracts teaching patterns, concepts, learning objectives, and more
- **💾 Vector DB Ready**: Output formatted for vector database ingestion
- **🎓 Universal Subject Support**: Works with any educational content (not limited to statistics)

## 🚀 Quick Start

### Prerequisites

1. **Fabric CLI** - Already installed in your system
2. **Python 3.8+** - Check with `python3 --version`
3. **Gemini API Key** - Get from https://makersuite.google.com/app/apikey

### Installation

```bash
# Navigate to the batch processor directory
cd scripts/batch_pdf_processor

# Install Python dependencies
pip install -r requirements.txt
```

### Configure Gemini API Key

**Option 1: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option 2: Configuration File**
```bash
mkdir -p ~/.config/fabric
cat > ~/.config/fabric/batch_processor_config.json <<EOF
{
  "gemini_api_key": "your-api-key-here",
  "pattern": "extract_teaching_content",
  "use_vision": true,
  "last_output_dir": "$HOME/fabric_output"
}
EOF
```

**Option 3: Command Line Argument**
```bash
python batch_processor.py --gemini-key "your-api-key-here" input.pdf -o output/
```

## 📖 Usage

### GUI Mode (Easiest)

```bash
python gui.py
```

Then:
1. Enter your Gemini API key (saved securely for future use)
2. Click "Select Folder" or "Select Files" to choose PDFs
3. Choose output directory
4. Enable/disable vision intelligence
5. Click "Process PDFs"

![GUI Interface](docs/gui_screenshot.png)

### CLI Mode (For Automation)

#### Process a single PDF

```bash
python batch_processor.py textbook.pdf -o output/
```

#### Process entire folder

```bash
python batch_processor.py /path/to/pdfs/ -o results/
```

#### Process with specific pattern

```bash
python batch_processor.py pdfs/ -o output/ -p create_teaching_pattern
```

#### Disable vision intelligence (faster, text-only)

```bash
python batch_processor.py pdfs/ -o output/ --no-vision
```

#### Sequential processing (no parallelization)

```bash
python batch_processor.py pdfs/ -o output/ --sequential
```

#### Custom number of parallel workers

```bash
python batch_processor.py pdfs/ -o output/ -w 5
```

### Direct Fabric Integration

You can also use Fabric CLI directly with individual PDFs:

```bash
# Extract teaching content from a single PDF
fabric --pattern extract_teaching_content -a textbook.pdf -o analysis.md

# With streaming output
fabric --pattern extract_teaching_content -a textbook.pdf --stream

# Multiple PDFs combined
fabric --pattern extract_teaching_content \
  -a chapter1.pdf \
  -a chapter2.pdf \
  -a chapter3.pdf \
  -o complete_analysis.md
```

## 📊 Output Structure

After processing, you'll get:

```
output/
├── processing_summary.json        # Overall summary
├── textbook1_extracted.txt       # Raw extracted text
├── textbook1_teaching.md         # Teaching pattern analysis
├── textbook1_metadata.json       # File metadata
├── textbook2_extracted.txt
├── textbook2_teaching.md
└── textbook2_metadata.json
```

### Teaching Pattern Analysis Includes:

- **Subject Domain & Level**: Automatically identified
- **Pedagogical Patterns**: Teaching methods used
- **Core Concepts Map**: Main topics and relationships
- **Knowledge Structure**: Hierarchical organization
- **Visual Elements Analysis**: Diagrams, charts, equations described
- **Learning Objectives**: What students should learn
- **Teaching Sequence**: Recommended presentation order
- **Assessment Opportunities**: Quiz questions and exercises
- **Vector-Ready Chunks**: Pre-formatted for embedding

## 🎯 Real-World Examples

### Example 1: Statistics Textbook Collection

```bash
# Process entire statistics textbook collection
python batch_processor.py ~/statistics_books/ -o ~/stats_knowledge_base/

# Output ready for vector database ingestion
# Each PDF analyzed for:
# - Statistical concepts and formulas
# - Diagrams and visualizations
# - Example problems and solutions
# - Learning progression
```

### Example 2: Mixed Subject PDFs

```bash
# Process research papers, manuals, and textbooks together
python batch_processor.py ~/research_papers/ -o ~/knowledge_base/

# System automatically:
# - Identifies subject domains
# - Extracts relevant teaching patterns
# - Analyzes visual elements
# - Creates structured knowledge chunks
```

### Example 3: Automation Pipeline

```bash
#!/bin/bash
# automated_processing.sh

INPUT_DIR="$HOME/Documents/educational_pdfs"
OUTPUT_DIR="$HOME/fabric_knowledge_base"

# Process new PDFs daily
python batch_processor.py "$INPUT_DIR" -o "$OUTPUT_DIR" --sequential

# Generate summary report
cat "$OUTPUT_DIR/processing_summary.json" | jq '.successful'

# Notify when complete
echo "Processed $(jq '.total_files' "$OUTPUT_DIR/processing_summary.json") PDFs"
```

## 🔧 Advanced Configuration

### Pattern Selection

Two patterns available:

1. **extract_teaching_content** (Default)
   - Comprehensive analysis optimized for vector databases
   - Includes structured knowledge chunks
   - Better for building knowledge bases

2. **create_teaching_pattern**
   - Focused on creating teaching materials
   - More narrative structure
   - Better for direct educational use

### Vision Intelligence

**When to use:**
- PDFs with diagrams, charts, or figures
- Mathematical content with equations
- Visual learning materials
- Scanned documents or images

**When to skip:**
- Text-only documents
- Fast processing needed
- API costs are a concern

### Parallel Processing

```bash
# Process 10 PDFs simultaneously (uses more RAM)
python batch_processor.py pdfs/ -o output/ -w 10

# Sequential processing (uses less RAM)
python batch_processor.py pdfs/ -o output/ --sequential
```

## 🗄️ Vector Database Integration

### Prepare for ChromaDB

```python
import chromadb
from chromadb.utils import embedding_functions
import json
from pathlib import Path

# Load processed results
output_dir = Path("output")
client = chromadb.Client()

# Create collection
collection = client.create_collection(
    name="teaching_knowledge",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

# Add processed content
for metadata_file in output_dir.glob("*_metadata.json"):
    with open(metadata_file) as f:
        metadata = json.load(f)

    # Load teaching content
    teaching_file = metadata_file.parent / f"{metadata_file.stem.replace('_metadata', '')}_teaching.md"
    with open(teaching_file) as f:
        content = f.read()

    # Add to collection
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[metadata['filename']]
    )
```

### Query the Knowledge Base

```python
# Semantic search
results = collection.query(
    query_texts=["regression analysis with Python"],
    n_results=5
)

# Use with Fabric to generate teaching materials
import subprocess

context = "\n\n".join(results['documents'][0])
result = subprocess.run(
    ['fabric', '--pattern', 'create_teaching_pattern'],
    input=context,
    capture_output=True,
    text=True
)

print(result.stdout)
```

## 🐛 Troubleshooting

### Issue: "No Gemini API key provided"

**Solution:**
```bash
export GEMINI_API_KEY="your-key-here"
# Or use --gemini-key argument
# Or create config file as shown above
```

### Issue: "Fabric command not found"

**Solution:**
```bash
# Ensure Fabric is in your PATH
which fabric

# If not, add to PATH or use full path
export PATH="$PATH:$HOME/go/bin"
```

### Issue: "No PDF files found"

**Solution:**
- Check that directory contains .pdf files (case sensitive)
- Verify path is correct
- Check file permissions

### Issue: "Vision analysis failing"

**Solution:**
- Verify Gemini API key is valid
- Check API quota/limits
- Try with --no-vision flag for text-only
- Ensure PDF is not corrupted

### Issue: GUI not starting

**Solution:**
```bash
# Install tkinter (if not already installed)
# Ubuntu/Debian:
sudo apt-get install python3-tk

# macOS:
# tkinter comes with Python

# Windows:
# Reinstall Python with tcl/tk option
```

## 📝 Example Workflows

### Workflow 1: Building a Statistics Course

```bash
# Step 1: Extract teaching patterns from textbooks
python batch_processor.py statistics_textbooks/ -o stats_base/

# Step 2: Generate specific topic materials
cat stats_base/*regression*_teaching.md | \
  fabric --pattern create_teaching_pattern > regression_course.md

# Step 3: Create assessments
cat stats_base/*regression*_teaching.md | \
  fabric --pattern create_quiz > regression_quiz.md
```

### Workflow 2: Research Paper Analysis

```bash
# Extract teaching content from research papers
python batch_processor.py research_papers/ -o paper_analysis/ -p extract_teaching_content

# Generate summary
python <<EOF
import json
from pathlib import Path

with open('paper_analysis/processing_summary.json') as f:
    summary = json.load(f)

print(f"Analyzed {summary['successful']} papers")
print(f"Extracted {len(summary['results'])} knowledge chunks")
EOF
```

### Workflow 3: Continuous Learning System

```bash
# Watch directory and auto-process new PDFs
#!/bin/bash

WATCH_DIR="$HOME/Dropbox/Educational_PDFs"
PROCESS_DIR="$HOME/knowledge_base"

while true; do
  # Process any new PDFs
  python batch_processor.py "$WATCH_DIR" -o "$PROCESS_DIR" --sequential

  # Wait 1 hour
  sleep 3600
done
```

## 🤝 Integration with Other Tools

### With LangChain

```python
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load processed teaching content
loader = DirectoryLoader('output/', glob="*_teaching.md", loader_cls=TextLoader)
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# Use with your vector store
```

### With llamaindex

```python
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex

# Load processed documents
documents = SimpleDirectoryReader('output/', file_extractor={".md": lambda x: x}).load_data()

# Create index
index = GPTVectorStoreIndex.from_documents(documents)

# Query
response = index.query("Explain regression analysis with Python examples")
```

## 📈 Performance Tips

1. **Parallel Processing**: Use `-w` flag to control workers
   - More workers = faster but uses more RAM
   - Recommended: 3-5 workers

2. **Vision Intelligence**: Enable only when needed
   - Adds processing time
   - Significantly better for visual content
   - Can be expensive with large batches

3. **Pattern Selection**: Choose the right pattern
   - `extract_teaching_content`: Better for knowledge extraction
   - `create_teaching_pattern`: Better for direct teaching materials

4. **Batch Size**: Process in manageable batches
   - 50-100 PDFs per batch recommended
   - Monitor memory usage

## 🔒 Security & Privacy

- API keys stored locally in `~/.config/fabric/`
- File permissions: 600 (user read/write only)
- No data sent to servers except Google Gemini API
- Processed content stays on your machine

## 📚 Additional Resources

- [Fabric Documentation](https://github.com/danielmiessler/fabric)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Pattern Writing Guide](../../data/patterns/README.md)

## 🐞 Reporting Issues

Found a bug or have a feature request? Please create an issue with:
- Python version
- Operating system
- Error message (if any)
- Sample PDF (if possible)

## 📄 License

Same as Fabric project - MIT License

---

**Happy Learning! 📖✨**
