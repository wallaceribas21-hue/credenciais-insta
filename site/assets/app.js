/* Assessoria WR — comportamento minimo: nav, revelacao, depoimentos, faq, form. */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav: fundo elevado ao rolar */
  var nav = document.getElementById('nav');
  var onScroll = function () {
    nav.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* nav: menu no celular */
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  toggle.addEventListener('click', function () {
    var open = links.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  links.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  /* revelacao no scroll */
  var revealables = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* depoimentos com indicador de bolinha */
  var slides = Array.prototype.slice.call(document.querySelectorAll('[data-slide]'));
  var dots = document.getElementById('dots');
  var atual = 0;
  var timer;

  function mostrar(i) {
    atual = (i + slides.length) % slides.length;
    slides.forEach(function (s, n) { s.hidden = n !== atual; });
    Array.prototype.forEach.call(dots.children, function (d, n) {
      d.classList.toggle('is-active', n === atual);
      d.setAttribute('aria-selected', String(n === atual));
    });
  }

  function agendar() {
    if (reduced) return;
    clearInterval(timer);
    timer = setInterval(function () { mostrar(atual + 1); }, 7000);
  }

  slides.forEach(function (_, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('role', 'tab');
    b.setAttribute('aria-label', 'Depoimento ' + (i + 1));
    b.addEventListener('click', function () { mostrar(i); agendar(); });
    dots.appendChild(b);
  });
  mostrar(0);
  agendar();

  /* faq */
  document.querySelectorAll('.faq__q').forEach(function (btn) {
    var item = btn.parentElement;
    var painel = item.querySelector('.faq__a');
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      var abrindo = !item.classList.contains('is-open');
      document.querySelectorAll('.faq__item.is-open').forEach(function (aberto) {
        aberto.classList.remove('is-open');
        aberto.querySelector('.faq__a').style.maxHeight = null;
        aberto.querySelector('.faq__q').setAttribute('aria-expanded', 'false');
      });
      if (abrindo) {
        item.classList.add('is-open');
        painel.style.maxHeight = painel.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* form: sem backend ainda, monta a mensagem no WhatsApp */
  var form = document.getElementById('form');
  var status = document.getElementById('formStatus');
  var WHATSAPP = '5500000000000'; // trocar pelo numero real

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var faltando = ['nome', 'empresa', 'email', 'telefone'].filter(function (k) {
      return !String(d.get(k) || '').trim();
    });
    if (faltando.length) {
      status.textContent = 'Preencha nome, empresa, e-mail e WhatsApp para continuar.';
      return;
    }
    var texto = 'Oi! Sou ' + d.get('nome') + ', da ' + d.get('empresa') + '.\n' +
                'E-mail: ' + d.get('email') + '\n' +
                'WhatsApp: ' + d.get('telefone') + '\n' +
                (d.get('mensagem') ? 'Contexto: ' + d.get('mensagem') : '');
    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
    status.textContent = 'Abrimos o WhatsApp com sua mensagem pronta. Se não abrir, chame direto pelo link acima.';
  });

  /* ano do rodape */
  document.getElementById('ano').textContent = new Date().getFullYear();
})();
