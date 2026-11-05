# Website CV Izdihaar 84

Situs statis enam halaman (Beranda, Tentang Kami, Layanan, Proyek, Berita, Hubungi Kami) untuk CV Izdihaar 84 sebagai induk perusahaan.

## Struktur
- `content/site.json`  semua data: kontak, profil, perusahaan, proyek, berita
- `src/assets/`        CSS (design system), JS, logo
- `build.py`           generator, menghasilkan folder `dist/`
- `dist/`              situs jadi, unggah isi folder ini ke hosting

## Memperbarui konten
1. Ubah `content/site.json`.
2. Jalankan `python3 build.py` (Python 3.12 atau lebih baru, tanpa pustaka tambahan).
3. Unggah isi `dist/` ke hosting.

Melihat situs di komputer: `cd dist && python3 -m http.server 8000`, lalu buka http://localhost:8000

## Desain (v6)
Company profile korporat: biru tua sebagai warna dasar, merah-biru-hijau logo sebagai aksen, foto
bersudut terpotong, dan garis tiga warna logo sebagai penanda identitas. Judul memakai Plus Jakarta Sans,
teks memakai Inter (keduanya berlisensi SIL Open Font License, disimpan di `src/assets/fonts/`).
Animasi muncul saat digulir hanya aktif bila JavaScript berjalan dan pengunjung tidak memilih
"kurangi gerakan" di perangkatnya; tanpa itu semua konten tetap tampil.

Struktur perusahaan: situs hanya menyebut bahwa CV Izdihaar 84 menaungi tiga perusahaan dengan fokus usaha
yang berbeda. Nama, logo, dan deskripsi perusahaan yang dinaungi tidak ditampilkan di mana pun, termasuk
metadata. Data `companies` di `content/site.json` hanya dipakai untuk menghitung jumlah dan bidangnya.
Logo lama disimpan di `content/arsip-logo-perusahaan/` dan tidak ikut diunggah.

Penanda isian yang belum dikonfirmasi tidak lagi ditampilkan di situs. Isinya tidak diubah.

## Foto
`furniture.jpg` sementara memakai foto ruang laboratorium (meja kerja, kabinet, lemari). Ganti dengan foto
furniture yang Anda pasok bila sudah tersedia, cukup timpa berkas dengan nama yang sama.

Foto di `src/assets/foto/` adalah foto ilustrasi dari Unsplash (Unsplash License: bebas dipakai
komersial, tanpa kewajiban atribusi). Ganti dengan foto perusahaan sendiri bila sudah tersedia,
cukup timpa berkas dengan nama yang sama.

| Berkas | Fotografer |
|---|---|
| hero.jpg | RephiLe water |
| ruang-lab.jpg | National Cancer Institute |
| jabat-tangan.jpg | Mina Rad |
| mikroskop.jpg | Logan Gutierrez |
| pipet.jpg | Louis Reed |
| pipet-meja.jpg | Adam Bezer |
| meja-lab.jpg | Trnava University |
| tabung.jpg | Testalize.me |
| sawah.jpg | Pan Species |
| sapi.jpg | Andrey Câmara |
| keramba.jpg | Bob Brewer |
| bibit.jpg | Roman Synkevych |
| gudang.jpg | Lance Chang |

## Yang masih perlu diisi (bertanda kuning di situs, atau disembunyikan sampai diisi)
- `contact.hours`: jam operasional tertulis "WIB", padahal Makassar memakai WITA. Mohon dicek.
- `about`: tahun berdiri, visi, misi, tonggak perjalanan (`milestones`: year, title, text)
- `site.base_url`: alamat domain, agar canonical, Open Graph, dan sitemap.xml dibuat
- `projects`: tahun dan perusahaan pelaksana untuk tiap proyek (kolom `year`, `company`), serta foto dokumentasi asli bila ada
- `companies[].website`: situs tiap perusahaan, bila ada
- Foto: simpan di `src/assets/`, lalu isi kolom `image` pada proyek atau berita
- Rumusan nilai perusahaan dan alur kontak di `build.py` (bertanda "perlu konfirmasi")

## Formulir pertanyaan bisnis
Formulir memeriksa isian, menyusun pesan, lalu menawarkan kirim lewat WhatsApp atau email
(aktif setelah `contact.whatsapp` / `contact.email` diisi) dan tombol salin. Situs ini statis,
jadi pesan tidak tersimpan di server. Untuk menerima pesan langsung di server, sambungkan
formulir ke layanan formulir atau backend milik perusahaan.
