# Avaliação de Conteúdo — feudo.org

**Data:** 23/04/2026  
**Avaliador:** Hermes  
**Referências consultadas:**
- Townsend Center (UC Berkeley) — Personal Academic Webpages: How-To's and Tips
- LSE — How do you create a good personal website?
- Power Your Research — 9 Essentials to Include On Your Personal Academic Website
- The Academic Designer — 10 Highlights to Include on Your Personal Academic Website
- Elsevier Connect — Creating a simple and effective academic personal website
- Hendrik Erz — Anatomy of a Successful Academic Website

---

## 1. Diagnóstico geral

O feudo.org é um cartão de visitas digital funcional e com identidade própria. O design minimalista (monocromático, tipografia serif/sans-serif, fundo pergaminho) comunica seriedade acadêmica e funciona bem como formato "CV online". A estrutura de seções é lógica e a i18n (PT/EN/RO) é um diferencial raríssimo.

**Pontuação qualitativa:** 7/10 — bom, mas com margem clara para evoluir de "CV online" para "presença academicamente estratégica".

---

## 2. Pontos fortes

| Aspecto | Avaliação |
|---------|-----------|
| **Identidade visual** | Paleta e tipografia criam atmosfera "arquivística" coerente com a área de atuação |
| **i18n trilingue** | PT/EN/RO é excepcional para um site pessoal — demonstra alcance internacional |
| **Links externos** | Todas as instituições e projetos são linkados — facilita verificação e aprofundamento |
| **Tags de projeto** | Categorização por tipo (Institucional, Software Livre, Comunidade, IA) — boa escaneabilidade |
| **Separação Ativos/Inativos** | Demonstra histórico sem poluir o foco atual |
| **Minimalismo** | Sem distrações, sem pop-ups, sem tracking — condizente com os valores do campo |
| **Responsividade** | Mobile funciona bem; layout de coluna única adapta-se corretamente |

---

## 3. Problemas de conteúdo

### 3.1 ❌ Bug: posição duplicada
A seção "Posições" tem **duas entradas usando `pos3-title`** (Coordenador): uma para Farinha (2024–) e outra para Arquivos da UFBA (2023–). O `data-key` é o mesmo, então ambos mostram o texto "Coordenador" — porém a segunda está semanticamente incorreta já que repete o mesmo cargo para projetos distintos. **Resolução:** criar `pos4-title`/`pos4-org` para Arquivos da UFBA.

### 3.2 ❌ Foto do hero com qualidade insuficiente
A foto atual é contra-luz (rosto na sombra), granulada e com resolução limitada (foto.png em largura 760px). Referências de sites acadêmicos bem-sucedidos enfatizam: **headshot profissional e bem iluminado** é o item #1 ou #2 em todas as checklists (The Academic Designer, Power Your Research, LSE). A foto com a ave de rapina é carregada de personalidade, mas a qualidade técnica compromete.

### 3.3 ❌ Sem "Sobre" / bio narrativa
O site tem uma tagline factual, mas **nenhuma seção narrativa**. Todas as referências consultadas apontam a biografia como o elemento essencial de um site acadêmico:
- "Your About page is where you tell your story and reiterate your differentiation" (Power Your Research)
- "A bio that introduces you to the public — who you are, what you're working on now, your general research" (The Academic Designer)
- "A short bio, research interests, why your research matters" (LSE, Townsend Center)

O site atual responde "o quê" mas não "por quê" — o que motivou a transição da editoração para a arquivologia digital? O que move o trabalho com Farinha? Um parágrafo de bio narrativa transformaria o site de catálogo em presença com voz.

### 3.4 ⚠️ Produção acadêmica ausente
Não há menção a **publicações, apresentações, palestras ou produções bibliográficas**. Para um profissional da área arquivística com mestrado e doutorado (mesmo incompleto), isso é uma omissão significativa. Não precisa ser uma lista completa — um link para o Lattes já ajuda, mas referenciar pelo menos as produções mais relevantes dá credibilidade. Elsevier: "Use your website to highlight research findings, publications, achievements."

### 3.5 ⚠️ Habilidades técnicas desatualizadas
A seção lista **PHP, Bash, Golang, Flutter, Fat-Free Framework, Selenium, WordPress, LAMP** — tecnologias que refletem o passado (~2010-2020), não o presente. Hoje o trabalho principal é **Python, Django, Docker, Alpine.js, Bulma, RAG, agentes de IA** — stack real do Farinha e dos projetos atuais. As skills antigas podem ser mencionadas, mas não devem dominar a seção.

### 3.6 ⚠️ "Extração de Dados" com apenas 1 item (Selenium)
Categoria com um só item dá impressão de escassez. Sugestão: renomear para algo mais amplo (ex: "Automação e Dados") ou mesclar com outra categoria.

### 3.7 ⚠️ Habilidades técnicas não internacionalizadas
As tags de skill (Linux, Docker, RAG, Agentes) estão hardcoded em PT ou misto. "Agentes" é a única palavra em PT entre termos em EN. Deveria haver chaves i18n para os termos que variam por idioma.

---

## 4. Sugestões de melhoria (priorizadas)

### 🔴 Alta prioridade

**S1 — Adicionar seção "Sobre" com bio narrativa**
Posição: logo após a tagline, antes das seções factuais. Um parágrafo (3-5 frases) que conta quem é Ricardo, o que omove seu trabalho e como arquivologia e tecnologia se cruzam na sua prática. Nos 3 idiomas. Transforma o site de "catálogo" em "presença com voz".

**S2 — Corrigir bug da posição duplicada**
Criar `pos4-title` e `pos4-org` para "Arquivos da UFBA", separando-a da posição do Farinha.

**S3 — Atualizar habilidades técnicas**
Reorganizar para refletir a stack atual:
- **Sistemas**: Linux, LXD, Docker, Nginx
- **Desenvolvimento**: Python, Django, Alpine.js, Bulma, Bash
- **IA e Dados**: RAG, Agentes de IA, IA generativa, Extração de dados
- **Serviços**: Nextcloud, WordPress, Gunicorn

Remover ou minimizar: PHP, Golang, Flutter, Fat-Free Framework, Selenium (stack legada).

**S4 — Substituir foto do hero**
Foto bem iluminada, preferencialmente profissional. Se quiser manter a foto com a ave de rapina (que tem personalidade), uma versão melhor iluminada/resoluta resolveria. Alternativa: foto profissional + foto com ave como secondária.

### 🟡 Média prioridade

**S5 — Adicionar produção acadêmica/bibliográfica**
Mesmo que mínima: referência a teses (Mestrado em Ciência da Informação — UFBA), apresentações em eventos (CNARQ, ODD, EBAM, FPC), ou produções do LABHD/CRIDI. Pode ser uma seção enxuta com links para o Lattes e algumas entradas-chave.

**S6 — Adicionar e-mail de contato**
O site não tem nenhuma forma de contato direto. Um `ricardo@feudo.org` ou `contato@yndexa.com` no topo (junto com os links sociais) tornaria o site funcionamente completo. Referências concordam: "Make it easy for media, organizations, collaborators to get in touch" (Power Your Research).

**S7 — Enriquecer footer**
O footer atual diz apenas "feudo.org". Adicionar © ano + e-mail + link para código-fonte (GitHub) daria fechamento e credibilidade.

**S8 — SEO: meta description e Open Graph**
A meta description atual é genérica: "Ricardo Sodré Andrade — Arquivista, Arquivo Nacional, UFBA". Poderia ser mais rica e atrativa. Faltam tags Open Graph (`og:title`, `og:description`, `og:image`) para que compartilhamentos em redes sociais mostrem preview adequado.

### 🟢 Baixa prioridade

**S9 — Internacionalizar habilidade técnica**
Tags como "Agentes" → "Agents"/"Agenți" nos outros idiomas. Termos em inglês (Linux, Docker) podem permanecer, mas rótulos de categoria ("Desenvolvimento", "Extração de Dados") já usam data-key e precisam de consistência.

**S10 — Reconsiderar projetos inativos**
Portal do Arquivista, Junte.se e Legatum são projetos encerrados. Manter 3 inativos entre 6 ativos dá uma proporção saudável (mostra histórico sem focar no passado). Porém, se os links apontam para sites fora do ar, pode dar impressão de desatualização. Verificar se os links ainda funcionam.

**S11 — Link para Yndexa na seção Posições**
A posição de "Coordenador" do Farinha linka para farinha.info mas não para yndexa.com. A conexão empresa-projeto fica subcomunicada.

**S12 — Indicadores de autoria nos projetos**
Nos cards de projeto ativos, indicar o papel ("Coordenador", "Desenvolvedor", "Colaborador") — hoje apenas o nome e a descrição aparecem, sem indicar qual é a relação de Ricardo com cada um.

---

## 5. Resumo executivo

| Prioridade | Item | Esforço |
|:---:|------|:---:|
| 🔴 | S1 — Seção "Sobre" com bio narrativa | Médio |
| 🔴 | S2 — Corrigir posição duplicada | Baixo |
| 🔴 | S3 — Atualizar habilidades técnicas | Baixo |
| 🔴 | S4 — Substituir foto do hero | Externo |
| 🟡 | S5 — Produção acadêmica/bibliográfica | Médio |
| 🟡 | S6 — E-mail de contato | Baixo |
| 🟡 | S7 — Enriquecer footer | Baixo |
| 🟡 | S8 — SEO / Open Graph | Baixo |
| 🟢 | S9 — i18n das habilidades | Baixo |
| 🟢 | S10 — Verificar links inativos | Baixo |
| 🟢 | S11 — Link Yndexa nas Posições | Baixo |
| 🟢 | S12 — Indicar papel nos projetos | Médio |

**Impacto maior com menor esforço:** S1 + S2 + S3 + S6 resolvem os problemas mais evidentes e transformam o site de um "CV factual" em uma "presença estratégica" — tudo com alterações que cabem em uma sessão de trabalho.