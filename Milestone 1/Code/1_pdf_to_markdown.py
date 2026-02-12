# STRATOS PDF-to-Markdown Extractor
# Converts academic PDFs to structured markdown using Docling.

# Usage: Type the following command in the terminal, with the input PDF path and optional output directory: python 1_pdf_to_markdown.py Dataset/<paper_name>.pdf Output/

# Context: Code is being run on an Apple Silicon Mac, so we set environment variables to force CPU fallback for PyTorch to avoid memory issues.
# The script uses Docling's DocumentConverter with specific options to preserve LaTeX formulas and tables.
# It logs the number of tables found and the size of the output markdown for each PDF processed.


# Platform Notes
# This script was developed on macOS with Apple Silicon (M-series chip).
# If you are running on a different platform, make the following changes:

#   Windows / Linux with NVIDIA GPU:
#     - Remove or comment out the two os.environ lines below (PYTORCH_ENABLE_MPS_FALLBACK and PYTORCH_MPS_HIGH_WATERMARK_RATIO). They are Apple-specific.
#     - Ensure you have a CUDA-compatible PyTorch installed (pip install torch) so Docling can use your GPU.

#   Windows / Linux CPU-only (no GPU):
#     - Remove or comment out the two os.environ lines below.
#     - A standard PyTorch CPU build is sufficient (pip install torch).
#     - Formula enrichment may be slow on CPU; set do_formula_enrichment = False if processing time is too long.

#   All platforms:
#     - Install Docling:  pip install docling
#     - Python 3.10+ is required.

import os
import sys
from pathlib import Path  # Cross-platform file path handling

# Force CPU fallback on Apple Silicon to prevent MPS memory issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = (
    "1"  # Fall back to CPU when MPS op is unsupported
)
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"  # Disable MPS memory caching

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)  # Core Docling converter
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)  # PDF-specific pipeline config
from docling.datamodel.base_models import InputFormat  # Enum for input file types


def extract_pdf_to_markdown(pdf_path: Path, output_dir: Path) -> Path:
    "Convert a single PDF to markdown, preserving tables and section structure."

    # Configure Docling pipeline
    pipeline_options = PdfPipelineOptions()  # Default PDF parsing options
    pipeline_options.do_formula_enrichment = False  # Enable LaTeX formula detection and preservation (if too slow, can be set to False)

    converter = DocumentConverter(  # Initialize the converter with PDF-specific options
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # Convert PDF
    print(f"Extracting: {pdf_path.name}")
    result = converter.convert(str(pdf_path))  # Run Docling extraction on the PDF
    markdown = (
        result.document.export_to_markdown()
    )  # Export parsed document as markdown string

    # Save output
    output_path = (
        output_dir / f"{pdf_path.stem}.md"
    )  # Name output file after the input PDF
    output_path.write_text(markdown, encoding="utf-8")  # Write markdown to disk
    print(f"Saved: {output_path}")

    # Log basic stats
    table_count = (
        len(result.document.tables) if result.document.tables else 0
    )  # Count extracted tables
    print(f"  Tables found: {table_count}")
    print(f"  Output size: {len(markdown):,} characters")

    return output_path


def main():
    if len(sys.argv) < 2:  # Check if user provided a PDF path
        print("Usage: python 1_pdf_to_markdown.py Dataset/<paper_name>.pdf Output/")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])  # First argument: path to input PDF
    output_dir = (
        Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./Output")
    )  # Optional second argument: output directory (defaults to Output/)

    # Validate input exists and is a PDF
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        print(f"Error: {pdf_path} is not a valid PDF file")
        sys.exit(1)

    output_dir.mkdir(
        parents=True, exist_ok=True
    )  # Create output directory if it doesn't exist

    # Run extraction
    output_path = extract_pdf_to_markdown(pdf_path, output_dir)
    print(f"\nDone. Output saved to: {output_path}")


if __name__ == "__main__":
    main()
