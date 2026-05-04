#!/usr/bin/env python3
"""Scrape Medium articles using undetected-chromedriver. Robust version."""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json, os, time, re, glob

OUTPUT_JSON = "/home/hermes/websites/feudo.org/quarto-projeto/posts/images/medium_texts.json"

medium_posts = {
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
}

# Find retrospective posts too
for f in glob.glob("/home/hermes/websites/feudo.org/quarto-projeto/posts/retrospectiva*.qmd"):
    with open(f) as fh:
        content = fh.read()
    slug = os.path.basename(f).replace('.qmd', '')
    match = re.search(r'https://medium\.com/[^\s\)]+', content)
    if match:
        medium_posts[slug] = match.group(0)

skip_patterns = ['Sign up', 'Sign in', 'Open in app', 'Follow', 'Write', 'Get app']

def main():
    print(f"Scraping {len(medium_posts)} Medium articles...", flush=True)
    
    options = uc.ChromeOptions()
    options.binary_location = "/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options, version_main=147)
    driver.set_page_load_timeout(60)
    
    results = {}
    ok = 0
    
    try:
        for i, (slug, url) in enumerate(medium_posts.items()):
            print(f"\n[{i+1}/{len(medium_posts)}] {slug}", flush=True)
            try:
                driver.get(url)
                time.sleep(8)
                
                # Wait for CF if present
                for _ in range(5):
                    if 'Just a moment' not in driver.title:
                        break
                    time.sleep(2)
                
                # Get article text
                content = ""
                for sel in ['article', '[role="article"]', 'main']:
                    try:
                        el = driver.find_element(By.CSS_SELECTOR, sel)
                        text = el.text.strip()
                        if len(text) > 200:
                            content = text
                            break
                    except:
                        continue
                
                if not content:
                    content = driver.find_element(By.TAG_NAME, "body").text.strip()
                
                # Clean Medium chrome
                lines = content.split('\n')
                clean = []
                for line in lines:
                    s = line.strip()
                    if not s:
                        continue
                    if any(s == p for p in skip_patterns):
                        continue
                    clean.append(s)
                content = '\n'.join(clean)
                
                results[slug] = content
                ok += 1
                print(f"  ✅ {len(content):,} chars", flush=True)
                
            except Exception as e:
                results[slug] = ""
                print(f"  ❌ {str(e)[:60]}", flush=True)
            
            time.sleep(3)
    
    finally:
        driver.quit()
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nDONE: {ok}/{len(medium_posts)}", flush=True)

if __name__ == "__main__":
    main()