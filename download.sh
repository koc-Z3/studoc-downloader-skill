#!/bin/bash
# Download Studocu page images from ordered_urls.txt

mkdir -p /tmp/studocu_images
cd /tmp/studocu_images

while IFS= read -r url; do
  filename=$(echo "$url" | grep -oP 'bg[^?]+')
  echo "Downloading $filename..."
  curl -s --proxy socks5://127.0.0.1:9050 \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -o "$filename" "$url" &
  
  # Limit concurrent downloads
  if (( $(jobs -r -p | wc -l) >= 5 )); then
    wait -n
  fi
done < /tmp/ordered_urls.txt
wait

echo "Download complete: $(ls /tmp/studocu_images | wc -l) files"
