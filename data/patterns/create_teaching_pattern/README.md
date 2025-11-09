# create_teaching_pattern

## Description

This pattern transforms documents, papers, manuals, and other educational content into comprehensive, domain-specific teaching resources. It's especially powerful when used with PDF files containing technical documentation, research papers, or professional materials.

## Use Cases

- Creating teaching materials from technical documentation
- Developing training content for professional development
- Converting research papers into educational resources
- Building course materials from industry whitepapers
- Designing domain-specific learning modules
- Generating instructional content from manuals and guides

## Usage

### Basic Usage

```bash
# Pipe text content
cat document.txt | fabric --pattern create_teaching_pattern

# From clipboard
pbpaste | fabric --pattern create_teaching_pattern
```

### With PDF Files (Recommended)

The pattern works exceptionally well with PDF attachments, automatically extracting text content:

```bash
# Single PDF file
fabric --pattern create_teaching_pattern -a document.pdf

# Multiple PDF files
fabric --pattern create_teaching_pattern -a file1.pdf -a file2.pdf -a file3.pdf

# PDF with additional context
fabric --pattern create_teaching_pattern -a document.pdf <<EOF
Please focus on creating materials for:
- Target audience: Mid-level software engineers
- Domain: Cloud architecture
- Emphasis on practical applications
EOF
```

### Advanced Usage

```bash
# Save output to markdown file
fabric --pattern create_teaching_pattern -a technical-paper.pdf -o teaching-materials.md

# Stream output while processing
fabric --pattern create_teaching_pattern -a manual.pdf --stream

# Use with specific model
fabric --pattern create_teaching_pattern -a document.pdf -m claude-opus-4

# Process multiple PDFs and combine into one teaching resource
fabric --pattern create_teaching_pattern \
  -a chapter1.pdf \
  -a chapter2.pdf \
  -a chapter3.pdf \
  -o complete-course.md
```

## Output

The pattern generates a comprehensive teaching resource including:

- Domain identification and audience assessment
- Specific learning objectives
- Key concepts and definitions
- Structured content outline
- Visual elements analysis (for diagrams/charts)
- Practical applications and use cases
- Teaching strategies and activities
- Common misconceptions
- Discussion questions
- Extension activities
- Assessment suggestions
- Recommended teaching sequence

## Tips

1. **For Best Results**: Use PDF files with clear, well-structured content
2. **Multiple Files**: Process related PDFs together to create comprehensive course materials
3. **Add Context**: Include specific instructions about your target audience or domain
4. **Iterative Refinement**: Use the output as a foundation and refine for your specific needs
5. **Diagrams**: The pattern identifies and describes visual elements from PDFs for incorporation in teaching

## Examples

### Example 1: Technical Documentation

```bash
fabric --pattern create_teaching_pattern -a kubernetes-guide.pdf <<EOF
Target: DevOps engineers new to Kubernetes
Focus: Hands-on deployment scenarios
EOF
```

### Example 2: Research Paper

```bash
fabric --pattern create_teaching_pattern -a machine-learning-paper.pdf <<EOF
Transform this into undergraduate-level teaching materials
Emphasize practical implementation over theory
EOF
```

### Example 3: Multiple Documents

```bash
fabric --pattern create_teaching_pattern \
  -a intro.pdf \
  -a advanced-topics.pdf \
  -a case-studies.pdf \
  --stream \
  -o complete-training-program.md
```

## Integration with Workflows

```bash
# Create teaching pattern from all PDFs in a directory
for pdf in documents/*.pdf; do
  fabric --pattern create_teaching_pattern -a "$pdf" -o "teaching-$(basename "$pdf" .pdf).md"
done

# Combine with other patterns
fabric --pattern create_teaching_pattern -a doc.pdf | \
  fabric --pattern improve_writing
```

## Notes

- PDF text extraction happens automatically - no preprocessing needed
- Diagrams and visual elements are analyzed and described in the output
- The pattern adapts to the domain and complexity of the input material
- Works with both text-heavy and diagram-rich PDFs
- Best results with well-formatted, professional documents

## Related Patterns

- `create_quiz` - Generate review questions from the teaching materials
- `create_flash_cards` - Create flashcards from key concepts
- `create_conceptmap` - Visualize concept relationships
- `explain_code` - For software documentation
- `create_reading_plan` - Structure the learning sequence
