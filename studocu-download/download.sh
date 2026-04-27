#!/bin/bash
# Download Studocu page images from ordered_urls.txt
#
# Usage:
#   bash download.sh                    # Uses /tmp/ordered_urls.txt
#   bash download.sh /path/to/urls.txt  # Custom urls file
#   bash download.sh /path/to/urls.txt /output/dir  # Custom urls + output dir
#
# Requirements:
#   - Tor running on localhost:9050 (or configure PROXY below)
#   - curl installed

# === CONFIGURATION ===
PROXY="socks5://127.0.0.1:9050"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
MAX_CONCURRENT=5
# ====================

URLS_FILE="${1:-/tmp/ordered_urls.txt}"
OUTPUT_DIR="${2:-/tmp/studocu_images}"

if [ ! -f "$URLS_FILE" ]; then
    echo "Error: URL file not found: $URLS_FILE"
    echo "Run discover.py first to generate it."
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR" || exit 1

echo "Reading URLs from: $URLS_FILE"
echo "Output directory: $OUTPUT_DIR"
echo ""

count=0
total=$(wc -l < "$URLS_FILE")

while IFS= read -r url; do
    count=$((count + 1))
    filename=$(echo "$url" | grep -oP 'bg[^?]+')
    echo "[$count/$total] Downloading $filename..."
    
    curl -s --proxy "$PROXY" \
         -A "$USER_AGENT" \
         -o "$filename" \
         "$url" &
    
    if (( $(jobs -r -p | wc -l) >= MAX_CONCURRENT )); then
        wait -n
    fi
done < "$URLS_FILE"

wait

echo ""
echo "Download complete: $(ls | wc -l) files in $OUTPUT_DIR"
