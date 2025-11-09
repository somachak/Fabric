#!/usr/bin/env python3
"""
Example: Query Vector Database and Generate Teaching Materials

This script demonstrates how to:
1. Query the vector database for specific topics
2. Retrieve relevant context
3. Use Fabric to generate comprehensive teaching materials

Usage:
    python query_and_generate.py <topic> [--subtopics ...]

Example:
    python query_and_generate.py "regression" --subtopics "linear regression" "Python scikit-learn"
"""

import argparse
from pathlib import Path
import subprocess
import sys

try:
    import chromadb
except ImportError:
    print("❌ ChromaDB not installed. Install with:")
    print("   pip install chromadb")
    sys.exit(1)

def query_knowledge_base(db_path: Path, collection_name: str, topic: str, subtopics: list = None, n_results: int = 10):
    """
    Query the vector database for a specific topic

    Args:
        db_path: Path to vector database
        collection_name: Collection name
        topic: Main topic to query
        subtopics: Optional list of subtopics
        n_results: Number of results to retrieve

    Returns:
        Combined context from relevant documents
    """

    print(f"🔍 Querying Knowledge Base")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    if subtopics:
        print(f"Subtopics: {', '.join(subtopics)}")
    print(f"Results: {n_results}\n")

    # Connect to vector database
    client = chromadb.PersistentClient(path=str(db_path))

    try:
        collection = client.get_collection(collection_name)
    except:
        print(f"❌ Collection '{collection_name}' not found!")
        print(f"   Run build_vector_db.py first to create the database.")
        sys.exit(1)

    # Build comprehensive query
    queries = [topic]
    if subtopics:
        queries.extend(subtopics)

    all_docs = []
    seen_ids = set()

    for query in queries:
        print(f"  Searching for: {query}")
        results = collection.query(
            query_texts=[query],
            n_results=n_results // len(queries) if len(queries) > 1 else n_results
        )

        # Deduplicate results
        for doc, doc_id in zip(results['documents'][0], results['ids'][0]):
            if doc_id not in seen_ids:
                all_docs.append(doc)
                seen_ids.add(doc_id)

    print(f"\n✓ Found {len(all_docs)} unique relevant documents")

    # Combine context
    context = "\n\n=== SECTION ===\n\n".join(all_docs)
    return context

def generate_teaching_materials(context: str, pattern: str = "create_teaching_pattern", output_file: Path = None):
    """
    Generate teaching materials using Fabric

    Args:
        context: Retrieved context from vector database
        pattern: Fabric pattern to use
        output_file: Optional file to save output

    Returns:
        Generated teaching materials
    """

    print(f"\n🎯 Generating Teaching Materials")
    print(f"{'='*60}")
    print(f"Pattern: {pattern}")
    if output_file:
        print(f"Output: {output_file}")
    print()

    # Call Fabric
    try:
        result = subprocess.run(
            ['fabric', '--pattern', pattern],
            input=context,
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout

        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ Saved to: {output_file}")

        return output

    except subprocess.CalledProcessError as e:
        print(f"❌ Fabric error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Fabric CLI not found. Make sure it's installed and in your PATH.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Query vector database and generate teaching materials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate regression teaching materials
    python query_and_generate.py "regression analysis" \\
        --subtopics "linear regression" "Python scikit-learn" \\
        --output regression_course.md

    # Generate time series materials
    python query_and_generate.py "time series" \\
        --subtopics "ARIMA" "forecasting" "statsmodels" \\
        --output timeseries_course.md

    # Use different pattern
    python query_and_generate.py "hypothesis testing" \\
        --pattern extract_teaching_content \\
        --output hypothesis_testing.md
        """
    )

    parser.add_argument('topic', type=str,
                       help='Main topic to query')
    parser.add_argument('--subtopics', nargs='+',
                       help='Additional subtopics to include')
    parser.add_argument('--db-path', type=Path, default=Path('./vectordb'),
                       help='Path to vector database (default: ./vectordb)')
    parser.add_argument('--collection', default='teaching_knowledge',
                       help='Collection name (default: teaching_knowledge)')
    parser.add_argument('--results', type=int, default=10,
                       help='Number of results to retrieve (default: 10)')
    parser.add_argument('--pattern', default='create_teaching_pattern',
                       help='Fabric pattern to use (default: create_teaching_pattern)')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output file for generated materials')
    parser.add_argument('--preview-only', action='store_true',
                       help='Only show context, don\'t generate materials')

    args = parser.parse_args()

    # Query vector database
    context = query_knowledge_base(
        db_path=args.db_path,
        collection_name=args.collection,
        topic=args.topic,
        subtopics=args.subtopics,
        n_results=args.results
    )

    print(f"\n📄 Retrieved Context ({len(context)} characters)")

    # Preview context if requested
    if args.preview_only:
        print(f"\n{'-'*60}")
        print(context[:1000])
        print(f"\n... ({len(context) - 1000} more characters) ...")
        return

    # Generate teaching materials
    output = generate_teaching_materials(
        context=context,
        pattern=args.pattern,
        output_file=args.output
    )

    # Print output if not saved to file
    if not args.output:
        print(f"\n{'='*60}")
        print("Generated Teaching Materials:")
        print(f"{'='*60}\n")
        print(output)

    print(f"\n✅ Complete!")

if __name__ == '__main__':
    main()
