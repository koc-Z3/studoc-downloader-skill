---
name: studocu-download
description: Download documents from Studocu when blocked by Cloudflare, by scraping lazy-loaded page images in scroll order and combining into PDF
category: productivity
---

# Studocu Document Download

Download documents from Studocu when the site blocks direct access or requires login for PDF download.

## Approach

1. **Bypass Cloudflare**: Use Playwright with Tor proxy (socks5://127.0.0.1:9050) with a real Chrome User-Agent
2. **Lazy loading**: Studocu loads document page images lazily as you scroll. Must scroll through ENTIRE page to discover all images. Initial load only shows ~7 images, scrolling reveals more (this document had 63 pages)
3. **Get images in page order**: Use Playwright to scroll in small increments (500px steps) and record which doc-assets image is visible at viewport center at each position. This gives the correct top-to-bottom page order.
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
- img2pdf: `uv pip install img2pdf Pillow`

## Complete End-to-End Workflow

### 1. Ensure Tor is running
```bash
pgrep -x tor || tor &
```

### 2. Discover all page images in scroll order
Save this as `/tmp/discover_studocu.py` and run it:

```python
from playwright.sync_api import sync_playwright
import time

url = 'STUDOCU_URL_HERE'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, proxy={'server': 'socks5://127.0.0.1:9050'})
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    page.goto(url, timeout=120000)
    time.sleep(20)
    
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(2)
    
    discovered = []
    seen = set()
    viewport_height = page.viewport_size['height']
    center_y = viewport_height // 2
    
    scroll_pos = 0
    step = 500
    max_scroll = 90000
    
    while scroll_pos <= max_scroll:
        page.evaluate('window.scrollTo(0, ' + str(scroll_pos) + ')')
        time.sleep(0.3)
        
        js_result = page.evaluate('''
            (centerY) => {
                const imgs = document.querySelectorAll('img[src*="doc-assets.studocu.com"]');
                for (const img of imgs) {
                    if (img.src.includes('/html/bg')) {
                        const rect = img.getBoundingClientRect();
                        if (rect.top <= centerY && rect.bottom >= centerY) {
                            return img.src;
                        }
                    }
                }
                return null;
            }
        ''', center_y)
        
        if js_result and js_result not in seen:
            seen.add(js_result)
            discovered.append(js_result)
            print(f'Discovered {len(discovered)}')
        
        scroll_pos += step
    
    with open('/tmp/ordered_urls.txt', 'w') as f:
        for url in discovered:
            f.write(url + chr(10))
    
    print(f'Total: {len(discovered)} pages')
    browser.close()
```

Run it:
```bash
python3 /tmp/discover_studocu.py
```

### 3. Download all images
```bash
mkdir -p /tmp/studocu_images
cd /tmp/studocu_images

while IFS= read -r url; do
  filename=$(echo "$url" | grep -oP 'bg[^?]+')
  curl -s --proxy socks5://127.0.0.1:9050 \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -o "$filename" "$url" &
  
  if (( $(jobs -r -p | wc -l) >= 5 )); then
    wait -n
  fi
done < /tmp/ordered_urls.txt
wait
```

### 4. Combine into PDF
```python
import img2pdf
import os

with open('/tmp/ordered_urls.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

image_paths = []
for url in urls:
    filename = url.split('/html/')[1].split('?')[0]
    path = f'/tmp/studocu_images/{filename}'
    if os.path.exists(path):
        image_paths.append(path)

output_path = '/tmp/studocu_document.pdf'
with open(output_path, 'wb') as f:
    f.write(img2pdf.convert(image_paths))

print(f'PDF: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB, {len(image_paths)} pages')
```

### 5. Deliver
```bash
zip -j /tmp/output.zip /tmp/studocu_document.pdf
```
Then send via Telegram: `MEDIA:/tmp/output.zip`
