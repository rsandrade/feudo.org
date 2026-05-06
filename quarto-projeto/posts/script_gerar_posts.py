#!/usr/bin/env python3
"""Generate .qmd files for all migrated posts from ricardo.arquivista.net"""
import os

posts = [
    {
        "date": "2020-08-03",
        "title": "Como criar sua carteira de papel para guardar seus bitcoins",
        "slug": "como-criar-sua-carteira-de-papel-para-guardar-seus-bitcoins",
        "desc": "Guia prático para criar uma carteira de papel (paper wallet) e armazenar bitcoins de forma segura, offline.",
        "url_path": "2020/08/03/como-criar-sua-carteira-de-papel-para-guardar-seus-bitcoins"
    },
    {
        "date": "2018-06-25",
        "title": "Configuring Golang Environment in your Raspberry Pi 3",
        "slug": "configuring-golang-environment-in-your-raspberry-pi-3",
        "desc": "Passo a passo para configurar o ambiente de desenvolvimento Go (Golang) em um Raspberry Pi 3.",
        "url_path": "2018/06/25/configuring-golang-environment-in-your-raspberry-pi-3"
    },
    {
        "date": "2017-10-16",
        "title": "Sobre blockchain, criptomoedas e outras aplicações — o básico de detalhes avançados",
        "slug": "sobre-blockchain-criptomoedas-e-outras-aplicacoes",
        "desc": "Artigo sobre blockchain, criptomoedas e suas aplicações, abordando conceitos básicos e aspectos avançados da tecnologia.",
        "url_path": "2017/10/16/sobre-blockchain-criptomoedas-e-outras-aplicacoes"
    },
    {
        "date": "2016-05-04",
        "title": "Todo mundo deveria desenvolver essas habilidades antes dos 18 anos",
        "slug": "todo-mundo-deveria-desenvolver-essas-habilidades-antes-dos-18-anos",
        "desc": "Reflexão sobre habilidades essenciais que todos deveriam desenvolver antes da maioridade, desde finanças até pensamento crítico.",
        "url_path": "2016/05/04/todo-mundo-deveria-desenvolver-essas-habilidades-antes-dos-18-anos"
    },
    {
        "date": "2015-10-14",
        "title": "The Order of Archivists is on sale!",
        "slug": "the-order-of-archivists-is-on-sale",
        "desc": "Anúncio da publicação do livro 'The Order of Archivists', obra de ficção com temática arquivística.",
        "url_path": "2015/10/14/the-order-of-archivists-is-on-sale"
    },
    {
        "date": "2014-07-28",
        "title": "Amazon AWS Glacier — alternativa em nuvem para cópias de segurança",
        "slug": "amazon-aws-glacier-alternativa-em-nuvem-para-copias-de-seguranca",
        "desc": "Análise do Amazon AWS Glacier como alternativa de armazenamento em nuvem para backups e cópias de segurança.",
        "url_path": "2014/07/28/amazon-aws-glacier-alternativa-em-nuvem-para-copias-de-seguranca"
    },
    {
        "date": "2014-04-10",
        "title": "Lusofonia como espaço cooperativo entre instituições arquivísticas",
        "slug": "lusofonia-como-espaco-cooperativo-entre-instituicoes-arquivisticas",
        "desc": "Discussão sobre o espaço da lusofonia como plataforma para cooperação entre instituições arquivísticas dos países de língua portuguesa.",
        "url_path": "2014/04/10/lusofonia-como-espaco-cooperativo-entre-instituicoes-arquivisticas"
    },
    {
        "date": "2014-03-24",
        "title": "Ingress",
        "slug": "ingress",
        "desc": "Impressões sobre o jogo Ingress, da Niantic Labs, um jogo de realidade aumentada baseado em localização.",
        "url_path": "2014/03/24/ingress"
    },
    {
        "date": "2014-01-11",
        "title": "Representação da informação e computação cognitiva",
        "slug": "representacao-da-informacao-e-computacao-cognitiva",
        "desc": "Artigo sobre a intersecção entre representação da informação e computação cognitiva, explorando novas fronteiras tecnológicas.",
        "url_path": "2014/01/11/representacao-da-informacao-e-computacao-cognitiva"
    },
    {
        "date": "2014-01-09",
        "title": "Em terras portuguesas…",
        "slug": "em-terras-portuguesas",
        "desc": "Relato de experiência sobre a chegada a Portugal para o doutoramento na Universidade do Porto e Universidade de Aveiro.",
        "url_path": "2014/01/09/em-terras-portuguesas"
    },
    {
        "date": "2013-04-21",
        "title": "Radioamadorismo",
        "slug": "radioamadorismo",
        "desc": "Introdução ao radioamadorismo, suas aplicações e relevância como hobby técnico e meio de comunicação alternativo.",
        "url_path": "2013/04/21/radioamadorismo"
    },
    {
        "date": "2012-06-25",
        "title": "A ordem dos arquivistas: centésimo",
        "slug": "a-ordem-dos-arquivistas-centesimo",
        "desc": "Centésimo post do blog — uma reflexão sobre a trajetória do blog e o universo dos arquivistas.",
        "url_path": "2012/06/25/a-ordem-dos-arquivistas-centesimo"
    },
    {
        "date": "2011-01-25",
        "title": "Lá fora",
        "slug": "la-fora",
        "desc": "Vídeo e reflexão sobre estar longe de casa, explorando novos lugares e perspectivas.",
        "url_path": "2011/01/25/la-fora"
    },
    {
        "date": "2011-01-23",
        "title": "Programando o doutorado",
        "slug": "programando-o-doutorado",
        "desc": "Planejamento e expectativas para o início do doutoramento em Informação e Comunicação em Plataformas Digitais.",
        "url_path": "2011/01/23/programando-o-doutorado"
    },
    {
        "date": "2010-06-02",
        "title": "PDF com a minha dissertação de mestrado",
        "slug": "pdf-com-minha-dissertacao-de-mestrado",
        "desc": "Disponibilização do PDF da dissertação de mestrado em Ciência da Informação pela UFBA.",
        "url_path": "2010/06/02/pdf-com-a-minha-dissertacao-de-mestrado"
    },
    {
        "date": "2010-05-08",
        "title": "Defesa de dissertação realizada: mais um passo dado",
        "slug": "defesa-de-dissertacao-realizada",
        "desc": "Registro da defesa da dissertação de mestrado em Ciência da Informação na UFBA.",
        "url_path": "2010/05/08/defesa-de-dissertacao-realizada"
    },
    {
        "date": "2010-04-24",
        "title": "Catálogo web do compositor Lindembergue Cardoso",
        "slug": "catalogo-web-do-compositor-lindembergue-cardoso",
        "desc": "Projeto de catálogo web para a obra do compositor baiano Lindembergue Cardoso, combinando representação arquivística e tecnologia.",
        "url_path": "2010/04/24/catalogo-web-do-compositor-lindembergue-cardoso"
    },
    {
        "date": "2010-02-12",
        "title": "Primeiros dias de trabalho na UFBA",
        "slug": "primeiros-dias-de-trabalho-na-ufba",
        "desc": "Relato pessoal dos primeiros dias como arquivista concursado na Universidade Federal da Bahia.",
        "url_path": "2010/02/12/primeiros-dias-de-trabalho-na-ufba"
    },
    {
        "date": "2009-12-20",
        "title": "Na gestão da Associação dos Arquivistas da Bahia",
        "slug": "na-gestao-da-associacao-dos-arquivistas-da-bahia",
        "desc": "Relato sobre a participação na gestão da Associação dos Arquivistas da Bahia (AAB).",
        "url_path": "2009/12/20/na-gestao-da-associacao-dos-arquivistas-da-bahia"
    },
    {
        "date": "2009-10-15",
        "title": "Saindo do Arquivo Público da Bahia",
        "slug": "saindo-do-arquivo-publico-da-bahia",
        "desc": "Relato de despedida do Arquivo Público da Bahia após período de trabalho na instituição.",
        "url_path": "2009/10/15/saindo-do-arquivo-publico-da-bahia"
    },
    {
        "date": "2009-08-15",
        "title": "Aprovação no concurso da UFBA",
        "slug": "aprovacao-no-concurso-da-ufba",
        "desc": "Registro da aprovação no concurso público para arquivista da Universidade Federal da Bahia.",
        "url_path": "2009/08/15/aprovacao-no-concurso-da-ufba"
    },
    {
        "date": "2009-05-27",
        "title": "Materiais das aulas — Curso de Arquivologia (noturno)",
        "slug": "materiais-das-aulas-curso-de-arquivologia-noturno",
        "desc": "Disponibilização de materiais didáticos utilizados nas aulas do curso noturno de Arquivologia da UFBA.",
        "url_path": "2009/05/27/materiais-das-aulas-curso-de-arquivologia-noturno"
    },
    {
        "date": "2009-04-27",
        "title": "Aula para turma de calouros do Curso de Arquivologia da UFBA",
        "slug": "aula-para-turma-de-calouros-do-curso-de-arquivologia-da-ufba",
        "desc": "Relato de aula ministrada para calouros do Curso de Arquivologia da UFBA, abordando a profissão arquivística.",
        "url_path": "2009/04/27/aula-para-turma-de-calouros-do-curso-de-arquivologia-da-ufba"
    },
    {
        "date": "2009-04-06",
        "title": "Curso de ontologia em 8 horas",
        "slug": "curso-de-ontologia-em-8-horas",
        "desc": "Experiência e materiais do curso intensivo de ontologia aplicada, abordando fundamentos e aplicações em ciência da informação.",
        "url_path": "2009/04/06/curso-de-ontologia-em-8-horas"
    },
    {
        "date": "2009-03-05",
        "title": "Yndexa DMS — sistema web para gestão de documentos",
        "slug": "yndexa-dms-sistema-web-para-gestao-de-documentos",
        "desc": "Apresentação do Yndexa DMS, sistema web desenvolvido para gestão documental com software livre.",
        "url_path": "2009/03/05/yndexa-dms-sistema-web-para-gestao-de-documentos"
    },
    {
        "date": "2008-12-15",
        "title": "Novo texto publicado em periódico trata de aspectos teóricos e históricos da descrição arquivística e a evolução dos instrumentos de referência até a Web 2.0",
        "slug": "novo-texto-publicado-em-periodico-descricao-arquivistica-web-2-0",
        "desc": "Anúncio de artigo publicado sobre descrição arquivística, evolução dos instrumentos de referência e impacto da Web 2.0.",
        "url_path": "2008/12/15/novo-texto-publicado-em-periodico-trata-de-aspectos-teoricos-e-historicos-da-descricao-arquivistica"
    },
    {
        "date": "2008-11-27",
        "title": "Mais sobre a premiação PRPPG/UFBA e FAPEX",
        "slug": "mais-sobre-premiacao-prppg-ufba-e-fapex",
        "desc": "Complemento de informações sobre a premiação de pesquisa concedida pela PRPPG/UFBA e FAPEX.",
        "url_path": "2008/11/27/mais-sobre-premiacao-prppg-ufba-e-fapex"
    },
    {
        "date": "2008-11-18",
        "title": "Produção de pesquisa premiada pela PRPPG/UFBA e FAPEX",
        "slug": "producao-de-pesquisa-premiada-pela-prppg-ufba-e-fapex",
        "desc": "Anúncio de premiação de produção de pesquisa pela Pró-Reitoria de Pesquisa da UFBA e FAPEX.",
        "url_path": "2008/11/18/producao-de-pesquisa-premiada-pela-prppg-ufba-e-fapex"
    },
    {
        "date": "2008-11-03",
        "title": "III Congresso Nacional de Arquivologia — algumas poucas fotos",
        "slug": "iii-congresso-nacional-de-arquivologia-algumas-fotos",
        "desc": "Registro fotográfico do III Congresso Nacional de Arquivologia (CNA), realizado no Rio de Janeiro.",
        "url_path": "2008/11/03/iii-congresso-nacional-de-arquivologia-algumas-poucas-fotos"
    },
    {
        "date": "2008-10-24",
        "title": "O Rio de Janeiro continua lindo: minhas impressões do III CNA e da cidade",
        "slug": "o-rio-de-janeiro-continua-lindo-impressoes-iii-cna",
        "desc": "Impressões pessoais sobre a participação no III Congresso Nacional de Arquivologia e a cidade do Rio de Janeiro.",
        "url_path": "2008/10/24/o-rio-de-janeiro-continua-lindo-minhas-impressoes-do-iii-cna"
    },
    {
        "date": "2008-09-29",
        "title": "Primeiro dia de aula de um novo professor",
        "slug": "primeiro-dia-de-aula-de-um-novo-professor",
        "desc": "Relato pessoal da experiência do primeiro dia de aula como professor no Curso de Arquivologia da UFBA.",
        "url_path": "2008/09/29/primeiro-dia-de-aula-de-um-novo-professor"
    },
    {
        "date": "2008-07-05",
        "title": "Andanças por Goiânia: XV Congresso Brasileiro de Arquivologia",
        "slug": "andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia",
        "desc": "Relato de participação no XV Congresso Brasileiro de Arquivologia, realizado em Goiânia.",
        "url_path": "2008/07/05/andancas-por-goiania-xv-congresso-brasileiro-de-arquivologia"
    },
    {
        "date": "2008-06-20",
        "title": "Resultado do concurso de monografias de Arquivologia da Bahia",
        "slug": "resultado-do-concurso-de-monografias-de-arquivologia-da-bahia",
        "desc": "Divulgação do resultado do concurso de monografias em Arquivologia promovido na Bahia.",
        "url_path": "2008/06/20/resultado-do-concurso-de-monografias-de-arquivologia-da-bahia"
    },
    {
        "date": "2008-06-05",
        "title": "Disponibilização de bases de dados arquivísticas legadas na Web",
        "slug": "disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web",
        "desc": "Artigo sobre estratégias e técnicas para disponibilizar bases de dados arquivísticas legadas na Web, combinando representação arquivística e tecnologia.",
        "url_path": "2008/06/05/disponibilizacao-de-bases-de-dados-arquivisticas-legadas-na-web"
    },
    {
        "date": "2008-05-04",
        "title": "Teste online para mensurar a \"personalidade\" e a \"múltipla inteligência\"",
        "slug": "teste-online-personalidade-multipla-inteligencia",
        "desc": "Indicação de testes online para avaliar traços de personalidade e inteligências múltiplas, com reflexões sobre os resultados.",
        "url_path": "2008/05/04/teste-online-para-mensurar-a-personalidade-e-a-multipla-inteligencia"
    },
    {
        "date": "2008-04-22",
        "title": "Usando milhagens para ir aos eventos de Arquivologia",
        "slug": "usando-milhagens-para-ir-aos-eventos-de-arquivologia",
        "desc": "Dicas sobre como utilizar programas de milhagem para viagens a eventos acadêmicos e profissionais de Arquivologia.",
        "url_path": "2008/04/22/usando-milhagens-para-ir-aos-eventos-de-arquivologia"
    },
    {
        "date": "2008-04-16",
        "title": "Holmes indexa mais um periódico em CI: Liinc em Revista",
        "slug": "holmes-indexa-liinc-em-revista",
        "desc": "Anúncio da indexação do periódico Liinc em Revista pelo sistema Holmes, ferramenta de indexação em Ciência da Informação.",
        "url_path": "2008/04/16/holmes-indexa-mais-um-periodico-em-ci-liinc-em-revista"
    },
    {
        "date": "2008-04-12",
        "title": "Descrição arquivística na Web: o que há de vir",
        "slug": "descricao-arquivistica-na-web-o-que-ha-de-vir",
        "desc": "Reflexão sobre o futuro da descrição arquivística na Web, tendências e possibilidades para a área.",
        "url_path": "2008/04/12/descricao-arquivistica-na-web-o-que-ha-de-vir"
    },
    {
        "date": "2008-04-10",
        "title": "Manipulando documentos PDF",
        "slug": "manipulando-documentos-pdf",
        "desc": "Dicas e ferramentas para manipulação de documentos PDF, incluindo edição, conversão e gerenciamento.",
        "url_path": "2008/04/10/manipulando-documentos-pdf"
    },
    {
        "date": "2008-04-09",
        "title": "Formas de comunicação pessoal: a utilidade desse blog",
        "slug": "formas-de-comunicacao-pessoal-utilidade-desse-blog",
        "desc": "Reflexão sobre as formas de comunicação pessoal na era digital e a utilidade de manter um blog como ferramenta de expressão.",
        "url_path": "2008/04/09/formas-de-comunicacao-pessoal-a-utilidade-desse-blog"
    },
]

dest = "/home/hermes/websites/feudo.org/novo-site/posts/"

for p in posts:
    # Escape quotes in title for YAML
    title_yaml = p["title"].replace('"', '\\"')
    desc_yaml = p["desc"].replace('"', '\\"')
    
    url = f"https://ricardo.arquivista.net/{p['url_path']}/"
    
    content = f'''---
title: "{title_yaml}"
author: "Ricardo Sodré Andrade"
date: "{p['date']}"
categories: [arquivista-net]
description: "{desc_yaml}"
draft: false
---

{p['desc']}

Leia o texto completo em [ricardo.arquivista.net]({url}).
'''
    filepath = os.path.join(dest, p['slug'] + '.qmd')
    # Check if file exists
    if os.path.exists(filepath):
        print(f"EXISTS: {filepath}")
    else:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"CREATED: {filepath}")

print(f"\nTotal: {len(posts)} posts processed")
