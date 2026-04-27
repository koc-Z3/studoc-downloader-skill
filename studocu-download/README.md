# Quick Reference

## Setup
```bash
pip install -r requirements.txt
playwright install chromium
tor &
```

## Full Workflow
```bash
# 1. Discover page URLs
python3 discover.py "STUDOCU_URL"

# 2. Download images
bash download.sh

# 3. Combine into PDF
python3 combine.py

# Output: /tmp/studocu_document.pdf
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
