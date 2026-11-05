#!/usr/bin/env python3
"""Generator situs statis CV Izdihaar 84.

Pakai:  python3 build.py
Sumber: content/site.json (data), src/assets (CSS, JS, font, logo, foto)
Hasil:  dist/ (siap diunggah ke hosting mana pun)
"""
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
SITE, CONTACT, ABOUT = DATA["site"], DATA["contact"], DATA["about"]
COMPANIES, PROJECTS, NEWS = DATA["companies"], DATA["projects"], DATA["news"]
DIST = ROOT / "dist"
YEAR = "2026"
e = html.escape

NAV = [("index.html", "Beranda"), ("tentang-kami.html", "Tentang Kami"), ("layanan.html", "Layanan"),
       ("proyek.html", "Proyek"), ("berita.html", "Berita"), ("hubungi-kami.html", "Hubungi Kami")]
FIELD = {"lab": ("Laboratorium", "chip-lab"), "agro": ("Pertanian, peternakan, perikanan", "chip-agro"), "red": ("Furniture", "chip-holding")}
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
CUR = ' aria-current="page"'

# Foto ilustrasi (Unsplash License). Teks alt menjelaskan isi foto.
PHOTOS = {
    "hero": "Tangan bersarung tangan biru memegang gelas kimia berisi cairan bening di laboratorium",
    "ruang-lab": "Ruang laboratorium dengan deretan alat di kedua sisi",
    "jabat-tangan": "Dua orang berjabat tangan di atas meja kerja",
    "mikroskop": "Lensa objektif mikroskop laboratorium dari dekat",
    "pipet": "Pipet meneteskan cairan ke deretan tabung kecil",
    "pipet-meja": "Meja laboratorium dengan pipet dan botol reagen",
    "meja-lab": "Meja kerja laboratorium dengan mikroskop dan alat analisis",
    "tabung": "Deretan tabung sampel bertutup warna-warni pada rak",
    "sawah": "Sawah berair dengan latar gunung",
    "sapi": "Sapi putih di kandang terbuka",
    "keramba": "Keramba ikan bundar dilihat dari udara",
    "bibit": "Bibit tanaman muda tumbuh dari tanah",
    "gudang": "Lorong gudang dengan rak berisi kardus",
    "furniture": "Ruang laboratorium dengan meja kerja, kabinet berlaci, dan lemari penyimpanan",
}

ICONS = {
    "arrow": "M5 12h14M13 6l6 6-6 6",
    "menu": "M4 7h16M4 12h16M4 17h16",
    "flask": "M9 3h6M10 3v6l-5.5 9.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3M7.6 15h8.8",
    "tubes": "M7 3v13a2.5 2.5 0 0 0 5 0V3M5 3h9M7 10h5M15 7v10a2 2 0 0 0 4 0V7M14 7h6",
    "sprout": "M12 21v-9M12 12c0-4-3-6.5-7.5-6.5C4.5 9.5 7.5 12 12 12zM12 15.5c0-3.5 2.6-5.5 6.5-5.5 0 3.5-2.6 5.5-6.5 5.5z",
    "building": "M4 21V6l8-3v18M12 9l8 3v9M2 21h20M7.5 9v.01M7.5 13v.01M7.5 17v.01M16 14.5v.01M16 17.5v.01",
    "mail": "M3 6h18v12H3zM3 7l9 6 9-6",
    "phone": "M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z",
    "pin": "M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
    "calendar": "M4 6h16v14H4zM4 10h16M8 3v4M16 3v4",
    "image": "M3 5h18v14H3zM3 16l5-5 4 4 3-3 6 6M15.5 9.5v.01",
    "heart": "M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z",
    "users": "M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 6.5M17.5 14a6.5 6.5 0 0 1 4 6",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4",
    "check": "M5 12.5l4.5 4.5L19 7.5",
    "box": "M3 8l9-5 9 5v8l-9 5-9-5zM3 8l9 5 9-5M12 13v8",
    "folder": "M3 6h6l2 3h10v10H3z",
    "up": "M12 19V5M6 11l6-6 6 6",
    "layers": "M12 3l9 5-9 5-9-5zM3 13l9 5 9-5",
    "close": "M6 6l12 12M18 6L6 18",
    "chair": "M7 11V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v6M5 11h14v3H5zM7 14v7M17 14v7M7 18h10",
    "cabinet": "M5 3h14v18H5zM5 12h14M11 7.5h2M11 16.5h2",
    "wa": "M20 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.2A8.5 8.5 0 1 1 20 11.5zM8.8 8.2c-.4 2.6 3.4 6.6 6.2 6.4l.9-1.4-2-1-.9.8a4.6 4.6 0 0 1-2.4-2.4l.8-.9-1-2z",
}
ASSET_LINKS = """<link rel="preload" href="assets/fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-400.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/site.css">"""


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


ARROW = icon("arrow")


def btn(label, href, kind="primary", attrs=""):
    arr = f'<span class="arr">{ARROW}</span>' if kind == "primary" else (ARROW if kind in ("ghost", "light") else "")
    return f'<a class="btn btn-{kind}" href="{href}"{attrs}>{label} {arr}</a>'


def wa_url(msg="Halo CV Izdihaar 84, saya ingin menanyakan kebutuhan laboratorium."):
    num = re.sub(r"\D", "", CONTACT["whatsapp"])
    if num.startswith("0"):
        num = "62" + num[1:]
    return f"https://wa.me/{num}?text={quote(msg)}" if num else "hubungi-kami.html"


def wa_btn(label="Chat WhatsApp", msg=None):
    url = wa_url(msg) if msg else wa_url()
    return f'<a class="btn btn-wa" href="{e(url)}" target="_blank" rel="noopener">{icon("wa")} {label}</a>'


def tel(v):
    return "tel:" + re.sub(r"[^\d+]", "", v)


def todo(text=""):
    """Penanda isian yang belum dikonfirmasi tidak ditampilkan di situs publik."""
    return ""


def val(v, label=""):
    return e(v) if v else ""


def tanggal(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {BULAN[int(m) - 1]} {y}"


def chip_field(field):
    label, cls = FIELD[field]
    return f'<span class="chip {cls}">{label}</span>'


FOCUS_TEXT = {"lab": "alat dan bahan habis pakai laboratorium",
              "agro": "mesin dan peralatan laboratorium untuk pertanian, peternakan, dan perikanan"}


def route_text(field):
    return f"Kebutuhan ini akan kami teruskan ke perusahaan di bawah naungan kami yang menangani {FOCUS_TEXT[field]}."


ANGKA = {1: "satu", 2: "dua", 3: "tiga", 4: "empat", 5: "lima", 6: "enam"}
N_CO = ANGKA.get(len(COMPANIES), str(len(COMPANIES)))
COUNT = {f: sum(1 for c in COMPANIES if c["field"] == f) for f in ("lab", "agro")}
SCOPE = {"lab": ["Alat laboratorium", "Bahan habis pakai laboratorium"],
         "agro": ["Mesin dan peralatan laboratorium", "Sektor pertanian, peternakan, dan perikanan"]}


def photo(name, ratio="r43", tag="", pos="", eager=False, src=None, alt=None):
    """Foto bersudut terpotong. pos = titik fokus (object-position), mis. '30% 50%'."""
    src = src or f"assets/foto/{name}.jpg"
    alt = PHOTOS.get(name, "") if alt is None else alt
    style = f' style="object-position:{pos}"' if pos else ""
    cap = f'<figcaption><span class="photo-tag">{e(tag)}</span></figcaption>' if tag else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<figure class="photo {ratio}"><img src="{e(src)}" alt="{e(alt)}" {load}{style}>{cap}</figure>'


# ---------- kerangka halaman ----------
def head(title, desc, path):
    full = SITE["name"] if path == "index.html" else f'{title} | {SITE["name"]}'
    base = SITE["base_url"].rstrip("/")
    url = f"{base}/{'' if path == 'index.html' else path}" if base else ""
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": SITE["name"], "slogan": SITE["tagline"],
          "description": SITE["description"]}
    if base:
        ld["url"] = base + "/"
        ld["logo"] = base + "/assets/logo-izdihaar84.png"
    if CONTACT["email"]:
        ld["email"] = CONTACT["email"]
    if CONTACT["phone"]:
        ld["telephone"] = CONTACT["phone"]
    if CONTACT["address"]:
        ld["address"] = {"@type": "PostalAddress", "streetAddress": "Jl. Kebahagiaan Utara 18 No. 371, Tamalanrea",
                         "addressLocality": "Makassar", "addressRegion": "Sulawesi Selatan", "postalCode": "90245", "addressCountry": "ID"} \
            if "Makassar" in CONTACT["address"] else CONTACT["address"]
    canon = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n' if url else ""
    og_img = f'{base}/assets/og-image.jpg' if base else "assets/og-image.jpg"
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
{canon}<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a2540">
<link rel="icon" type="image/png" href="assets/favicon.png">
{ASSET_LINKS}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
"""


def header(active):
    items = "".join(f'<li><a href="{h}"{CUR if h == active else ""}>{t}</a></li>' for h, t in NAV)
    left = []
    if CONTACT["phone"]:
        left.append(f'<a href="{tel(CONTACT["phone"])}">{icon("phone")}{e(CONTACT["phone"])}</a>')
    if CONTACT["email"]:
        left.append(f'<a href="mailto:{e(CONTACT["email"])}">{icon("mail")}{e(CONTACT["email"])}</a>')
    right = f'<span>{icon("clock")}{e(CONTACT["hours"])}</span>' if CONTACT["hours"] else f'<span>{e(SITE["tagline"])}</span>'
    return f"""<a class="skip" href="#main">Langsung ke konten</a>
<div class="topbar"><div class="wrap topbar-in"><div class="topbar-links">{''.join(left)}</div>{right}</div></div>
<header class="hdr" id="top">
  <div class="wrap hdr-in">
    <a class="brand" href="index.html" aria-label="{e(SITE['name'])}, ke Beranda">
      <img src="assets/logo-mark.png" alt="" width="148" height="160">
      <span><b>IZDIHAAR 84</b><small>{e(SITE['tagline'])}</small></span>
    </a>
    <nav class="nav" id="nav" aria-label="Navigasi utama">
      <ul>{items}</ul>
      <div class="nav-cta"><a class="btn btn-primary" href="hubungi-kami.html">Hubungi kami <span class="arr">{ARROW}</span></a></div>
    </nav>
    <div class="hdr-actions">
      {btn("Hubungi kami", "hubungi-kami.html")}
      <button class="menu-btn" id="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Buka menu"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
    </div>
  </div>
</header>
"""


def footer():
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    cos = "".join(f'<li><a href="layanan.html#{sid}">{t}</a></li>' for sid, _, _, t, _, _ in SERVICES)
    k = []
    if CONTACT["address"]:
        k.append(f'<li class="contact-line">{icon("pin")}<span>{e(CONTACT["address"])}</span></li>')
    if CONTACT["phone"]:
        k.append(f'<li class="contact-line">{icon("phone")}<a href="{tel(CONTACT["phone"])}">{e(CONTACT["phone"])}</a></li>')
    if CONTACT["whatsapp"]:
        k.append(f'<li class="contact-line">{icon("wa")}<a href="{e(wa_url())}" target="_blank" rel="noopener">WhatsApp {e(CONTACT["whatsapp"])}</a></li>')
    if CONTACT["email"]:
        k.append(f'<li class="contact-line">{icon("mail")}<a href="mailto:{e(CONTACT["email"])}">{e(CONTACT["email"])}</a></li>')
    if CONTACT["hours"]:
        k.append(f'<li class="contact-line">{icon("clock")}<span>{e(CONTACT["hours"])}</span></li>')
    if not k:
        k.append('<li><a href="hubungi-kami.html">Kirim pertanyaan bisnis</a></li>')
    routing = {"alat-lab": route_text("lab"), "bhp": route_text("lab"), "agro": route_text("agro"),
               "furniture": f"Kebutuhan furniture umum dan furniture laboratorium ditangani oleh {SITE['name']}.",
               "kerja-sama": f"Kebutuhan ini akan ditangani langsung oleh {SITE['name']}."}
    cfg = json.dumps({"contact": CONTACT, "routing": routing}, ensure_ascii=False)
    wa = (f'<a class="wa-float" href="{e(wa_url())}" target="_blank" rel="noopener" aria-label="Chat WhatsApp dengan {e(SITE["name"])}">'
          f'{icon("wa")}<span>Chat WhatsApp</span></a>') if CONTACT["whatsapp"] else ""
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr-cta">
      <h2>Butuh alat atau bahan laboratorium? <span class="accent">Mari bicara.</span></h2>
    </div>
    <div class="ftr-cols">
      <div class="ftr-about">
        <div class="ftr-brand"><span><img src="assets/logo-mark.png" alt="" width="148" height="160" loading="lazy"></span><b>IZDIHAAR 84</b></div>
        <p>{e(SITE['name'])} menaungi {N_CO} perusahaan yang bergerak di bidang alat dan bahan habis pakai laboratorium, serta mesin dan peralatan laboratorium untuk pertanian, peternakan, dan perikanan. Kami juga melayani pengadaan furniture umum dan laboratorium.</p>
        <p class="ftr-tagline">{e(SITE['tagline'])}</p>
      </div>
      <div><h3>Navigasi</h3><ul>{nav}</ul></div>
      <div><h3>Bidang usaha</h3><ul>{cos}</ul></div>
      <div><h3>Kantor</h3><ul>{''.join(k)}</ul></div>
    </div>
  </div>
  <div class="ftr-bottom"><div class="wrap"><span>&copy; {YEAR} {e(SITE['name'])}. Hak cipta dilindungi.</span><a class="to-top" href="#top">Kembali ke atas {icon("up")}</a></div></div>
</footer>
{wa}
<script>window.SITE = {cfg};</script>
<script src="assets/site.js" defer></script>
"""


def banner(title, intro="", crumbs=None):
    trail = '<a href="index.html">Beranda</a><span aria-hidden="true">/</span>'
    for h, t in (crumbs or []):
        trail += f'<a href="{h}">{e(t)}</a><span aria-hidden="true">/</span>'
    last = "Artikel" if crumbs else e(title)
    return f"""<section class="banner{' banner-article' if crumbs else ''}"><div class="wrap banner-in">
  <nav class="crumb" aria-label="Jejak halaman">{trail}<span aria-current="page">{last}</span></nav>
  <h1>{e(title)}</h1>
  {f'<p>{e(intro)}</p>' if intro else ''}
</div></section>
"""


def sec_head(kicker, line1, line2="", extra="", center=False, lead="", inline=False):
    acc = f' <span class="accent{" inline" if inline else ""}">{line2}</span>' if line2 else ""
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<div class="sec-head{" center" if center else ""}"><div><span class="kicker">{kicker}</span>'
            f'<h2>{line1}{acc}</h2>{ld}</div>{extra}</div>')


PAGES = {}


def page(path, title, desc, active, body, ban=None):
    main = (banner(title, *ban) if ban is not None else "") + body
    PAGES[path] = main
    out = head(title, desc, path) + header(active) + f'<main id="main">\n{main}\n</main>\n' + footer() + "</body>\n</html>\n"
    (DIST / path).write_text(out, encoding="utf-8")


# ---------- komponen ----------
FOCUS = [
    ("lab", "flask", "mikroskop", "Alat dan bahan habis pakai laboratorium",
     "Penyediaan alat laboratorium dan bahan habis pakai untuk kebutuhan penelitian, pendidikan, industri, dan laboratorium.",
     ["Alat laboratorium", "Bahan habis pakai laboratorium", "Laboratorium farmasi, kedokteran, pertanian, dan peternakan"],
     "layanan.html#alat-laboratorium"),
    ("agro", "sprout", "sawah", "Mesin dan peralatan untuk pertanian, peternakan, dan perikanan",
     "Penyediaan mesin dan peralatan laboratorium untuk menunjang pekerjaan di sektor pertanian, peternakan, dan perikanan.",
     ["Sektor pertanian", "Sektor peternakan", "Sektor perikanan"],
     "layanan.html#pertanian-peternakan-perikanan"),
]


def group(ids=False):
    """CV Izdihaar 84 dan fokus usaha perusahaan di bawah naungannya (tanpa identitas perusahaan)."""
    cards = ""
    for field, ic, ph, title, desc, scope, href in FOCUS:
        n = COUNT[field]
        who = f"Dijalankan oleh {ANGKA.get(n, str(n))} perusahaan di bawah naungan kami"
        items = "".join(f"<li>{icon('check')}<span>{x}</span></li>" for x in scope)
        cards += (f'<article class="focus {field}">{photo(ph, "")}<div class="focus-body">'
                  f'<span class="focus-count"><span class="ico {field}">{icon(ic)}</span><span>{who}</span></span>'
                  f'<h3>{title}</h3><p>{desc}</p><ul class="company-scope">{items}</ul>'
                  f'<a class="link-more" href="{href}">Lihat layanan {ARROW}</a></div></article>')
    return f"""<div class="group" role="group" aria-label="{e(SITE['name'])} menaungi {N_CO} perusahaan">
  <div class="group-root"><span class="group-mark"><img src="assets/logo-mark.png" alt="" width="148" height="160" loading="lazy"></span>
    <div><span class="group-eyebrow">Perusahaan penaung</span><b>{e(SITE['name'])}</b><span>Menaungi {N_CO} perusahaan dengan fokus usaha yang berbeda</span></div></div>
  <div class="group-lines two" aria-hidden="true"><i></i></div>
  <div class="focus-grid">{cards}</div>
</div>"""


def facts():
    return f"""<ul class="facts">
    <li><span class="ico">{icon("layers")}</span><div><b>{len(COMPANIES)} perusahaan</b><span>di bawah naungan {e(SITE['name'])}</span></div></li>
    <li><span class="ico lab">{icon("flask")}</span><div><b>4 bidang layanan</b><span>laboratorium, sektor agro, dan furniture</span></div></li>
    <li><span class="ico agro">{icon("users")}</span><div><b>Kampus dan instansi</b><span>pelanggan yang telah kami layani</span></div></li>
    <li><span class="ico red">{icon("pin")}</span><div><b>Makassar</b><span>kantor di Tamalanrea</span></div></li>
  </ul>"""


SERVICES = [
    ("alat-laboratorium", "flask", "lab", "Alat laboratorium",
     "Peralatan untuk pengujian, praktikum, dan penelitian, termasuk laboratorium farmasi, kedokteran, pertanian, dan peternakan.", "mikroskop"),
    ("bahan-habis-pakai", "tubes", "lab", "Bahan habis pakai laboratorium",
     "Bahan dan perlengkapan yang terpakai setiap hari di laboratorium dan perlu diganti secara berkala.", "pipet"),
    ("pertanian-peternakan-perikanan", "sprout", "agro", "Mesin dan peralatan pertanian, peternakan, perikanan",
     "Mesin dan peralatan laboratorium untuk menunjang pekerjaan di sektor pertanian, peternakan, dan perikanan.", "sawah"),
    ("pengadaan-furniture", "chair", "red", "Pengadaan furniture umum & laboratorium",
     "Furniture untuk perkantoran, ruang rapat, instansi, dan fasilitas pendidikan, serta furniture khusus laboratorium.", "furniture"),
]
FURNITURE = [
    ("chair", "Furniture umum", "Untuk perkantoran, ruang kerja, ruang rapat, instansi, fasilitas pendidikan, dan kebutuhan interior lainnya."),
    ("cabinet", "Furniture laboratorium", "Meja laboratorium, lemari penyimpanan, kabinet, kursi laboratorium, dan furniture pendukung aktivitas laboratorium lainnya."),
]


def handled(field, link=False):
    if field == "red":
        return (f'<p class="handled">{icon("layers")}<span>Disediakan oleh {e(SITE["name"])}, '
                f'untuk furniture umum maupun furniture laboratorium.</span></p>')
    bidang = "laboratorium" if field == "lab" else "pertanian, peternakan, dan perikanan"
    return (f'<p class="handled">{icon("layers")}<span>Ditangani oleh perusahaan di bawah naungan kami '
            f'yang berfokus pada bidang {bidang}.</span></p>')


def service_photo_cards():
    out = ""
    for sid, ic, field, title, desc, ph in SERVICES:
        out += (f'<a class="svc-card" href="layanan.html#{sid}">{photo(ph, "")}<span class="ico {field}">{icon(ic)}</span>'
                f'<div class="svc-body"><h3>{title}</h3><p>{desc}</p>{handled(field)}'
                f'<span class="link-more">Selengkapnya {ARROW}</span></div></a>')
    return f'<div class="svc-grid">{out}</div>'


def service_cards():
    out = ""
    for sid, ic, field, title, desc, _ in SERVICES:
        out += (f'<article class="card"><span class="ico {field}">{icon(ic)}</span><h3>{title}</h3><p>{desc}</p>{handled(field)}</article>')
    return f'<div class="grid-4">{out}</div>'


def project_card(p):
    media = (photo("", "", src=p["image"], alt=PHOTOS.get(Path(p["image"]).stem, ""), tag="Foto ilustrasi") if p.get("image")
             else f'<div class="proj-slot">{icon("image")}<span>Foto proyek belum ditambahkan</span></div>')
    rows = [("Lingkup", p.get("scope")), ("Lokasi", p.get("location")), ("Tahun", p.get("year"))]
    dl = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows if v)
    return (f'<article class="proj" data-cat="{e(p.get("category", ""))}"><div class="proj-media">{media}</div><div class="proj-body">'
            f'<div class="row"><span class="chip chip-navy">{e(p.get("category", ""))}</span><span class="muted" style="font-size:.9rem">{e(p["title"])}</span></div>'
            f'<h3>{e(p["client"])}</h3><p class="muted">{e(p.get("summary", ""))}</p><dl>{dl}</dl></div></article>')


def client_list(final_and=True):
    cs = [p["client"] for p in PROJECTS if p["client"] != "Instansi pemerintah"]
    if final_and and len(cs) > 1:
        return ", ".join(cs[:-1]) + ", dan " + cs[-1]
    return ", ".join(cs)


def client_cards():
    out = ""
    for p in PROJECTS:
        loc = f'<span class="client-loc">{icon("pin")}{e(p["location"])}</span>' if p.get("location") else ""
        out += (f'<article class="client"><span class="client-tag">{e(p.get("category", ""))}</span>'
                f'<h3>{e(p["client"])}</h3><p>{e(p.get("scope", ""))}</p>{loc}</article>')
    return f'<div class="clients">{out}</div>'


def cover(n, ratio=""):
    if n.get("image"):
        key = Path(n["image"]).stem
        return photo(key, ratio, src=n["image"], alt=PHOTOS.get(key, ""))
    return f'<figure class="photo {ratio}" style="background:var(--navy);display:grid;place-items:center;color:#fff;min-height:200px">{icon("flask")}</figure>'


def post_card(n, feature=False):
    return (f'<a class="post{" feature" if feature else ""}" href="berita-{n["slug"]}.html" data-cat="{e(n["category"])}">{cover(n)}'
            f'<span class="post-cat">{e(n["category"])}</span>'
            f'<div class="post-body"><div class="post-meta"><span>{icon("calendar")}<time datetime="{n["date"]}">{tanggal(n["date"])}</time></span></div>'
            f'<h3>{e(n["title"])}</h3><p>{e(n["summary"])}</p><span class="link-more">Baca artikel {ARROW}</span></div></a>')


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "src/assets", DIST / "assets")
    news = sorted(NEWS, key=lambda n: n["date"], reverse=True)
    loc = "Tamalanrea, Makassar" if "Makassar" in CONTACT["address"] else ""

    # ---------- Beranda ----------
    if PROJECTS:
        fields = "".join(f'<span class="chip">{e(f)}</span>' for f in DATA.get("project_fields", []))
        proj_home = (f'{client_cards()}<div class="clients-foot"><div class="row">{fields}</div>'
                     f'{btn("Lihat semua proyek", "proyek.html")}</div>')
    else:
        proj_home = (f'<div class="notice"><span class="ico">{icon("folder")}</span><div><b>Dokumentasi proyek sedang disusun</b>'
                     f'<p>Daftar pengadaan dan kerja sama akan kami tampilkan di sini setelah datanya lengkap.</p></div>'
                     f'{btn("Lihat halaman Proyek", "proyek.html")}</div>')
    meta = []
    if loc:
        meta.append(f'<span>{icon("pin")}Kantor di {loc}</span>')
    if CONTACT["hours"]:
        meta.append(f'<span>{icon("clock")}{e(CONTACT["hours"])}</span>')
    trust = "".join(f"<li>{e(p['client'])}</li>" for p in PROJECTS)
    trust_html = (f'<div class="trust"><div class="wrap trust-in"><span class="trust-label">Telah memasok</span><ul>{trust}</ul></div></div>'
                  if PROJECTS else "")
    home = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="kicker">Menaungi {N_CO} perusahaan</span>
      <h1>Pemasok alat dan bahan laboratorium <span class="accent">untuk kampus dan instansi</span></h1>
      <p class="hero-lead">{e(SITE['name'])} menaungi {N_CO} perusahaan dengan bidang usaha dan spesialisasi masing-masing: alat laboratorium, bahan habis pakai, serta mesin dan peralatan untuk pertanian, peternakan, dan perikanan. {e(SITE['name'])} juga melayani pengadaan furniture umum dan furniture laboratorium.</p>
      <div class="hero-cta">{btn("Konsultasikan kebutuhan", "hubungi-kami.html")}{btn("Lihat layanan", "layanan.html", "ghost")}</div>
      <div class="hero-meta">{''.join(meta)}</div>
    </div>
    <div class="hero-visual">
      {photo("hero", "", pos="42% 50%", eager=True)}
      <div class="hero-badge"><img src="assets/logo-mark.png" alt="" width="148" height="160"><div><b>{e(SITE['tagline'])}</b><span>{e(SITE['name'])}</span></div></div>
    </div>
  </div>
  {trust_html}
</section>

<section class="sec sec-mist" id="perusahaan"><div class="wrap">
  {sec_head("Perusahaan kami", f"Satu naungan,", f"{N_CO} perusahaan", center=True, inline=True, lead=f"Setiap perusahaan memiliki bidang usaha, spesialisasi, dan tanggung jawab operasional sendiri. {e(SITE['name'])} menaungi ketiganya dan memastikan setiap kebutuhan ditangani oleh perusahaan yang tepat.")}
  {group()}
</div></section>

<section class="sec"><div class="wrap">
  <div class="overview">
    <div class="overview-media">
      {photo("jabat-tangan", "", pos="62% 50%")}
      <div class="overview-note"><b>Kantor di Makassar</b><span>{e(CONTACT["address"])}</span></div>
    </div>
    <div class="overview-body">
      {sec_head("Tentang kami", "Satu kontak", "untuk beberapa kebutuhan")}
      <p class="lead">Satu pengadaan sering melibatkan beberapa jenis barang sekaligus: alat, bahan habis pakai, peralatan untuk sektor pertanian dan perikanan, hingga furniture. Di bawah naungan {e(SITE['name'])}, setiap jenis kebutuhan itu ditangani oleh perusahaan yang memang menekuni bidangnya.</p>
      <ul class="checks">
        <li>{icon("check")}<span>Melayani perguruan tinggi, laboratorium, instansi pemerintah, dan pelaku usaha.</span></li>
        <li>{icon("check")}<span>Pertanyaan Anda diteruskan ke perusahaan yang paling sesuai dengan bidangnya.</span></li>
        <li>{icon("check")}<span>Telah memasok {client_list()}.</span></li>
      </ul>
      <div class="row">{btn("Profil perusahaan", "tentang-kami.html", "ghost")}</div>
    </div>
  </div>
  {facts()}
</div></section>

<section class="sec sec-mist"><div class="wrap">
  {sec_head("Bidang usaha", "Empat bidang", "layanan", center=True, inline=True, lead="Dari alat dan bahan laboratorium, peralatan untuk sektor agro, hingga furniture untuk ruang kerja dan laboratorium.")}
  {service_photo_cards()}
</div></section>

<section class="sec"><div class="wrap">
  {sec_head("Alur kerja sama", "Dari pertanyaan", "sampai ditangani tim yang tepat")}
  <ol class="steps">
    <li><h3>Sampaikan kebutuhan</h3><p>Lewat formulir, telepon, atau WhatsApp. Sertakan jenis barang, jumlah, dan kapan dibutuhkan.</p></li>
    <li><h3>Kami teruskan</h3><p>Permintaan Anda diarahkan ke perusahaan yang menangani bidang tersebut.</p></li>
    <li><h3>Tim terkait menghubungi Anda</h3><p>Pembahasan detail kebutuhan dilanjutkan langsung dengan tim dari perusahaan itu.</p></li>
  </ol>
</div></section>

<section class="sec sec-navy"><div class="wrap">
  {sec_head("Rekam jejak", "Perguruan tinggi dan instansi", "yang pernah kami layani", center=True, lead="Kami memasok alat laboratorium farmasi, kedokteran, pertanian, dan peternakan beserta bahan habis pakainya ke perguruan tinggi dan instansi pemerintah, di antaranya:")}
  {proj_home}
</div></section>

<section class="sec"><div class="wrap">
  {sec_head("Berita", "Kabar dan", "artikel terbaru", btn("Semua berita", "berita.html", "ghost"))}
  <div class="grid-3">{"".join(post_card(n) for n in news[:3])}</div>
</div></section>
"""
    page("index.html", "Beranda", SITE["description"], "index.html", home)

    # ---------- Tentang Kami ----------
    if ABOUT["vision"]:
        vision = f'<p>{e(ABOUT["vision"])}</p>'
        mission = "".join(f'<li>{icon("check")}<span>{e(m)}</span></li>' for m in ABOUT["mission"])
        vm_flag = ""
    else:
        vision = "<p>Menjadi grup penyedia kebutuhan laboratorium yang dipercaya oleh dunia pendidikan, penelitian, dan industri, serta oleh sektor pertanian, peternakan, dan perikanan.</p>"
        mission = "".join(f'<li>{icon("check")}<span>{m}</span></li>' for m in (
            "Menjaga setiap perusahaan dalam grup tetap fokus pada bidang keahliannya.",
            "Menyediakan alat dan bahan habis pakai laboratorium yang sesuai dengan kebutuhan pengguna.",
            "Menghadirkan mesin dan peralatan laboratorium untuk sektor pertanian, peternakan, dan perikanan.",
            "Melayani pelanggan dan mitra dengan setia, sesuai semboyan Service with Loyalty."))
        vm_flag = todo("Draf, perlu konfirmasi")
    founded = f'<p><b>Tahun berdiri:</b> {e(ABOUT["founded"])}</p>' if ABOUT["founded"] else ""
    miles = ""
    if ABOUT["milestones"]:
        items = "".join(f'<li><h3>{e(m["year"])}: {e(m["title"])}</h3><p>{e(m.get("text", ""))}</p></li>' for m in ABOUT["milestones"])
        miles = f"""<section class="sec"><div class="wrap">{sec_head("Perjalanan kami", "Tonggak", "perusahaan")}<ol class="steps">{items}</ol></div></section>"""
    clients = client_list()
    track = ""
    if PROJECTS:
        names_html = "".join(f'<li>{e(p["client"])}</li>' for p in PROJECTS)
        track = f"""<section class="track"><div class="wrap track-in">
  <div><span class="kicker">Rekam jejak</span><h2>Pernah kami layani</h2></div>
  <ul>{names_html}</ul>
  {btn("Lihat proyek", "proyek.html")}
</div></section>
"""
    office_card = ""
    if CONTACT["address"]:
        maps_l = ""
        office_card = (f'<div class="office"><span class="ico red">{icon("pin")}</span><div><b>Kantor</b>'
                       f'<p>{e(CONTACT["address"])}</p><p class="muted">{e(CONTACT["hours"])}</p>{maps_l}</div></div>')
    about = f"""<section class="sec"><div class="wrap">
  {sec_head("Profil perusahaan", "Satu naungan,", f"{N_CO} perusahaan")}
  <div class="profile">
    <div class="profile-text">
      <p class="lead-lg">{e(SITE['name'])} menaungi {N_CO} perusahaan yang masing-masing memiliki bidang usaha, spesialisasi, dan tanggung jawab operasional yang berbeda.</p>
      <p>Dua di antaranya bergerak di bidang alat dan bahan habis pakai laboratorium untuk kebutuhan penelitian, pendidikan, industri, dan laboratorium. Satu perusahaan lainnya berfokus pada mesin dan peralatan laboratorium untuk sektor pertanian, peternakan, dan perikanan.</p>
      <p>Selain itu, {e(SITE['name'])} menyediakan layanan pengadaan furniture, baik furniture umum untuk perkantoran, ruang rapat, instansi, dan fasilitas pendidikan, maupun furniture khusus laboratorium.</p>
      <p>Setiap perusahaan menjalankan operasionalnya secara mandiri sesuai bidangnya. {e(SITE['name'])} menjaga arah usaha bersama, menjaga standar layanan, dan memastikan setiap kebutuhan pelanggan ditangani oleh perusahaan yang tepat.</p>
      <p>Perusahaan di bawah naungan kami telah memasok alat laboratorium farmasi, kedokteran, pertanian, dan peternakan beserta bahan habis pakainya ke sejumlah perguruan tinggi, di antaranya {client_list(False)}, serta ke beberapa instansi pemerintah.</p>
      {founded}
    </div>
    <aside class="profile-side">
      <div class="logo-tile"><img src="assets/logo-izdihaar84.png" alt="Logo CV Izdihaar 84: dua tangan berjabat dalam lingkaran merah, biru, dan hijau, dengan tulisan Service with Loyalty" width="592" height="520"></div>
      {office_card}
    </aside>
  </div>
  {facts()}
</div></section>
{track}
<section class="sec sec-mist"><div class="wrap">
  {sec_head("Visi dan misi", "Arah", "yang kami tuju", vm_flag)}
  <div class="split">
    <div class="panel-navy"><h3>Visi</h3>{vision}</div>
    <div class="card"><h3>Misi</h3><ul class="checks">{mission}</ul></div>
  </div>
</div></section>
<div class="scale" aria-hidden="true"></div>

<section class="sec" id="nilai"><div class="wrap">
  <div class="split mid">
    {photo("jabat-tangan", "r43", pos="60% 50%")}
    <div>
      {sec_head("Nilai perusahaan", "Service", "with Loyalty", todo("Rumusan perlu konfirmasi"))}
      <div>
        <div class="value"><span class="ico red">{icon("heart")}</span><div><h3>Pelayanan</h3><p>Kami mendengarkan kebutuhan Anda lebih dulu, lalu membantu mencari solusi yang paling sesuai.</p></div></div>
        <div class="value"><span class="ico lab">{icon("users")}</span><div><h3>Loyalitas</h3><p>Kami menjaga hubungan jangka panjang dengan pelanggan dan mitra, dan menepati apa yang sudah disepakati.</p></div></div>
      </div>
    </div>
  </div>
</div></section>

<section class="sec sec-mist" id="struktur"><div class="wrap">
  {sec_head("Struktur perusahaan", "Perusahaan di bawah naungan", e(SITE['name']), center=True, lead="Masing-masing perusahaan memiliki fokus bisnis tersendiri dan menjalankan operasionalnya sesuai bidang usahanya.")}
  {group(ids=True)}
</div></section>
{miles}"""
    page("tentang-kami.html", "Tentang Kami",
         "Profil CV Izdihaar 84 di Makassar, yang menaungi tiga perusahaan di bidang alat dan bahan habis pakai laboratorium serta mesin dan peralatan untuk pertanian, peternakan, dan perikanan.",
         "tentang-kami.html", about, ())

    # ---------- Layanan ----------
    trio = (f'<div class="trio">{photo("sawah", "", tag="Pertanian", pos="60% 50%")}{photo("sapi", "", tag="Peternakan", pos="45% 50%")}'
            f'{photo("keramba", "", tag="Perikanan")}</div>')
    media = {"alat-laboratorium": photo("pipet-meja", "r43"), "bahan-habis-pakai": photo("tabung", "r43"),
             "pertanian-peternakan-perikanan": trio, "pengadaan-furniture": photo("furniture", "r43", pos="50% 70%")}
    copy = {"alat-laboratorium": "Peralatan untuk pengujian, praktikum, dan penelitian di laboratorium farmasi, kedokteran, pertanian, dan peternakan. Cocok untuk laboratorium yang baru dibangun, sedang dilengkapi, atau perlu memperbarui alatnya.",
            "bahan-habis-pakai": "Bahan dan perlengkapan yang terpakai setiap hari di laboratorium. Untuk laboratorium yang ingin pasokannya tetap terjaga tanpa harus mencari pemasok satu per satu.",
            "pertanian-peternakan-perikanan": "Mesin dan peralatan laboratorium untuk sektor pertanian, peternakan, dan perikanan, bagi laboratorium maupun unit kerja di ketiga sektor tersebut.",
            "pengadaan-furniture": "Pengadaan dan penyediaan furniture untuk melengkapi ruang kerja dan fasilitas laboratorium. Kebutuhan alat, bahan, dan furniture dapat dibahas dalam satu kali komunikasi."}
    furn = "".join(f'<li><span class="ico red">{icon(ic)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for ic, t, d in FURNITURE)
    extra = {"pengadaan-furniture": f'<ul class="subcats">{furn}</ul>'}
    feats = ""
    for sid, ic, field, title, _, _ in SERVICES:
        ask = wa_btn("Tanya lewat WhatsApp", f"Halo CV Izdihaar 84, saya ingin menanyakan {title.lower()}.") if CONTACT["whatsapp"] else btn("Tanyakan kebutuhan ini", "hubungi-kami.html", "ghost")
        feats += (f'<article class="feature" id="{sid}"><div class="feature-media">{media[sid]}</div><div class="feature-body">'
                  f'<span class="ico {field}">{icon(ic)}</span><h2>{title}</h2><p class="lead">{copy[sid]}</p>{extra.get(sid, "")}{handled(field, link=True)}'
                  f'<div class="row">{ask}{btn("Kirim pertanyaan", "hubungi-kami.html", "ghost")}</div></div></article>')
    layanan = f"""<section class="sec"><div class="wrap">
  {sec_head("Layanan", "Empat bidang layanan", "dalam satu naungan", center=True)}
  {feats}
</div></section>

<section class="sec sec-mist"><div class="wrap">
  {sec_head("Untuk siapa", "Siapa saja", "yang kami layani")}
  <div class="grid-4">
    <article class="card"><span class="ico">{icon("search")}</span><h3>Penelitian</h3><p>Laboratorium riset yang membutuhkan alat dan bahan untuk penelitian.</p></article>
    <article class="card"><span class="ico">{icon("building")}</span><h3>Pendidikan</h3><p>Perguruan tinggi dan sekolah yang mengelola laboratorium praktikum dan riset.</p></article>
    <article class="card"><span class="ico">{icon("tubes")}</span><h3>Industri dan pengujian</h3><p>Laboratorium industri dan pengujian yang membutuhkan pasokan rutin.</p></article>
    <article class="card"><span class="ico agro">{icon("sprout")}</span><h3>Instansi pemerintah</h3><p>Dinas dan lembaga yang membutuhkan alat dan bahan laboratorium, termasuk di sektor pertanian, peternakan, dan perikanan.</p></article>
  </div>
</div></section>

"""
    page("layanan.html", "Layanan",
         "Alat laboratorium, bahan habis pakai, serta mesin dan peralatan laboratorium untuk pertanian, peternakan, dan perikanan dari grup CV Izdihaar 84.",
         "layanan.html", layanan, ())

    # ---------- Proyek ----------
    if PROJECTS:
        fields = "".join(f'<span class="chip">{e(f)}</span>' for f in DATA.get("project_fields", []))
        plist = f'<div class="stack-lg" id="proj-list">{"".join(project_card(p) for p in PROJECTS)}</div>'
        intro = (f'<div class="proj-intro"><p class="lead">Grup kami memasok alat laboratorium beserta bahan habis pakainya untuk perguruan tinggi dan instansi pemerintah. '
                 f'Di antaranya {client_list()}.</p>'
                 f'<div class="stack"><span class="muted" style="font-size:.9rem">Bidang alat yang kami pasok</span><div class="row">{fields}</div></div></div>')
    else:
        plist = intro = ('<div class="empty"><b>Dokumentasi proyek sedang disusun</b><span>Daftar pengadaan dan kerja sama akan ditampilkan di sini.</span></div>')
        plist = ""
    proyek = f"""<section class="sec"><div class="wrap">
  {sec_head("Portofolio", "Proyek", "yang telah kami jalankan")}
  {intro}{plist}
  <p class="hint" style="margin-top:var(--s-5)">Foto pada halaman ini adalah foto ilustrasi, bukan dokumentasi proyek.</p>
</div></section>

<section class="sec sec-mist"><div class="wrap">
  <div class="split mid">
    {photo("tabung", "r43", tag="Foto ilustrasi")}
    <div>
      {sec_head("Ingin bekerja sama?", "Kebutuhan laboratorium", "instansi Anda")}
      <p class="lead" style="margin-bottom:var(--s-4)">Kirim daftar kebutuhan alat atau bahan habis pakai, lengkap dengan jumlah dan waktu yang dibutuhkan. Tim kami akan menghubungi Anda untuk membahasnya.</p>
      <div class="row">{wa_btn("Tanya lewat WhatsApp", "Halo CV Izdihaar 84, kami ingin membahas kebutuhan pengadaan alat laboratorium untuk instansi kami.") if CONTACT["whatsapp"] else ""}{btn("Kirim pertanyaan", "hubungi-kami.html", "ghost")}</div>
    </div>
  </div>
</div></section>
"""
    page("proyek.html", "Proyek", "Rekam jejak CV Izdihaar 84 sebagai pemasok alat dan bahan laboratorium untuk Universitas Khairun, UIN Alauddin Makassar, dan instansi pemerintah.",
         "proyek.html", proyek, ())

    # ---------- Berita ----------
    ncats = ["Kegiatan perusahaan", "Kerja sama", "Informasi bisnis", "Artikel"]
    count = lambda c: sum(1 for n in news if n["category"] == c)
    fbtn = (f'<button type="button" data-value="semua" aria-pressed="true"><span>Semua</span><span>{len(news)}</span></button>'
            + "".join(f'<button type="button" data-value="{c}" aria-pressed="false"><span>{c}</span><span>{count(c)}</span></button>' for c in ncats))
    first = post_card(news[0], feature=True).replace('class="post feature"', 'class="post feature" style="grid-column:1/-1"') if news else ""
    berita = f"""<section class="sec"><div class="wrap">
  {sec_head("Berita dan artikel", "Kabar grup dan", "catatan seputar laboratorium", center=True)}
  <div class="news-layout">
    <div>
      <div class="grid-2" id="news-list">{first}{"".join(post_card(n) for n in news[1:])}</div>
      <div class="empty" id="news-list-empty" hidden><b>Belum ada tulisan di sini</b><span>Coba kategori lain atau hapus kata pencarian.</span></div>
    </div>
    <aside class="side" aria-label="Saring berita">
      <div><h2>Cari</h2><div class="field"><label class="sr" for="news-search">Cari berita</label><input id="news-search" type="search" placeholder="Cari judul atau topik" data-search="news-list"></div></div>
      <div><h2>Kategori</h2><div class="filters" data-filter-group="news-list" role="group" aria-label="Kategori berita">{fbtn}</div></div>
      <p class="note">Kabar kegiatan perusahaan dan kerja sama akan dimuat di halaman ini.</p>
    </aside>
  </div>
</div></section>
"""
    page("berita.html", "Berita",
         "Kabar kegiatan grup CV Izdihaar 84 dan artikel seputar alat laboratorium, bahan habis pakai, serta peralatan pertanian, peternakan, dan perikanan.",
         "berita.html", berita, ())

    for n in news:
        body = ""
        for b in n["body"]:
            if "h" in b:
                body += f'<h2>{e(b["h"])}</h2>'
            elif "p" in b:
                body += f'<p>{e(b["p"])}</p>'
            elif "ul" in b:
                body += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in b["ul"]) + "</ul>"
        words = sum(len(" ".join(x for v in b.values() for x in (v if isinstance(v, list) else [v])).split()) for b in n["body"])
        others = "".join(post_card(o) for o in news if o["slug"] != n["slug"])
        art = f"""<section class="sec"><div class="wrap">
  <div class="article-cover">{cover(n, "r219")}</div>
  <article class="article">
    <div class="article-head">
      <span class="chip chip-holding">{e(n["category"])}</span>
      <div class="post-meta"><span>{icon("calendar")}<time datetime="{n["date"]}">{tanggal(n["date"])}</time></span><span>{icon("clock")}{max(1, round(words / 200))} menit baca</span><span>Tim {e(SITE["name"])}</span></div>
    </div>
    {body}
    <div class="row" style="margin-top:12px">{btn("Kembali ke Berita", "berita.html", "ghost")}{btn("Hubungi kami", "hubungi-kami.html")}</div>
  </article>
</div></section>
<section class="sec sec-mist"><div class="wrap">
  {sec_head("Artikel lain", "Baca", "juga", center=True)}
  <div class="grid-2">{others}</div>
</div></section>
"""
        page(f'berita-{n["slug"]}.html', n["title"], n["summary"], "berita.html", art, ("", [("berita.html", "Berita")]))

    # ---------- Hubungi Kami ----------
    maps = ""
    phone = f'<a href="{tel(CONTACT["phone"])}">{e(CONTACT["phone"])}</a>' if CONTACT["phone"] else todo("Belum diisi")
    wa = f'<a href="{e(wa_url())}" target="_blank" rel="noopener">{e(CONTACT["whatsapp"])}</a>' if CONTACT["whatsapp"] else todo("Belum diisi")
    mail = f'<a href="mailto:{e(CONTACT["email"])}">{e(CONTACT["email"])}</a>' if CONTACT["email"] else todo("Belum diisi")
    actions = f'<div class="actions">{wa_btn()}</div>' if CONTACT["whatsapp"] else ""
    hubungi = f"""<section class="sec"><div class="wrap">
  {sec_head("Hubungi kami", "Ceritakan kebutuhan Anda,", "kami bantu arahkan", center=True)}
  <div class="contact-layout">
    <form class="form" id="inquiry-form" novalidate>
      <div class="field"><label for="f-nama">Nama *</label><input id="f-nama" name="nama" autocomplete="name" required aria-describedby="f-nama-err"><span class="err" id="f-nama-err" role="alert"></span></div>
      <div class="field"><label for="f-instansi">Instansi atau perusahaan</label><input id="f-instansi" name="instansi" autocomplete="organization"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="nama@instansi.ac.id" aria-describedby="f-email-err"><span class="err" id="f-email-err" role="alert"></span></div>
      <div class="field"><label for="f-telepon">Telepon atau WhatsApp</label><input id="f-telepon" name="telepon" type="tel" autocomplete="tel" placeholder="08xx xxxx xxxx" aria-describedby="f-telepon-err"><span class="err" id="f-telepon-err" role="alert"></span></div>
      <div class="field full"><label for="f-kebutuhan">Jenis kebutuhan *</label>
        <select id="f-kebutuhan" name="kebutuhan" required aria-describedby="f-kebutuhan-err">
          <option value="">Pilih jenis kebutuhan</option>
          <option value="alat-lab">Alat laboratorium</option>
          <option value="bhp">Bahan habis pakai laboratorium</option>
          <option value="agro">Mesin dan peralatan pertanian, peternakan, perikanan</option>
          <option value="furniture">Furniture umum atau furniture laboratorium</option>
          <option value="kerja-sama">Kerja sama atau kemitraan</option>
          <option value="lainnya">Lainnya</option>
        </select><span class="err" id="f-kebutuhan-err" role="alert"></span></div>
      <p class="route" id="route" hidden aria-live="polite"></p>
      <div class="field full"><label for="f-pesan">Pesan *</label><textarea id="f-pesan" name="pesan" required placeholder="Contoh: nama alat atau bahan, jumlah, lokasi pengiriman, dan kapan dibutuhkan" aria-describedby="f-pesan-err"></textarea><span class="err" id="f-pesan-err" role="alert"></span></div>
      <div class="field full"><div class="row"><button class="btn btn-primary" type="submit">Siapkan pesan <span class="arr">{ARROW}</span></button></div></div>
      <div class="result" id="result" hidden tabindex="-1" aria-live="polite">
        <h3>Pesan Anda sudah siap</h3>
        <p class="hint">Tekan tombol di bawah untuk mengirim pesan ini lewat WhatsApp.</p>
        <pre id="result-text"></pre>
        <div class="row">
          <a class="btn btn-wa" id="wa-link" href="#" target="_blank" rel="noopener" hidden>{icon("wa")} Kirim lewat WhatsApp</a>
          <button class="btn btn-ghost" id="copy-btn" type="button">Salin pesan</button>
          <span id="copy-state" role="status"></span>
        </div>
        <p class="hint" id="no-channel" hidden>Salin pesan di atas, lalu kirim melalui kontak yang tercantum di halaman ini.</p>
      </div>
    </form>
    <aside class="info" aria-label="Informasi kontak">
      {photo("meja-lab", "", pos="50% 70%")}
      <div class="info-body">
        <h2>{e(SITE['name'])}</h2>
        <dl>
          <div><dt>{icon("pin")}Alamat kantor</dt><dd>{val(CONTACT['address'])}</dd>{maps}</div>
          <div><dt>{icon("phone")}Telepon</dt><dd>{phone}</dd></div>
          <div><dt>{icon("wa")}WhatsApp</dt><dd>{wa}</dd></div>
          <div><dt>{icon("mail")}Email</dt><dd>{mail}</dd></div>
          <div><dt>{icon("clock")}Jam operasional</dt><dd>{val(CONTACT['hours'])}</dd></div>
        </dl>
        {actions}
      </div>
    </aside>
  </div>
</div></section>

<section class="sec sec-mist"><div class="wrap">
  {sec_head("Arah pertanyaan", "Perusahaan yang", "akan menindaklanjuti", center=True)}
  {service_cards()}
</div></section>
"""
    page("hubungi-kami.html", "Hubungi Kami",
         "Alamat, telepon, WhatsApp, dan email CV Izdihaar 84 di Tamalanrea, Makassar, serta formulir pertanyaan bisnis.",
         "hubungi-kami.html", hubungi, ())

    # ---------- berkas SEO ----------
    base = SITE["base_url"].rstrip("/")
    if base:
        urls = "".join(f"<url><loc>{base}/{'' if p == 'index.html' else p}</loc></url>" for p in PAGES)
        (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n" + (f"Sitemap: {base}/sitemap.xml\n" if base else ""), encoding="utf-8")

    # ---------- varian pratinjau (halaman utama tanpa kerangka dokumen) ----------
    prev = ROOT / "preview"
    prev.mkdir(exist_ok=True)
    (prev / "index.html").write_text(
        f"<title>{e(SITE['name'])}</title>\n{ASSET_LINKS}\n" + header("index.html") + f'<main id="main">\n{PAGES["index.html"]}\n</main>\n' + footer(),
        encoding="utf-8")
    print("Selesai:", ", ".join(sorted(PAGES)))


if __name__ == "__main__":
    build()
