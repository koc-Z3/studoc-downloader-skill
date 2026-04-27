#!/usr/bin/env python3
"""
Discover Studocu document page images in scroll order.

Usage:
    python3 discover.py "STUDOCU_URL" [--output /path/to/urls.txt]

Requirements:
    - Tor running on localhost:9050 (or configure PROXY below)
    - Playwright: pip install playwright && playwright install chromium
"""

import sys
import time
import argparse
import tempfile
import os
from playwright.sync_api import sync_playwright

# === CONFIGURATION ===
PROXY = "socks5://127.0.0.1:9050"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
VIEWPORT = {"width": 1920, "height": 1080}
SCROLL_STEP = 500
INITIAL_WAIT = 20
# ====================

def discover_pages(url: str, output_path: str = None) -> list[str]:
    """Discover all page image URLs by scrolling through the document."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy={"server": PROXY})
        page = browser.new_page(viewport=VIEWPORT)
        
        page.set_extra_http_headers({"User-Agent": USER_AGENT})
        
        print(f"Loading {url}...")
        page.goto(url, timeout=120000)
        time.sleep(INITIAL_WAIT)
        
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)
        
        discovered = []
        seen = set()
        viewport_height = page.viewport_size["height"]
        center_y = viewport_height // 2
        
        scroll_pos = 0
        max_scroll = page.evaluate("document.body.scrollHeight") + 10000
        
        while scroll_pos <= max_scroll:
            page.evaluate(f"window.scrollTo(0, {scroll_pos})")
            time.sleep(0.3)
            
            js_result = page.evaluate("""
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
            """, center_y)
            
            if js_result and js_result not in seen:
                seen.add(js_result)
                discovered.append(js_result)
                print(f"  Discovered page {len(discovered)}")
            
            scroll_pos += SCROLL_STEP
        
        browser.close()
    
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), "ordered_urls.txt")
    
    with open(output_path, "w") as f:
        for url in discovered:
            f.write(url + "\n")
    
    print(f"\nTotal: {len(discovered)} pages")
    print(f"Saved to: {output_path}")
    return discovered


def main():
    parser = argparse.ArgumentParser(description="Discover Studocu document pages in scroll order")
    parser.add_argument("url", help="Studocu document URL")
    parser.add_argument("--output", "-o", help="Output file path (default: system temp)")
    args = parser.parse_args()
    
    discover_pages(args.url, args.output)


if __name__ == "__main__":
    main()
