# Studocu Downloader For Agents

Download documents from Studocu when blocked by Cloudflare, by scraping lazy-loaded page images in scroll order and combining into PDF.

## Quick Start

```bash
# 1. Start Tor
tor &

# 2. Discover pages
python3 studocu-download/discover.py "STUDOCU_URL"

# 3. Download images
bash studocu-download/download.sh

# 4. Combine to PDF
python3 studocu-download/combine.py
```

## Project Structure

```
studocu-download/
├── SKILL.md        # Full skill documentation
├── README.md       # Quick reference
├── discover.py     # Scroll page, collect image URLs
├── download.sh     # Download images via Tor
└── combine.py     # Combine images into PDF
```

## Requirements

- Tor (running on localhost:9050)
- Playwright (`pip install playwright && playwright install chromium`)
- img2pdf (`pip install img2pdf Pillow`)
