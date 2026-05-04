#!/usr/bin/env python3
"""Download Medium post images using undetected-chromedriver with JS fetch."""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json, os, time, base64, re

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"

# Medium posts - we need their images
medium_slugs = [
    "acesso-a-internet-como-direito-humano-basico", "algumas-coisas-para-pensar-antes-de-enviar-um-email",
    "autenticacao-de-dois-fatores", "carteiras-de-bitcoin-entenda-e-garanta-posse-de-seus-ativos",
    "dilemas-entre-react-native-e-flutter", "hackerspaces-espacos-de-tecnologia-etica-e-solidariedade",
    "mapeando-todos-os-acervos-documentais-do-mundo-com-o-archives-world-map",
    "motivos-para-acompanhar-o-movimento-indie-hackers",
    "o-direito-a-privacidade-no-hostil-ciberespaco", "os-sabores-de-linux-que-eu-ja-usei",
    "para-que-serve-o-bitcoin-pior-cenario-possivel",
    "preservacao-digital-e-nossos-documentos-pessoais",
    "se-as-redes-sociais-estao-mudando-para-onde-vamos",
    "senha-e-frase-senha-proteger-contas-plataformas",
    "um-aplicativo-movel-para-o-archives-world-map",
    "um-passo-fora-da-normalidade-semana-no-empretec",
    "vasculham-tudo-sobre-nos-recuperar-privacidade-email",
    "voce-deveria-se-voluntariar", "retrospectiva-de-textos-produzidos-1", "retrospectiva-2"
]

medium_urls = {
    "acesso-a-internet-como-direito-humano-basico": "https://medium.com/@ricsodre/acesso-%C3%A0-internet-como-direito-humano-b%C3%A1sico-5c0df4db3f3d",
    "algumas-coisas-para-pensar-antes-de-enviar-um-email": "https://medium.com/@ricsodre/algumas-coisas-para-pensar-antes-de-enviar-um-e-mail-para-pessoas-ocupadas-ou-seja-todas-d376f2ae0481",
    "autenticacao-de-dois-fatores": "https://medium.com/@ricsodre/autentica%C3%A7%C3%A3o-de-dois-fatores-um-fator-al%C3%A9m-da-senha-para-proteger-as-suas-contas-na-internet-197a3686c17d",
    "carteiras-de-bitcoin-entenda-e-garanta-posse-de-seus-ativos": "https://medium.com/@ricsodre/carteiras-de-bitcoin-entenda-e-garanta-posse-de-seus-ativos-3fdb4239c298",
    "dilemas-entre-react-native-e-flutter": "https://medium.com/@ricsodre/dilemas-de-uma-escolha-entre-react-native-e-flutter-para-desenvolvimento-de-aplicativos-android-e-9d1d4811b1",
    "hackerspaces-espacos-de-tecnologia-etica-e-solidariedade": "https://medium.com/@ricsodre/hackerspaces-espa%C3%A7os-de-tecnologia-%C3%A9tica-e-solidariedade-d136e91b1c3e",
    "mapeando-todos-os-acervos-documentais-do-mundo-com-o-archives-world-map": "https://medium.com/@ricsodre/mapeando-todos-os-acervos-documentais-do-mundo-com-o-archives-world-map-d145b0033eee",
    "motivos-para-acompanhar-o-movimento-indie-hackers": "https://medium.com/@ricsodre/motivos-pelos-quais-estou-acompanhando-atentamente-o-movimento-indie-hackers-f0bb3cd5dfcf",
    "o-direito-a-privacidade-no-hostil-ciberespaco": "https://medium.com/@ricsodre/o-direito-%C3%A0-privacidade-no-hostil-ciberespa%C3%A7o-ou-tenha-seu-cofre-digital-pessoal-e-confi%C3%A1vel-9c770d3f8099",
    "os-sabores-de-linux-que-eu-ja-usei": "https://medium.com/@ricsodre/os-sabores-de-linux-que-eu-j%C3%A1-usei-do-adolescente-curioso-ao-adulto-sem-tempo-119a8f99c76c",
    "para-que-serve-o-bitcoin-pior-cenario-possivel": "https://medium.com/@ricsodre/para-que-serve-o-bitcoin-dizem-que-%C3%A9-para-o-pior-cen%C3%A1rio-poss%C3%ADvel-ccc8a0c1442e",
    "preservacao-digital-e-nossos-documentos-pessoais": "https://medium.com/@ricsodre/preserva%C3%A7%C3%A3o-digital-e-nossos-documentos-pessoais-confiar-em-servi%C3%A7os-de-terceiros-%C3%A9-arriscado-b4b9e7a3f967",
    "se-as-redes-sociais-estao-mudando-para-onde-vamos": "https://medium.com/@ricsodre/se-as-redes-sociais-est%C3%A3o-mudando-para-onde-todos-n%C3%B3s-estamos-indo-1390b8fb49dc",
    "senha-e-frase-senha-proteger-contas-plataformas": "https://medium.com/@ricsodre/senha-e-frase-senha-dois-dedos-de-prosa-sobre-como-proteger-melhor-suas-contas-em-plataformas-60b56ed7987b",
    "um-aplicativo-movel-para-o-archives-world-map": "https://medium.com/@ricsodre/um-aplicativo-m%C3%B3vel-para-o-archives-world-map-planos-para-logo-quando-for-poss%C3%ADvel-93dab9522a34",
    "um-passo-fora-da-normalidade-semana-no-empretec": "https://medium.com/@ricsodre/um-passo-fora-da-normalidade-ou-uma-semana-no-semin%C3%A1rio-empretec-c06800b23a20",
    "vasculham-tudo-sobre-nos-recuperar-privacidade-email": "https://medium.com/@ricsodre/vasculham-tudo-sobre-n%C3%B3s-%C3%A9-hora-de-recuperar-a-privacidade-de-nossos-e-mails-2956ac0cfe1a",
    "voce-deveria-se-voluntariar": "https://medium.com/@ricsodre/voc%C3%AA-deveria-se-voluntariar-e-tornar-seu-entorno-um-lugar-melhor-55baca3d0102",
    "retrospectiva-de-textos-produzidos-1": "https://medium.com/@ricsodre/retrospectiva-de-textos-produzidos-1-8-textos-em-7-dias-9a88ed8e28da",
    "retrospectiva-2": "https://medium.com/@ricsodre/retrospectiva-2-a-meta-dos-30-textos-em-30-dias-e-um-balanco-da-semana-2-aee9acbb4e41",
}

# Only download images for posts that don't already have a valid image
to_process = []
for slug in medium_slugs:
    has_img = False
    for ext in ['jpg', 'png', 'webp']:
        path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
        if os.path.exists(path) and os.path.getsize(path) > 1024:
            has_img = True
            break
    if not has_img and slug in medium_urls:
        to_process.append(slug)

print(f"Posts needing images: {len(to_process)}", flush=True)

if not to_process:
    print("All posts already have images!", flush=True)
    exit(0)

options = uc.ChromeOptions()
options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
driver = uc.Chrome(options=options, version_main=147)
driver.set_page_load_timeout(45)

downloaded = 0
failed = 0

try:
    for i, slug in enumerate(to_process):
        url = medium_urls[slug]
        print(f"\n[{i+1}/{len(to_process)}] {slug}", flush=True)
        try:
            driver.get(url)
            time.sleep(8)
            
            # Wait for CF
            for _ in range(5):
                if 'Just a moment' not in driver.title:
                    break
                time.sleep(2)
            
            # Find hero/featured image
            img_url = ""
            for sel in ['img[width="720"]', 'article img', 'figure img', 'img[src*="miro.medium"]']:
                try:
                    imgs = driver.find_elements(By.CSS_SELECTOR, sel)
                    for img in imgs:
                        src = img.get_attribute("src") or ""
                        if 'miro.medium' in src or 'cdn-images' in src:
                            if 'profile' not in src.lower() and 'avatar' not in src.lower():
                                img_url = src
                                break
                    if img_url:
                        break
                except:
                    pass
            
            if not img_url:
                print(f"  ⚠️ No image found", flush=True)
                failed += 1
                continue
            
            # Download via JS fetch
            ext = "jpg"
            if ".png" in img_url.lower(): ext = "png"
            elif ".webp" in img_url.lower(): ext = "webp"
            
            result = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            fetch(arguments[0], {mode: 'cors', credentials: 'include'})
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
                    img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
                    with open(img_path, 'wb') as fh:
                        fh.write(img_bytes)
                    downloaded += 1
                    print(f"  ✅ {slug}.{ext}: {len(img_bytes):,} bytes", flush=True)
                else:
                    failed += 1
                    print(f"  ❌ Too small ({len(img_bytes)}b)", flush=True)
            else:
                failed += 1
                print(f"  ❌ JS fetch failed", flush=True)
            
        except Exception as e:
            failed += 1
            print(f"  ❌ {str(e)[:60]}", flush=True)
        
        time.sleep(3)

finally:
    driver.quit()

print(f"\nDownloaded: {downloaded} | Failed: {failed}", flush=True)