/* Assessoria WR
   1. constelação de triângulos (a imagem da marca, desenhada em canvas)
   2. menu, entrada no scroll, depoimentos, dúvidas e formulário          */

(function () {
  'use strict';

  var semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------
     1. CONSTELAÇÃO
     Milhares de triângulos pequenos, contorno de 1px, em cores vivas.
     Duas formas: "curva" (crescimento) e "orbita" (contas convergindo).
     ------------------------------------------------------------------ */

  var CORES = [
    '#8052ff', '#8052ff', '#8052ff', '#9b7bff',   /* violeta domina */
    '#ffb829', '#ffb829',                          /* âmbar pontua   */
    '#15846e', '#1fb392',                          /* verde fundo    */
    '#e254c8',                                     /* magenta        */
    '#4d7dff'                                      /* azul           */
  ];

  function aleatorioNormal() {
    var u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  /* devolve um ponto em coordenadas 0..1 conforme a forma pedida */
  function ponto(forma) {
    if (forma === 'orbita') {
      var raio = Math.pow(Math.random(), 2.3) * 0.46;
      if (Math.random() < 0.16) raio = 0.40 + Math.random() * 0.06;   /* anel externo */
      var ang = Math.random() * Math.PI * 2;
      return { x: 0.5 + Math.cos(ang) * raio * 1.02, y: 0.5 + Math.sin(ang) * raio * 0.94 };
    }

    /* curva: fita que sobe da esquerda para a direita e afina no topo */
    var t = Math.pow(Math.random(), 0.88);
    var x = 0.09 + t * 0.83;
    var y = 0.86 - Math.pow(t, 1.28) * 0.70;
    var espessura = 0.135 * (1 - t * 0.45);
    y += aleatorioNormal() * espessura;
    x += aleatorioNormal() * 0.02;
    return { x: x, y: y };
  }

  function constelacao(canvas) {
    var ctx = canvas.getContext('2d');
    var forma = canvas.getAttribute('data-constelacao');
    var particulas = [];
    var largura = 0, altura = 0, quadro = 0, visivel = true;

    function medir() {
      var r = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      largura = r.width;
      altura = r.height;
      canvas.width = Math.round(largura * dpr);
      canvas.height = Math.round(altura * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function semear() {
      var area = largura * altura;
      var total = Math.max(900, Math.min(2800, Math.round(area / 165)));
      particulas = [];
      for (var i = 0; i < total; i++) {
        var ambiente = Math.random() < 0.10;          /* poeira em volta */
        var p = ambiente ? { x: Math.random(), y: Math.random() } : ponto(forma);
        particulas.push({
          x: p.x, y: p.y,
          tamanho: 1.5 + Math.random() * (ambiente ? 1.4 : 2.8),
          cor: CORES[(Math.random() * CORES.length) | 0],
          base: ambiente ? 0.14 + Math.random() * 0.2 : 0.42 + Math.random() * 0.58,
          giro: Math.random() * Math.PI * 2,
          giroVel: (Math.random() - 0.5) * 0.004,
          fase: Math.random() * Math.PI * 2,
          ritmo: 0.0004 + Math.random() * 0.0011,
          deriva: 2 + Math.random() * 7
        });
      }
    }

    function desenhar(tempo) {
      ctx.clearRect(0, 0, largura, altura);
      ctx.lineWidth = 1;
      for (var i = 0; i < particulas.length; i++) {
        var p = particulas[i];
        var onda = Math.sin(tempo * p.ritmo + p.fase);
        var px = p.x * largura + onda * p.deriva;
        var py = p.y * altura + Math.cos(tempo * p.ritmo * 0.8 + p.fase) * p.deriva * 0.6;
        var s = p.tamanho;
        var giro = p.giro + tempo * p.giroVel;

        ctx.globalAlpha = Math.max(0.06, p.base * (0.62 + 0.38 * onda));
        ctx.strokeStyle = p.cor;
        ctx.save();
        ctx.translate(px, py);
        ctx.rotate(giro);
        ctx.beginPath();
        ctx.moveTo(0, -s);
        ctx.lineTo(s * 0.87, s * 0.5);
        ctx.lineTo(-s * 0.87, s * 0.5);
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
      }
      ctx.globalAlpha = 1;
    }

    function animar(tempo) {
      desenhar(tempo);
      if (visivel) quadro = requestAnimationFrame(animar);
    }

    function iniciar() {
      medir();
      semear();
      if (semMovimento) { desenhar(0); return; }
      cancelAnimationFrame(quadro);
      quadro = requestAnimationFrame(animar);
    }

    iniciar();

    /* só anima o que está na tela */
    if ('IntersectionObserver' in window && !semMovimento) {
      new IntersectionObserver(function (entradas) {
        visivel = entradas[0].isIntersecting;
        if (visivel) { cancelAnimationFrame(quadro); quadro = requestAnimationFrame(animar); }
        else cancelAnimationFrame(quadro);
      }, { rootMargin: '160px' }).observe(canvas);
    }

    var espera;
    window.addEventListener('resize', function () {
      clearTimeout(espera);
      espera = setTimeout(iniciar, 200);
    });
  }

  document.querySelectorAll('[data-constelacao]').forEach(constelacao);

  /* ------------------------------------------------------------------
     2. MENU
     ------------------------------------------------------------------ */

  var abrir = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');

  abrir.addEventListener('click', function () {
    var aberto = links.classList.toggle('is-open');
    abrir.setAttribute('aria-expanded', String(aberto));
  });
  links.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      links.classList.remove('is-open');
      abrir.setAttribute('aria-expanded', 'false');
    }
  });

  /* ------------------------------------------------------------------
     3. ENTRADA NO SCROLL
     ------------------------------------------------------------------ */

  var subindo = document.querySelectorAll('.rise');
  if (semMovimento || !('IntersectionObserver' in window)) {
    subindo.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var olho = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('is-in');
          olho.unobserve(entrada.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    subindo.forEach(function (el) { olho.observe(el); });
  }

  /* ------------------------------------------------------------------
     4. DEPOIMENTOS
     ------------------------------------------------------------------ */

  var falas = Array.prototype.slice.call(document.querySelectorAll('[data-slide]'));
  var pontos = document.getElementById('dots');
  var atual = 0;
  var relogio;

  function mostrar(i) {
    atual = (i + falas.length) % falas.length;
    falas.forEach(function (f, n) { f.hidden = n !== atual; });
    Array.prototype.forEach.call(pontos.children, function (d, n) {
      d.classList.toggle('is-active', n === atual);
      d.setAttribute('aria-selected', String(n === atual));
    });
  }

  function agendar() {
    if (semMovimento) return;
    clearInterval(relogio);
    relogio = setInterval(function () { mostrar(atual + 1); }, 8000);
  }

  falas.forEach(function (_, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('role', 'tab');
    b.setAttribute('aria-label', 'Depoimento ' + (i + 1));
    b.addEventListener('click', function () { mostrar(i); agendar(); });
    pontos.appendChild(b);
  });
  mostrar(0);
  agendar();

  /* ------------------------------------------------------------------
     5. DÚVIDAS
     ------------------------------------------------------------------ */

  document.querySelectorAll('.faq__q').forEach(function (botao) {
    var item = botao.parentElement;
    var painel = item.querySelector('.faq__a');
    botao.setAttribute('aria-expanded', 'false');

    botao.addEventListener('click', function () {
      var abrindo = !item.classList.contains('is-open');
      document.querySelectorAll('.faq__item.is-open').forEach(function (outro) {
        outro.classList.remove('is-open');
        outro.querySelector('.faq__a').style.maxHeight = null;
        outro.querySelector('.faq__q').setAttribute('aria-expanded', 'false');
      });
      if (abrindo) {
        item.classList.add('is-open');
        painel.style.maxHeight = painel.scrollHeight + 'px';
        botao.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ------------------------------------------------------------------
     6. FORMULÁRIO — sem backend: monta a mensagem e abre o WhatsApp
     ------------------------------------------------------------------ */

  var WHATSAPP = '5500000000000';   /* trocar pelo número real */

  var form = document.getElementById('form');
  var aviso = document.getElementById('formStatus');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var faltando = ['nome', 'empresa', 'email', 'telefone'].filter(function (k) {
      return !String(d.get(k) || '').trim();
    });
    if (faltando.length) {
      aviso.textContent = 'Preencha nome, empresa, e-mail e WhatsApp para continuar.';
      return;
    }
    var texto = 'Oi! Sou ' + d.get('nome') + ', da ' + d.get('empresa') + '.\n' +
                'E-mail: ' + d.get('email') + '\n' +
                'WhatsApp: ' + d.get('telefone') +
                (d.get('mensagem') ? '\nContexto: ' + d.get('mensagem') : '');
    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
    aviso.textContent = 'Abrimos o WhatsApp com a mensagem pronta.';
  });

  document.getElementById('ano').textContent = new Date().getFullYear();
})();
