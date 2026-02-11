import os
import time


SAVE_FILE = "data.txt"


def write_data(nama_pemain, scene_id, inventory, jam_tersisa):
    """
    Menyimpan progres ke file data.txt.
    Format:
      Baris 1: Nama Pemain
      Baris 2: Scene ID
      Baris 3: Inventory (dipisah koma)
      Baris 4: Jam tersisa
    """
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(str(nama_pemain) + "\n")
            f.write(str(scene_id) + "\n")
            f.write(",".join(inventory) + "\n")
            f.write(str(jam_tersisa))
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan data: {e}")


def load_progress():
    """
    Membaca data dari file data.txt.
    Mengembalikan tuple (nama, scene, inventory, jam).
    Jika file tidak ada/rusak, kembalikan default.
    """
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                baris = f.readlines()
                if len(baris) >= 4:
                    nama    = baris[0].strip()
                    scene   = baris[1].strip()
                    inv_raw = baris[2].strip()
                    jam     = int(baris[3].strip())
                    inventory = [i for i in inv_raw.split(",") if i]
                    return nama, scene, inventory, jam
        except Exception as e:
            print(f"[ERROR] Gagal membaca save: {e}")
    return None, "awal", [], 48


def delete_save():
    """Menghapus file save saat game selesai."""
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
        except Exception:
            pass



def slow_print(text, delay=0.015):
    """Efek ketik seperti novel."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(bab, jam_tersisa, inventory):
    """Mencetak header scene dengan status jam dan inventory."""
    print("=" * 60)
    print(f"  ESCAPE FROM EPSTEIN ISLAND")
    print(f"  {bab}")
    print("=" * 60)

    bar_panjang = 30
    sisa_ratio  = jam_tersisa / 48
    bar_isi     = int(bar_panjang * sisa_ratio)
    bar         = "[" + "█" * bar_isi + "░" * (bar_panjang - bar_isi) + "]"
    print(f"  ⏱  WAKTU TERSISA: {jam_tersisa} jam  {bar}")

    if inventory:
        print(f"  🎒 Inventory: {', '.join(inventory)}")
    else:
        print(f"  🎒 Inventory: (kosong)")
    print("-" * 60)


def tampilkan_inventory(inventory):
    """Menampilkan isi inventory secara detail."""
    print("\n" + "=" * 40)
    print("  🎒 INVENTORY KAMU")
    print("=" * 40)
    deskripsi = {
        "Kunci Rekreasi"  : "Kunci dari Ignatius. Buka beberapa pintu.",
        "Buku Merah"      : "Buku milik Haikaru. Berisi peta rahasia.",
        "Kalkulator Vio"  : "Alat Vio. Bisa hack panel listrik.",
        "Rosario Arganta" : "Pemberian Arganta. Simbol keberanian.",
        "Peta Dermaga"    : "Ditemukan di perpustakaan. Tunjukkan jalan.",
        "Pisau Dapur"     : "Ditemukan di dapur. Untuk berjaga-jaga.",
    }
    if not inventory:
        print("  Kamu belum punya item apapun.")
    else:
        for item in inventory:
            desc = deskripsi.get(item, "Item misterius.")
            print(f"  • {item}: {desc}")
    print("=" * 40)
    input("\nTekan [Enter] untuk kembali...")



def tampilkan_judul():
    """Layar judul utama game."""
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        E S C A P E   F R O M   E P S T E I N            ║
║                I S L A N D                              ║
║                                                          ║
║              ── The 48-Hour Countdown ──                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)


def menu_utama():
    """
    Menampilkan menu utama dan mengembalikan pilihan user.
    Return: 'baru', 'lanjut', 'tentang', atau 'keluar'
    """
    ada_save = os.path.exists(SAVE_FILE)

    print("  MENU UTAMA")
    print("-" * 30)
    print("  1. Mulai Game Baru")
    if ada_save:
        print("  2. Lanjutkan Permainan")
    print("  3. Tentang Game")
    print("  4. Keluar")
    print("-" * 30)

    while True:
        try:
            pil = int(input("  Pilihan: "))
            if pil == 1:
                return "baru"
            elif pil == 2 and ada_save:
                return "lanjut"
            elif pil == 3:
                return "tentang"
            elif pil == 4:
                return "keluar"
            else:
                print("  Pilihan tidak valid.")
        except ValueError:
            print("  Masukkan angka!")


def layar_tentang():
    """Menampilkan info tentang game."""
    clear_screen()
    print("=" * 50)
    print("  TENTANG GAME")
    print("=" * 50)
    slow_print("  Escape from Epstein Island adalah game")
    slow_print("  petualangan teks berbasis pilihan.")
    slow_print("")
    slow_print("  Kamu berperan sebagai anak 12 tahun yang")
    slow_print("  terjebak di pulau misterius milik Epstein.")
    slow_print("  Bersama Haikaru, Aolinh, Ignatius, Arganta,")
    slow_print("  dan Vio — kalian punya 48 jam untuk kabur.")
    slow_print("")
    slow_print("  Setiap pilihan menguras waktu.")
    slow_print("  Kumpulkan item. Selesaikan tantangan.")
    slow_print("  Kalahkan Epstein. Raih kebebasan.")
    print("=" * 50)
    input("\nTekan [Enter] untuk kembali ke menu...")


def intro_epstein():
    """Cutscene intro untuk game baru."""
    clear_screen()
    print("   ESCAPE FROM EPSTEIN ISLAND")
    print("      (The 48-Hour Countdown)")
    print("-" * 40)
    time.sleep(1.5)
    print("\n[Suara intercom berbunyi dengan nada rendah dan mengancam...]\n")
    time.sleep(1.5)
    slow_print("Epstein: 'Selamat pagi, anak-anak kecilku. Tidur nyenyak?'")
    slow_print("Epstein: 'Aku bukan monster yang suka membunuh cepat.'")
    slow_print("Epstein: 'Jadi, aku kasih kalian waktu dua hari — empat puluh delapan jam.'")
    slow_print("Epstein: 'Silakan coba keluar. Aku sudah siapkan permainannya.'")
    slow_print("Epstein: 'Selamat bermain lari-lari... Jangan sampai aku kecewa.'")
    slow_print("\n[Suara tertawa dingin menghilang, digantikan detak jam...]")
    time.sleep(1)
    input("\nTekan [Enter] untuk membuka mata...")


def intro_player():
    """Meminta nama pemain untuk game baru."""
    clear_screen()
    print("   IDENTIFIKASI KARAKTER")
    print("-" * 30)
    while True:
        nama = input("\nSiapa namamu? : ").strip()
        if nama:
            return nama
        print("Nama tidak boleh kosong!")



def get_story():
    """
    Mengembalikan dictionary berisi semua scene cerita.
    Setiap scene punya: bab, text, dialog karakter,
    choices, next scenes, item (opsional), jam_kurang.
    """
    story = {


        "awal": {
            "bab": "HARI KE-1: 07:00 PAGI — SEL PENJARA",
            "text": (
                "Kamu terbangun dengan rasa berat di dada.\n"
                "Bau pengap dan lembab menyengat hidungmu.\n\n"
                "Di sudut kamar yang paling gelap, ada dua sosok.\n\n"
                "Pertama, AOLINH. Gadis 9 tahun itu meringkut\n"
                "memakai gaun hitam panjang, matanya merah habis menangis.\n\n"
                "Kedua, HAIKARU (13 tahun) berdiri di dekat jendela,\n"
                "memegang sebuah Buku Merah dengan erat.\n\n"
                "Di dinding sel ada coretan tangan anak-anak:\n"
                "'TOLONG KAMI.'"
            ),
            "haikaru": "Haikaru: 'Kau akhirnya bangun juga. Waktunya kita terbatas.'",
            "aolinh" : "Aolinh: 'Kak... aku takut. Aku mimpi Epstein datang...'",
            "choices": [
                "1. Tanya rencana pada Haikaru",
                "2. Tenangkan Aolinh dulu",
                "3. Coba keluar sendiri (berbahaya)",
                "4. Periksa seluruh isi sel"
            ],
            "next"    : ["tanya_haikaru", "tenangkan_aolinh", "jalan_sendiri", "periksa_sel"],
            "jam_kurang": 0,
        },

        "periksa_sel": {
            "bab"  : "HARI KE-1: 07:15 PAGI — MENGGELEDAH SEL",
            "text" : (
                "Kamu memeriksa setiap sudut sel dengan teliti.\n\n"
                "Di bawah kasur tipis, ada FOTO KELUARGA.\n"
                "Foto itu milik siapa? Tidak ada nama.\n"
                "Tapi di baliknya ada tulisan kecil:\n"
                "'Pintu barat lemah di malam hari. — R'\n\n"
                "Siapa R? Dan apa artinya 'lemah'?\n\n"
                "Kamu menyimpan foto itu."
            ),
            "haikaru" : "Haikaru: 'Apa kamu temukan? Bagus. Simpan itu baik-baik.'",
            "choices" : ["1. Lanjutkan ke rencana bersama Haikaru"],
            "next"    : ["tanya_haikaru"],
            "item"    : "Foto Misterius",
            "jam_kurang": 1,
        },

        "jalan_sendiri": {
            "bab"  : "HARI KE-1: 07:15 PAGI — KESALAHAN",
            "text" : (
                "Kamu mencoba berlari ke pintu utama sendirian.\n"
                "Seketika medan magnet menyengat seluruh tubuhmu!\n"
                "Kamu terpental ke dinding. Seluruh badan lemas.\n\n"
                "Penjaga tidak muncul — mungkin mereka memang\n"
                "sudah tahu kamu akan gagal."
            ),
            "epstein": "Epstein [intercom]: 'Ah, egois. Kembali dalam, bodoh kecil.'",
            "haikaru": "Haikaru: 'Sudah kubilang. Jangan sendirian.'",
            "choices" : ["1. Kembali dan dengarkan Haikaru"],
            "next"    : ["awal"],
            "jam_kurang": 2,
        },

        "tenangkan_aolinh": {
            "bab"  : "HARI KE-1: 07:30 PAGI — PERSAHABATAN",
            "text" : (
                "Kamu duduk di sebelah Aolinh dan menggenggam tangannya.\n"
                "'Kita akan keluar bersama, aku janji.'\n\n"
                "Aolinh mengangguk pelan. Ada senyum tipis di bibirnya.\n"
                "Haikaru memandang kalian dari ambang pintu.\n\n"
                "Ada sesuatu yang berbeda dari tatapan Aolinh sekarang.\n"
                "Ketakutan masih ada, tapi ada api kecil di matanya."
            ),
            "aolinh" : "Aolinh: 'Aku percaya kamu, Kak. Kalau kamu ada, aku tidak takut.'",
            "haikaru": "Haikaru: 'Bagus. Sekarang ayo. Tidak ada waktu terbuang.'",
            "choices" : [
                "1. Ikuti Haikaru ke koridor",
                "2. Tanya Aolinh apakah dia tahu sesuatu tentang pulau ini"
            ],
            "next"    : ["koridor_utama", "aolinh_tau_rahasia"],
            "jam_kurang": 1,
        },

        "aolinh_tau_rahasia": {
            "bab"  : "HARI KE-1: 07:45 PAGI — RAHASIA AOLINH",
            "text" : (
                "Kamu bertanya pelan pada Aolinh.\n"
                "Gadis kecil itu ragu sebentar, lalu berbisik.\n\n"
                "'Waktu aku tidak bisa tidur... aku dengar dua penjaga\n"
                " bicara. Mereka bilang ada ruangan tersembunyi\n"
                " di bawah kapel. Katanya di sana ada... tombol darurat.\n"
                " Tombol yang bisa matikan semua magnet sekaligus.'\n\n"
                "Aolinh meremas tanganmu. 'Tapi itu tempat yang\n"
                "paling dijaga, Kak.'"
            ),
            "aolinh"  : "Aolinh: 'Aku tidak mau kamu kenapa-kenapa karena info itu.'",
            "haikaru" : "Haikaru: 'Tombol darurat... Vio pasti bisa aktifkan itu.'",
            "choices" : ["1. Catat info ini dan lanjutkan ke koridor"],
            "next"    : ["koridor_utama"],
            "item"    : "Info Tombol Darurat",
            "jam_kurang": 1,
        },

        "tanya_haikaru": {
            "bab"  : "HARI KE-1: 07:30 PAGI — RENCANA HAIKARU",
            "text" : (
                "Kamu menghampiri Haikaru. Dia membuka Buku Merah\n"
                "dan menunjukkan coretan peta yang samar.\n\n"
                "'Pulau ini punya sistem keamanan magnetik.\n"
                " Untuk menonaktifkannya, kita butuh tiga komponen:\n"
                " kunci dari Ignatius, kalkulasi dari Vio,\n"
                " dan... sesuatu di Perpustakaan Tua.'\n\n"
                "Haikaru menunjuk halaman terakhir buku.\n"
                "Ada satu kata besar ditulis tangan: DERMAGA."
            ),
            "haikaru": "Haikaru: 'Tujuan akhir kita dermaga. Ikuti urutannya.'",
            "choices" : [
                "1. Langsung ikuti rencana Haikaru",
                "2. Tanya tentang isi Buku Merah lebih lanjut"
            ],
            "next"    : ["koridor_utama", "isi_buku_merah"],
            "jam_kurang": 1,
        },

        "isi_buku_merah": {
            "bab"  : "HARI KE-1: 07:50 PAGI — BUKU MERAH",
            "text" : (
                "Haikaru menghela napas, lalu menyerahkan buku itu.\n\n"
                "Kamu membukanya. Isinya bukan hanya peta.\n"
                "Ada nama-nama. Tanggal. Foto buram.\n"
                "Dan di halaman terakhir — daftar panjang\n"
                "nama orang-orang yang pernah berada di pulau ini.\n\n"
                "Banyak yang tidak pernah kembali.\n\n"
                "Kamu menutup buku itu. Tanganmu gemetar."
            ),
            "haikaru" : "Haikaru: 'Sekarang kamu tahu mengapa kita harus keluar.'",
            "choices" : ["1. Tekadmu semakin kuat. Ayo pergi."],
            "next"    : ["koridor_utama"],
            "jam_kurang": 1,
        },


        "koridor_utama": {
            "bab"  : "HARI KE-1: 08:30 PAGI — PERSIMPANGAN",
            "text" : (
                "Kalian berjalan di koridor kotor berlampu remang.\n"
                "Ada tiga percabangan di depan:\n\n"
                " → Kiri   : Ruang Rekreasi (terdengar suara game)\n"
                " → Tengah : Laboratorium  (bau kimia menyengat)\n"
                " → Kanan  : Koridor Layanan (gelap dan sepi)\n\n"
                "Haikaru membaca peta dan menunjuk ke kiri."
            ),
            "aolinh" : "Aolinh: 'Aku dengar suara ketawa dari kiri...'",
            "haikaru": "Haikaru: 'Itu Ignatius. Ikuti aku, jangan terpisah.'",
            "choices" : [
                "1. Masuk Ruang Rekreasi (ikuti Haikaru)",
                "2. Intip Laboratorium dulu — cari item",
                "3. Cek Koridor Layanan — ada yang menarik",
                "4. Sembunyikan Aolinh dulu sebelum melanjutkan"
            ],
            "next"     : ["ruang_rekreasi", "laboratorium_awal", "koridor_layanan", "sembunyikan_aolinh"],
            "jam_kurang": 1,
        },

        "sembunyikan_aolinh": {
            "bab"  : "HARI KE-1: 08:45 PAGI — TEMPAT AMAN",
            "text" : (
                "Kamu memutuskan Aolinh terlalu berisiko dibawa ke depan.\n"
                "Kamu menemukan lemari tua di sudut koridor.\n\n"
                "Aolinh masuk tanpa protes, tapi matanya basah.\n"
                "'Kamu akan kembali kan, Kak?'\n\n"
                "Kamu mengangguk mantap."
            ),
            "aolinh"  : "Aolinh: 'Kalau 2 jam tidak kembali... aku akan cari jalan sendiri.'",
            "haikaru" : "Haikaru: 'Keputusan yang bijak. Dia lebih aman di sana.'",
            "choices" : ["1. Lanjutkan ke Ruang Rekreasi"],
            "next"    : ["ruang_rekreasi"],
            "jam_kurang": 1,
        },

        "laboratorium_awal": {
            "bab"  : "HARI KE-1: 09:00 PAGI — LABORATORIUM",
            "text" : (
                "Kamu mengintip ke Laboratorium.\n"
                "Rak-rak penuh tabung kimia berjajar rapi.\n"
                "Bau asam membakar hidung.\n\n"
                "Di pojok, ada laci terbuka...\n"
                "Kamu menemukan PISAU DAPUR berkarat\n"
                "tersembunyi di balik kain lap.\n\n"
                "Di meja sebelahnya ada CATATAN PENELITI:\n"
                "'Sistem pengaman diperbarui setiap Selasa. Hari ini Selasa.'"
            ),
            "haikaru": "Haikaru: 'Ambil pisau itu. Catatan itu juga berguna.'",
            "choices" : ["1. Ambil keduanya dan ke Ruang Rekreasi"],
            "next"    : ["ruang_rekreasi"],
            "item"    : "Pisau Dapur",
            "jam_kurang": 2,
        },

        "koridor_layanan": {
            "bab"  : "HARI KE-1: 09:00 PAGI — KORIDOR LAYANAN",
            "text" : (
                "Koridor ini sangat gelap. Langkahmu bergema.\n"
                "Tiba-tiba kamu melihat sesuatu di lantai:\n"
                "sebuah KARTU AKSES warna merah, tergeletak\n"
                "di dekat saluran pembuangan.\n\n"
                "Sebelum kamu mengambilnya, suara langkah terdengar!\n"
                "Kalian berlari dan nyaris tertangkap.\n"
                "Kamu berhasil lolos, tapi habis banyak waktu."
            ),
            "aolinh" : "Aolinh: 'Jangan tinggalkan aku di tempat gelap!'",
            "haikaru": "Haikaru: 'Tapi kartu itu mungkin penting. Bagus kamu ambil.'",
            "choices" : ["1. Ke Ruang Rekreasi dengan kartu akses"],
            "next"    : ["ruang_rekreasi"],
            "item"    : "Kartu Akses Merah",
            "jam_kurang": 3,
        },


        "ruang_rekreasi": {
            "bab"  : "HARI KE-1: 09:30 PAGI — RUANG REKREASI",
            "text" : (
                "Kalian masuk ke ruangan penuh poster game.\n"
                "IGNATIUS (12 tahun) duduk di kursi usang,\n"
                "matanya tertancap di layar kecil, bermain game retro.\n\n"
                "Rambutnya acak-acakan, ada kemeja bermotif pixel art.\n"
                "Di meja sebelahnya ada beberapa snack kosong\n"
                "dan sebuah solder yang terlihat baru dipakai."
            ),
            "haikaru": "Haikaru: 'Ignatius. Berhenti sebentar. Ini serius.'",
            "choices" : [
                "1. Minta kunci dengan baik-baik",
                "2. Paksa ambil kunci",
                "3. Tantang dia main game",
                "4. Tunjukkan Kartu Akses (jika punya)"
            ],
            "next"     : ["minta_kunci_baik", "paksa_kunci", "tantang_game", "tunjuk_kartu"],
            "jam_kurang": 0,
        },

        "tunjuk_kartu": {
            "bab"  : "HARI KE-1: 10:00 PAGI — KARTU AJAIB",
            "text" : (
                "Kamu mengeluarkan Kartu Akses Merah.\n"
                "Ignatius langsung melonjak dari kursinya!\n\n"
                "'ITU KARTU LEVEL 3! Dari mana kamu dapat itu?!'\n\n"
                "Matanya berbinar tidak percaya.\n"
                "'Dengan kartu itu kita bisa buka pintu lift bawah tanah\n"
                " langsung ke area dermaga tanpa lewat terowongan panjang!'"
            ),
            "ignatius": "Ignatius: 'Deal. Kamu bawa kartu itu, aku bawa kunci dan skillku.'",
            "choices" : ["1. Sepakat — Ignatius bergabung dengan cara terbaik!"],
            "next"    : ["cari_arganta"],
            "item"    : "Kunci Rekreasi",
            "jam_kurang": 0,
        },

        "minta_kunci_baik": {
            "bab"  : "HARI KE-1: 10:00 PAGI — NEGOSIASI",
            "text" : (
                "Kamu duduk di sebelah Ignatius dan bercerita\n"
                "tentang rencana kabur kalian.\n\n"
                "Mata Ignatius perlahan berubah serius.\n"
                "Game-nya masih berjalan tapi dia tidak peduli lagi.\n\n"
                "'Jadi... kita beneran bisa keluar dari sini?\n"
                " Aku udah tiga bulan di sini sendirian...'\n\n"
                "Suaranya patah di akhir kalimat."
            ),
            "ignatius": "Ignatius: 'Oke. Aku ikut. Game bisa dilanjut nanti... kalau ada nanti.'",
            "choices"  : [
                "1. Sambut Ignatius bergabung",
                "2. Tanya kenapa dia bisa bertahan 3 bulan sendirian"
            ],
            "next"     : ["cari_arganta", "ignatius_cerita"],
            "item"     : "Kunci Rekreasi",
            "jam_kurang": 1,
        },

        "ignatius_cerita": {
            "bab"  : "HARI KE-1: 10:30 PAGI — KISAH IGNATIUS",
            "text" : (
                "Ignatius menatap lantai. Suaranya pelan.\n\n"
                "'Aku bertahan karena punya misi. Aku modifikasi\n"
                " semua mesin game di sini. Di dalamnya aku sembunyikan\n"
                " rekaman audio percakapan para penjaga.\n"
                " Semua tersimpan di chip kecil di sini.'\n\n"
                "Dia mengeluarkan sebuah chip dari dalam game console.\n\n"
                "'Ini bukti yang lebih kuat dari apapun yang ada di\n"
                " Buku Merah itu. Suara asli. Tanggal asli.'"
            ),
            "ignatius": "Ignatius: 'Sekarang aku punya alasan untuk keluar.'",
            "haikaru" : "Haikaru: 'Ini... luar biasa. Ambil chip itu.'",
            "choices" : ["1. Ambil chip dan lanjutkan misi"],
            "next"    : ["cari_arganta"],
            "item"    : "Chip Bukti Rekaman",
            "jam_kurang": 1,
        },

        "paksa_kunci": {
            "bab"  : "HARI KE-1: 10:00 PAGI — KONFRONTASI",
            "text" : (
                "Kamu mencoba merebut kunci secara paksa.\n"
                "Ignatius kaget dan berteriak keras!\n\n"
                "Suaranya bergema ke seluruh lorong.\n"
                "Kamu dengar langkah penjaga mendekat!\n\n"
                "Kalian berlari ke dalam gudang dan bersembunyi\n"
                "hampir dua jam dalam gelap yang pengap."
            ),
            "haikaru" : "Haikaru: 'Itu ceroboh sekali. Kita buang banyak waktu!'",
            "ignatius" : "Ignatius: '...Aku ikut. Tapi jangan perlakukan aku seperti itu lagi.'",
            "choices"  : ["1. Minta maaf dan lanjutkan"],
            "next"     : ["cari_arganta"],
            "item"     : "Kunci Rekreasi",
            "jam_kurang": 3,
        },

        "tantang_game": {
            "bab"  : "HARI KE-1: 10:30 PAGI — DUEL RETRO",
            "text" : (
                "Kamu menantang Ignatius bermain game.\n"
                "'Kalau aku menang, kamu kasih kuncinya.'\n\n"
                "Ignatius menatapmu sedetik lalu menyeringai lebar.\n"
                "'Kamu berani. Deal.'\n\n"
                "Lima menit pertama — Ignatius dominan.\n"
                "Sepuluh menit — kamu mulai menemukan ritme.\n"
                "Dua puluh menit — ronde ketiga.\n\n"
                "KAMU MENANG tipis. Ignatius melempar controller\n"
                "ke kursi, tertawa tidak percaya."
            ),
            "ignatius" : "Ignatius: 'WHAT?! Oke oke, kuncinya. Dan aku ikut — aku mau rematch!'",
            "choices"  : ["1. Tertawa dan ajak Ignatius bergabung"],
            "next"     : ["cari_arganta"],
            "item"     : "Kunci Rekreasi",
            "jam_kurang": 2,
        },


        "cari_arganta": {
            "bab"  : "HARI KE-1: 12:00 SIANG — RUANG MEDITASI",
            "text" : (
                "Kalian berempat kini menuju Ruang Meditasi.\n"
                "Ruangan itu tenang, berbau dupa dan kayu tua.\n\n"
                "ARGANTA (12 tahun) berlutut di pojok ruangan,\n"
                "mata tertutup, tangan mengatup di atas rosario.\n\n"
                "Tidak ada suara selain dengung angin dari ventilasi\n"
                "dan bisikan Arganta yang berdoa pelan."
            ),
            "arganta" : "Arganta: 'Aku sudah menunggu kalian. Tuhan tidak pernah salah waktu.'",
            "haikaru" : "Haikaru: 'Arganta, kami butuh kamu. Kamu tahu jalan bawah tanah.'",
            "choices" : [
                "1. Minta Arganta memimpin jalan bawah tanah",
                "2. Tanya apa yang Arganta ketahui tentang pulau ini",
                "3. Tanya apakah Arganta pernah mencoba kabur sebelumnya"
            ],
            "next"    : ["arganta_ikut", "arganta_cerita", "arganta_pernah_coba"],
            "jam_kurang": 1,
        },

        "arganta_pernah_coba": {
            "bab"  : "HARI KE-1: 12:30 SIANG — PERCOBAAN LAMA",
            "text" : (
                "Arganta membuka matanya. Ada kesedihan di sana.\n\n"
                "'Tiga bulan lalu. Aku dan dua orang lain.\n"
                " Kami hampir sampai ke dermaga.\n"
                " Tapi Epstein sudah menunggu.\n"
                " Yang dua... tidak kembali ke sel.'\n\n"
                "Arganta menelan ludah.\n\n"
                "'Kali ini berbeda. Karena kalian lebih banyak.\n"
                " Dan aku tahu di mana letak blind spot kamera\n"
                " di sepanjang jalur dermaga.'"
            ),
            "arganta" : "Arganta: 'Aku catat semua di kepala. Ikuti aku.'",
            "choices" : ["1. Percayakan jalur pada Arganta"],
            "next"    : ["cari_vio"],
            "item"    : "Rute Blind Spot",
            "jam_kurang": 1,
        },

        "arganta_cerita": {
            "bab"  : "HARI KE-1: 12:30 SIANG — RAHASIA ARGANTA",
            "text" : (
                "Arganta membuka matanya perlahan.\n\n"
                "'Pulau ini punya terowongan bawah tanah\n"
                " yang dibangun sebelum Epstein datang.\n"
                " Aku temukan dari buku tua di kapel.'\n\n"
                "Dia menyodorkan sebuah rosario tua ke tanganmu.\n"
                "'Ini untuk keberanian. Kamu akan butuh itu.'"
            ),
            "arganta" : "Arganta: 'Aku siap. Tuhan yang akan lindungi kita.'",
            "choices" : ["1. Terima rosario dan ajak Arganta"],
            "next"    : ["cari_vio"],
            "item"    : "Rosario Arganta",
            "jam_kurang": 1,
        },

        "arganta_ikut": {
            "bab"  : "HARI KE-1: 12:30 SIANG — BERGABUNG",
            "text" : (
                "Arganta berdiri, memasukkan rosarionya ke saku,\n"
                "dan mengangguk mantap.\n\n"
                "'Jalan bawah tanah ada di bawah kapel.\n"
                " Tapi kita butuh seseorang yang bisa\n"
                " membobol panel elektroniknya.'"
            ),
            "haikaru" : "Haikaru: 'Vio. Kita butuh Vio.'",
            "choices"  : ["1. Cari Vio di Laboratorium"],
            "next"     : ["cari_vio"],
            "jam_kurang": 1,
        },


        "cari_vio": {
            "bab"  : "HARI KE-1: 14:00 SORE — LABORATORIUM",
            "text" : (
                "Kalian kembali ke Laboratorium, kali ini lebih dalam.\n"
                "Di balik rak reagen, ada sosok mungil bersembunyi.\n\n"
                "VIO (11 tahun) memeluk kalkulator sambil gemetar.\n"
                "Matanya besar dan waspada.\n\n"
                "Di tangannya yang satunya, ada BUKU CATATAN penuh\n"
                "rumus dan angka yang ditulis sangat kecil."
            ),
            "vio"    : "Vio: 'Sstttt! Sensor gerak aktif tiap 20 menit! Jangan berisik!'",
            "haikaru": "Haikaru: 'Vio, kita butuh kamu matikan panel bawah kapel.'",
            "choices": [
                "1. Tunggu sensor mati lalu ajak Vio bicara",
                "2. Langsung ajak Vio ikut sekarang",
                "3. Minta Vio jelaskan cara kerja sistem keamanan"
            ],
            "next"    : ["vio_sabar", "vio_paksa", "vio_jenius"],
            "jam_kurang": 0,
        },

        "vio_jenius": {
            "bab"  : "HARI KE-1: 14:30 SORE — KULIAH SINGKAT VIO",
            "text" : (
                "Vio menatapmu sebentar, lalu seperti ada saklar\n"
                "yang dinyalakan — dia mulai bicara cepat sekali.\n\n"
                "'Sistem magnet punya tiga lapis. Lapis pertama:\n"
                " sensor gerak di koridor. Lapis kedua: medan elektrik\n"
                " di pintu keluar. Lapis ketiga: sistem terpusat\n"
                " di panel bawah kapel.'\n\n"
                "Dia mencoret-coret di buku catatannya.\n"
                "'Kalau panel utama mati, lapis satu dan dua mati otomatis.\n"
                " Butuh waktu 4 menit 37 detik untuk reboot.\n"
                " Itu jendela waktu kita.'"
            ),
            "vio"    : "Vio: 'Aku ikut. Tapi HARUS tepat 4 menit 37 detik. Tidak boleh lebih.'",
            "choices": ["1. Bergabung dengan Vio — ke Perpustakaan"],
            "next"   : ["perpustakaan"],
            "item"   : "Kalkulator Vio",
            "jam_kurang": 1,
        },

        "vio_sabar": {
            "bab"  : "HARI KE-1: 14:30 SORE — MENUNGGU SENSOR",
            "text" : (
                "Kalian diam menunggu. 22 menit berlalu.\n"
                "Vio mengangkat tangannya: 'Sekarang. Lima menit.'\n\n"
                "Dalam waktu itu Vio menjelaskan seluruh sistem\n"
                "keamanan pulau dengan berbisik cepat.\n"
                "Kamu tercengang — dia jenius."
            ),
            "vio"    : "Vio: 'Aku ikut. Tapi kita harus tepat waktu. Aku tidak suka terlambat.'",
            "choices": ["1. Vio bergabung — menuju Perpustakaan"],
            "next"   : ["perpustakaan"],
            "item"   : "Kalkulator Vio",
            "jam_kurang": 1,
        },

        "vio_paksa": {
            "bab"  : "HARI KE-1: 14:20 SORE — SENSOR AKTIF",
            "text" : (
                "Terlalu terburu-buru — sensor aktif!\n"
                "Lampu merah berkedip! Kalian berlari!\n\n"
                "Vio memang ikut, tapi pintu laboratorium\n"
                "sempat terkunci dan memakan waktu lama untuk dibuka."
            ),
            "vio"    : "Vio: 'Aku bilang tunggu! Kenapa tidak dengarkan aku?!'",
            "haikaru": "Haikaru: 'Tidak apa-apa. Tetap jalan.'",
            "choices": ["1. Lanjutkan ke Perpustakaan"],
            "next"   : ["perpustakaan"],
            "item"   : "Kalkulator Vio",
            "jam_kurang": 3,
        },


        "perpustakaan": {
            "bab"  : "HARI KE-1: 17:00 SORE — PERPUSTAKAAN TUA",
            "text" : (
                "Kalian berlima sampai di Perpustakaan Tua.\n"
                "Debu tebal melapisi setiap rak buku.\n"
                "Cahaya sore menyelinap lewat jendela retak.\n\n"
                "Haikaru langsung menuju rak paling belakang.\n"
                "Dia menarik sebuah buku merah tebal — dan sebuah\n"
                "PETA DERMAGA jatuh dari dalamnya.\n\n"
                "Di sudut perpustakaan, ada pintu kecil\n"
                "yang setengah tersembunyi oleh rak buku."
            ),
            "epstein" : "Epstein [intercom]: 'Kalian dekat sekali... ini mulai menarik.'",
            "haikaru" : "Haikaru: 'Peta dermaga. Tapi apa itu pintu di sana?'",
            "choices" : [
                "1. Ambil peta dan langsung ke terowongan",
                "2. Cari informasi tambahan di perpustakaan",
                "3. Buka pintu tersembunyi itu"
            ],
            "next"    : ["terowongan", "cari_info_perpus", "pintu_tersembunyi"],
            "item"    : "Peta Dermaga",
            "jam_kurang": 1,
        },

        "pintu_tersembunyi": {
            "bab"  : "HARI KE-1: 17:30 SORE — KAMAR RAHASIA",
            "text" : (
                "Kalian mendorong rak buku — bergeser berat.\n"
                "Di balik pintu ada kamar sempit, penuh debu.\n\n"
                "Tapi di dalamnya:\n"
                "Sebuah RADIO DARURAT yang masih berfungsi.\n"
                "Dan di dindingnya, foto-foto pulau dari udara.\n\n"
                "Vio langsung menghidupkan radio.\n"
                "Ada sinyal! Samar, tapi ada!\n\n"
                "Vio mengirim pesan koordinat pulau ke frekuensi darurat.\n"
                "'Kalau ada yang dengar ini... bantuan mungkin datang.'"
            ),
            "vio"    : "Vio: 'Sinyal terkirim. Tidak ada jaminan — tapi lebih baik dari tidak.'",
            "haikaru": "Haikaru: 'Bagus. Sekarang kita tidak hanya kabur — kita minta bantuan.'",
            "choices": ["1. Lanjutkan ke terowongan dengan harapan baru"],
            "next"   : ["terowongan"],
            "item"   : "Sinyal Terkirim",
            "jam_kurang": 2,
        },

        "cari_info_perpus": {
            "bab"  : "HARI KE-1: 18:00 MALAM — TEMUAN PERPUSTAKAAN",
            "text" : (
                "Kamu menyisir rak-rak perpustakaan.\n"
                "Di balik kamus usang, ada folder berisi foto-foto\n"
                "dan dokumen tentang pulau ini.\n\n"
                "Termasuk gambar DENAH LENGKAP sistem keamanan dermaga!\n"
                "Vio langsung mempelajarinya dengan cepat.\n\n"
                "Di halaman terakhir folder, ada satu lembar surat\n"
                "dengan amplop bertuliskan: 'Untuk siapa saja yang membaca ini.'"
            ),
            "vio"    : "Vio: 'Dengan denah ini — aku bisa matikan sistem dalam 2 menit tepat!'",
            "choices": [
                "1. Ke terowongan bawah tanah",
                "2. Baca surat misterius itu dulu"
            ],
            "next"   : ["terowongan", "baca_surat_misterius"],
            "jam_kurang": 2,
        },

        "baca_surat_misterius": {
            "bab"  : "HARI KE-1: 18:30 MALAM — SURAT DARI MASA LALU",
            "text" : (
                "Kamu membuka amplop itu dengan tangan gemetar.\n\n"
                "Isinya surat tulis tangan:\n\n"
                "'Aku adalah mantan kepala keamanan pulau ini.\n"
                " Aku tidak sanggup lagi melihat semua ini.\n"
                " Di bawah dermaga ada sebuah kapal kecil\n"
                " yang sengaja aku sembunyikan.\n"
                " Nomor kuncinya: 4-8-1-5.\n"
                " Pergi. Selamatkan dirimu.\n"
                "                        — R'\n\n"
                "R. Sama dengan inisial di Foto Misterius!"
            ),
            "haikaru": "Haikaru: 'Jadi ada orang dalam yang membantu kita. R sudah merencanakan ini.'",
            "choices": ["1. Simpan surat ini dan ke terowongan"],
            "next"   : ["terowongan"],
            "item"   : "Surat dari R",
            "jam_kurang": 1,
        },


        "terowongan": {
            "bab"  : "HARI KE-1: 20:00 MALAM — TEROWONGAN BAWAH TANAH",
            "text" : (
                "Arganta memimpin kalian ke bawah kapel.\n"
                "Ada panel elektronik tua di dinding.\n\n"
                "Vio membuka kalkulator dan mulai bekerja.\n"
                "Jari-jarinya bergerak cepat seperti pianis.\n\n"
                "Dua menit kemudian, pintu besi berat bergeser.\n"
                "Di baliknya: sebuah terowongan gelap panjang.\n\n"
                "Bau tanah lembab. Dingin. Tapi ini jalan keluar."
            ),
            "arganta" : "Arganta: 'Tuhan membuka jalan. Ayo.'",
            "aolinh"  : "Aolinh: 'Aku takut gelap...' (menggandeng tanganmu erat)",
            "choices" : [
                "1. Masuki terowongan — pegang tangan Aolinh",
                "2. Biarkan Haikaru masuk duluan sebagai penjaga",
                "3. Minta Vio nyalakan senter lebih terang"
            ],
            "next"    : ["dalam_terowongan", "dalam_terowongan", "terowongan_terang"],
            "jam_kurang": 1,
        },

        "terowongan_terang": {
            "bab"  : "HARI KE-1: 20:10 MALAM — SENTER MAKSIMAL",
            "text" : (
                "Vio memutar tombol senternya ke maksimal.\n"
                "Terowongan tiba-tiba terlihat jelas.\n\n"
                "Dan di dinding samping, kalian melihat sesuatu\n"
                "yang tidak terlihat sebelumnya:\n"
                "Sebuah jalur cabang yang sempit mengarah ke kiri.\n\n"
                "Di dindingnya ada tanda panah dan tulisan:\n"
                "'LIFT DARURAT →'"
            ),
            "ignatius": "Ignatius: 'Lift darurat?! Kalau punya Kartu Akses — kita bisa pakai itu!'",
            "choices" : [
                "1. Gunakan Lift Darurat (butuh Kartu Akses)",
                "2. Tetap lewat jalur utama terowongan"
            ],
            "next"    : ["lift_darurat", "dalam_terowongan"],
            "jam_kurang": 0,
        },

        "lift_darurat": {
            "bab"  : "HARI KE-1: 20:20 MALAM — LIFT DARURAT",
            "text" : (
                "Ignatius menggesek Kartu Akses Merah ke panel.\n"
                "KLIK. Lampu hijau menyala!\n\n"
                "Pintu lift terbuka. Dalamnya sempit, muat untuk lima orang\n"
                "berdiri rapat.\n\n"
                "Vio menekan tombol paling bawah. Lift bergerak turun.\n"
                "Lalu berhenti. Pintu terbuka.\n\n"
                "Kalian langsung berada di area belakang dermaga\n"
                "— melewati semua terowongan panjang dan penjaga patroli!\n\n"
                "Vio menghitung: 'Kita hemat empat jam.'"
            ),
            "ignatius": "Ignatius: 'YESSS! Level shortcut unlocked!'",
            "arganta" : "Arganta: 'Tuhan memang selalu siapkan jalan.'",
            "choices" : ["1. Keluar lift — menuju dermaga!"],
            "next"    : ["ujung_terowongan"],
            "jam_kurang": 0,
        },

        "dalam_terowongan": {
            "bab"  : "HARI KE-2: 02:00 PAGI — DALAM TEROWONGAN",
            "text" : (
                "Kalian berjalan dalam gelap total selama beberapa jam.\n"
                "Hanya senter kecil milik Vio yang menerangi jalan.\n\n"
                "Tiba-tiba Ignatius berhenti dan mengangkat tangan.\n\n"
                "Suara berderak. Lalu langkah kaki berat.\n"
                "PENJAGA — sedang patroli di ujung terowongan.\n"
                "Senter mereka bergerak ke sini."
            ),
            "ignatius": "Ignatius: 'Aku bisa alihkan perhatiannya. Percayakan pada aku.'",
            "haikaru" : "Haikaru: 'Jangan gegabah, Ignatius...'",
            "choices" : [
                "1. Biarkan Ignatius mengalihkan penjaga",
                "2. Cari jalan lain memutar",
                "3. Semua diam total dan tunggu penjaga lewat"
            ],
            "next"    : ["ignatius_aksi", "jalan_memutar", "tunggu_penjaga"],
            "jam_kurang": 0,
        },

        "tunggu_penjaga": {
            "bab"  : "HARI KE-2: 02:15 PAGI — BERSEMBUNYI",
            "text" : (
                "Kalian menekan diri ke dinding. Berhenti nafas.\n"
                "Total kegelapan. Total keheningan.\n\n"
                "Langkah penjaga semakin dekat.\n"
                "Kamu bisa mencium bau rokok murahan mereka.\n\n"
                "...Satu meter.\n"
                "...Setengah meter.\n\n"
                "Penjaga berhenti tepat di depan kalian.\n"
                "Radio mereka berbunyi.\n"
                "'Sektor 7 clear. Balik ke pos.'\n\n"
                "Mereka berbalik. Pergi."
            ),
            "aolinh" : "Aolinh: (tangannya masih gemetar tapi tidak bersuara)",
            "choices": ["1. Hembuskan napas — lanjutkan ke ujung terowongan"],
            "next"   : ["ujung_terowongan"],
            "jam_kurang": 1,
        },

        "ignatius_aksi": {
            "bab"  : "HARI KE-2: 02:30 PAGI — PENGALIHAN",
            "text" : (
                "Ignatius melempar batu kecil ke arah berlawanan.\n"
                "KLIK. Penjaga menoleh dan berjalan ke sana.\n\n"
                "Kalian menerobos lewat dalam keheningan total.\n"
                "Nafas tertahan. Jantung berdegup kencang.\n\n"
                "Berhasil! Ignatius nyengir puas."
            ),
            "ignatius": "Ignatius: 'Gampang. Level stealth 100.' (nyengir lebar)",
            "choices" : ["1. Lanjutkan ke ujung terowongan"],
            "next"    : ["ujung_terowongan"],
            "jam_kurang": 1,
        },

        "jalan_memutar": {
            "bab"  : "HARI KE-2: 03:30 PAGI — JALAN MEMUTAR",
            "text" : (
                "Kalian memilih jalan memutar melalui pipa drainase.\n"
                "Sempit, berbau, dan memakan waktu hampir satu jam.\n\n"
                "Tapi kalian aman. Tidak ada yang menyadari.\n\n"
                "Aolinh keluar dari pipa dengan ekspresi datar:\n"
                "'Aku tidak akan ceritakan ini ke siapapun seumur hidup.'"
            ),
            "aolinh" : "Aolinh: 'Kak... kamu berhutang satu es krim padaku.'",
            "choices": ["1. Keluar ke ujung terowongan"],
            "next"   : ["ujung_terowongan"],
            "jam_kurang": 2,
        },


        "ujung_terowongan": {
            "bab"  : "HARI KE-2: 04:00 PAGI — UJUNG TEROWONGAN",
            "text" : (
                "Udara segar menghantam wajah kalian.\n"
                "Kalian keluar di balik semak-semak tebal.\n\n"
                "Di kejauhan, kilatan air laut.\n"
                "DERMAGA — tinggal seratus meter.\n\n"
                "Lampu sorot berputar. Penjaga berjaga.\n"
                "Dan di ujung dermaga, siluet satu orang\n"
                "berdiri tegak. Menunggu.\n\n"
                "Di bawah dermaga... apakah ada kapal yang tersembunyi?"
            ),
            "haikaru" : "Haikaru: 'Dia sudah tahu kita akan datang. Tidak apa-apa.'",
            "choices" : [
                "1. Maju langsung ke dermaga",
                "2. Periksa bawah dermaga dulu (jika punya Surat dari R)"
            ],
            "next"    : ["dermaga_epstein", "kapal_tersembunyi"],
            "jam_kurang": 1,
        },

        "kapal_tersembunyi": {
            "bab"  : "HARI KE-2: 04:15 PAGI — BAWAH DERMAGA",
            "text" : (
                "Kalian mengendap ke bawah dermaga.\n"
                "Air laut dingin menyentuh kaki kalian.\n\n"
                "Dan di sana — tersembunyi di balik tiang dermaga,\n"
                "ditutup terpal hijau tua:\n"
                "SEBUAH KAPAL KECIL dengan tangki bensin penuh.\n\n"
                "Ignatius menemukan panel kunci.\n"
                "Kode: 4-8-1-5.\n\n"
                "Kalau kode itu benar, kalian bisa start kapal\n"
                "dan langsung kabur — tanpa harus hadapi Epstein!"
            ),
            "ignatius": "Ignatius: 'Kode-nya... siapa yang tahu angkanya?'",
            "choices" : [
                "1. Masukkan kode 4-8-1-5 (dari Surat R)",
                "2. Tidak tahu kode — terpaksa hadapi Epstein"
            ],
            "next"    : ["ending_sempurna", "dermaga_epstein"],
            "jam_kurang": 0,
        },

        "dermaga_epstein": {
            "bab"  : "HARI KE-2: 05:00 PAGI — DERMAGA",
            "text" : (
                "Fajar mulai mewarnai langit dengan merah dan oranye.\n"
                "Kalian berdiri di dermaga kayu yang berderit.\n\n"
                "EPSTEIN berdiri di ujung dermaga, tangan bersedekap.\n"
                "Jas putihnya berkibar diterpa angin laut.\n"
                "Dia tersenyum — senyum yang tidak menyenangkan.\n\n"
                "Di belakangnya, sebuah kapal mewah sudah siap berlayar."
            ),
            "epstein" : "Epstein: 'Selamat datang di akhir perjalanan kalian, anak-anak.'",
            "haikaru" : "Haikaru: 'Ini berakhir hari ini, Epstein.'",
            "choices" : [
                "1. Serang bersama sekarang!",
                "2. Negosiasi untuk mengulur waktu",
                "3. Tunjukkan Chip Bukti Rekaman (jika punya)"
            ],
            "next"    : ["serangan_final", "negosiasi_epstein", "chip_bukti"],
            "jam_kurang": 0,
        },

        "chip_bukti": {
            "bab"  : "HARI KE-2: 05:05 PAGI — SENJATA RAHASIA",
            "text" : (
                "Ignatius melangkah maju dan mengangkat chip kecil itu.\n\n"
                "'Ini semua suaramu, Epstein. Semua percakapanmu\n"
                " dengan para penjaga. Tanggal, waktu, nama.'\n\n"
                "Wajah Epstein berubah seketika.\n"
                "Bukan marah. Tapi — takut.\n\n"
                "Untuk pertama kalinya, Epstein mundur setengah langkah."
            ),
            "epstein" : "Epstein: '...Darimana kalian mendapat—'",
            "ignatius": "Ignatius: 'Dari dalam game console-mu sendiri. Kamu tidak periksa.'",
            "choices" : ["1. Manfaatkan kelengahannya — SERANG!"],
            "next"    : ["serangan_final"],
            "jam_kurang": 0,
        },

        "negosiasi_epstein": {
            "bab"  : "HARI KE-2: 05:10 PAGI — NEGOSIASI",
            "text" : (
                "Kamu melangkah maju dengan tenang.\n"
                "'Kamu tidak akan menang. Koordinat pulau ini\n"
                " sudah dikirim ke frekuensi darurat internasional.\n"
                " Bantuan dalam perjalanan.'\n\n"
                "Epstein mengernyit. Sedetik — ragu.\n\n"
                "Itu cukup. Vio berlari ke panel listrik dermaga!"
            ),
            "vio"    : "Vio: 'Dapat! Semua sistem — MATI!'",
            "choices": ["1. Sekarang! SERANG!"],
            "next"   : ["serangan_final"],
            "jam_kurang": 1,
        },

        "serangan_final": {
            "bab"  : "HARI KE-2: 05:30 PAGI — PERTEMPURAN TERAKHIR",
            "text" : (
                "Kalian berlima menyerang bersama!\n\n"
                "IGNATIUS melempar batu ke generator!\n"
                "VIO menghantam panel listrik — semua sensor mati!\n"
                "ARGANTA memblokir jalan mundur Epstein!\n"
                "AOLINH menendang kaki Epstein dengan sekuat tenaga!\n\n"
                "Epstein sempoyongan ke tepi dermaga.\n\n"
                "HAIKARU membuka Buku Merah di hadapannya.\n"
                "'Ini semua buktinya. Nama-nama. Foto. Rekaman.\n"
                " Semua sudah dikirim ke seluruh dunia setengah jam lalu.'\n\n"
                "Epstein menatap buku itu. Lalu menatap kalian.\n"
                "Lalu — untuk pertama kalinya — dia tidak bisa berkata apa-apa."
            ),
            "epstein": "Epstein: 'Tidak... tidak mungkin... kalian anak-anak kecil...'",
            "choices": [
                "1. Lompat ke kapal — KABUR sekarang!",
                "2. Tunggu sebentar — pastikan Epstein tidak bisa lari"
            ],
            "next"   : ["ending", "ending_heroik"],
            "jam_kurang": 2,
        },


        "ending": {
            "bab"  : "ENDING A — KEBEBASAN",
            "text" : (
                "Mesin kapal menderum. Ombak pecah di haluan.\n"
                "Pulau itu mengecil di kejauhan.\n\n"
                "Epstein ditangkap oleh pihak berwenang yang sudah\n"
                "menunggu berdasarkan data dari Buku Merah.\n\n"
                "Kalian duduk bersama di dek kapal.\n"
                "Angin pagi terasa hangat dan bebas.\n"
                "Aolinh tidur bersandar di bahumu.\n"
                "Haikaru menutup Buku Merah untuk terakhir kalinya.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "   ENDING A: K A L I A N   B E B A S\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "haikaru": "Haikaru: 'Kita bebas. Sungguh bebas.'",
            "aolinh" : "Aolinh: 'Kak... terima kasih sudah tidak meninggalkan aku.'",
            "choices": ["1. Tamat — Kembali ke Menu Utama"],
            "next"   : [None],
            "jam_kurang": 0,
        },

        "ending_heroik": {
            "bab"  : "ENDING B — PAHLAWAN DERMAGA",
            "text" : (
                "Kalian menahan Epstein di dermaga.\n"
                "Tidak lari — tapi berdiri.\n\n"
                "Dua puluh menit kemudian, suara helikopter.\n"
                "Lalu kapal patroli dari kejauhan.\n"
                "Sinyal yang Vio kirimkan — berhasil!\n\n"
                "Petugas mengikat tangan Epstein.\n"
                "Epstein dibawa pergi sambil terus menoleh ke belakang\n"
                "menatap kalian dengan tidak percaya.\n\n"
                "Kamera wartawan menyorot kalian berenam.\n"
                "Aolinh menutup wajahnya dengan tangan.\n"
                "Ignatius justru melambai.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "  ENDING B: PAHLAWAN — Epstein DITANGKAP di TKP\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "ignatius": "Ignatius: 'Kita yang tangkap dia. High score baru.'",
            "haikaru" : "Haikaru: 'Ini bukan game, Ignatius.' (tapi dia tersenyum)",
            "choices" : ["1. Tamat — Kembali ke Menu Utama"],
            "next"    : [None],
            "jam_kurang": 0,
        },

        "ending_sempurna": {
            "bab"  : "ENDING C — RENCANA SEMPURNA",
            "text" : (
                "Ignatius memasukkan kode 4-8-1-5.\n"
                "KLIK. Panel terbuka. Mesin kapal menyala perlahan.\n\n"
                "Kalian masuk satu per satu ke dalam kapal.\n"
                "Aolinh yang terakhir, sambil melihat ke atas dermaga.\n"
                "Epstein masih berdiri di sana — sendirian, menunggu —\n"
                "tidak tahu bahwa di bawahnya, kapal sudah bergerak pergi.\n\n"
                "Tidak ada pertempuran. Tidak ada keributan.\n"
                "Kalian cukup... pergi.\n\n"
                "Satu jam kemudian, kapal patroli tiba — berdasarkan\n"
                "sinyal dari Vio — dan Epstein ditangkap tanpa perlawanan.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "  ENDING C ★ SEMPURNA — Keluar Tanpa Konfrontasi\n"
                "           Semua Selamat. Epstein Ditangkap.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "arganta" : "Arganta: 'Ini yang disebut kemenangan sejati. Tanpa pertumpahan.'",
            "aolinh"  : "Aolinh: 'Kita benar-benar bebas... dengan cara yang benar.'",
            "choices" : ["1. Tamat — Kembali ke Menu Utama"],
            "next"    : [None],
            "jam_kurang": 0,
        },
    }
    return story



def jalankan_scene(scene_id, nama_player, inventory, jam_tersisa, story):
    """
    Menampilkan satu scene dan memproses pilihan pemain.
    Mengembalikan (scene_berikutnya, inventory_baru, jam_baru).
    """
    if scene_id not in story:
        print(f"\n[ERROR] Scene '{scene_id}' tidak ditemukan. Reset ke awal.")
        return "awal", inventory, jam_tersisa

    data = story[scene_id]

    clear_screen()
    print_header(data["bab"], jam_tersisa, inventory)

    teks = data["text"].replace("[Nama]", nama_player)
    slow_print(teks)
    print()

    karakter_list = [
        ("aolinh",   "AOLINH"),
        ("haikaru",  "HAIKARU"),
        ("ignatius", "IGNATIUS"),
        ("arganta",  "ARGANTA"),
        ("vio",      "VIO"),
        ("epstein",  "EPSTEIN"),
    ]
    for key, label in karakter_list:
        if key in data and data[key]:
            dialog = data[key].replace("[Nama]", nama_player)
            print(f"\n  [{label}]")
            slow_print(f"  {dialog}", delay=0.012)

    if "item" in data and data["item"] not in inventory:
        item_baru = data["item"]
        inventory.append(item_baru)
        print(f"\n  ✨ Item didapat: [ {item_baru} ]")

    print("\n" + "-" * 60)

    choices = data["choices"]
    print("  Apa yang kamu lakukan?\n")
    for pilihan in choices:
        print(f"    {pilihan}")
    print(f"    i. Lihat Inventory")
    print(f"    s. Simpan & Keluar ke Menu")
    print()

    while True:
        try:
            masukan = input("  Pilihan: ").strip().lower()

            if masukan == "i":
                tampilkan_inventory(inventory)
                return scene_id, inventory, jam_tersisa  # Ulang scene yang sama

            elif masukan == "s":
                write_data(nama_player, scene_id, inventory, jam_tersisa)
                print("\n  [Progres tersimpan. Sampai jumpa!]")
                time.sleep(1.5)
                return "__menu__", inventory, jam_tersisa

            else:
                idx = int(masukan) - 1
                if 0 <= idx < len(choices):
                    jam_baru    = max(0, jam_tersisa - data.get("jam_kurang", 0))
                    scene_berikut = data["next"][idx]
                    return scene_berikut, inventory, jam_baru
                else:
                    print("  Pilihan tidak valid. Coba lagi.")

        except ValueError:
            print("  Masukkan angka atau huruf yang sesuai!")
        except Exception as e:
            print(f"  [ERROR] {e}")



def cek_game_over(jam_tersisa, nama_player, story):
    """Mengembalikan True jika waktu habis (game over)."""
    if jam_tersisa <= 0:
        clear_screen()
        print("=" * 60)
        print("  W A K T U   H A B I S")
        print("=" * 60)
        slow_print(f"\n  48 jam sudah berlalu, {nama_player}.")
        slow_print("  Epstein menang kali ini.")
        slow_print("  Kalian tidak berhasil keluar tepat waktu.")
        slow_print("\n  'Sangat mengecewakan,' suara Epstein terdengar.")
        slow_print("  'Aku harap kalian bisa lebih baik lagi... next time.'\n")
        print("=" * 60)
        input("\n  Tekan [Enter] untuk kembali ke menu...")
        return True
    return False



def main():
    story = get_story()

    while True:
        tampilkan_judul()
        pilihan_menu = menu_utama()

        if pilihan_menu == "keluar":
            clear_screen()
            print("\n  Sampai jumpa. Jangan lupa — kebebasan itu diperjuangkan.\n")
            break

        elif pilihan_menu == "tentang":
            layar_tentang()
            continue

        elif pilihan_menu == "baru":
            delete_save()
            intro_epstein()
            nama_player = intro_player()
            scene       = "awal"
            inventory   = []
            jam_tersisa = 48
            write_data(nama_player, scene, inventory, jam_tersisa)

        elif pilihan_menu == "lanjut":
            nama_load, scene_load, inv_load, jam_load = load_progress()
            if nama_load:
                nama_player = nama_load
                scene       = scene_load
                inventory   = inv_load
                jam_tersisa = jam_load
                clear_screen()
                slow_print(f"\n  Selamat datang kembali, {nama_player}.")
                slow_print(f"  Waktu tersisa: {jam_tersisa} jam.")
                time.sleep(1.5)
            else:
                print("\n  Tidak ada save ditemukan. Memulai game baru...")
                time.sleep(1.5)
                intro_epstein()
                nama_player = intro_player()
                scene       = "awal"
                inventory   = []
                jam_tersisa = 48
                write_data(nama_player, scene, inventory, jam_tersisa)

        while True:
            if scene == "__menu__":
                break

            if cek_game_over(jam_tersisa, nama_player, story):
                delete_save()
                break

            if scene is None:
                clear_screen()
                slow_print("\n  ✨ Terima kasih telah bermain! ✨")
                slow_print("  Kamu telah menyelesaikan Escape from Epstein Island.")
                delete_save()
                input("\n  Tekan [Enter] untuk kembali ke menu utama...")
                break

            scene, inventory, jam_tersisa = jalankan_scene(
                scene, nama_player, inventory, jam_tersisa, story
            )

            if scene not in (None, "__menu__"):
                write_data(nama_player, scene, inventory, jam_tersisa)


if __name__ == "__main__":
    main()
