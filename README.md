# Studocu Downloader

Download documents from Studocu as PDFs by scraping lazy-loaded page images in scroll order.

## Overview

When Studocu blocks direct PDF download or requires login, this tool extracts the document pages by:

1. Bypassing Cloudflare with Playwright + Tor
2. Scrolling through the document to discover all lazy-loaded page images
3. Recording the correct page order using viewport position tracking
4. Downloading images via curl through Tor
5. Combining into a PDF with img2pdf

## Prerequisites

- Tor: `pgrep -x tor || tor &`
- Python packages: `uv pip install img2pdf Pillow playwright`
- Playwright browsers: `playwright install chromium`

## Usage

```bash
# 1. Discover all pages in scroll order
python3 discover.py https://www.studocu.com/en-au/document/...

# 2. Download images
./download.sh

# 3. Combine into PDF
python3 combine.py
```

## How It Works

Studocu loads document pages lazily as images (`doc-assets.studocu.com/{hash}/html/bg{N}.png`). The images are loaded in scroll order, not by page number. We scroll in 500px increments and track which image is visible at the viewport center to get the correct page order.

## License

MIT
