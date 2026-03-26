# feudo.org

Site cartão de visitas de Ricardo Sodré Andrade.

## Stack

Arquivo único `index.html` — HTML, CSS e JS embutidos, sem dependências externas.

## Estrutura do site

- **Hero:** foto + nome centralizados, tagline alinhada à esquerda dentro do `.page`
- **Seções** (ordem atual): Posições · Formação · Grupos de Pesquisa · Projetos e Websites · Experiência · Habilidades Técnicas · Voluntariado · Outras Informações · Links

## Internacionalização

Trilingue: PT-BR, EN, RO. Todas as strings visíveis ao usuário usam `data-key` e são definidas no objeto `translations` no `<script>` ao final do arquivo. Textos que são nomes próprios ou siglas (ex: instituições linkadas no HTML) ficam hardcoded.

## Convenções

- Instituições e projetos são linkados diretamente nos elementos `entry-org` ou em âncoras hardcoded
- A seção Experiência usa `entry-list` padrão (cargo em destaque, instituição abaixo em cor secundária) — igual à Formação
- Projetos divididos em **Ativos** e **Inativos**
- Separador entre itens: "e" (PT), "and" (EN), "și" (RO) — nunca "&"

## Sobre Ricardo

- Arquivista da UFBA, cedido ao Arquivo Nacional
- Chefe do Escritório Regional Nordeste do Arquivo Nacional (2025–)
- Coordenador dos projetos Farinha (farinha.info) e Arquivos da UFBA (arquivos.ufba.br)
- Radioamador Classe C, brasileiro e português
