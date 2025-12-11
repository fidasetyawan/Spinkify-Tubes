# SPINKIFY – Aplikasi Pemutar Musik Berbasis Python & Tkinter
SPINKIFY adalah aplikasi pemutar musik desktop yang dikembangkan sebagai proyek Tugas Besar Mata Kuliah Struktur Data. Aplikasi ini dibangun menggunakan Python dan Tkinter dengan tema antarmuka dark charcoal + pink accent untuk memberikan pengalaman visual yang modern dan nyaman digunakan.

Aplikasi ini mengimplementasikan dua struktur data utama:
- Binary Search Tree (BST) untuk menyimpan dan mencari lagu dalam library.
- Doubly Linked List (DLL) untuk mengelola playlist dan navigasi lagu (next/prev).

SPINKIFY menyediakan dua peran utama, yaitu Admin dan User, dengan fitur yang berbeda sesuai kebutuhan pengelolaan dan pemutaran lagu.
 
📌 Fitur Utama Aplikasi

🔐 1. Role Selection
Pengguna dapat memilih masuk sebagai:
- Admin → mengelola data lagu
- User → memutar lagu, membuat playlist, memberi like

🛠️ 2. Fitur Admin
Admin dapat melakukan operasi penuh pada library lagu:
- Menambahkan lagu baru
- Mengubah data lagu
- Menghapus lagu
- Menampilkan seluruh daftar lagu
- Validasi otomatis:
  - Tidak boleh menambah lagu dengan ID yang sama
  - Tidak boleh menambah lagu dengan data yang tidak lengkap
Semua data tersimpan permanen di file JSON.

🎧 3. Fitur User
User memiliki akses ke fitur pemutaran lagu dan personalisasi:

🎼 Library
- Melihat seluruh daftar lagu
- Melihat halaman Liked Songs
- Memberikan “like” pada lagu
- Mencari lagu berdasarkan judul/artist

📂 Playlist
- Membuat playlist baru
- Menambah lagu ke playlist melalui popup
- Menghapus lagu dari playlist
- Menavigasi playlist dengan tombol next/prev

▶️ Music Player
- Menampilkan cover album, judul, dan artis
- Tombol previous – play/pause – next
- Algoritma similarity untuk next/prev:
  - Prioritas artis sama → genre sama → fallback

🔍 Detail Lagu
- Halaman tampilan penuh (full card view)
- Tombol like, play, next, previous

🧱 Struktur Data yang Digunakan

🌲 1. Binary Search Tree (BST) – Library Lagu
Digunakan untuk:
- Menyimpan seluruh lagu berdasarkan ID
- Operasi insert, search, delete, in-order traversal
- Pencarian lebih cepat dan terstruktur

🔗 2. Doubly Linked List – Playlist
Dipilih karena:
- Mendukung navigasi dua arah (next & previous)
- Efisien untuk menambah/menghapus lagu dari playlist

📃 3. List/Array
Digunakan untuk:
- Hasil pencarian
- Menyusun daftar lagu mirip berdasarkan artist/genre

🖥️ Cara Instalasi & Menjalankan Aplikasi
1. Persyaratan
Pastikan sudah menginstal:
- Python 3.10+
- Library tambahan:

```python
from app import main
main()
```
2. Clone Repository
```python
git clone <URL_GITHUB_REPOSITORY>
cd spinkify
```
3. Menjalankan Aplikasi
```python
python app.py
```
4. Cara Menggunakan
- Jalankan aplikasi → halaman role selection
- Pilih Admin untuk mengelola lagu
- Pilih User untuk memutar lagu
- Gunakan sidebar untuk navigasi (All Songs, Liked, Playlist)
- Klik lagu untuk membuka halaman detail

👥 Anggota Kelompok
1. Nurul Firdasari Setyawan (103102400005)
2. Nadia Clearesta Shafira (103102400007)
3. Eliza Sekar Arum (103102400071)
