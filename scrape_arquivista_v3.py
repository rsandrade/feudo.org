#!/usr/bin/env python3
"""Scrape full text + images from ricardo.arquivista.net using undetected-chromedriver.
Must run with: xvfb-run python3 -u scrape_arquivista_v3.py"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, subprocess, re, sys

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"
OUTPUT_JSON = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images/scrape_v3_results.json"
os.makedirs(IMAGES_DIR, exist_ok=True)

# Correct WordPress URLs (with /yyyy/mm/dd/ prefix)
POST_MAP = {
    "a-ordem-dos-arquivistas-centesimo-blog": "https://ricardo.arquivista.net/2012/06/25/a-ordem-dos-arquivistas-centesimo/",
    "aprovacao-concurso-ufba": "https://ricardo.arquivista.net/2009/08/15/aprovacao-no-concurso-da-ufba/",
    "aula-calouros-arquivologia": "https://ricardo.arquivista.net/2009/04/27/aula-para-turma-de-calouros-do-curso-noturno-de-arquivologia-da-ufba/",
    "aws-glacier-copias-seguranca": "https://ricardo.arquivista.net/2014/07/28/amazon-aws-glacier-alternativa-em-nuvem-para-copias-de-seguranca/",
    "bases-dados-arquivisticas-web": "https://ricardo.arquivista.net/2008/06/05/disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web/",
    "blockchain-criptomoedas-aplicacoes": "https://ricardo.arquivista.net/2017/10/16/sobre-blockchain-criptomoedas-e-outras-aplicacoes-o-basico-de-detalhes-avancados/",
    "carteira-de-papel-bitcoin": "https://ricardo.arquivista.net/2020/08/03/como-criar-sua-carteira-de-papel-para-guardar-seus-bitcoins/",
    "catalogo-lindembergue-cardoso": "https://ricardo.arquivista.net/2010/04/24/catalogo-web-do-compositor-lindembergue-cardoso/",
    "concurso-monografias-bahia": "https://ricardo.arquivista.net/2008/06/20/resultado-do-concurso-de-monografias-de-arquivologia-da-bahia/",
    "curso-ontologia-8-horas": "https://ricardo.arquivista.net/2009/04/06/curso-de-ontologia-em-8-horas/",
    "defesa-dissertacao": "https://ricardo.arquivista.net/2010/05/08/defesa-de-dissertacao-realizada-mais-um-passo-dado/",
    "descricao-arquivistica-web": "https://ricardo.arquivista.net/2008/04/12/descricao-arquivistica-na-web-os-pontos-importantes-da-questao/",
    "descricao-arquivistica-web2": "https://ricardo.arquivista.net/2008/12/15/novo-texto-publicado-em-periodico-aspectos-teoricos-e-historicos-da-descricao-arquivistica-e-a-evolucao-dos-instrumentos-de-referencia-ate-a-web-20/",
    "dissertacao-mestrado-pdf": "https://ricardo.arquivista.net/2010/06/02/pdf-com-a-minha-dissertacao-de-mestrado/",
    "em-terras-portuguesas": "https://ricardo.arquivista.net/2014/01/09/em-terras-portuguesas/",
    "formas-comunicacao-blog": "https://ricardo.arquivista.net/2008/04/09/formas-de-comunicacao-pessoal-a-utilidade-desse-blog/",
    "gestao-aaba": "https://ricardo.arquivista.net/2009/12/20/na-gestao-da-associacao-dos-arquivistas-da-bahia/",
    "goiania-xv-cba": "https://ricardo.arquivista.net/2008/07/05/andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia/",
    "golang-raspberry-pi-3": "https://ricardo.arquivista.net/2018/06/25/configuring-golang-environment-in-your-raspberry-pi-3/",
    "habilidades-antes-dos-18": "https://ricardo.arquivista.net/2016/05/04/todo-mundo-deveria-desenvolver-essas-habilidades-antes-dos-18-anos/",
    "holmes-liinc-em-revista": "https://ricardo.arquivista.net/2008/04/16/holmes-indexa-mais-um-periodico-em-ci-liinc-em-revista/",
    "iii-cna-fotos": "https://ricardo.arquivista.net/2008/11/03/iii-congresso-nacional-de-arquivologia-algumas-poucas-fotos/",
    "ingress": "https://ricardo.arquivista.net/2014/03/24/ingress/",
    "la-fora": "https://ricardo.arquivista.net/2011/01/25/la-fora/",
    "lusofonia-instituicoes-arquivisticas": "https://ricardo.arquivista.net/2014/04/10/lusofonia-como-espaco-cooperativo-entre-instituicoes-arquivisticas/",
    "manipulando-documentos-pdf": "https://ricardo.arquivista.net/2008/04/10/manipulando-documentos-pdf/",
    "materiais-aulas-arquivologia": "https://ricardo.arquivista.net/2009/05/27/materiais-das-aulas-curso-de-arquivologia-noturno/",
    "milhagens-eventos-arquivologia": "https://ricardo.arquivista.net/2008/04/22/usando-milhagens-para-ir-aos-eventos-de-arquivologia/",
    "order-of-archivists-on-sale": "https://ricardo.arquivista.net/2015/10/14/the-order-of-archivists-is-on-sale/",
    "premiacao-prppg-fapex": "https://ricardo.arquivista.net/2008/11/27/mais-sobre-a-premiacao-prppgufba-e-fapex/",
    "primeiro-dia-aula-professor": "https://ricardo.arquivista.net/2008/09/29/primeiro-dia-de-aula/",
    "primeiros-dias-ufba": "https://ricardo.arquivista.net/2010/02/12/primeiros-dias-de-trabalho-na-ufba/",
    "producao-pesquisa-premiada": "https://ricardo.arquivista.net/2008/11/27/mais-sobre-a-premiacao-prppgufba-e-fapex/",
    "programando-o-doutorado": "https://ricardo.arquivista.net/2011/01/23/programando-o-doutorado/",
    "radioamadorismo": "https://ricardo.arquivista.net/2013/04/21/radioamadorismo/",
    "representacao-informacao-computacao-cognitiva": "https://ricardo.arquivista.net/2014/01/11/representacao-da-informacao-e-computacao-cognitiva/",
    "rio-de-janeiro-iii-cna": "https://ricardo.arquivista.net/2008/10/24/o-rio-de-janeiro-continua-lindo-minhas-impressoes-do-iii-cna-e-da-cidade/",
    "saindo-arquivo-publico-bahia": "https://ricardo.arquivista.net/2009/10/15/saindo-do-arquivo-publico-da-bahia/",
    "teste-personalidade-inteligencia": "https://ricardo.arquivista.net/2008/05/04/teste-online-para-mensurar-a-multipla-inteligencia/",
    "yndexa-dms": "https://ricardo.arquivista.net/2009/03/05/yndexa-dms-sistema-web-para-gestao-de-documentos/",
}

def html_to_markdown(text):
    """Basic cleanup of extracted text."""
    # Remove common WordPress cruft
    lines = text.split('\n')
    clean = []
    skip_patterns = ['Pular para o conteúdo', 'Pesquisar', 'ABOUT ME', 'CONTATO', 
                     'CURRÍCULO', 'PERFIL', 'PRODUÇÃO', 'VISITED ARCHIVES',
                     'Arhivele Naţionale', 'Arquivo de Galicia', 'Deixe um comentário',
                     'DEIXE UM COMENTÁRIO', 'Continue lendo', 'Pesquisar por:']
    for line in lines:
        s = line.strip()
        if not s:
            clean.append('')
            continue
        if any(p in s for p in skip_patterns):
            continue
        clean.append(s)
    return '\n'.join(clean).strip()


def main():
    print("Starting Chrome (non-headless, via xvfb)...", flush=True)
    options = uc.ChromeOptions()
    options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options, version_main=147)
    driver.set_page_load_timeout(45)

    # First visit homepage to establish CF session
    print("Visiting homepage to establish CF session...", flush=True)
    driver.get("https://ricardo.arquivista.net/")
    for i in range(20):
        time.sleep(2)
        if 'Just a moment' not in driver.title:
            print(f"Homepage loaded: {driver.title}", flush=True)
            break
    time.sleep(3)

    results = []
    ok = 0
    no_content = 0

    try:
        for i, (slug, url) in enumerate(POST_MAP.items()):
            print(f"\n[{i+1}/{len(POST_MAP)}] {slug}", flush=True)
            print(f"  URL: {url}", flush=True)
            try:
                driver.get(url)
                
                # Wait for Cloudflare
                bypassed = False
                for attempt in range(15):
                    time.sleep(2)
                    title = driver.title
                    if 'Just a moment' not in title and title.strip():
                        bypassed = True
                        break
                
                if not bypassed:
                    print(f"  ❌ CF not bypassed", flush=True)
                    results.append({"slug": slug, "status": "cf_blocked", "text": "", "image": ""})
                    continue
                
                time.sleep(2)  # extra for JS render
                
                # Check for 404
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if 'Não encontrado' in body_text or 'nada foi encontrado' in body_text.lower():
                    print(f"  ❌ 404 page", flush=True)
                    results.append({"slug": slug, "status": "404", "text": "", "image": ""})
                    continue
                
                # Check for password protected
                if 'protegido por senha' in body_text.lower() or 'password protected' in body_text.lower():
                    print(f"  ⚠️ Password protected", flush=True)
                    results.append({"slug": slug, "status": "password_protected", "text": "", "image": ""})
                    continue
                
                # Extract post content with multiple selectors
                content = ""
                for sel in ['.entry-content', '.post-content', '.wp-block-post-content', 'article .entry-content', 'article']:
                    try:
                        el = driver.find_element(By.CSS_SELECTOR, sel)
                        content = el.text.strip()
                        if len(content) > 100:
                            break
                    except:
                        continue
                
                if not content or len(content) < 50:
                    print(f"  ⚠️ Short content ({len(content)}c)", flush=True)
                    no_content += 1
                
                content = html_to_markdown(content)
                
                # Extract hero/featured image
                hero_img = ""
                try:
                    # Try featured image first
                    for sel in ['.wp-post-image', '.featured-image img', 'article img', '.entry-content img']:
                        try:
                            imgs = driver.find_elements(By.CSS_SELECTOR, sel)
                            for img in imgs:
                                src = img.get_attribute("src") or ""
                                if src.startswith("http") and 'gravatar' not in src.lower() and 'avatar' not in src.lower():
                                    hero_img = src
                                    break
                            if hero_img:
                                break
                        except:
                            pass
                except:
                    pass
                
                # Download image
                img_file = ""
                if hero_img:
                    # Clean URL
                    clean_url = hero_img.split("?")[0]
                    ext = "jpg"
                    if ".png" in clean_url.lower(): ext = "png"
                    elif ".webp" in clean_url.lower(): ext = "webp"
                    elif ".gif" in clean_url.lower(): ext = "gif"
                    img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
                    
                    # Try downloading with wget using same session (no CF cookies though)
                    # Instead, use JS to get the image data or just record the URL
                    try:
                        r = subprocess.run(["wget", "-q", "-O", img_path, clean_url, "--timeout=15"], 
                                         capture_output=True, timeout=20)
                        if r.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                            img_file = f"{slug}.{ext}"
                        else:
                            # Try with full URL including params
                            r2 = subprocess.run(["wget", "-q", "-O", img_path, hero_img, "--timeout=15"],
                                              capture_output=True, timeout=20)
                            if r2.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                                img_file = f"{slug}.{ext}"
                    except:
                        pass
                
                status = "ok" if len(content) > 50 else "short"
                results.append({
                    "slug": slug, "status": status, "text": content, 
                    "image": img_file, "image_url": hero_img, "url": url
                })
                ok += 1
                print(f"  ✅ text={len(content)}c img={img_file or 'NONE'}", flush=True)
                
            except Exception as e:
                print(f"  ❌ error: {e}", flush=True)
                results.append({"slug": slug, "status": f"error:{str(e)[:100]}", "text": "", "image": "", "url": url})
            
            time.sleep(2)  # polite delay
    
    finally:
        driver.quit()

    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}", flush=True)
    print(f"DONE: {ok}/{len(POST_MAP)} scraped ({no_content} short/empty)", flush=True)
    print(f"Images downloaded: {sum(1 for r in results if r.get('image'))}", flush=True)
    print(f"Image URLs found: {sum(1 for r in results if r.get('image_url'))}", flush=True)

if __name__ == "__main__":
    main()