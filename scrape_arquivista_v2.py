#!/usr/bin/env python3
"""Scrape ricardo.arquivista.net using undetected-chromedriver. Must run with xvfb-run."""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time, json, os, subprocess

IMAGES_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images"
OUTPUT_JSON = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images/scrape_results.json"
os.makedirs(IMAGES_DIR, exist_ok=True)

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

def main():
    print("Starting Chrome (non-headless, via xvfb)...")
    options = uc.ChromeOptions()
    options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options, version_main=147)
    driver.set_page_load_timeout(30)

    results = []
    ok = 0

    try:
        for i, (slug, url) in enumerate(POST_MAP.items()):
            print(f"\n[{i+1}/{len(POST_MAP)}] {slug}")
            try:
                driver.get(url)
                
                # Wait for Cloudflare
                bypassed = False
                for attempt in range(20):
                    time.sleep(2)
                    title = driver.title
                    if 'Just a moment' not in title and title.strip():
                        bypassed = True
                        break
                
                if not bypassed:
                    print(f"  ❌ CF not bypassed")
                    results.append({"slug": slug, "status": "cf_blocked", "text": "", "image": ""})
                    continue
                
                time.sleep(1)
                
                # Extract text
                try:
                    content = driver.find_element(By.CSS_SELECTOR, ".entry-content, .post-content, article, main").text.strip()
                except:
                    content = driver.find_element(By.TAG_NAME, "body").text.strip()
                
                # Extract hero image
                hero_img = ""
                try:
                    imgs = driver.find_elements(By.CSS_SELECTOR, "img")
                    for img in imgs:
                        src = img.get_attribute("src") or ""
                        cls = img.get_attribute("class") or ""
                        if any(s in src.lower() for s in ["gravatar","avatar","icon","logo","emoji","widget","comment"]):
                            continue
                        if any(s in cls.lower() for s in ["avatar","icon","logo","emoji","widget"]):
                            continue
                        if src.startswith("http"):
                            hero_img = src
                            break
                except:
                    pass
                
                # Download image
                img_ext = ""
                if hero_img:
                    ext = "jpg"
                    if ".png" in hero_img.lower(): ext = "png"
                    elif ".webp" in hero_img.lower(): ext = "webp"
                    img_path = os.path.join(IMAGES_DIR, f"{slug}.{ext}")
                    r = subprocess.run(["wget","-q","-O",img_path,hero_img.split("?")[0]], capture_output=True, timeout=15)
                    if r.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                        img_ext = ext
                        print(f"  ✅ text={len(content)}c img={slug}.{ext}")
                    else:
                        # Try full URL with params
                        r2 = subprocess.run(["wget","-q","-O",img_path,hero_img], capture_output=True, timeout=15)
                        if r2.returncode == 0 and os.path.exists(img_path) and os.path.getsize(img_path) > 500:
                            img_ext = ext
                            print(f"  ✅ text={len(content)}c img={slug}.{ext}")
                        else:
                            print(f"  ✅ text={len(content)}c img=FAILED")
                else:
                    print(f"  ✅ text={len(content)}c img=NONE")
                
                results.append({"slug": slug, "status": "ok", "text": content, "image": f"{slug}.{img_ext}" if img_ext else "", "url": url})
                ok += 1
                
            except Exception as e:
                print(f"  ❌ error: {e}")
                results.append({"slug": slug, "status": f"error:{e}", "text": "", "image": "", "url": url})
            
            time.sleep(2)
    
    finally:
        driver.quit()

    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== DONE: {ok}/{len(POST_MAP)} ===")

if __name__ == "__main__":
    main()