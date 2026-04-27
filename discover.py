#!/usr/bin/env python3
"""
Discover Studocu document page images in scroll order.
Run this first to collect all page URLs.
"""

import sys
import time
from playwright.sync_api import sync_playwright

STUDOCU_URL = sys.argv[1] if len(sys.argv) > 1 else 'https://www.studocu.com/en-au/document/high-school-australia/chemistry/strive-module-7-cololllllll/54267304'

def discover_pages(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy={'server': 'socks5://127.0.0.1:9050'})
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        print(f'Loading {url}...')
        page.goto(url, timeout=120000)
        time.sleep(20)  # Wait for Cloudflare
        
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
            page.evaluate(f'window.scrollTo(0, {scroll_pos})')
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
                print(f'Discovered page {len(discovered)}')
            
            scroll_pos += step
        
        with open('/tmp/ordered_urls.txt', 'w') as f:
            for url in discovered:
                f.write(url + chr(10))
        
        print(f'\nTotal: {len(discovered)} pages saved to /tmp/ordered_urls.txt')
        browser.close()

if __name__ == '__main__':
    discover_pages(STUDOCU_URL)
