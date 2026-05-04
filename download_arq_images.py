#!/usr/bin/env python3
"""Download images from arquivista.net by injecting JS fetch in the browser.
Must run with: xvfb-run python3 -u download_arq_images.py"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json, os, time, base64

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"
RESULTS_JSON = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images/scrape_v3_results.json"

with open(RESULTS_JSON) as f:
    data = json.load(f)

# Filter posts with image_url but no valid file
to_download = []
for r in data:
    if r.get('image_url'):
        slug = r['slug']
        img_url = r['image_url']
        ext = "jpg"
        if ".png" in img_url.lower(): ext = "png"
        elif ".webp" in img_url.lower(): ext = "webp"
        img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
        # Check if file exists and is > 1KB
        if os.path.exists(img_path) and os.path.getsize(img_path) > 1024:
            r['image'] = f"{slug}.{ext}"
            continue
        to_download.append((slug, img_url, ext, img_path, r))

print(f"Images to download: {len(to_download)}", flush=True)

if not to_download:
    print("Nothing to download!", flush=True)
    with open(RESULTS_JSON, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    exit(0)

options = uc.ChromeOptions()
options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = uc.Chrome(options=options, version_main=147)
driver.set_page_load_timeout(45)

# Establish CF session on the homepage
print("Establishing CF session...", flush=True)
driver.get("https://ricardo.arquivista.net/")
for i in range(15):
    time.sleep(2)
    if 'Just a moment' not in driver.title:
        print(f"CF bypassed: {driver.title}", flush=True)
        break
time.sleep(3)

downloaded = 0
failed = 0

try:
    for slug, img_url, ext, img_path, r in to_download:
        try:
            # Use JS fetch to download image data from within the browser (CF cookies apply)
            result = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            var url = arguments[0];
            fetch(url, {mode: 'cors', credentials: 'include'})
                .then(function(r) {
                    if (!r.ok) { callback(null); return; }
                    return r.blob();
                })
                .then(function(blob) {
                    if (!blob) { callback(null); return; }
                    var reader = new FileReader();
                    reader.onloadend = function() { callback(reader.result); };
                    reader.onerror = function() { callback(null); };
                    reader.readAsDataURL(blob);
                })
                .catch(function() { callback(null); });
            """, img_url)
            
            if result and result.startswith('data:'):
                _, b64data = result.split(',', 1)
                img_bytes = base64.b64decode(b64data)
                if len(img_bytes) > 500:
                    with open(img_path, 'wb') as f:
                        f.write(img_bytes)
                    r['image'] = f"{slug}.{ext}"
                    downloaded += 1
                    print(f"  ✅ {slug}: {len(img_bytes):,} bytes", flush=True)
                else:
                    failed += 1
                    print(f"  ❌ {slug}: too small ({len(img_bytes)}b)", flush=True)
            else:
                failed += 1
                print(f"  ❌ {slug}: no data returned", flush=True)
        except Exception as e:
            failed += 1
            print(f"  ❌ {slug}: {str(e)[:80]}", flush=True)

finally:
    driver.quit()

with open(RESULTS_JSON, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Downloaded: {downloaded} | ❌ Failed: {failed}", flush=True)