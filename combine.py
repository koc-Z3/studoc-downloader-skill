#!/usr/bin/env python3
"""
Combine downloaded Studocu page images into a single PDF.

Usage:
    python3 combine.py                    # Uses defaults
    python3 combine.py /path/to/urls.txt   # Custom urls file
    python3 combine.py /path/to/urls.txt /path/to/images/  # Custom urls + images dir
    python3 combine.py /path/to/urls.txt /path/to/images/ /output.pdf  # All custom
"""

import sys
import os
import tempfile
import argparse

try:
    import img2pdf
except ImportError:
    print("Error: img2pdf not installed. Run: pip install img2pdf Pillow")
    sys.exit(1)


def combine_to_pdf(
    urls_file: str = None,
    images_dir: str = None,
    output_file: str = None
) -> str:
    """Combine images into PDF. Returns path to output file."""
    
    if urls_file is None:
        urls_file = os.path.join(tempfile.gettempdir(), "ordered_urls.txt")
    if images_dir is None:
        images_dir = os.path.join(tempfile.gettempdir(), "studocu_images")
    if output_file is None:
        output_file = os.path.join(tempfile.gettempdir(), "studocu_document.pdf")
    
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found. Run discover.py first.")
        sys.exit(1)
    
    with open(urls_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    image_paths = []
    missing = 0
    for url in urls:
        try:
            filename = url.split("/html/")[1].split("?")[0]
        except IndexError:
            continue
        path = os.path.join(images_dir, filename)
        if os.path.exists(path):
            image_paths.append(path)
        else:
            missing += 1
    
    if missing > 0:
        print(f"Warning: {missing} images missing")
    
    if not image_paths:
        print("Error: No images found")
        sys.exit(1)
    
    print(f"Combining {len(image_paths)} images into PDF...")
    
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    
    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"Done: {output_file} ({size_mb:.2f} MB, {len(image_paths)} pages)")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Combine Studocu images into PDF")
    parser.add_argument("urls_file", nargs="?", help="Path to ordered_urls.txt")
    parser.add_argument("images_dir", nargs="?", help="Path to images directory")
    parser.add_argument("output_file", nargs="?", help="Output PDF path")
    args = parser.parse_args()
    
    combine_to_pdf(args.urls_file, args.images_dir, args.output_file)


if __name__ == "__main__":
    main()
