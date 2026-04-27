# Studoc Downloader Skill

Download documents from Studocu when blocked by Cloudflare, by scraping lazy-loaded page images in scroll order and combining into PDF.

## Quick Start

```bash
# 1. Start Tor
tor &

# 2. Discover pages
python3 discover.py "STUDOCU_URL"

# 3. Download images
bash download.sh

# 4. Combine to PDF
python3 combine.py
```

## Project Structure

```
├── SKILL.md         # Skill documentation (for agents)
├── README.md        # This file
├── requirements.txt # Python dependencies
├── discover.py      # Scroll page, collect image URLs
├── download.sh      # Download images via Tor
└── combine.py       # Combine images into PDF
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Custom Paths

```bash
python3 discover.py "URL" -o ./my_urls.txt
bash download.sh ./my_urls.txt ./my_images/
python3 combine.py ./my_urls.txt ./my_images/ ./output.pdf
```

## Troubleshooting

### Cloudflare blocked
Increase `INITIAL_WAIT` in discover.py (try 30-60 seconds)

### Missing pages
Increase `max_scroll` calculation in discover.py or `SCROLL_STEP`

### Slow download
Adjust `MAX_CONCURRENT` in download.sh (default: 5)

### Check Tor working
```bash
curl --proxy socks5://127.0.0.1:9050 https://check.torproject.org
```
