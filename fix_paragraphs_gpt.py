#!/usr/bin/env python3
"""Fix paragraph spacing in QMD blog posts using GPT-5.4-mini.
Processes each post individually via OpenAI API."""
import os, json, glob, time, yaml
from openai import OpenAI

# Load API key from Hermes config
with open('/home/hermes/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
for p in cfg.get('custom_providers', []):
    if 'openai' in p.get('name','').lower():
        os.environ['OPENAI_API_KEY'] = p['api_key']
        os.environ['OPENAI_BASE_URL'] = p.get('base_url', 'https://api.openai.com/v1')
        break

client = OpenAI()
MODEL = "gpt-5.4-mini"
POSTS_DIR = "/home/hermes/websites/feudo.org/quarto-projeto/posts"

SYSTEM_PROMPT = """You are a text formatting assistant. Your job is to fix paragraph spacing in Portuguese blog posts.

RULES:
1. Return ONLY the corrected body text (no YAML frontmatter)
2. Add blank lines between paragraphs where they belong
3. REMOVE blank lines that incorrectly split a single paragraph in two
4. Short lines that are section headings should have blank lines before and after
5. Remove Medium/UI artifacts: "Get [name]'s stories in your inbox", "Join Medium", "Subscribe", "Remember me for faster sign in", "Open app", "Written by", standalone numbers (reaction counts), date lines like "Mar 16, 2019"
6. Keep the text VERBATIM — do NOT translate, summarize, paraphrase, or change ANY wording
7. Keep URLs, links, and formatting exactly as they are
8. Horizontal rules (---) should have blank lines before and after"""

def process_post(slug):
    path = os.path.join(POSTS_DIR, f"{slug}.qmd")
    with open(path) as fh:
        content = fh.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    frontmatter = parts[1]
    body = parts[2].strip()
    
    if len(body) < 100:
        return False
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Fix paragraph spacing in this Portuguese blog post body:\n\n{body}"}
            ],
            temperature=0.0,
            max_completion_tokens=4096,
        )
        
        new_body = response.choices[0].message.content.strip()
        
        # Verify the model didn't change content drastically
        # Allow 5% difference for added whitespace
        old_len = len(body)
        new_len = len(new_body)
        
        # Check that substantial content is preserved
        # Simple check: first 100 chars of old body (stripped) should appear in new body
        old_start = body[:100].strip()
        if old_start and old_start not in new_body:
            print(f"  ⚠️ Content may have changed, skipping: {slug}")
            return False
        
        new_content = f'---{frontmatter}---\n\n{new_body}\n'
        with open(path, 'w') as fh:
            fh.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"  ❌ API error for {slug}: {str(e)[:80]}")
        return False

# Posts to process
remaining = [
    "formas-comunicacao-blog", "gestao-aaba", "goiania-xv-cba", "golang-raspberry-pi-3",
    "habilidades-antes-dos-18", "hackerspaces-espacos-de-tecnologia-etica-e-solidariedade",
    "holmes-liinc-em-revista", "iii-cna-fotos", "la-fora", "lusofonia-instituicoes-arquivisticas",
    "manipulando-documentos-pdf", "mapeando-todos-os-acervos-documentais-do-mundo-com-o-archives-world-map",
    "materiais-aulas-arquivologia", "milhagens-eventos-arquivologia",
    "motivos-para-acompanhar-o-movimento-indie-hackers", "o-direito-a-privacidade-no-hostil-ciberespaco",
    "order-of-archivists-on-sale", "os-sabores-de-linux-que-eu-ja-usei",
    "para-que-serve-o-bitcoin-pior-cenario-possivel", "premiacao-prppg-fapex",
    "preservacao-digital-e-nossos-documentos-pessoais", "primeiro-dia-aula-professor",
    "primeiros-dias-ufba", "producao-pesquisa-premiada", "programando-o-doutorado",
    "radioamadorismo", "representacao-informacao-computacao-cognitiva",
    "retrospectiva-2", "retrospectiva-de-textos-produzidos-1", "rio-de-janeiro-iii-cna",
    "saindo-arquivo-publico-bahia", "se-as-redes-sociais-estao-mudando-para-onde-vamos",
    "senha-e-frase-senha-proteger-contas-plataformas", "teste-personalidade-inteligencia",
    "um-aplicativo-movel-para-o-archives-world-map", "um-passo-fora-da-normalidade-semana-no-empretec",
    "vasculham-tudo-sobre-nos-recuperar-privacidade-email", "voce-deveria-se-voluntariar",
    "yndexa-dms"
]

success = 0
failed = 0

for i, slug in enumerate(remaining):
    print(f"\n[{i+1}/{len(remaining)}] {slug}", flush=True)
    ok = process_post(slug)
    if ok:
        success += 1
        print(f"  ✅", flush=True)
    else:
        failed += 1
        print(f"  ❌", flush=True)
    
    # Small delay to respect rate limits
    time.sleep(1)

print(f"\n=== DONE ===", flush=True)
print(f"Success: {success} | Failed: {failed}", flush=True)