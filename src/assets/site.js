/* CV Izdihaar 84 — interaksi situs: menu, filter, formulir pertanyaan bisnis */
(function () {
  'use strict';
  var SITE = window.SITE || { contact: {}, routing: {} };

  /* Menu mobile */
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('nav');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  }
  if (btn && nav) {
    btn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); btn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) setMenu(false);
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1080 && nav.classList.contains('open')) setMenu(false); });
  }

  /* Header saat digulir */
  var hdr = document.querySelector('.hdr');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Animasi muncul saat digulir (konten tetap terlihat bila JavaScript atau observer tidak tersedia) */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    var sel = '.sec-head, .group-root, .company, .overview-media, .overview-body, .facts, .svc-card, .steps li, .client, .post, .card, .feature-media, .feature-body, .proj, .profile-text, .profile-side, .panel-navy, .value, .form, .info, .proj-intro, .track-in';
    var els = Array.prototype.slice.call(document.querySelectorAll(sel));
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) {
      var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      if (el.matches('.company, .svc-card, .steps li, .client, .post, .card')) el.style.setProperty('--d', Math.min(sibs, 5) * 0.08 + 's');
      var r = el.getBoundingClientRect();
      el.classList.add('rv');
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('in');
      else io.observe(el);
    });
    document.documentElement.classList.add('anim');
    window.addEventListener('beforeprint', function () { els.forEach(function (el) { el.classList.add('in'); }); });
  }

  /* Filter kategori + pencarian (Berita, Proyek) */
  document.querySelectorAll('[data-filter-group]').forEach(function (group) {
    var list = document.getElementById(group.getAttribute('data-filter-group'));
    if (!list) return;
    var items = Array.prototype.slice.call(list.querySelectorAll('[data-cat]'));
    var empty = document.getElementById(list.id + '-empty');
    var search = document.querySelector('[data-search="' + list.id + '"]');
    var current = 'semua';
    function apply() {
      var q = search ? search.value.trim().toLowerCase() : '';
      var shown = 0;
      items.forEach(function (it) {
        var okCat = current === 'semua' || it.getAttribute('data-cat') === current;
        var okQ = !q || it.textContent.toLowerCase().indexOf(q) !== -1;
        it.hidden = !(okCat && okQ);
        if (okCat && okQ) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    }
    group.querySelectorAll('button[data-value]').forEach(function (b) {
      b.addEventListener('click', function () {
        current = b.getAttribute('data-value');
        group.querySelectorAll('button[data-value]').forEach(function (x) {
          x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
        });
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
  });

  /* Formulir pertanyaan bisnis */
  var form = document.getElementById('inquiry-form');
  if (form) {
    var need = document.getElementById('f-kebutuhan');
    var route = document.getElementById('route');
    var result = document.getElementById('result');
    var out = document.getElementById('result-text');
    var copyBtn = document.getElementById('copy-btn');
    var copyState = document.getElementById('copy-state');
    var waLink = document.getElementById('wa-link');
    var noChannel = document.getElementById('no-channel');

    function showRoute() {
      var r = SITE.routing[need.value];
      route.hidden = !r;
      if (r) route.textContent = r;
    }
    need.addEventListener('change', showRoute);
    showRoute();

    function setErr(el, msg) {
      var err = document.getElementById(el.id + '-err');
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (err) err.textContent = msg || '';
      return !msg;
    }
    function validate() {
      var ok = true, first = null;
      var nama = document.getElementById('f-nama');
      var email = document.getElementById('f-email');
      var telp = document.getElementById('f-telepon');
      var pesan = document.getElementById('f-pesan');
      function check(el, msg) { if (!setErr(el, msg)) { ok = false; first = first || el; } }
      check(nama, nama.value.trim() ? '' : 'Isi nama Anda.');
      var e = email.value.trim(), t = telp.value.trim();
      check(email, (!e && !t) ? 'Isi email atau nomor telepon agar kami bisa membalas.' : (e && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e) ? 'Format email belum benar, contoh: nama@instansi.ac.id' : ''));
      check(telp, t && !/^[0-9+()\-\s]{8,}$/.test(t) ? 'Nomor telepon hanya berisi angka, minimal 8 digit.' : '');
      check(need, need.value ? '' : 'Pilih jenis kebutuhan.');
      check(pesan, pesan.value.trim().length >= 10 ? '' : 'Tulis kebutuhan Anda, minimal 10 karakter.');
      if (first) first.focus();
      return ok;
    }
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!validate()) { result.hidden = true; return; }
      var v = function (id) { return document.getElementById(id).value.trim(); };
      var lines = [
        'Pertanyaan bisnis untuk CV Izdihaar 84',
        '',
        'Nama: ' + v('f-nama'),
        'Instansi/perusahaan: ' + (v('f-instansi') || '-'),
        'Email: ' + (v('f-email') || '-'),
        'Telepon/WhatsApp: ' + (v('f-telepon') || '-'),
        'Jenis kebutuhan: ' + need.options[need.selectedIndex].text
      ];
      var r = SITE.routing[need.value];
      lines.push('', 'Pesan:', v('f-pesan'));
      var text = lines.join('\n');
      out.textContent = text;
      var c = SITE.contact || {};
      var wa = (c.whatsapp || '').replace(/[^0-9]/g, '');
      if (wa.indexOf('0') === 0) wa = '62' + wa.slice(1);
      waLink.hidden = !wa;
      if (wa) waLink.href = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(text);
      noChannel.hidden = !!wa;
      copyState.textContent = '';
      result.hidden = false;
      result.focus();
    });
    copyBtn.addEventListener('click', function () {
      var text = out.textContent;
      function fallback() {
        var range = document.createRange(); range.selectNodeContents(out);
        var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
        copyState.textContent = 'Teks sudah dipilih. Tekan Ctrl+C untuk menyalin.';
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { copyState.textContent = 'Pesan disalin.'; }, fallback);
      } else { fallback(); }
    });
  }
})();
