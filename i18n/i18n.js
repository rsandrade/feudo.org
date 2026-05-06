// feudo.org i18n system — language detection, ?lang= parameter, selector
// Detects: ?lang= > localStorage > browser > pt (default)
// Translates elements with data-i18n="" attribute + navbar + footer
(function() {
  'use strict';

  const SUPPORTED = ['pt', 'en', 'es', 'fr', 'ro'];
  const DEFAULT = 'pt';
  const STORAGE_KEY = 'feudo-lang';
  const cache = {};

  /* ── Detection ──────────────────────────────────────── */
  function detectLang() {
    const p = new URLSearchParams(location.search);
    const urlLang = p.get('lang');
    if (urlLang && SUPPORTED.includes(urlLang)) { localStorage.setItem(STORAGE_KEY, urlLang); return urlLang; }
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED.includes(saved)) return saved;
    for (const bl of (navigator.languages || [navigator.language || ''])) {
      const c = bl.split('-')[0].toLowerCase();
      if (SUPPORTED.includes(c)) return c;
    }
    return DEFAULT;
  }

  /* ── Load JSON ─────────────────────────────────────── */
  async function load(lang) {
    if (cache[lang]) return cache[lang];
    try {
      const r = await fetch(`/i18n/${lang}.json`);
      if (!r.ok) throw new Error(r.status);
      cache[lang] = await r.json();
      return cache[lang];
    } catch (e) { console.warn('i18n load fail:', lang, e); return null; }
  }

  /* ── Tag navbar elements with i18n keys (once, on first load) ── */
  function tagNavbar() {
    // Top-level nav items: map by original PT text → key
    const navMap = {
      'Sobre': 'nav-about',
      'Trajetória': 'nav-trajetoria',
      'Pesquisa': 'nav-pesquisa',
      'Desenvolvimento': 'nav-desenvolvimento',
      'Textos': 'nav-textos',
    };
    const dropMap = {
      'Bio': 'nav-about-sub-sobre',
      'Contato': 'nav-about-sub-contato',
      'LABHDUFBA': 'nav-pesquisa-sub-labhd',
      'Inteligência Artificial': 'nav-pesquisa-sub-ia',
      'Grupos anteriores': 'nav-pesquisa-sub-groups',
      'Grupos de Pesquisa': 'nav-pesquisa-sub-groups',
      'Publicações': 'page-publicacoes-title',
      'Apresentações': 'page-apresentacoes-title',
      'Farinha': 'nav-desenvolvimento-sub-farinha',
      'Archives World Map': 'nav-desenvolvimento-sub-awm',
      'Medium': 'category-medium',
      'ricardo.arquivista.net': 'category-arquivista-net',
    };

    document.querySelectorAll('.navbar-nav .menu-text').forEach(el => {
      if (!el.dataset.i18nKey) {
        const txt = el.textContent.trim();
        if (navMap[txt]) el.dataset.i18nKey = navMap[txt];
      }
    });
    document.querySelectorAll('.navbar-nav .dropdown-text').forEach(el => {
      if (!el.dataset.i18nKey) {
        const txt = el.textContent.trim();
        if (dropMap[txt]) el.dataset.i18nKey = dropMap[txt];
      }
    });
  }

  /* ── Translate navbar (uses data-i18n-key) ────────── */
  function translateNavbar(t) {
    if (!t) return;
    document.querySelectorAll('.navbar-nav [data-i18n-key]').forEach(el => {
      const k = el.dataset.i18nKey;
      if (t[k] !== undefined) el.textContent = t[k];
    });
  }

  /* ── Translate footer ──────────────────────────────── */
  function translateFooter(t) {
    if (!t) return;
    // Find the footer center paragraph
    const footer = document.querySelector('.nav-footer-center');
    if (!footer) return;
    const p = footer.querySelector('p');
    if (!p) return;
    
    // Footer structure: "Construído com [Quarto] · Template [Dr. Gang He]"
    // Rebuild from translations
    const builtWith = t['footer-built'] || 'Construído com';
    const templateWord = t['footer-template'] || 'Template';
    
    // Get the existing links
    const links = p.querySelectorAll('a');
    const quartoHref = links[0]?.href || 'https://quarto.org';
    const templateHref = links[1]?.href || 'https://github.com/drganghe/quarto-academic-website-template';
    const quartoText = links[0]?.textContent || 'Quarto';
    const templateText = links[1]?.textContent || 'Dr. Gang He';
    
    p.innerHTML = `${builtWith} <a href="${quartoHref}">${quartoText}</a> · ${templateWord} <a href="${templateHref}">${templateText}</a>`;
  }

  /* ── Apply translations ─────────────────────────────── */
  function apply(t) {
    if (!t) return;
    const d = document;

    // 1. data-i18n="key" → textContent
    d.querySelectorAll('[data-i18n]').forEach(el => {
      const k = el.getAttribute('data-i18n');
      if (t[k] !== undefined) el.textContent = t[k];
    });

    // 2. data-i18n-html="key" → innerHTML
    d.querySelectorAll('[data-i18n-html]').forEach(el => {
      const k = el.getAttribute('data-i18n-html');
      if (t[k] !== undefined) el.innerHTML = t[k];
    });

    // 3. data-i18n-title="key" → title attr
    d.querySelectorAll('[data-i18n-title]').forEach(el => {
      const k = el.getAttribute('data-i18n-title');
      if (t[k] !== undefined) el.title = t[k];
    });

    // 4. <html lang>
    d.documentElement.lang = (t.html === 'pt') ? 'pt-BR' : t.html;

    // 5. Page <title> and <meta description>
    const titleKey = d.body.dataset.i18nPageTitle;
    if (titleKey && t[titleKey]) d.title = t[titleKey] + ' – Ricardo Sodré Andrade';
    const descKey = d.body.dataset.i18nPageDesc;
    if (descKey && t[descKey]) {
      const meta = d.querySelector('meta[name="description"]');
      if (meta) meta.content = t[descKey];
    }

    // 6. Navbar
    translateNavbar(t);

    // 7. Footer
    translateFooter(t);
  }

  /* ── Language selector ─────────────────────────────── */
  function buildSelector(lang) {
    if (document.getElementById('lang-selector')) return;
    const labels = {pt:'PT', en:'EN', es:'ES', fr:'FR', ro:'RO'};
    const full   = {pt:'Português', en:'English', es:'Español', fr:'Français', ro:'Română'};

    const nav = document.querySelector('.navbar-collapse');
    if (!nav) return;

    const wrap = document.createElement('div');
    wrap.id = 'lang-selector';
    wrap.className = 'lang-selector nav-item';

    SUPPORTED.forEach(l => {
      const btn = document.createElement('button');
      btn.textContent = labels[l];
      btn.className = 'lang-btn' + (l === lang ? ' lang-btn-active' : '');
      btn.dataset.lang = l;
      btn.title = full[l];
      btn.setAttribute('aria-label', full[l]);
      btn.addEventListener('click', () => switchLang(l));
      wrap.appendChild(btn);
    });

    nav.appendChild(wrap);
  }

  /* ── Switch ────────────────────────────────────────── */
  async function switchLang(lang) {
    if (!SUPPORTED.includes(lang)) return;
    localStorage.setItem(STORAGE_KEY, lang);

    // Update URL
    const u = new URL(location);
    u.searchParams.set('lang', lang);
    history.replaceState({}, '', u);

    // Update buttons
    document.querySelectorAll('.lang-btn').forEach(b => {
      b.classList.toggle('lang-btn-active', b.dataset.lang === lang);
    });

    const t = await load(lang);
    apply(t);
  }

  /* ── Init ───────────────────────────────────────────── */
  async function init() {
    // Tag navbar BEFORE any translation (save original PT text → key mapping)
    tagNavbar();
    
    const lang = detectLang();
    const t = await load(lang);
    apply(t);
    buildSelector(lang);
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init);
  else init();
})();