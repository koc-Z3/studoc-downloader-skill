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
- Naming: bg1, bg2... bg9, bga, bgb... bgf, bg10, bg11... bg3f (hex for pages 10-15)
- 63 pages = bg1 through bg3f

### Important: Image naming does NOT equal page order
The bg* names appear sequential but pages may not load in order. Must use scroll position to determine actual page order.

## Prerequisites

- Tor running: `pgrep -x tor || tor &`
- Playwright installed
- img2pdf: `pip install img2pdf Pillow`

## Complete End-to-End Workflow

### 1. Ensure Tor is running
```bash
pgrep -x tor || tor &
```

### 2. Discover all page images in scroll order
```bash
python3 discover.py "STUDOCU_URL_HERE"
```

### 3. Download all images
```bash
bash download.sh
```

### 4. Combine into PDF
```bash
python3 combine.py
```

### 5. Deliver
```bash
zip -j /tmp/output.zip /tmp/studocu_document.pdf
```
