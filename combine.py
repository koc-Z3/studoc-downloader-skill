#!/usr/bin/env python3
"""
Combine downloaded Studocu page images into a PDF.
Run after download.sh completes.
"""

import img2pdf
import os

def combine_to_pdf():
    with open('/tmp/ordered_urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    image_paths = []
    for url in urls:
        filename = url.split('/html/')[1].split('?')[0]
        path = f'/tmp/studocu_images/{filename}'
        if os.path.exists(path):
            image_paths.append(path)
        else:
            print(f'Missing: {filename}')
    
    output_path = '/tmp/studocu_document.pdf'
    with open(output_path, 'wb') as f:
        f.write(img2pdf.convert(image_paths))
    
    size = os.path.getsize(output_path)
    print(f'PDF: {size / 1024 / 1024:.2f} MB, {len(image_paths)} pages')
    print(f'Saved to: {output_path}')

if __name__ == '__main__':
    combine_to_pdf()
