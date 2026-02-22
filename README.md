#  CURSED ISLAND ESCAPE

<img width="3780" height="1890" alt="CURSED(1)" src="https://github.com/user-attachments/assets/a6bd0ded-f651-48ea-a334-554426b8d1f0" />

<p align="center">
<strong>RPG Adventure Game dengan Sistem Pertarungan Kartu (Big Two) Berbasis Command Line Interface (CLI)</strong>

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
</p>

---

## Deskripsi Singkat

Cursed Island adalah sebuah permainan petualangan RPG berbasis Command Line Interface (CLI) yang dibangun menggunakan bahasa pemrograman Python. Pemain berperan sebagai salah satu dari lima karakter unik yang terjebak di sebuah pulau misterius.

Tujuan utama pemain adalah melarikan diri dari pulau terkutuk ini dengan cara mengumpulkan anggota tim, mencari item kunci, memecahkan misteri, dan mengalahkan musuh menggunakan strategi kombinasi kartu poker. Proyek ini merupakan tugas akhir dari kelas X RPL 1 SMKN 2 JAKARTA dan kegabutan para contributornya.

---

## Fitur Utama

- **Sistem Karakter Unik:** 5 karakter pilihan (Vio, Haikaru, Ao Lin, Arganta, Ignatius) dengan latar belakang, stats, dan skill spesifik yang memengaruhi strategi permainan.
- **Mekanisme Combat Kartu:** Sistem pertarungan turn-based menggunakan logika poker (High Card, Pair, Flush, Straight Flush, dll) untuk menentukan kekuatan serangan.
- **Inventory:** Pengelolaan item kunci dan *quest items* untuk memecahkan puzzle lingkungan serta membuka progres chapter.
- **Peta Eksplorasi:** Sistem pergerakan pemain di peta 2D yang dinamis, lengkap dengan kemunculan musuh, NPC interaktif, dan objek tersembunyi.
- **Save/Load System:** Fitur penyimpanan progres yang kini mendukung hingga 5 slot (data.txt hingga data4.txt) dengan sistem proteksi data Base64.
- **Multi-language UI:** Antarmuka yang mendukung karakter UTF-8 untuk visualisasi peta yang kaya warna dan fitur *autofit* yang responsif terhadap ukuran terminal.
- **Boss Retry & Checkpoint:** Mekanisme percobaan ulang hingga 3 kali saat kalah melawan Boss dan sistem *snapshot* status otomatis sebelum pertempuran besar dimulai.
- **Layanan Walkie-Talkie:** Akses menu toko dan interaksi NPC khusus (Bran Edwards) secara praktis melalui tombol pintas **[B]** tanpa harus kembali ke lokasi tertentu.
- **Progresi Chapter:** Alur cerita mendalam yang terbagi dalam 6 Chapter, di mana setiap Chapter memiliki objektif unik dan syarat penyelesaian *sidequest* tertentu.

---

## Cara Menjalankan Program

### Prasyarat (Requirements)
- **Python 3.6 atau versi lebih baru** terinstal di komputer Anda.
- Terminal atau Command Prompt (Windows/Linux/macOS).

### Langkah Instalasi & Menjalankan

1.  **Clone Repository**
    Unduh atau clone repository ini ke komputer lokal Anda.
    ```bash
    git clone https://github.com/Prono365/ludo.git
    cd ludo
    ```
    *(Jika menggunakan file ZIP, ekstrak file tersebut dan buka foldernya).*

2.  **Verifikasi File**
    Pastikan file utama `main.py` dan file pendukung lainnya (`characters.py`, `story.py`, `combat.py`, dll.) berada dalam satu folder yang sama.

3.  **Jalankan Game**
    Buka terminal di dalam folder proyek, jalankan `launcher.bat` atau ketik perintah berikut:

    ```bash
    python main.py
    ```
    *(Jika perintah di atas tidak bekerja, coba gunakan `python3 main.py`).*

4.  **Mulai Bermain**
    Game akan membersihkan layar terminal dan memulai dengan menu utama. Ikuti petunjuk pada layar untuk memilih karakter dan memulai petualangan.

---

## Struktur Folder/File

Berikut adalah penjelasan singkat mengenai struktur utama proyek ini:

```
├── launcher.bat           # Launcher program.
├── main.py                # Entry point utama program, loop game, dan menu.
├── characters.py          # Database karakter, stats, skill, dan data NPC.
├── enemies.py             # Data musuh, boss, dan logika spawn musuh.
├── exploration.py         # Logika pembuatan peta (GameMap), pergerakan, dan eksplorasi.
├── combat.py              # Sistem pertarungan, logika kartu poker, dan damage calculation.
├── story.py               # Database narasi cerita, dialog, dan ending.
├── character_routes.py    # Konfigurasi rute spesifik per karakter dan quest NPC.
├── npc_interactions.py    # Dialog panjang untuk interaksi NPC (Side Quest & Story).
├── sprites.py             # Definisi warna ANSI dan karakter ASCII untuk UI.
├── gamestate.py           # Kelas GameState untuk manajemen data pemain (HP, Inventory, Save/Load).
├── utils.py               # Fungsi utilitas bantu (clear screen, input handling).
├── constants.py           # Konstanta global game (versi, ukuran terminal, dll).
├── tutorial.py            # Modul tutorial interaktif untuk pemain baru.
├── card_dialogs.json      # Database dialog singkat saat combat (kutipan kartu).
└── README.md              # Dokumentasi proyek (file ini).
```

---

## Anggota Kelompok

Proyek ini dikembangkan oleh siswa **SMKN 2 JAKARTA Kelas X RPL 1**:

1.  **Ahmad Haikal Ramadhan**
2.  **Alif Rizky Ramadhan Atmadja**
3.  **M Vallerian Aprilio Gunawan**
4.  **Ignatius Nino Jumantoro**
5.  **Evan Arganta**

---

## Cara Bermain (Singkat)

- **Navigasi:** Gunakan tombol `W`, `A`, `S`, `D` untuk bergerak di peta.
- **Interaksi:** Tekan `I` untuk Inventory,`X` untuk Save.
- **Combat:** Pilih kartu dengan memasukkan nomor indeks (contoh: `0,1,2` untuk memainkan 3 kartu sekaligus).
- **Skill:** Tekan `S` saat bertarung untuk menggunakan kemampuan khusus karakter.
- **Tujuan:** Selesaikan quest utama setiap chapter, rekrut teman, dan kalahkan boss untuk melarikan diri.

---

## Lisensi

Proyek ini dibuat sebagai tugas sekolah dan dirilis di bawah ![License](https://img.shields.io/badge/license-MIT-blue).

---

<p align="center">
<strong>Justice for the Victims</strong>
</p>
