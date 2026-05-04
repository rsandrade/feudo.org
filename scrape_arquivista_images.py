#!/usr/bin/env python3
"""Download cover images from arquivista.net using undetected-chromedriver.
Slow mode: ~15s pause between each request.
Run: xvfb-run --auto-servernum python3 -u scrape_arquivista_images.py
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json, os, time, base64, re

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"

# Correct URLs from scrape_complete.json
posts = [
    ("aprovacao-concurso-ufba", "https://ricardo.arquivista.net/2009/08/15/aprovacao-no-concurso-da-ufba/"),
    ("aula-calouros-arquivologia", "https://ricardo.arquivista.net/2009/04/27/aula-para-turma-de-calouros-do-curso-noturno-de-arquivologia-da-ufba/"),
    ("bases-dados-arquivisticas-web", "https://ricardo.arquivista.net/2008/06/05/disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web/"),
    ("catalogo-lindembergue-cardoso", "https://ricardo.arquivista.net/2010/04/24/catalogo-web-do-compositor-lindembergue-cardoso/"),
    ("concurso-monografias-bahia", "https://ricardo.arquivista.net/2008/06/20/resultado-do-concurso-de-monografias-de-arquivologia-da-bahia/"),
    ("curso-ontologia-8-horas", "https://ricardo.arquivista.net/2009/04/06/curso-de-ontologia-em-8-horas/"),
    ("defesa-dissertacao", "https://ricardo.arquivista.net/2010/05/08/defesa-de-dissertacao-realizada-mais-um-passo-dado/"),
    ("descricao-arquivistica-web", "https://ricardo.arquivista.net/2008/04/12/descricao-arquivistica-na-web-os-pontos-importantes-da-questao/"),
    ("descricao-arquivistica-web2", "https://ricardo.arquivista.net/2008/12/15/novo-texto-publicado-em-periodico-aspectos-teoricos-e-historicos-da-descricao-arquivistica-e-a-evolucao-dos-instrumentos-de-referencia-ate-a-web-20/"),
    ("dissertacao-mestrado-pdf", "https://ricardo.arquivista.net/2010/06/02/pdf-com-a-minha-dissertacao-de-mestrado/"),
    ("formas-comunicacao-blog", "https://ricardo.arquivista.net/2008/04/09/formas-de-comunicacao-pessoal-a-utilidade-desse-blog/"),
    ("gestao-aaba", "https://ricardo.arquivista.net/2009/12/20/na-gestao-da-associacao-dos-arquivistas-da-bahia/"),
    ("goiania-xv-cba", "https://ricardo.arquivista.net/2008/07/05/andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia/"),
    ("golang-raspberry-pi-3", "https://ricardo.arquivista.net/2018/06/25/configuring-golang-environment-in-your-raspberry-pi-3/"),
    ("holmes-liinc-em-revista", "https://ricardo.arquivista.net/2008/04/16/holmes-indexa-mais-um-periodico-em-ci-liinc-em-revista/"),
    ("la-fora", "https://ricardo.arquivista.net/2011/01/25/la-fora/"),
    ("manipulando-documentos-pdf", "https://ricardo.arquivista.net/2008/04/10/manipulando-documentos-pdf/"),
    ("milhagens-eventos-arquivologia", "https://ricardo.arquivista.net/2008/04/22/usando-milhagens-para-ir-aos-eventos-de-arquivologia/"),
    ("order-of-archivists-on-sale", "https://ricardo.arquivista.net/2015/10/14/the-order-of-archivists-is-on-sale/"),
    ("premiacao-prppg-fapex", "https://ricardo.arquivista.net/2008/11/27/mais-sobre-a-premiacao-prppgufba-e-fapex/"),
    ("primeiro-dia-aula-professor", "https://ricardo.arquivista.net/2008/09/29/primeiro-dia-de-aula/"),
    ("primeiros-dias-ufba", "https://ricardo.arquivista.net/2010/02/12/primeiros-dias-de-trabalho-na-ufba/"),
    ("producao-pesquisa-premiada", "https://ricardo.arquivista.net/2008/11/27/mais-sobre-a-premiacao-prppgufba-e-fapex/"),
    ("rio-de-janeiro-iii-cna", "https://ricardo.arquivista.net/2008/10/24/o-rio-de-janeiro-continua-lindo-minhas-impressoes-do-iii-cna-e-da-cidade/"),
    ("saindo-arquivo-publico-bahia", "https://ricardo.arquivista.net/2009/10/15/saindo-do-arquivo-publico-da-bahia/"),
    ("teste-personalidade-inteligencia", "https://ricardo.arquivista.net/2008/05/04/teste-online-para-mensurar-a-multipla-inteligencia/"),
    ("yndexa-dms", "https://ricardo.arquivista.net/2009/03/05/yndexa-dms-sistema-web-para-gestao-de-documentos/"),
]

# Skip posts that already have images
to_process = []
for slug, url in posts:
    has_img = False
    for ext in ['jpg', 'png', 'webp', 'gif']:
        path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
        if os.path.exists(path) and os.path.getsize(path) > 1024:
            has_img = True
            break
    if not has_img:
        to_process.append((slug, url))

print(f"Posts to process: {len(to_process)}/{len(posts)}", flush=True)

if not to_process:
    print("All images already downloaded!", flush=True)
    exit(0)

options = uc.ChromeOptions()
options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
driver = uc.Chrome(options=options, version_main=147)
driver.set_page_load_timeout(60)

downloaded = 0
failed = 0
results = []

try:
    for i, (slug, url) in enumerate(to_process):
        print(f"\n[{i+1}/{len(to_process)}] {slug}", flush=True)

        try:
            driver.get(url)
            time.sleep(10)

            # Wait for CF
            for _ in range(8):
                if 'Just a moment' not in driver.title:
                    break
                time.sleep(3)

            page_title = driver.title
            print(f"  Title: {page_title[:60]}", flush=True)

            # Check if page loaded (not 404)
            if 'não encontrada' in page_title.lower() or 'not found' in page_title.lower():
                print(f"  ⚠️ 404 page", flush=True)
                failed += 1
                results.append({"slug": slug, "status": "404"})
                time.sleep(15)
                continue

            # Find featured/hero image - try multiple strategies
            img_url = ""

            # Strategy 1: og:image meta tag (most reliable for WP)
            try:
                og_imgs = driver.find_elements(By.CSS_SELECTOR, 'meta[property="og:image"]')
                for og in og_imgs:
                    content = og.get_attribute("content") or ""
                    if content.startswith('http') and 'emoji' not in content and 'avatar' not in content.lower():
                        img_url = content
                        break
            except:
                pass

            # Strategy 2: WP featured image selectors
            if not img_url:
                for sel in ['img.wp-post-image', 'img.attachment-post-thumbnail',
                            '.featured-image img', '.post-thumbnail img',
                            'article img:first-of-type', '.entry-content img:first-of-type',
                            'figure img']:
                    try:
                        imgs = driver.find_elements(By.CSS_SELECTOR, sel)
                        for img in imgs:
                            src = img.get_attribute("src") or ""
                            if not src or 'emoji' in src or 'avatar' in src.lower() or 'gravatar' in src.lower():
                                continue
                            if src.startswith('http'):
                                img_url = src
                                break
                    except:
                        pass
                    if img_url:
                        break

            # Strategy 3: any large image in content
            if not img_url:
                try:
                    imgs = driver.find_elements(By.CSS_SELECTOR, '.entry-content img, article img')
                    for img in imgs:
                        src = img.get_attribute("src") or ""
                        w = img.get_attribute("width") or "0"
                        if src.startswith('http') and 'emoji' not in src and 'avatar' not in src.lower() and 'gravatar' not in src.lower():
                            img_url = src
                            break
                except:
                    pass

            if not img_url:
                print(f"  ⚠️ No image found", flush=True)
                failed += 1
                results.append({"slug": slug, "status": "no_image"})
                time.sleep(15)
                continue

            # Try higher resolution version (remove WP size suffix)
            img_url_hires = re.sub(r'-\d+x\d+\.', '.', img_url)

            # Download via JS fetch
            target_url = img_url_hires if img_url_hires != img_url else img_url
            print(f"  Trying: {target_url[:80]}...", flush=True)

            result = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            fetch(arguments[0], {mode: 'cors', credentials: 'include'})
                .then(function(r) {
                    if (!r.ok) { callback({ok: false, status: r.status}); return; }
                    return r.blob();
                })
                .then(function(blob) {
                    if (!blob || typeof blob === 'object' && blob.ok === false) {
                        callback(typeof blob === 'object' ? blob : {ok: false});
                        return;
                    }
                    var reader = new FileReader();
                    reader.onloadend = function() { callback({ok: true, data: reader.result}); };
                    reader.onerror = function() { callback({ok: false}); };
                    reader.readAsDataURL(blob);
                })
                .catch(function(e) { callback({ok: false, error: e.message}); });
            """, target_url)

            if not result or not result.get('ok'):
                # Try original URL if hires failed
                if target_url != img_url:
                    print(f"  Hires failed, trying original...", flush=True)
                    result = driver.execute_async_script("""
                    var callback = arguments[arguments.length - 1];
                    fetch(arguments[0], {mode: 'cors', credentials: 'include'})
                        .then(function(r) {
                            if (!r.ok) { callback({ok: false, status: r.status}); return; }
                            return r.blob();
                        })
                        .then(function(blob) {
                            if (!blob || typeof blob === 'object' && blob.ok === false) {
                                callback(typeof blob === 'object' ? blob : {ok: false});
                                return;
                            }
                            var reader = new FileReader();
                            reader.onloadend = function() { callback({ok: true, data: reader.result}); };
                            reader.onerror = function() { callback({ok: false}); };
                            reader.readAsDataURL(blob);
                        })
                        .catch(function(e) { callback({ok: false, error: e.message}); });
                    """, img_url)

            if result and result.get('ok') and result.get('data', '').startswith('data:'):
                data_url = result['data']
                _, b64data = data_url.split(',', 1)
                img_bytes = base64.b64decode(b64data)
                if len(img_bytes) > 500:
                    ext = "jpg"
                    mime = data_url.split(':')[1].split(';')[0]
                    if 'png' in mime: ext = "png"
                    elif 'webp' in mime: ext = "webp"
                    elif 'gif' in mime: ext = "gif"

                    img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
                    with open(img_path, 'wb') as fh:
                        fh.write(img_bytes)
                    downloaded += 1
                    print(f"  ✅ {slug}.{ext}: {len(img_bytes):,} bytes", flush=True)
                    results.append({"slug": slug, "status": "ok", "size": len(img_bytes), "ext": ext})
                else:
                    failed += 1
                    print(f"  ❌ Too small ({len(img_bytes)}b)", flush=True)
                    results.append({"slug": slug, "status": "too_small"})
            else:
                failed += 1
                err_info = result if result else "None"
                print(f"  ❌ Download failed: {err_info}", flush=True)
                results.append({"slug": slug, "status": "fetch_failed", "detail": str(err_info)[:100]})

        except Exception as e:
            failed += 1
            print(f"  ❌ Error: {str(e)[:80]}", flush=True)
            results.append({"slug": slug, "status": "error", "error": str(e)[:100]})

        # ~15s pause between requests
        pause = 15 + (i % 3) * 3
        print(f"  ⏳ Pausing {pause}s...", flush=True)
        time.sleep(pause)

finally:
    driver.quit()

with open('/tmp/arquivista_images_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n=== DONE ===", flush=True)
print(f"Downloaded: {downloaded} | Failed: {failed}", flush=True)