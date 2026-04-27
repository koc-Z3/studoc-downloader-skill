---
name: studocu-download
description: Download documents from Studocu when blocked by Cloudflare, by scraping lazy-loaded page images in scroll order and combining into PDF
category: productivity
---

# Studocu Document Download

Download documents from Studocu when the site blocks direct access or requires login for PDF download.

## Approach

1. **Bypass Cloudflare**: Use Playwright with Tor proxy (socks5://127.0.0.1:9050)
2. **Lazy loading**: Studocu loads document page images lazily as you scroll. Must scroll through ENTIRE page to discover all images
3. **Get images in page order**: Use Playwright to scroll in small increments and record which doc-assets image is visible at viewport center at each position
4. **Download via curl with Tor**: The signed URLs work for direct download through Tor proxy
5. **Combine to PDF**: Use img2pdf to combine downloaded PNGs

## Technical Details

### Image URL pattern
```
https://doc-assets.studocu.com/{hash}/html/bg{N}.png?Policy=...&Signature=...&Key-Pair-Id=...
```

### Important: Image naming does NOT equal page order
The bg* names appear sequential but pages may not load in order. Must use scroll position to determine actual page order.

## Prerequisites

```bash
# Tor must be running
pgrep -x tor || tor &

# Install dependencies
pip install playwright img2pdf Pillow
playwright install chromium
```

## Usage

### Step 1: Discover pages
```bash
python3 discover.py "STUDOCU_URL" [--output /path/to/urls.txt]
```
- Uses Tor proxy by default (configure PROXY in script if needed)
- Outputs to `/tmp/ordered_urls.txt` by default (or custom path)

### Step 2: Download images
```bash
bash download.sh                     # Uses defaults
bash download.sh /path/to/urls.txt   # Custom urls file
bash download.sh /path/to/urls.txt /output/dir  # Custom output dir
```
- Downloads to `/tmp/studocu_images/` by default
- Uses Tor proxy, 5 concurrent downloads by default

### Step 3: Combine into PDF
```bash
python3 combine.py                           # Uses defaults
python3 combine.py /urls.txt /images/ /out.pdf  # All custom
```

## Configuration

All scripts have configurable constants at the top:

**discover.py**
- `PROXY` - Tor proxy address
- `USER_AGENT` - Browser user agent
- `VIEWPORT` - Browser viewport size
- `SCROLL_STEP` - Pixels per scroll step
- `INITIAL_WAIT` - Seconds to wait for Cloudflare

**download.sh**
- `PROXY` - Tor proxy address
- `USER_AGENT` - Browser user agent
- `MAX_CONCURRENT` - Concurrent download limit

## Cross-Platform

- Scripts use `tempfile` and `os.path.join` for OS-agnostic paths
- Works on Linux, macOS, and Windows (with Git Bash or WSL)
- Bash scripts require standard Unix tools (curl, grep)
