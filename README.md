# SPINKIFY – Aplikasi Pemutar Musik Berbasis Python & Tkinter

SPINKIFY adalah aplikasi pemutar musik desktop yang dikembangkan sebagai proyek Tugas Besar Mata Kuliah Struktur Data. Aplikasi ini dibangun menggunakan bahasa pemrograman Python dan library Tkinter dengan tema antarmuka dark charcoal dengan aksen pink untuk memberikan pengalaman visual yang modern dan nyaman digunakan.

Aplikasi ini mengimplementasikan beberapa struktur data utama, yaitu:
- Doubly Linked List (DLL) untuk menyimpan library lagu dan mendukung navigasi next/previous.
- Singly Linked List (SLL) untuk mengelola playlist lagu.
- Record (tipe data bentukan) untuk merepresentasikan data lagu.

SPINKIFY menyediakan dua peran utama, yaitu Admin dan User, dengan fitur yang berbeda sesuai kebutuhan pengelolaan dan pemutaran lagu.

---

## 📌 Fitur Utama Aplikasi

### 🔐 1. Role Selection
Pengguna dapat memilih masuk sebagai:
- **Admin** → mengelola data lagu
- **User** → memutar lagu, membuat playlist, dan memberi like

---

### 🛠️ 2. Fitur Admin
Admin memiliki akses penuh terhadap pengelolaan library lagu:
- Menambahkan lagu baru
- Mengubah data lagu
- Menghapus lagu
- Menampilkan seluruh daftar lagu
- Validasi otomatis:
  - ID lagu tidak boleh duplikat
  - Data lagu wajib diisi lengkap

Seluruh data disimpan secara permanen dalam berkas JSON.

---

### 🎧 3. Fitur User

#### 🎼 Library
- Melihat seluruh daftar lagu
- Melihat halaman Liked Songs
- Memberikan tanda like pada lagu
- Mencari lagu berdasarkan judul atau artis

#### 📂 Playlist
- Membuat playlist baru
- Menambahkan lagu ke playlist melalui popup
- Menghapus lagu dari playlist
- Navigasi playlist menggunakan tombol next dan previous

#### ▶️ Music Player
- Menampilkan sampul album, judul lagu, dan artis
- Tombol previous, play/pause, dan next
- Navigasi next dan previous menggunakan logika kemiripan lagu:
  - Prioritas artis yang sama
  - Dilanjutkan genre yang sama
  - Fallback ke lagu lain jika tidak ditemukan

#### 🔍 Detail Lagu
- Tampilan detail lagu secara penuh
- Tombol like, play, next, dan previous

---

## 🧱 Struktur Data yang Digunakan

### 🔗 1. Doubly Linked List – Library Lagu
Digunakan untuk:
- Menyimpan seluruh lagu dalam library
- Mendukung navigasi dua arah (next dan previous)
- Mempermudah penghapusan dan traversal lagu

### 🔗 2. Singly Linked List – Playlist
Digunakan karena:
- Playlist bersifat linier
- Tidak membutuhkan navigasi dua arah
- Efisien untuk penambahan dan penghapusan lagu

### 📃 3. Record (Tipe Data Bentukan)
Setiap lagu direpresentasikan sebagai record yang berisi:
- ID lagu
- Judul
- Artis
- Genre
- Album
- Tahun rilis
- Path audio dan gambar

## 👥 Anggota Kelompok
1. Nurul Firdasari Setyawan (103102400005)
2. Nadia Clearesta Shafira (103102400007)
3. Eliza Sekar Arum (103102400071)
