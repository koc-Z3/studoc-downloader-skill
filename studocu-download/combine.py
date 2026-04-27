#!/usr/bin/env python3
"""
Combine downloaded Studocu page images into a single PDF.
Run after download.sh completes.
"""

import img2pdf
import os
import sys

URLS_FILE = '/tmp/ordered_urls.txt'
OUTPUT_FILE = '/tmp/studocu_document.pdf'
IMAGES_DIR = '/tmp/studocu_images'

def combine_to_pdf():
    if not os.path.exists(URLS_FILE):
        print(f'Error: {URLS_FILE} not found. Run discover.py first.')
        sys.exit(1)
    
    with open(URLS_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    image_paths = []
    missing = 0
    for url in urls:
        filename = url.split('/html/')[1].split('?')[0]
        path = f'{IMAGES_DIR}/{filename}'
        if os.path.exists(path):
            image_paths.append(path)
        else:
            missing += 1
    
    if missing > 0:
        print(f'Warning: {missing} images missing')
    
    if not image_paths:
        print('Error: No images found')
        sys.exit(1)
    
    print(f'Combining {len(image_paths)} images into PDF...')
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(img2pdf.convert(image_paths))
    
    size_mb = os.path.getsize(OUTPUT_FILE) / 1024 / 1024
    print(f'Done: {OUTPUT_FILE} ({size_mb:.2f} MB, {len(image_paths)} pages)')

if __name__ == '__main__':
    combine_to_pdf()
