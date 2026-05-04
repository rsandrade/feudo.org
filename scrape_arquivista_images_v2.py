#!/usr/bin/env python3
"""Second pass: find ANY image in post body (inline images), not just featured.
Also retries formas-comunicacao-blog.
Run: xvfb-run --auto-servernum python3 -u scrape_arquivista_images_v2.py
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json, os, time, base64, re

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"

# Posts that had no featured image - look for inline images instead
posts = [
    ("aprovacao-concurso-ufba", "https://ricardo.arquivista.net/2009/08/15/aprovacao-no-concurso-da-ufba/"),
    ("aula-calouros-arquivologia", "https://ricardo.arquivista.net/2009/04/27/aula-para-turma-de-calouros-do-curso-noturno-de-arquivologia-da-ufba/"),
    ("bases-dados-arquivisticas-web", "https://ricardo.arquivista.net/2008/06/05/disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web/"),
    ("catalogo-lindembergue-cardoso", "https://ricardo.arquivista.net/2010/04/24/catalogo-web-do-compositor-lindembergue-cardoso/"),
    ("concurso-monografias-bahia", "https://ricardo.arquivista.net/2008/06/20/resultado-do-concurso-de-monografias-de-arquivologia-da-bahia/"),
    ("curso-ontologia-8-horas", "https://ricardo.arquivista.net/2009/04/06/curso-de-ontologia-em-8-horas/"),
    ("defesa-dissertacao", "https://ricardo.arquivista.net/2010/05/08/defesa-de-dissertacao-realizada-mais-um-passo-dado/"),
    ("descricao-arquivistica-web2", "https://ricardo.arquivista.net/2008/12/15/novo-texto-publicado-em-periodico-aspectos-teoricos-e-historicos-da-descricao-arquivistica-e-a-evolucao-dos-instrumentos-de-referencia-ate-a-web-20/"),
    ("dissertacao-mestrado-pdf", "https://ricardo.arquivista.net/2010/06/02/pdf-com-a-minha-dissertacao-de-mestrado/"),
    ("formas-comunicacao-blog", "https://ricardo.arquivista.net/2008/04/09/formas-de-comunicacao-pessoal-a-utilidade-desse-blog/"),
    ("gestao-aaba", "https://ricardo.arquivista.net/2009/12/20/na-gestao-da-associacao-dos-arquivistas-da-bahia/"),
    ("goiania-xv-cba", "https://ricardo.arquivista.net/2008/07/05/andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia/"),
    ("holmes-liinc-em-revista", "https://ricardo.arquivista.net/2008/04/16/holmes-indexa-mais-um-periodico-em-ci-liinc-em-revista/"),
    ("la-fora", "https://ricardo.arquivista.net/2011/01/25/la-fora/"),
    ("manipulando-documentos-pdf", "https://ricardo.arquivista.net/2008/04/10/manipulando-documentos-pdf/"),
    ("milhagens-eventos-arquivologia", "https://ricardo.arquivista.net/2008/04/22/usando-milhagens-para-ir-aos-eventos-de-arquivologia/"),
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

print(f"Still need images: {len(to_process)}/{len(posts)}", flush=True)

if not to_process:
    print("All images downloaded!", flush=True)
    exit(0)

options = uc.ChromeOptions()
options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
driver = uc.Chrome(options=options, version_main=147)
driver.set_page_load_timeout(60)

downloaded = 0
no_img = 0
failed = 0
results = []

try:
    for i, (slug, url) in enumerate(to_process):
        print(f"\n[{i+1}/{len(to_process)}] {slug}", flush=True)

        try:
            driver.get(url)
            time.sleep(10)

            for _ in range(8):
                if 'Just a moment' not in driver.title:
                    break
                time.sleep(3)

            page_title = driver.title
            print(f"  Title: {page_title[:50]}", flush=True)

            # Strategy 1: og:image
            img_url = ""
            try:
                og_imgs = driver.find_elements(By.CSS_SELECTOR, 'meta[property="og:image"]')
                for og in og_imgs:
                    content = og.get_attribute("content") or ""
                    if content.startswith('http') and 'emoji' not in content and 'avatar' not in content.lower():
                        img_url = content
                        break
            except:
                pass

            # Strategy 2: ALL images in page (not just featured)
            if not img_url:
                try:
                    all_imgs = driver.find_elements(By.CSS_SELECTOR, 'img')
                    for img in all_imgs:
                        src = img.get_attribute("src") or ""
                        w = img.get_attribute("width") or "0"
                        h = img.get_attribute("height") or "0"
                        # Skip tiny, emoji, avatar, gravatar, logo, icon
                        skip_words = ['emoji', 'avatar', 'gravatar', 'icon', 'logo', 'banner', 'pixel', 'spacer', 'cloudflare', 'turnstile', 'badge']
                        if any(sw in src.lower() for sw in skip_words):
                            continue
                        if not src.startswith('http'):
                            continue
                        # Skip very small images (likely icons/spacers)
                        try:
                            if int(w) > 0 and int(w) < 50:
                                continue
                            if int(h) > 0 and int(h) < 50:
                                continue
                        except:
                            pass
                        img_url = src
                        break
                except:
                    pass

            if not img_url:
                no_img += 1
                print(f"  ⚠️ No image at all", flush=True)
                results.append({"slug": slug, "status": "no_image"})
                time.sleep(12)
                continue

            # Remove WP size suffix for higher res
            img_url_hires = re.sub(r'-\d+x\d+\.', '.', img_url)

            # Download
            target_url = img_url_hires
            print(f"  Trying: {target_url[:80]}...", flush=True)

            result = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            fetch(arguments[0], {mode: 'cors', credentials: 'include'})
                .then(function(r) {
                    if (!r.ok) { callback({ok: false, status: r.status}); return; }
                    return r.blob();
                })
                .then(function(blob) {
                    if (!blob || (typeof blob === 'object' && blob.ok === false)) {
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

            # Fall back to original URL if hires failed
            if not result or not result.get('ok'):
                if target_url != img_url:
                    print(f"  Hires failed, trying original URL...", flush=True)
                    result = driver.execute_async_script("""
                    var callback = arguments[arguments.length - 1];
                    fetch(arguments[0], {mode: 'cors', credentials: 'include'})
                        .then(function(r) {
                            if (!r.ok) { callback({ok: false, status: r.status}); return; }
                            return r.blob();
                        })
                        .then(function(blob) {
                            if (!blob || (typeof blob === 'object' && blob.ok === false)) {
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
                print(f"  ❌ Fetch failed: {result}", flush=True)
                results.append({"slug": slug, "status": "fetch_failed"})

        except Exception as e:
            failed += 1
            print(f"  ❌ Error: {str(e)[:60]}", flush=True)
            results.append({"slug": slug, "status": "error"})

        pause = 15 + (i % 3) * 4
        print(f"  ⏳ {pause}s pause", flush=True)
        time.sleep(pause)

finally:
    driver.quit()

with open('/tmp/arquivista_images_v2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n=== DONE ===", flush=True)
print(f"Downloaded: {downloaded} | No image: {no_img} | Failed: {failed}", flush=True)