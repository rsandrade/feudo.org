#!/usr/bin/env python3
"""
Scrape ricardo.arquivista.net posts using undetected-chromedriver + xvfb-run.
Bypasses Cloudflare JS Challenge.
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, time, os, re, sys

OUTPUT_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Map of qmd-slug -> WordPress URL
POST_MAP = {
    "a-ordem-dos-arquivistas-centesimo-blog": "https://ricardo.arquivista.net/a-ordem-dos-arquivistas-centesimo/",
    "aprovacao-concurso-ufba": "https://ricardo.arquivista.net/aprovacao-no-concurso-da-ufba/",
    "aula-calouros-arquivologia": "https://ricardo.arquivista.net/aula-para-turma-de-calouros-do-curso-de-arquivologia-da-ufba/",
    "aws-glacier-copias-seguranca": "https://ricardo.arquivista.net/amazon-aws-glacier-alternativa-em-nuvem-para-copias-de-seguranca/",
    "bases-dados-arquivisticas-web": "https://ricardo.arquivista.net/disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web/",
    "blockchain-criptomoedas-aplicacoes": "https://ricardo.arquivista.net/sobre-blockchain-criptomoedas-e-outras-aplicacoes-o-basico-de-detalhes-avancados/",
    "carteira-de-papel-bitcoin": "https://ricardo.arquivista.net/como-criar-sua-carteira-de-papel-para-guardar-seus-bitcoins/",
    "catalogo-lindembergue-cardoso": "https://ricardo.arquivista.net/catalogo-web-do-compositor-lindembergue-cardoso/",
    "concurso-monografias-bahia": "https://ricardo.arquivista.net/resultado-do-concurso-de-monografias-de-arquivologia-da-bahia/",
    "curso-ontologia-8-horas": "https://ricardo.arquivista.net/curso-de-ontologia-em-8-horas/",
    "defesa-dissertacao": "https://ricardo.arquivista.net/defesa-de-dissertacao-realizada-mais-um-passo-dado/",
    "descricao-arquivistica-web": "https://ricardo.arquivista.net/descricao-arquivistica-na-web-o-que-ha-de-vir/",
    "descricao-arquivistica-web2": "https://ricardo.arquivista.net/novo-texto-publicado-em-periodico-trata-de-aspectos-teoricos-e-historicos-da-descricao-arquivistica/",
    "dissertacao-mestrado-pdf": "https://ricardo.arquivista.net/pdf-com-a-minha-dissertacao-de-mestrado/",
    "em-terras-portuguesas": "https://ricardo.arquivista.net/em-terras-portuguesas/",
    "formas-comunicacao-blog": "https://ricardo.arquivista.net/formas-de-comunicacao-pessoal-a-utilidade-desse-blog/",
    "gestao-aaba": "https://ricardo.arquivista.net/na-gestao-da-associacao-dos-arquivistas-da-bahia/",
    "goiania-xv-cba": "https://ricardo.arquivista.net/andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia/",
    "golang-raspberry-pi-3": "https://ricardo.arquivista.net/configuring-golang-environment-in-your-raspberry-pi-3/",
    "habilidades-antes-dos-18": "https://ricardo.arquivista.net/todo-mundo-deveria-desenvolver-essas-habilidades-antes-dos-18-anos/",
    "holmes-liinc-em-revista": "https://ricardo.arquivista.net/holmes-indexa-mais-um-periodico-em-ci-liinc-em-revista/",
    "iii-cna-fotos": "https://ricardo.arquivista.net/iii-congresso-nacional-de-arquivologia-algumas-poucas-fotos/",
    "ingress": "https://ricardo.arquivista.net/ingress/",
    "la-fora": "https://ricardo.arquivista.net/la-fora/",
    "lusofonia-instituicoes-arquivisticas": "https://ricardo.arquivista.net/lusofonia-como-espaco-cooperativo-entre-instituicoes-arquivisticas/",
    "manipulando-documentos-pdf": "https://ricardo.arquivista.net/manipulando-documentos-pdf/",
    "materiais-aulas-arquivologia": "https://ricardo.arquivista.net/materiais-das-aulas-curso-de-arquivologia-noturno/",
    "milhagens-eventos-arquivologia": "https://ricardo.arquivista.net/usando-milhagens-para-ir-aos-eventos-de-arquivologia/",
    "order-of-archivists-on-sale": "https://ricardo.arquivista.net/the-order-of-archivists-is-on-sale/",
    "premiacao-prppg-fapex": "https://ricardo.arquivista.net/mais-sobre-a-premiacao-prppgufba-e-fapex/",
    "primeiro-dia-aula-professor": "https://ricardo.arquivista.net/primeiro-dia-de-aula-de-um-novo-professor/",
    "primeiros-dias-ufba": "https://ricardo.arquivista.net/primeiros-dias-de-trabalho-na-ufba/",
    "producao-pesquisa-premiada": "https://ricardo.arquivista.net/producao-de-pesquisa-premiada-pela-prppgufba-e-fapex/",
    "programando-o-doutorado": "https://ricardo.arquivista.net/programando-o-doutorado/",
    "radioamadorismo": "https://ricardo.arquivista.net/radioamadorismo/",
    "representacao-informacao-computacao-cognitiva": "https://ricardo.arquivista.net/representacao-da-informacao-e-computacao-cognitiva/",
    "rio-de-janeiro-iii-cna": "https://ricardo.arquivista.net/o-rio-de-janeiro-continua-lindo-minhas-impressoes-do-iii-cna-e-da-cidade/",
    "saindo-arquivo-publico-bahia": "https://ricardo.arquivista.net/saindo-do-arquivo-publico-da-bahia/",
    "teste-personalidade-inteligencia": "https://ricardo.arquivista.net/teste-online-para-mensurar-a-personalidade-e-a-multipla-inteligencia/",
    "yndexa-dms": "https://ricardo.arquivista.net/yndexa-dms-sistema-web-para-gestao-de-documentos/",
}

def setup_driver():
    options = uc.ChromeOptions()
    options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # Do NOT add --headless — Cloudflare detects it
    driver = uc.Chrome(options=options, version_main=147)
    driver.set_page_load_timeout(30)
    return driver

def bypass_cloudflare(driver, url, max_wait=20):
    """Navigate to URL and wait for Cloudflare challenge to resolve."""
    driver.get(url)
    for i in range(max_wait // 2):
        time.sleep(2)
        title = driver.title
        if 'Just a moment' not in title and title.strip():
            return True
    return False

def extract_post_content(driver, slug, url):
    """Extract full text content and hero image URL from a WordPress post."""
    result = {"slug": slug, "url": url, "text": "", "image": ""}
    
    try:
        # Get main content
        content_el = driver.find_element(By.CSS_SELECTOR, ".entry-content, .post-content, article .content, .post-body, main .entry")
        if not content_el:
            content_el = driver.find_element(By.TAG_NAME, "article")
        if not content_el:
            content_el = driver.find_element(By.TAG_NAME, "body")
        
        result["text"] = content_el.text.strip()
    except:
        # Fallback to body
        try:
            result["text"] = driver.find_element(By.TAG_NAME, "body").text.strip()
        except:
            pass
    
    # Get all images with wp-content/uploads in src (WordPress media)
    try:
        imgs = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in imgs:
            src = img.get_attribute("src") or ""
            w = img.get_attribute("width") or "0"
            cls = img.get_attribute("class") or ""
            # Skip avatars, icons, logos
            if any(skip in src.lower() for skip in ["gravatar", "avatar", "icon", "logo", "emoji", "wpemoji", "comment"]):
                continue
            if any(skip in cls.lower() for skip in ["avatar", "icon", "logo", "emoji", "widget"]):
                continue
            # Prefer WordPress uploads (original content images)
            if "wp-content/uploads" in src or "wp-content" in src:
                result["image"] = src
                break
            # Also accept other large images that aren't UI elements
            if src and src.startswith("http") and not result["image"]:
                result["image"] = src
    except:
        pass
    
    return result

def main():
    # Skip already-downloaded slugs
    already_done = set()
    json_path = os.path.join(IMAGES_DIR, "scrape_results.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            existing = json.load(f)
        for item in existing:
            already_done.add(item["slug"])
    
    slugs_to_process = [s for s in POST_MAP if s not in already_done]
    
    if not slugs_to_process:
        print("All posts already scraped!")
        return
    
    print(f"Scraping {len(slugs_to_process)} posts from ricardo.arquivista.net...")
    
    driver = setup_driver()
    results = []
    
    try:
        for i, slug in enumerate(slugs_to_process):
            url = POST_MAP[slug]
            print(f"\n[{i+1}/{len(slugs_to_process)}] {slug}")
            print(f"  URL: {url}")
            
            try:
                success = bypass_cloudflare(driver, url)
                if not success:
                    print("  ❌ Cloudflare challenge not resolved")
                    results.append({"slug": slug, "url": url, "text": "", "image": "", "status": "cloudflare_failed"})
                    continue
                
                # Wait for content to load
                time.sleep(2)
                
                result = extract_post_content(driver, slug, url)
                result["status"] = "ok"
                
                # Download image if found
                if result["image"]:
                    img_url = result["image"]
                    # Determine extension
                    ext = "jpg"
                    if ".png" in img_url.lower():
                        ext = "png"
                    elif ".webp" in img_url.lower():
                        ext = "webp"
                    # Remove query params
                    img_url_clean = img_url.split("?")[0]
                    
                    img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
                    # Use driver to get cookies for image download too
                    import subprocess
                    dl_result = subprocess.run(
                        ["wget", "-q", "-O", img_path, img_url_clean],
                        capture_output=True, text=True, timeout=15
                    )
                    if dl_result.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                        print(f"  ✅ Image downloaded: {slug}.{ext}")
                    else:
                        # Try with full URL
                        dl_result2 = subprocess.run(
                            ["wget", "-q", "-O", img_path, img_url],
                            capture_output=True, text=True, timeout=15
                        )
                        if dl_result2.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                            print(f"  ✅ Image downloaded (full URL): {slug}.{ext}")
                        else:
                            print(f"  ⚠️ Image download failed: {img_url[:80]}")
                            result["image"] = ""
                
                text_len = len(result.get("text", ""))
                print(f"  ✅ Text extracted: {text_len} chars")
                results.append(result)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                results.append({"slug": slug, "url": url, "text": "", "image": "", "status": f"error: {e}"})
            
            # Be polite
            time.sleep(3)
    
    finally:
        driver.quit()
    
    # Save results
    # Load existing if any
    all_results = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            all_results = json.load(f)
    
    # Merge
    existing_slugs = {r["slug"] for r in all_results}
    for r in results:
        if r["slug"] not in existing_slugs:
            all_results.append(r)
        else:
            # Update
            for i, er in enumerate(all_results):
                if er["slug"] == r["slug"]:
                    all_results[i] = r
                    break
    
    with open(json_path, "w") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    ok_count = sum(1 for r in results if r.get("status") == "ok")
    print(f"\n=== DONE: {ok_count}/{len(results)} posts scraped successfully ===")
    print(f"Results saved to {json_path}")

if __name__ == "__main__":
    main()