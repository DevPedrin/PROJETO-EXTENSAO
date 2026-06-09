(function () {
  'use strict';

  // ─── 1. MODAL DE REPRODUÇÃO DE VÍDEO YOUTUBE ───
  function initVideoModal() {
    const videoCards = document.querySelectorAll('.video-card');
    const modal = document.getElementById('video-modal');
    const closeBtn = document.getElementById('modal-close');
    const iframe = document.getElementById('modal-iframe');

    if (!videoCards.length || !modal || !closeBtn || !iframe) {
      return; // Elementos não presentes nesta página
    }

    console.log("Inicializando script do modal de vídeo...");

    // Função para extrair o ID de vídeo do YouTube a partir de qualquer URL comum
    function getYouTubeId(url) {
      const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
      const match = url.match(regExp);
      return (match && match[2].length === 11) ? match[2] : null;
    }

    // Abre o modal ao clicar no card de vídeo
    videoCards.forEach(function (card) {
      card.addEventListener('click', function () {
        const videoUrl = card.getAttribute('data-video-url');
        if (!videoUrl) return;

        const videoId = getYouTubeId(videoUrl);
        if (videoId) {
          iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0`;
          modal.classList.add('open');
          document.body.style.overflow = 'hidden'; // Impede scroll do body
        }
      });
    });

    // Função para fechar o modal e pausar o vídeo (limpa o src do iframe)
    function fecharModal() {
      modal.classList.remove('open');
      iframe.src = '';
      document.body.style.overflow = ''; // Restaura scroll
    }

    closeBtn.addEventListener('click', fecharModal);

    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        fecharModal();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        fecharModal();
      }
    });
  }

  // ─── 2. FILTRAGEM DINÂMICA DE DELEGACIAS (RN006) ───
  function initDelegaciasFilter() {
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroTexto = document.getElementById('filtro-texto');
    const filtroCidade = document.getElementById('filtro-cidade');
    const itens = document.querySelectorAll('.delegacia-item');

    if (!filtroTipo || !filtroTexto || !filtroCidade || !itens.length) {
      return; // Elementos não presentes nesta página
    }

    console.log("Inicializando script de filtragem de delegacias...");

    function filtrar() {
      const tipoVal = filtroTipo.value.toLowerCase().trim();
      const textoVal = filtroTexto.value.toLowerCase().trim();
      const cidadeVal = filtroCidade.value.toLowerCase().trim();

      itens.forEach(function (item) {
        const itemTipo = (item.getAttribute('data-tipo') || '').toLowerCase().trim();
        const itemCidade = (item.getAttribute('data-cidade') || '').toLowerCase().trim();
        const itemNome = (item.querySelector('h3') ? item.querySelector('h3').textContent : '').toLowerCase().trim();

        // Regras de correspondência dos filtros
        const bateTipo = !tipoVal || itemTipo === tipoVal;
        const bateCidade = !cidadeVal || itemCidade === cidadeVal;
        
        // A busca por texto pesquisa no nome do órgão (h3) e no conteúdo geral do card
        const textoCompleto = itemNome + ' ' + item.textContent.toLowerCase();
        const bateTexto = !textoVal || textoCompleto.includes(textoVal);

        if (bateTipo && bateCidade && bateTexto) {
          item.style.display = ''; // Exibe o item
        } else {
          item.style.display = 'none'; // Oculta o item
        }
      });
    }

    // Escuta eventos de alteração de estado dos filtros
    filtroTipo.addEventListener('change', filtrar);
    filtroTexto.addEventListener('input', filtrar);
    filtroCidade.addEventListener('change', filtrar);
  }

  // ─── 3. INICIALIZADOR GLOBAL ───
  function init() {
    initVideoModal();
    initDelegaciasFilter();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
