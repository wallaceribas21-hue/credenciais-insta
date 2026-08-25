/* =========================================================
   ASSESSORIA WR — comportamento

   A página é uma cena só. Uma constelação de triângulos vive
   atrás de tudo e muda de forma conforme a rolagem: sobe como
   curva no hero, se espalha nos números, monta a marca nos
   serviços, converge num ponto no relatório, vira onda no
   depoimento e grade nos planos.

   Cada seção pede sua forma pelo atributo data-forma.
   ========================================================= */

(function () {
  'use strict';

  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var celular = function () { return window.innerWidth <= 1000; };
  var limitar = function (v, a, b) { return v < a ? a : (v > b ? b : v); };

  /* =========================================================
     1. CONSTELAÇÃO
     ========================================================= */

  var CORES = [
    '#ff6b1a', '#ff6b1a', '#ff8a3d',        /* laranja da marca */
    '#8052ff', '#8052ff', '#9b7bff',        /* violeta          */
    '#ffb829',                              /* âmbar            */
    '#15846e', '#1fb392',                   /* verde            */
    '#4d7dff', '#e254c8'                    /* azul e magenta   */
  ];

  /* O traçado da marca. Trocar por outro path aqui muda a forma que a
     constelação monta na seção de serviços, e a logo no cabeçalho. */
  var MARCA = 'M11 13 20 35 24 23 28 35 37 13';
  var MARCA_CAIXA = 48;
  var MARCA_TRACO = 6.4;

  var tela = document.getElementById('ceu');
  var ctx = tela.getContext('2d');
  var L = 0, A = 0;
  var particulas = [];
  var formaAtual = 'curva';
  var amostraMarca = null;
  var quadro = 0;

  function normal() {
    var u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  /* onde a forma é desenhada. O texto sempre mora na metade esquerda,
     então a constelação mora na direita — menos no fecho, onde ela
     desce para o canto vazio embaixo do título. */
  function caixa(forma) {
    if (celular()) {
      var lado = Math.min(L * 0.94, A * 0.62);
      return { x: (L - lado) / 2, y: A * 0.5 - lado / 2, l: lado, a: lado };
    }
    if (forma === 'ponto') {
      var d = Math.min(L * 0.28, A * 0.4);
      return { x: L * 0.09, y: A * 0.48, l: d, a: d };
    }
    var w = L * 0.46;
    var h = Math.min(w, A * 0.82);
    return { x: L * 0.5, y: (A - h) / 2, l: w, a: h };
  }

  /* amostra o traçado da marca em pontos 0..1 */
  function amostrar() {
    var lado = 260;
    var off = document.createElement('canvas');
    off.width = off.height = lado;
    var o = off.getContext('2d');
    var e = lado / MARCA_CAIXA;
    o.setTransform(e, 0, 0, e, 0, 0);
    o.strokeStyle = '#fff';
    o.lineWidth = MARCA_TRACO;
    o.lineJoin = 'miter';
    o.stroke(new Path2D(MARCA));

    var dados = o.getImageData(0, 0, lado, lado).data;
    var achados = [];
    for (var y = 0; y < lado; y += 2) {
      for (var x = 0; x < lado; x += 2) {
        if (dados[(y * lado + x) * 4 + 3] > 120) achados.push({ x: x / lado, y: y / lado });
      }
    }
    /* embaralha para a nuvem preencher a forma de maneira uniforme */
    for (var i = achados.length - 1; i > 0; i--) {
      var j = (Math.random() * (i + 1)) | 0;
      var t = achados[i]; achados[i] = achados[j]; achados[j] = t;
    }
    return achados;
  }

  /* devolve o destino de uma partícula, em pixels */
  function destino(forma, i, n) {
    var c = caixa(forma);

    if (forma === 'dispersa') {
      return { x: Math.random() * L, y: Math.random() * A };
    }

    if (forma === 'marca') {
      if (!amostraMarca) amostraMarca = amostrar();
      var p = amostraMarca[i % amostraMarca.length];
      var ruido = 0.007;
      var escala = 1.12;                       /* a marca ocupa a caixa inteira */
      var folga = (1 - escala) / 2;
      return {
        x: c.x + (folga + (p.x + normal() * ruido) * escala) * c.l,
        y: c.y + (folga + (p.y + normal() * ruido) * escala) * c.a
      };
    }

    if (forma === 'ponto') {
      var rr = Math.pow(Math.random(), 3.2) * 0.5;
      var aa = Math.random() * Math.PI * 2;
      return { x: c.x + (0.5 + Math.cos(aa) * rr) * c.l, y: c.y + (0.5 + Math.sin(aa) * rr) * c.a };
    }

    if (forma === 'orbita') {
      var raio = Math.pow(Math.random(), 2.4) * 0.46;
      if (Math.random() < 0.18) raio = 0.40 + Math.random() * 0.05;
      var ang = Math.random() * Math.PI * 2;
      return { x: c.x + (0.5 + Math.cos(ang) * raio) * c.l, y: c.y + (0.5 + Math.sin(ang) * raio) * c.a };
    }

    if (forma === 'onda') {
      var t = i / n;
      var y = 0.5 + Math.sin(t * Math.PI * 3.2) * 0.24 + normal() * 0.05;
      return { x: c.x + t * c.l, y: c.y + y * c.a };
    }

    if (forma === 'grade') {
      var col = 19, lin = 12;
      var cx = (i % col) / (col - 1);
      var cy = (Math.floor(i / col) % lin) / (lin - 1);
      if (Math.floor(i / (col * lin)) % 2) return { x: c.x + Math.random() * c.l, y: c.y + Math.random() * c.a };
      return { x: c.x + (cx + normal() * 0.012) * c.l, y: c.y + (cy + normal() * 0.012) * c.a };
    }

    /* curva: fita que sobe da esquerda para a direita */
    var q = Math.pow(Math.random(), 0.88);
    var espessura = 0.15 * (1 - q * 0.45);
    return {
      x: c.x + (0.06 + q * 0.88 + normal() * 0.02) * c.l,
      y: c.y + (0.9 - Math.pow(q, 1.28) * 0.78 + normal() * espessura) * c.a
    };
  }

  function aplicar(forma) {
    formaAtual = forma;
    for (var i = 0; i < particulas.length; i++) {
      var p = particulas[i];
      if (p.ambiente) continue;                    /* a poeira nunca migra */
      var d = destino(forma, i, particulas.length);
      p.ax = d.x; p.ay = d.y;
    }
  }

  function semear() {
    var total = celular() ? 700 : limitar(Math.round(L * A / 900), 900, 2200);
    particulas = [];
    for (var i = 0; i < total; i++) {
      var ambiente = Math.random() < 0.12;
      particulas.push({
        x: Math.random() * L, y: Math.random() * A,
        ax: 0, ay: 0,
        ambiente: ambiente,
        tamanho: 1.5 + Math.random() * (ambiente ? 1.3 : 2.7),
        cor: CORES[(Math.random() * CORES.length) | 0],
        base: ambiente ? 0.1 + Math.random() * 0.16 : 0.4 + Math.random() * 0.6,
        giro: Math.random() * Math.PI * 2,
        giroVel: (Math.random() - 0.5) * 0.005,
        fase: Math.random() * Math.PI * 2,
        ritmo: 0.0004 + Math.random() * 0.0012,
        deriva: 2 + Math.random() * 7,
        passo: 0.03 + Math.random() * 0.045          /* cada uma chega no seu tempo */
      });
      if (ambiente) { var u = particulas[i]; u.ax = u.x; u.ay = u.y; }
    }
    aplicar(formaAtual);
    if (reduz) for (var k = 0; k < particulas.length; k++) { particulas[k].x = particulas[k].ax; particulas[k].y = particulas[k].ay; }
  }

  function medir() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    L = window.innerWidth;
    A = window.innerHeight;
    tela.width = Math.round(L * dpr);
    tela.height = Math.round(A * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function desenhar(tempo) {
    ctx.clearRect(0, 0, L, A);
    ctx.lineWidth = 1;
    ctx.globalAlpha = 1;
    var opacidadeGeral = (celular() ? 0.42 : 0.9) * (formaAtual === 'dispersa' ? 0.5 : (formaAtual === 'ponto' ? 0.7 : 1));

    for (var i = 0; i < particulas.length; i++) {
      var p = particulas[i];
      p.x += (p.ax - p.x) * p.passo;
      p.y += (p.ay - p.y) * p.passo;

      var onda = Math.sin(tempo * p.ritmo + p.fase);
      var px = p.x + onda * p.deriva;
      var py = p.y + Math.cos(tempo * p.ritmo * 0.8 + p.fase) * p.deriva * 0.6;
      var s = p.tamanho;

      ctx.globalAlpha = Math.max(0.05, p.base * (0.6 + 0.4 * onda)) * opacidadeGeral;
      ctx.strokeStyle = p.cor;
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate(p.giro + tempo * p.giroVel);
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

  function laco(t) {
    desenhar(t);
    quadro = requestAnimationFrame(laco);
  }

  medir();
  semear();
  if (reduz) desenhar(0);
  else quadro = requestAnimationFrame(laco);

  var esperaMedida;
  window.addEventListener('resize', function () {
    clearTimeout(esperaMedida);
    esperaMedida = setTimeout(function () {
      medir();
      semear();
      montarPalco();
    }, 220);
  });

  /* a seção que estiver no centro da tela manda na forma */
  if ('IntersectionObserver' in window) {
    var olhoForma = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) aplicar(e.target.getAttribute('data-forma'));
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    document.querySelectorAll('[data-forma]').forEach(function (s) { olhoForma.observe(s); });
  }

  /* =========================================================
     2. REVELAÇÃO DE TEXTO — palavra por palavra
     ========================================================= */

  function fatiar(el) {
    var palavras = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    palavras.forEach(function (w, i) {
      var fora = document.createElement('span');
      fora.className = 'palavra';
      var dentro = document.createElement('i');
      dentro.textContent = w;
      dentro.style.transitionDelay = (i * 55) + 'ms';
      fora.appendChild(dentro);
      el.appendChild(fora);
      if (i < palavras.length - 1) el.appendChild(document.createTextNode(' '));
    });
  }

  document.querySelectorAll('[data-revelar]').forEach(fatiar);

  var subindo = document.querySelectorAll('.sobe, .revela');
  if (reduz || !('IntersectionObserver' in window)) {
    subindo.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var olho = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); olho.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
    subindo.forEach(function (el) { olho.observe(el); });
  }

  /* =========================================================
     3. DESTAQUE PALAVRA A PALAVRA NO DEPOIMENTO
     ========================================================= */

  var destaques = [];
  document.querySelectorAll('[data-destacar]').forEach(function (el) {
    var palavras = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    palavras.forEach(function (w, i) {
      var s = document.createElement('span');
      s.className = 'p';
      s.textContent = w;
      el.appendChild(s);
      if (i < palavras.length - 1) el.appendChild(document.createTextNode(' '));
    });
    destaques.push({ el: el, spans: el.querySelectorAll('.p') });
  });

  function pintarDestaques() {
    destaques.forEach(function (d) {
      var r = d.el.getBoundingClientRect();
      var curso = r.height + A * 0.35;
      var avanco = limitar((A * 0.86 - r.top) / curso, 0, 1);
      var corte = Math.round(avanco * d.spans.length);
      for (var i = 0; i < d.spans.length; i++) d.spans[i].classList.toggle('is-on', i < corte);
    });
  }

  /* =========================================================
     4. CONTAGEM DOS NÚMEROS
     ========================================================= */

  document.querySelectorAll('[data-contar]').forEach(function (el) {
    var alvo = parseInt(el.getAttribute('data-contar'), 10);
    if (reduz || !('IntersectionObserver' in window)) { el.textContent = alvo; return; }
    var o = new IntersectionObserver(function (entradas) {
      if (!entradas[0].isIntersecting) return;
      o.disconnect();
      var t0 = performance.now(), dur = 1100;
      (function passo(t) {
        var p = limitar((t - t0) / dur, 0, 1);
        el.textContent = Math.round(alvo * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(passo);
      })(t0);
    }, { threshold: 0.6 });
    o.observe(el);
  });

  /* =========================================================
     4b. O RELATÓRIO — números contados, barras que sobem,
         dica ao passar o mouse e uma inclinação de leve
     ========================================================= */

  function formatar(v, tipo) {
    if (tipo === 'moeda0') return 'R$ ' + Math.round(v).toLocaleString('pt-BR');
    if (tipo === 'moeda2') return 'R$ ' + v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return Math.round(v).toLocaleString('pt-BR');
  }

  var relato = document.getElementById('relato');

  if (relato) {
    var valores = relato.querySelectorAll('[data-valor]');

    function preencher(instantaneo) {
      valores.forEach(function (el) {
        var alvo = parseFloat(el.getAttribute('data-valor'));
        var tipo = el.getAttribute('data-formato');
        if (instantaneo) { el.textContent = formatar(alvo, tipo); return; }
        var t0 = performance.now(), dur = 1200;
        (function passo(t) {
          var q = limitar((t - t0) / dur, 0, 1);
          el.textContent = formatar(alvo * (1 - Math.pow(1 - q, 3)), tipo);
          if (q < 1) requestAnimationFrame(passo);
        })(t0);
      });
    }

    if (reduz || !('IntersectionObserver' in window)) {
      relato.classList.add('is-in');
      preencher(true);
    } else {
      var olhoRelato = new IntersectionObserver(function (entradas) {
        if (!entradas[0].isIntersecting) return;
        olhoRelato.disconnect();
        relato.classList.add('is-in');
        preencher(false);
      }, { threshold: 0.35 });
      olhoRelato.observe(relato);
    }

    /* dica por barra */
    var dica = document.getElementById('dica');
    var barras = relato.querySelectorAll('.barra');

    barras.forEach(function (b) {
      function mostrar() {
        dica.textContent = b.getAttribute('data-dia') + ': ' + b.getAttribute('data-n') + ' contatos';
        dica.classList.add('is-on');
        var area = b.closest('.grafico__area').getBoundingClientRect();
        var r = b.getBoundingClientRect();
        dica.style.left = (r.left - area.left + r.width / 2) + 'px';
      }
      function esconder() { dica.classList.remove('is-on'); }
      b.addEventListener('mouseenter', mostrar);
      b.addEventListener('focus', mostrar);
      b.addEventListener('mouseleave', esconder);
      b.addEventListener('blur', esconder);
      b.addEventListener('click', function (e) { e.preventDefault(); });
    });

    /* inclinação de leve seguindo o ponteiro, só no desktop */
    var folha = relato.querySelector('.relato__folha');
    if (!reduz) {
      relato.addEventListener('mousemove', function (e) {
        if (celular()) return;
        var r = relato.getBoundingClientRect();
        var gx = (e.clientX - r.left) / r.width - 0.5;
        var gy = (e.clientY - r.top) / r.height - 0.5;
        folha.style.transform = 'perspective(1100px) rotateY(' + (gx * 4.5) + 'deg) rotateX(' + (-gy * 3.5) + 'deg)';
      });
      relato.addEventListener('mouseleave', function () { folha.style.transform = ''; });
    }
  }

  /* =========================================================
     5. PALCO FIXO DOS SERVIÇOS
     ========================================================= */

  var palco = document.getElementById('servicos');
  var caixaPassos = document.getElementById('passos');
  var passos = caixaPassos ? caixaPassos.querySelectorAll('.passo') : [];
  var marcas = document.getElementById('indice');

  function montarPalco() {
    if (!palco) return;
    if (celular()) { palco.style.height = ''; caixaPassos.style.height = ''; return; }
    palco.style.height = (passos.length * 100) + 'vh';
    var maior = 0;
    passos.forEach(function (p) {
      var altura = p.scrollHeight;
      if (altura > maior) maior = altura;
    });
    caixaPassos.style.height = maior + 'px';
    caixaPassos.style.minHeight = '0';
  }

  function moverPalco() {
    if (!palco || celular()) return;
    var r = palco.getBoundingClientRect();
    var curso = palco.offsetHeight - A;
    var avanco = limitar(-r.top / curso, 0, 0.9999);
    var idx = Math.floor(avanco * passos.length);
    passos.forEach(function (p, i) { p.classList.toggle('is-active', i === idx); });
    if (marcas) Array.prototype.forEach.call(marcas.children, function (m, i) {
      m.classList.toggle('is-active', i === idx);
    });
  }

  montarPalco();

  /* =========================================================
     6. LETREIRO DE CLIENTES
     ========================================================= */

  var trilho = document.getElementById('trilho');
  var deslocamento = 0, metade = 0, velocidadeExtra = 0;

  if (trilho) {
    trilho.innerHTML += trilho.innerHTML;   /* duplica para o laço não ter emenda */
    metade = trilho.scrollWidth / 2;
    if (!reduz) (function correr() {
      deslocamento -= 0.55 + velocidadeExtra;
      velocidadeExtra *= 0.92;
      if (deslocamento <= -metade) deslocamento += metade;
      if (deslocamento > 0) deslocamento -= metade;
      trilho.style.transform = 'translate3d(' + deslocamento + 'px,0,0)';
      requestAnimationFrame(correr);
    })();
  }

  /* =========================================================
     7. ROLAGEM — barra de progresso, menu e o resto
     ========================================================= */

  var barra = document.getElementById('progresso');
  var nav = document.getElementById('nav');
  var ultimoY = window.scrollY;
  var pedido = false;

  function aoRolar() {
    var y = window.scrollY;
    var curso = document.documentElement.scrollHeight - A;
    if (barra) barra.style.transform = 'scaleX(' + (curso > 0 ? limitar(y / curso, 0, 1) : 0) + ')';
    if (nav) nav.classList.toggle('is-baixo', y > 40);
    velocidadeExtra += Math.min(Math.abs(y - ultimoY) * 0.03, 2.2);
    ultimoY = y;
    moverPalco();
    pintarDestaques();
    pedido = false;
  }

  window.addEventListener('scroll', function () {
    if (pedido) return;
    pedido = true;
    requestAnimationFrame(aoRolar);
  }, { passive: true });

  aoRolar();

  /* =========================================================
     8. MENU, FORMULÁRIO, ANO
     ========================================================= */

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
                'E-mail: ' + d.get('email') + '\nWhatsApp: ' + d.get('telefone') +
                (d.get('mensagem') ? '\nContexto: ' + d.get('mensagem') : '');
    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
    aviso.textContent = 'Abrimos o WhatsApp com a mensagem pronta.';
  });

  document.getElementById('ano').textContent = new Date().getFullYear();

  window.addEventListener('load', montarPalco);
})();
