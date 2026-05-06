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

  /* ── Translate navbar ─────────────────────────────── */
  function translateNavbar(t) {
    if (!t) return;
    // Navigation bar: top-level menu items use <span class="menu-text">
    // Map portuguese text → i18n key
    const navMap = {
      'Sobre': 'nav-about',
      'Trajetória': 'nav-trajetoria',
      'Pesquisa': 'nav-pesquisa',
      'Desenvolvimento': 'nav-desenvolvimento',
      'Textos': 'nav-textos',
    };
    // Dropdown items use <span class="dropdown-text">
    const dropMap = {
      'Bio': 'nav-about-sub-sobre',
      'Contato': 'nav-about-sub-contato',
      'LABHDUFBA': 'nav-pesquisa-sub-labhd',
      'Inteligência Artificial': 'nav-pesquisa-sub-ia',
      'Grupos anteriores': 'nav-pesquisa-sub-groups',
      'Grupos de Pesquisa': 'nav-pesquisa-sub-groups',
      'Farinha': 'nav-desenvolvimento-sub-farinha',
      'Archives World Map': 'nav-desenvolvimento-sub-awm',
      'Publicações': 'page-publicacoes-title',
      'Apresentações': 'page-apresentacoes-title',
      'Medium': 'category-medium',
      'ricardo.arquivista.net': 'category-arquivista-net',
    };

    // Translate top-level nav items
    document.querySelectorAll('.navbar-nav .menu-text').forEach(el => {
      const txt = el.textContent.trim();
      if (navMap[txt] && t[navMap[txt]]) el.textContent = t[navMap[txt]];
    });

    // Translate dropdown items
    document.querySelectorAll('.navbar-nav .dropdown-text').forEach(el => {
      const txt = el.textContent.trim();
      if (dropMap[txt] && t[dropMap[txt]]) el.textContent = t[dropMap[txt]];
    });

    // Also translate the E-mail link in about section (index.qmd)
    document.querySelectorAll('.about-links .about-link').forEach(el => {
      const txt = el.textContent.trim();
      if (txt === 'E-mail' && t['link-email']) el.textContent = t['link-email'];
    });
  }

  /* ── Translate footer ──────────────────────────────── */
  function translateFooter(t) {
    if (!t) return;
    const footer = document.querySelector('.nav-footer-center');
    if (!footer) return;
    // Structure: "Ricardo Sodré Andrade © 2026" · "Construído com [Quarto] · Template [Dr. Gang He]"
    // We look for text containing "Construído com" or "Built with"
    const nodes = footer.childNodes;
    for (const node of nodes) {
      if (node.nodeType === 3) { // text node
        const txt = node.textContent;
        if (txt.includes('Construído com') && t['footer-built']) {
          node.textContent = txt.replace('Construído com', t['footer-built']);
        }
        if (txt.includes('Template') && t['footer-template']) {
          node.textContent = txt.replace('Template', t['footer-template']);
        }
      }
    }
    // Also check <span> and other text elements in footer
    footer.querySelectorAll('*').forEach(el => {
      if (el.children.length === 0) { // leaf text node container
        const txt = el.textContent;
        if (txt.includes('Construído com') && t['footer-built']) {
          el.innerHTML = el.innerHTML.replace('Construído com', t['footer-built']);
        }
        if (txt.includes('Template') && t['footer-template']) {
          el.innerHTML = el.innerHTML.replace('Template', t['footer-template']);
        }
      }
    });
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
    const lang = detectLang();
    const t = await load(lang);
    apply(t);
    buildSelector(lang);
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init);
  else init();
})();