# feudo.org

Site cartão de visitas de Ricardo Sodré Andrade.

## Stack

- `index.html` — HTML e CSS embutidos, sem dependências externas
- `i18n/pt.json`, `i18n/en.json`, `i18n/ro.json` — traduções carregadas via fetch async
- `foto.png` — foto do hero
- Hospedado no GitHub Pages (`github.com/rsandrade/feudo.org`), domínio via Cloudflare (DNS only)

## Estrutura do site

- **Hero:** foto em largura máxima (760px) + nome centralizado; tagline alinhada à esquerda dentro do `.page`
- **Seções** (ordem atual): Posições · Formação · Grupos de Pesquisa · Projetos e Websites · Experiência · Habilidades Técnicas · Voluntariado · Outras Informações · Links

## Internacionalização

Trilingue: PT-BR, EN, RO. Strings visíveis usam `data-key` no HTML; as traduções vivem em `i18n/{lang}.json` e são carregadas com `fetch` assíncrono e cache em memória (`_i18nCache`). O idioma é detectado automaticamente via `navigator.language` ao carregar a página (PT como fallback). O usuário pode trocar manualmente pelos botões PT / EN / RO.

Textos que são nomes próprios, siglas ou institucições linkadas diretamente no HTML ficam hardcoded (ex: nomes das universidades com `<a>`).

## Convenções

- Instituições e projetos são linkados nos elementos `entry-org` (âncoras com `data-key` ou hardcoded)
- Seções Experiência e Formação usam `entry-list` padrão: cargo/título em destaque, instituição abaixo em cor secundária
- Projetos divididos em **Ativos** e **Inativos**
- Separador entre itens: "e" (PT), "and" (EN), "și" (RO) — nunca "&"
- Para adicionar uma nova chave de tradução: adicionar `data-key="chave"` no HTML e a chave nos três arquivos JSON

## Sobre Ricardo

- Arquivista da UFBA (ufba.br), cedido ao Arquivo Nacional (arquivonacional.gov.br)
- Chefe do Escritório Regional Nordeste do Arquivo Nacional (2025–)
- Coordenador dos projetos Farinha (farinha.info) e Arquivos da UFBA (arquivos.ufba.br)
- Membro do LABHDUFBA (labhd.ufba.br) desde 2024
- Coordenador do CRIDI (cridi.ici.ufba.br) 2019–2026, membro desde 2008
- Radioamador Classe C, brasileiro e português
