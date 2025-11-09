#!/usr/bin/env python3
"""
Example: Build Vector Database from Extracted Teaching Content

This script shows how to create a vector database from the teaching patterns
extracted by the batch processor. It works with any vector database (ChromaDB,
Pinecone, Qdrant, etc.) - this example uses ChromaDB.

Usage:
    python build_vector_db.py <extracted_dir> [--db-path <path>]

Example:
    python build_vector_db.py ~/stats_knowledge_base/extracted/
"""

import argparse
from pathlib import Path
import json
import sys

try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
except ImportError:
    print("❌ ChromaDB not installed. Install with:")
    print("   pip install chromadb")
    sys.exit(1)

def build_vector_database(extracted_dir: Path, db_path: Path, collection_name: str = "teaching_knowledge"):
    """
    Build a vector database from extracted teaching content

    Args:
        extracted_dir: Directory containing extracted teaching content
        db_path: Path where vector database should be stored
        collection_name: Name for the collection
    """

    print(f"📊 Building Vector Database")
    print(f"{'='*60}")
    print(f"Input: {extracted_dir}")
    print(f"Database: {db_path}")
    print(f"Collection: {collection_name}\n")

    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=str(db_path))

    # Try to get existing collection or create new one
    try:
        collection = client.get_collection(collection_name)
        print(f"✓ Found existing collection '{collection_name}'")
        # Optionally, you could delete and recreate:
        # client.delete_collection(collection_name)
        # collection = client.create_collection(collection_name)
    except:
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "Teaching patterns and knowledge extracted from PDFs"}
        )
        print(f"✓ Created new collection '{collection_name}'")

    # Load all teaching content files
    teaching_files = list(extracted_dir.glob("*_teaching.md"))

    if not teaching_files:
        print(f"\n❌ No teaching files found in {extracted_dir}")
        print("   Make sure you've run batch_processor.py first!")
        sys.exit(1)

    print(f"\n📚 Found {len(teaching_files)} teaching content files")

    documents = []
    metadatas = []
    ids = []

    for teaching_file in teaching_files:
        print(f"  Processing: {teaching_file.name}")

        # Read teaching content
        with open(teaching_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Read metadata if available
        metadata_file = teaching_file.parent / teaching_file.name.replace('_teaching.md', '_metadata.json')

        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {
                'filename': teaching_file.stem,
                'source': str(teaching_file)
            }

        # Add to lists
        documents.append(content)
        metadatas.append(metadata)
        ids.append(teaching_file.stem)

    # Add to vector database
    print(f"\n💾 Adding {len(documents)} documents to vector database...")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Successfully added {len(documents)} documents to '{collection_name}'")
    print(f"\n📊 Vector Database Statistics:")
    print(f"   Total documents: {collection.count()}")
    print(f"   Database location: {db_path}")

    return collection

def test_query(collection, query: str = "regression analysis with Python"):
    """Test the vector database with a sample query"""

    print(f"\n🔍 Testing Query: '{query}'")
    print(f"{'='*60}")

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    print(f"\nFound {len(results['documents'][0])} relevant documents:\n")

    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"{i}. {metadata.get('filename', 'Unknown')}")
        print(f"   Preview: {doc[:150]}...")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='Build vector database from extracted teaching content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python build_vector_db.py ~/stats_knowledge_base/extracted/

This will:
    1. Load all *_teaching.md files
    2. Create embeddings using ChromaDB defaults
    3. Store in ./vectordb/ directory
    4. Run a test query
        """
    )

    parser.add_argument('extracted_dir', type=Path,
                       help='Directory containing extracted teaching content')
    parser.add_argument('--db-path', type=Path, default=Path('./vectordb'),
                       help='Path for vector database (default: ./vectordb)')
    parser.add_argument('--collection', default='teaching_knowledge',
                       help='Collection name (default: teaching_knowledge)')
    parser.add_argument('--test-query', type=str,
                       help='Test query to run after building database')
    parser.add_argument('--no-test', action='store_true',
                       help='Skip test query')

    args = parser.parse_args()

    # Verify input directory exists
    if not args.extracted_dir.exists():
        print(f"❌ Directory not found: {args.extracted_dir}")
        sys.exit(1)

    # Build vector database
    try:
        collection = build_vector_database(
            args.extracted_dir,
            args.db_path,
            args.collection
        )

        # Run test query
        if not args.no_test:
            query = args.test_query or "regression analysis with Python"
            test_query(collection, query)

        print("\n✅ Vector database ready for use!")
        print(f"\n💡 You can now query this database from Python:")
        print(f"""
import chromadb
client = chromadb.PersistentClient(path="{args.db_path}")
collection = client.get_collection("{args.collection}")
results = collection.query(query_texts=["your query"], n_results=5)
        """)

    except Exception as e:
        print(f"\n❌ Error building vector database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
