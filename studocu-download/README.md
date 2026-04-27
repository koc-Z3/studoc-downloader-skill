# Quick Reference

## Start Here
```bash
# 1. Ensure Tor is running
pgrep -x tor || tor &

# 2. Discover pages (replace URL)
python3 discover.py "STUDOCU_URL"

# 3. Download images
bash download.sh

# 4. Combine to PDF
python3 combine.py

# 5. Output
ls -lh /tmp/studocu_document.pdf
```

## Troubleshooting

### Cloudflare blocked
- Increase initial wait time in discover.py (time.sleep(20))
- Check Tor is working: `curl --proxy socks5://127.0.0.1:9050 https://check.torproject.org`

### Missing pages
- Increase max_scroll in discover.py
- Some documents have 60+ pages

### Slow download
- Adjust concurrent download limit in download.sh (default: 5)
