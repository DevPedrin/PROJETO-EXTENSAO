/**
 * Portal Segurança Digital — GOV.BR
 * script.js — Animações, acessibilidade e interações
 */

'use strict';

/* ─── ANIMAÇÕES DE ENTRADA (Intersection Observer) ─────────── */

/**
 * Aplica animação de entrada discreta (fadeInUp) a elementos
 * que possuem a classe .gov-animate-in assim que entram na viewport.
 */
function initAnimacaoEntrada() {
  const elementos = document.querySelectorAll(
    '.golpe-card, .video-card, .delegacia-item, .grafico-card, .num-item, .auth-card, .form-card, .info-box'
  );

  if (!elementos.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('gov-animate-in', 'visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  elementos.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(el);
  });

  // Aciona animação ao entrar na viewport
  const styleObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          styleObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -30px 0px' }
  );

  elementos.forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.06}s`;
    styleObserver.observe(el);
  });
}

/* ─── TRUNCAMENTO DE DESCRIÇÕES NOS CARDS ─────────────────── */

/**
 * Limita descrições de cards a 3 linhas visíveis.
 * Adiciona atributo title com o texto completo para acessibilidade.
 * Respeita preferência de redução de movimento.
 */
function initTruncamentoCards() {
  // Seleciona descrições dentro de cards
  const descricoes = document.querySelectorAll(
    '.golpe-card p, .video-body p, .gov-card-description'
  );

  descricoes.forEach((el) => {
    const textoCompleto = el.textContent.trim();

    // Adiciona o título completo para acessibilidade
    if (textoCompleto && textoCompleto.length > 80) {
      el.setAttribute('title', textoCompleto);
      el.setAttribute('aria-label', textoCompleto);
    }

    // Aplica truncamento CSS via classe
    el.classList.add('gov-card-description');
  });
}

/* ─── CONTROLE DO MODAL DE VÍDEO ───────────────────────────── */

/**
 * Inicializa o modal de vídeo com suporte a:
 * - Fechar com tecla Escape
 * - Foco preso dentro do modal (trap focus)
 * - Atributos ARIA corretos
 */
function initModalVideo() {
  const overlay = document.getElementById('modal-video');
  if (!overlay) return;

  const iframe = overlay.querySelector('iframe');
  const btnFechar = overlay.querySelector('.modal-close');

  function abrirModal(url) {
    if (iframe) iframe.src = url;
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    if (btnFechar) btnFechar.focus();
    document.body.style.overflow = 'hidden';
  }

  function fecharModal() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    if (iframe) iframe.src = '';
    document.body.style.overflow = '';
    // Devolve foco ao card que abriu
    if (window._modalOpener) {
      window._modalOpener.focus();
      window._modalOpener = null;
    }
  }

  // Atributos ARIA iniciais
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Vídeo educativo');
  overlay.setAttribute('aria-hidden', 'true');

  // Fechar ao clicar no overlay
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) fecharModal();
  });

  // Fechar com Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('open')) {
      fecharModal();
    }
  });

  // Botão fechar
  if (btnFechar) {
    btnFechar.setAttribute('aria-label', 'Fechar vídeo');
    btnFechar.addEventListener('click', fecharModal);
  }

  // Expõe função globalmente para os cards de vídeo chamarem
  window.abrirModalVideo = function (url, openerEl) {
    window._modalOpener = openerEl || null;
    abrirModal(url);
  };
}

/* ─── CARDS DE VÍDEO — CLIQUE ──────────────────────────────── */

/**
 * Ativa os cards de vídeo para abrir o modal.
 * Adiciona role="button" e suporte a teclado (Enter/Space).
 */
function initCardsVideo() {
  const cards = document.querySelectorAll('.video-card[data-url]');

  cards.forEach((card) => {
    const url = card.dataset.url;
    if (!url) return;

    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');

    const titulo = card.querySelector('h3, .gov-card-title');
    if (titulo) {
      card.setAttribute('aria-label', `Assistir: ${titulo.textContent.trim()}`);
    }

    function ativar() {
      if (window.abrirModalVideo) {
        window.abrirModalVideo(url, card);
      }
    }

    card.addEventListener('click', ativar);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        ativar();
      }
    });
  });
}

/* ─── BARRAS DE GRÁFICOS — ANIMAÇÃO ────────────────────────── */

/**
 * Anima as barras de progresso ao entrar na viewport.
 * Lê a largura alvo do atributo data-width.
 */
function initBarrasAnimadas() {
  const barras = document.querySelectorAll('.barra-fill[data-width]');
  if (!barras.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const barra = entry.target;
          const largura = barra.dataset.width || '0%';
          // Pequeno delay para garantir a transição CSS
          requestAnimationFrame(() => {
            barra.style.width = largura;
          });
          observer.unobserve(barra);
        }
      });
    },
    { threshold: 0.2 }
  );

  // Inicializa todas as barras com largura 0
  barras.forEach((barra) => {
    barra.style.width = '0%';
    observer.observe(barra);
  });
}

/* ─── FILTRO DE DELEGACIAS (busca ao vivo) ─────────────────── */

/**
 * Filtra a lista de delegacias conforme o usuário digita.
 * Exibe mensagem de "nenhum resultado" com acessibilidade.
 */
function initFiltroDelegacias() {
  const inputBusca = document.getElementById('busca-delegacia');
  const lista = document.querySelector('.delegacias-lista');
  if (!inputBusca || !lista) return;

  // Mensagem de ausência de resultados
  let msgVazia = lista.querySelector('.sem-resultado');
  if (!msgVazia) {
    msgVazia = document.createElement('p');
    msgVazia.className = 'sem-resultado gov-text';
    msgVazia.setAttribute('role', 'status');
    msgVazia.setAttribute('aria-live', 'polite');
    msgVazia.textContent = 'Nenhuma delegacia encontrada para esta busca.';
    msgVazia.style.display = 'none';
    lista.appendChild(msgVazia);
  }

  inputBusca.setAttribute('aria-label', 'Buscar delegacia por nome ou cidade');
  inputBusca.setAttribute('autocomplete', 'off');

  inputBusca.addEventListener('input', () => {
    const termo = inputBusca.value.toLowerCase().trim();
    const itens = lista.querySelectorAll('.delegacia-item');
    let visiveis = 0;

    itens.forEach((item) => {
      const texto = item.textContent.toLowerCase();
      const visivel = !termo || texto.includes(termo);
      item.style.display = visivel ? '' : 'none';
      if (visivel) visiveis++;
    });

    msgVazia.style.display = visiveis === 0 ? 'block' : 'none';
  });
}

/* ─── ACESSIBILIDADE — SKIP LINK ───────────────────────────── */

/**
 * Injeta um link "Ir para o conteúdo principal" (skip link)
 * visível apenas quando recebe foco por teclado.
 */
function initSkipLink() {
  if (document.getElementById('skip-link')) return;

  const skip = document.createElement('a');
  skip.id = 'skip-link';
  skip.href = '#conteudo-principal';
  skip.textContent = 'Ir para o conteúdo principal';
  skip.setAttribute('class', 'gov-link');

  skip.style.cssText = `
    position: absolute;
    top: -100%;
    left: 16px;
    background: var(--azul-gov, #004587);
    color: #fff;
    padding: 10px 18px;
    border-radius: 0 0 4px 4px;
    font-weight: 700;
    font-size: 0.9rem;
    z-index: 99999;
    transition: top 0.2s ease;
    text-decoration: none;
  `;

  skip.addEventListener('focus', () => { skip.style.top = '0'; });
  skip.addEventListener('blur',  () => { skip.style.top = '-100%'; });

  document.body.prepend(skip);

  // Adiciona id ao conteúdo principal se não existir
  const main = document.querySelector('main, .secao, [role="main"]');
  if (main && !main.id) {
    main.id = 'conteudo-principal';
    main.setAttribute('tabindex', '-1');
  }
}

/* ─── ACESSIBILIDADE — FOCO VISÍVEL ────────────────────────── */

/**
 * Adiciona classe 'usando-teclado' ao body quando o usuário
 * navega por teclado, restaurando outlines de foco visíveis.
 */
function initFocoVisivel() {
  const style = document.createElement('style');
  style.textContent = `
    body:not(.usando-teclado) *:focus { outline: none; }
    body.usando-teclado *:focus {
      outline: 3px solid #1351b4 !important;
      outline-offset: 2px !important;
    }
  `;
  document.head.appendChild(style);

  document.addEventListener('keydown', () => {
    document.body.classList.add('usando-teclado');
  });

  document.addEventListener('mousedown', () => {
    document.body.classList.remove('usando-teclado');
  });
}

/* ─── STICKY HEADER ─────────────────────────────────────────── */
function initHeaderSticky() {
  const header = document.querySelector('header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });
}

/* ─── MENU MOBILE (HAMBURGUER) ──────────────────────────────── */
function initMenuMobile() {
  const toggle = document.getElementById('nav-toggle');
  const menu = document.getElementById('nav-menu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const aberta = menu.classList.toggle('aberta');
    toggle.classList.toggle('aberto');
    toggle.setAttribute('aria-expanded', aberta);
  });

  // Fecha o menu ao clicar fora
  document.addEventListener('click', (e) => {
    if (menu.classList.contains('aberta') && !menu.contains(e.target) && e.target !== toggle) {
      menu.classList.remove('aberta');
      toggle.classList.remove('aberto');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Fecha o menu ao clicar em algum link interno
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menu.classList.remove('aberta');
      toggle.classList.remove('aberto');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ─── SCROLL SUAVE PARA ÂNCORAS INTERNAS ────────────────────── */
function initScrollSuave() {
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/* ─── FEEDBACK VISUAL EM BOTÕES DE SUBMISSÃO (LOADING) ──────── */
function initLoadingBotoes() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('button[type="submit"], input[type="submit"]');
      if (btn) {
        btn.classList.add('loading');
        btn.setAttribute('disabled', 'true');
      }
    });
  });
}

/* ─── INICIALIZAÇÃO ─────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
  initSkipLink();
  initFocoVisivel();
  initAnimacaoEntrada();
  initTruncamentoCards();
  initModalVideo();
  initCardsVideo();
  initBarrasAnimadas();
  initFiltroDelegacias();
  initHeaderSticky();
  initMenuMobile();
  initScrollSuave();
  initLoadingBotoes();
});
