#!/usr/bin/env python3
"""
Batch PDF Processor for Teaching Pattern Extraction
Supports both vision and text intelligence using Gemini API
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from dataclasses import dataclass, asdict
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import shutil

@dataclass
class ProcessingResult:
    """Result of processing a single PDF"""
    filename: str
    success: bool
    extracted_content: Optional[str] = None
    teaching_patterns: Optional[Dict] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None

class GeminiPDFProcessor:
    """Process PDFs using Gemini's vision and text capabilities"""

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize Gemini processor"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_pdf_content(self, pdf_path: Path, use_vision: bool = True) -> str:
        """
        Extract content from PDF using Gemini's vision capabilities
        This allows understanding of diagrams, charts, and equations
        """
        try:
            if use_vision:
                # Upload PDF for vision analysis
                print(f"  📸 Analyzing with vision intelligence: {pdf_path.name}")
                uploaded_file = genai.upload_file(str(pdf_path))

                prompt = """Analyze this PDF document comprehensively:

1. Extract ALL text content while preserving structure
2. Describe ALL visual elements (diagrams, charts, figures, equations, tables)
3. Explain what each visual element teaches or illustrates
4. Identify mathematical notation, formulas, and their context
5. Capture the pedagogical flow and organization
6. Note any examples, exercises, or practice problems

Format your response as structured text that can be processed by an educational content analyzer.
Include both the textual content and detailed descriptions of visual elements."""

                response = self.model.generate_content([prompt, uploaded_file])
                return response.text
            else:
                # Text-only extraction using Fabric
                print(f"  📝 Extracting text: {pdf_path.name}")
                result = subprocess.run(
                    ['fabric', '-a', str(pdf_path)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout

        except Exception as e:
            raise Exception(f"Failed to extract content: {str(e)}")

class FabricBatchProcessor:
    """Batch process PDFs through Fabric patterns"""

    def __init__(self,
                 gemini_api_key: Optional[str] = None,
                 pattern: str = "extract_teaching_content",
                 use_vision: bool = True,
                 max_workers: int = 3):
        """
        Initialize batch processor

        Args:
            gemini_api_key: Gemini API key for vision intelligence
            pattern: Fabric pattern to use
            use_vision: Whether to use Gemini vision capabilities
            max_workers: Number of parallel processing threads
        """
        self.pattern = pattern
        self.use_vision = use_vision and gemini_api_key is not None
        self.max_workers = max_workers

        if self.use_vision:
            self.gemini_processor = GeminiPDFProcessor(gemini_api_key)
        else:
            self.gemini_processor = None

    def find_pdfs(self, path: Path) -> List[Path]:
        """Find all PDF files in path (file or directory)"""
        if path.is_file():
            if path.suffix.lower() == '.pdf':
                return [path]
            else:
                raise ValueError(f"{path} is not a PDF file")
        elif path.is_dir():
            pdfs = list(path.rglob('*.pdf'))
            print(f"📁 Found {len(pdfs)} PDF files in {path}")
            return pdfs
        else:
            raise ValueError(f"{path} does not exist")

    def process_single_pdf(self, pdf_path: Path, output_dir: Path) -> ProcessingResult:
        """Process a single PDF file"""
        print(f"\n🔍 Processing: {pdf_path.name}")

        try:
            # Step 1: Extract content (with or without vision)
            if self.use_vision and self.gemini_processor:
                extracted_content = self.gemini_processor.extract_pdf_content(pdf_path)
            else:
                # Use Fabric's built-in PDF extraction
                result = subprocess.run(
                    ['fabric', '-a', str(pdf_path)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                extracted_content = result.stdout

            # Step 2: Process through Fabric pattern
            print(f"  🎯 Applying pattern: {self.pattern}")
            result = subprocess.run(
                ['fabric', '--pattern', self.pattern],
                input=extracted_content,
                capture_output=True,
                text=True,
                check=True
            )

            teaching_patterns = result.stdout

            # Step 3: Save results
            output_base = output_dir / pdf_path.stem

            # Save raw extracted content
            with open(f"{output_base}_extracted.txt", 'w', encoding='utf-8') as f:
                f.write(extracted_content)

            # Save teaching pattern analysis
            with open(f"{output_base}_teaching.md", 'w', encoding='utf-8') as f:
                f.write(teaching_patterns)

            # Parse metadata if possible
            metadata = {
                'filename': pdf_path.name,
                'size_bytes': pdf_path.stat().st_size,
                'vision_used': self.use_vision,
                'pattern': self.pattern
            }

            with open(f"{output_base}_metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

            print(f"  ✅ Success: {pdf_path.name}")

            return ProcessingResult(
                filename=str(pdf_path),
                success=True,
                extracted_content=extracted_content,
                teaching_patterns=teaching_patterns,
                metadata=metadata
            )

        except subprocess.CalledProcessError as e:
            error_msg = f"Fabric processing failed: {e.stderr}"
            print(f"  ❌ Error: {error_msg}")
            return ProcessingResult(
                filename=str(pdf_path),
                success=False,
                error=error_msg
            )
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Error: {error_msg}")
            return ProcessingResult(
                filename=str(pdf_path),
                success=False,
                error=error_msg
            )

    def process_batch(self,
                     input_path: Path,
                     output_dir: Path,
                     parallel: bool = True) -> List[ProcessingResult]:
        """
        Process multiple PDFs in batch

        Args:
            input_path: Path to PDF file or directory
            output_dir: Directory to save results
            parallel: Whether to process in parallel

        Returns:
            List of processing results
        """
        # Find all PDFs
        pdf_files = self.find_pdfs(input_path)

        if not pdf_files:
            print("⚠️  No PDF files found!")
            return []

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🚀 Processing {len(pdf_files)} PDFs...")
        print(f"📊 Vision Intelligence: {'Enabled ✓' if self.use_vision else 'Disabled'}")
        print(f"🎯 Pattern: {self.pattern}")
        print(f"💾 Output: {output_dir}\n")

        results = []

        if parallel and len(pdf_files) > 1:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_pdf = {
                    executor.submit(self.process_single_pdf, pdf, output_dir): pdf
                    for pdf in pdf_files
                }

                for future in as_completed(future_to_pdf):
                    result = future.result()
                    results.append(result)
        else:
            # Sequential processing
            for pdf in pdf_files:
                result = self.process_single_pdf(pdf, output_dir)
                results.append(result)

        # Print summary
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        print(f"\n{'='*60}")
        print(f"📊 Processing Complete!")
        print(f"✅ Successful: {successful}/{len(results)}")
        if failed > 0:
            print(f"❌ Failed: {failed}/{len(results)}")
        print(f"💾 Results saved to: {output_dir}")
        print(f"{'='*60}\n")

        # Save summary report
        summary = {
            'total_files': len(results),
            'successful': successful,
            'failed': failed,
            'vision_used': self.use_vision,
            'pattern': self.pattern,
            'results': [asdict(r) for r in results]
        }

        with open(output_dir / 'processing_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

        return results

def load_config() -> Dict:
    """Load configuration from file or environment"""
    config = {}

    # Try to load from config file
    config_path = Path.home() / '.config' / 'fabric' / 'batch_processor_config.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)

    # Environment variables override config file
    if 'GEMINI_API_KEY' in os.environ:
        config['gemini_api_key'] = os.environ['GEMINI_API_KEY']

    return config

def main():
    parser = argparse.ArgumentParser(
        description='Batch process PDFs to extract teaching patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single PDF with vision intelligence
  python batch_processor.py input.pdf -o output/

  # Process entire folder
  python batch_processor.py pdfs/ -o results/

  # Disable vision intelligence (faster, text-only)
  python batch_processor.py pdfs/ -o results/ --no-vision

  # Use different pattern
  python batch_processor.py pdfs/ -o results/ -p create_teaching_pattern

  # Sequential processing (no parallelization)
  python batch_processor.py pdfs/ -o results/ --sequential
        """
    )

    parser.add_argument('input', type=Path, help='Input PDF file or directory')
    parser.add_argument('-o', '--output', type=Path, required=True,
                       help='Output directory')
    parser.add_argument('-p', '--pattern', default='extract_teaching_content',
                       help='Fabric pattern to use (default: extract_teaching_content)')
    parser.add_argument('--no-vision', action='store_true',
                       help='Disable Gemini vision intelligence (text-only)')
    parser.add_argument('--sequential', action='store_true',
                       help='Process files sequentially (no parallelization)')
    parser.add_argument('-w', '--workers', type=int, default=3,
                       help='Number of parallel workers (default: 3)')
    parser.add_argument('--gemini-key', type=str,
                       help='Gemini API key (or set GEMINI_API_KEY env var)')

    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Get Gemini API key
    gemini_key = args.gemini_key or config.get('gemini_api_key')

    if not args.no_vision and not gemini_key:
        print("⚠️  Warning: No Gemini API key provided!")
        print("Vision intelligence disabled. Using text-only extraction.")
        print("\nTo enable vision intelligence:")
        print("  1. Set GEMINI_API_KEY environment variable, or")
        print("  2. Use --gemini-key argument, or")
        print("  3. Create config at ~/.config/fabric/batch_processor_config.json")
        use_vision = False
    else:
        use_vision = not args.no_vision

    # Create processor
    processor = FabricBatchProcessor(
        gemini_api_key=gemini_key,
        pattern=args.pattern,
        use_vision=use_vision,
        max_workers=args.workers
    )

    # Process files
    try:
        results = processor.process_batch(
            input_path=args.input,
            output_dir=args.output,
            parallel=not args.sequential
        )

        # Exit with error code if any failed
        if any(not r.success for r in results):
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
