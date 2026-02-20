"""
NPC INTERACTIONS
 NPC dialogs and sidequest system - give key items to progress chapters

Mengelola dialog intro, sidequest briefing, dan completion dialog untuk setiap NPC.
NPC tidak join party — mereka kasih key item yang dibutuhkan untuk lanjut chapter.
"""

from sprites import Warna
import time
from contextlib import suppress
from utils import clear_screen, wait_input, separator, flush_input


#  NPC sidequest data - available_chapter, reward_item, chapter_unlock tracking
# ─────────────────────────────────────────────────────────────────────────────
#  DATA SIDEQUEST NPC
#  Setiap NPC punya:
#    available_chapter   : minimum chapter agar bisa ditemui
#    location            : lokasi di mana NPC bisa ditemui
#    reward_item         : item kunci yang diberikan setelah sidequest selesai
#    reward_flag         : story flag yang di-set setelah reward diberikan
#    required_item / required_action : syarat penyelesaian sidequest
#    main_quest_impact   : kalimat singkat dampak ke main quest
#    chapter_unlock      : sidequest ini membuka akses ke chapter ini
# ─────────────────────────────────────────────────────────────────────────────
NPC_SIDEQUEST_DATA = {
    'haikaru': {
        'name':             'Haikaru Fumika',
        'title':            'Analis Strategis',
        'available_chapter': 2,
        'location':          'prison_north',
        'sidequest_id':      'sq_haikaru',
        'sidequest_title':   'Catatan yang Tersita',
        'required_item':     'Buku Catatan Haikaru',
        'required_action':   None,
        'reward_item':       'Catatan Sandi Haikaru',
        'reward_flag':       'haikaru_sidequest_done',
        'main_quest_impact': 'Diperlukan untuk decode dokumen rahasia mansion (Ch3→Ch4)',
        'chapter_unlock':    4,

        # ── Dialog pertama kali ketemu ──────────────────────────────────────
        'intro_dialog': [
            ("Haikaru", "..."),
            ("Haikaru", "Kamu... bukan penjaga."),
            ("Haikaru", "47 detik untuk sampai ke sini dari koridor barat. Kamu tidak berlari. Menarik."),
            (None,      "Gadis itu berdiri tegak meskipun dalam seragam penjara. Matanya menganalisa setiap gerakan kamu."),
            ("Haikaru", "Haikaru Fumika. 12 tahun. IQ 178. Dijebloskan ke sini karena 'terlalu tahu'."),
            ("Haikaru", "Tapi mereka melakukan kesalahan. Mereka pikir mengambil kebebasanku akan menghentikanku berpikir."),
            ("Haikaru", "Salah. Setiap detik di sini — aku hitung. Setiap pola penjaga — aku hafal."),
            ("Haikaru", "Kamu butuh bantuanku. Dan aku butuh sesuatu dari kamu."),
        ],

        # ── Dialog saat assign sidequest ────────────────────────────────────
        'quest_dialog': [
            ("Haikaru", "Penjaga Selatan menyita buku catatanku. 312 halaman analisis enkripsi."),
            ("Haikaru", "Di dalamnya ada pola akses sistem keamanan mansion. Pola yang... tidak seharusnya ada."),
            ("Haikaru", "Temukan buku itu. Ruang penjaga di locker nomor 7. Kombinasi: tanggal lahir kepala penjaga."),
            ("Haikaru", "Aku sudah hitung — dia lahir 3 Maret 1972. Jadi: 03-03-72."),
            (None,      "Haikaru menyerahkan sketsa kasar denah ruang penjaga."),
            ("Haikaru", "Kembalikan bukuku dan aku akan terjemahkan semua dokumen mansion yang tidak bisa kalian baca."),
            ("Haikaru", "Dokumen itu... aku yakin isinya adalah daftar 'tamu'. Nama-nama besar. Bukti nyata."),
        ],

        # ── Dialog saat quest selesai ────────────────────────────────────────
        'complete_dialog': [
            ("Haikaru", "Kamu berhasil. 94% lebih cepat dari estimasiku. Kecepatanmu mengejutkan."),
            (None,      "Haikaru segera membuka buku catatan, tangannya bergerak cepat membalik halaman."),
            ("Haikaru", "...Ada. Persis di halaman 247. Cipher Vigenère, kunci 'LITTLE_SAINT_JAMES'."),
            ("Haikaru", "Ini bukan sekadar catatan keuangan. Ini jadwal 'kunjungan'. Nama-nama."),
            ("Haikaru", "Aku salin bagian terpenting. Ambil ini."),
            (None,      "Kamu menerima [Catatan Sandi Haikaru] — kunci untuk decode dokumen mansion."),
            ("Haikaru", "Jangan sampai jatuh ke tangan penjaga. Kalau itu terjadi, semua orang di pulau ini dalam bahaya."),
        ],

        # ── Dialog setelah quest selesai — muncul SEKALI saat kembali mengobrol ──
        'after_complete_dialog': [
            ("Haikaru", "...Aku masih menganalisa fragmentasi data di catatan itu. Ada anomali di halaman 89."),
            ("Haikaru", "Pola enkripsi berubah tiap tiga bulan. Artinya ada orang dalam yang update sistemnya."),
            (None,      "Haikaru menyerahkan selembar kecil kertas tambahan."),
            ("Haikaru", "Tambahan. Koordinat yang selalu dipakai untuk 'drop point'. Mungkin berguna nanti."),
            ("Haikaru", "Kalau kamu bertemu jalan buntu — lihat polanya. Setiap sistem punya celah. Cari saja."),
        ],
    },

    'aolinh': {
        'name':             'Ao Lin',
        'title':            'Violinis & Harapan',
        'available_chapter': 2,
        'location':          'theater',
        'sidequest_id':      'sq_aolinh',
        'sidequest_title':   'Melodi di Tengah Kegelapan',
        'required_item':     None,
        'required_action':   'defeat_theater_guard',
        'reward_item':       'Rekaman Distraksi Aolinh',
        'reward_flag':       'aolinh_sidequest_done',
        'main_quest_impact': 'Rekaman musik mengalihkan penjaga dock (Ch4 — akses kapal)',
        'chapter_unlock':    4,

        # ── Dialog pertama kali ketemu ──────────────────────────────────────
        'intro_dialog': [
            (None,      "Suara biola mengalun pelan dari balik tirai panggung. Melodi yang... terlalu indah untuk tempat seperti ini."),
            ("Aolinh",  "...Siapa di sana?"),
            (None,      "Seorang gadis muncul dari balik tirai. Biola di tangan, earphone biru menggantung di leher."),
            ("Aolinh",  "O — kamu bukan penjaga. Syukurlah. Jantungku hampir copot."),
            ("Aolinh",  "Namaku Ao Lin. Panggil Aolinh. Dari Hongkong. Dipisah dari Jiejie-ku di sini."),
            (None,      "Matanya berkaca-kaca sesaat, tapi dia tersenyum — senyum yang dipaksakan tapi tulus."),
            ("Aolinh",  "音乐给我力量 — Musik memberi kekuatan. Selama aku bisa main biola, aku tidak akan menyerah."),
            ("Aolinh",  "Kamu mau cari cara keluar? Aku mau bantu. Tapi aku butuh sesuatu darimu dulu."),
        ],

        # ── Dialog saat assign sidequest ────────────────────────────────────
        'quest_dialog': [
            ("Aolinh",  "Di ruang backstage ada guard yang selalu berjaga. Dia yang mengambil HP-ku — satu-satunya koneksi ke Jiejie."),
            ("Aolinh",  "Kalahkan dia. Ambil kembali HP-ku."),
            (None,      "Aolinh mengencangkan genggaman pada biolanya."),
            ("Aolinh",  "Setelah itu... aku punya ide. Rekaman music performance-ku masih ada di HP itu."),
            ("Aolinh",  "Penjaga di dermaga selalu ngantuk shift malam. Tapi kalau ada musik... mereka pasti terdistraksi."),
            ("Aolinh",  "Kita bisa manfaatkan itu. Satu rekaman, satu kesempatan untuk kalian lewat."),
            ("Aolinh",  "♪ Tapi pertama — tolong ambil HP-ku itu. Please? ♪"),
        ],

        # ── Dialog saat quest selesai ────────────────────────────────────────
        'complete_dialog': [
            ("Aolinh",  "Kamu berhasil! Oh, Dewa — terimakasih, terimakasih banyak!"),
            (None,      "Aolinh memeluk HP-nya erat-erat, kemudian segera memutar sesuatu."),
            ("Aolinh",  "Ini... rekaman terakhirku sebelum ditangkap. Competition di Hongkong."),
            ("Aolinh",  "Aku buat versi loop-nya. Sambungkan ke speaker dermaga, dan semua penjaga akan terpaku 10 menit."),
            (None,      "Aolinh menyerahkan USB kecil. Di labelnya tertulis: 'DISTRAKSI — JANGAN DIPUTAR SEKARANG'."),
            ("Aolinh",  "Gunakan ini saat kalian butuh jalan lewat dermaga tanpa keributan."),
            ("Aolinh",  "Dan... kalau kalian menemukan Jiejie-ku di suatu tempat — tolong beritahu aku. ♪"),
        ],

        # ── Dialog setelah quest selesai — muncul SEKALI saat kembali mengobrol ──
        'after_complete_dialog': [
            (None,      "Aolinh sedang memainkan melodi pelan di atas panggung. Senyumnya lebih tenang dari sebelumnya."),
            ("Aolinh",  "Oh, kamu lagi. Duduk, kalau mau. ♪"),
            ("Aolinh",  "Aku nulis lagu baru. Tentang pulau ini. Tentang kita semua."),
            ("Aolinh",  "Judulnya... belum ada. Mungkin 'Lari dari Kegelapan'. Mungkin 'Kita Akan Pulang'."),
            (None,      "Dia memainkan beberapa nada lembut — melodi yang entah kenapa terasa seperti harapan."),
            ("Aolinh",  "Apapun yang terjadi nanti — aku percaya kalian bisa. 音乐给我力量. ♪"),
        ],
    },

    'arganta': {
        'name':             'Amerigo Arganta',
        'title':            'Pathfinder & Navigator',
        'available_chapter': 2,
        'location':          'beach',
        'sidequest_id':      'sq_arganta',
        'sidequest_title':   "Rute Nonno",
        'required_item':     'Kompas Nonno Arganta',
        'required_action':   None,
        'reward_item':       'Peta Jalur Rahasia',
        'reward_flag':       'arganta_sidequest_done',
        'main_quest_impact': 'Reveal jalur alternatif ke laboratorium bawah tanah (Ch4/Ch5)',
        'chapter_unlock':    4,

        # ── Dialog pertama kali ketemu ──────────────────────────────────────
        'intro_dialog': [
            (None,      "Seseorang bersembunyi di balik batu karang pantai. Pisau lipat siap di tangan."),
            ("Arganta", "Fermo! Diam dulu — siapa kamu?!"),
            (None,      "Pemuda itu menatap tajam, tapi menurunkan pisaunya perlahan saat mengenali pakaianmu."),
            ("Arganta", "...Seragam penjara. Jadi kamu juga tahanan. Amerigo Arganta. Napoli."),
            ("Arganta", "Keluargaku dibunuh karena Papà mendokumentasikan aktivitas di pulau ini."),
            (None,      "Tangannya menggenggam kompas tua. Jarinya menelusuri ukiran di permukaannya."),
            ("Arganta", "Nonno bilang: 'La via è sempre avanti.' Jalan selalu ada di depan."),
            ("Arganta", "Aku tidak kabur dari sini tanpa bukti. Per famiglia. Kamu mau bantu?"),
        ],

        # ── Dialog saat assign sidequest ────────────────────────────────────
        'quest_dialog': [
            ("Arganta", "Nonno-ku meninggalkan kompas ini untukku. Kompas antik, tapi spesial."),
            ("Arganta", "Di dalamnya ada peta tersembunyi — diukir di bagian dalam tutupnya. Sangat kecil, perlu kaca pembesar."),
            ("Arganta", "Penjaga pantai mengambilnya waktu aku ditangkap. Mereka taruh di pos pantai, loker kecil."),
            (None,      "Arganta menunjuk arah dengan percaya diri."),
            ("Arganta", "Kalau bisa ambil kembali — aku bisa tunjukkan jalur yang tidak ada di peta resmi pulau ini."),
            ("Arganta", "Terowongan lama. Nonno pernah survei pulau ini sebelum Epstein beli. Dia catat semua."),
            ("Arganta", "Itu akses ke laboratorium bawah tanah yang tidak ada di denah resmi. Capisci?"),
        ],

        # ── Dialog saat quest selesai ────────────────────────────────────────
        'complete_dialog': [
            ("Arganta", "Il compasso! Grazie mille — mille grazie!"),
            (None,      "Arganta membuka kompas dengan hati-hati, mengeluarkan lensa kecil dari sakunya."),
            ("Arganta", "Eccola — ini dia. Peta Nonno. Lihat — terowongan ini dimulai di balik batu besar pantai barat."),
            ("Arganta", "Nonno pernah bantu konstruksi awal pulau ini. Dia tahu setiap sudut yang tidak ada di blueprint."),
            (None,      "Arganta menyalin peta ke selembar kertas dengan tangan yang terlatih."),
            ("Arganta", "Ambil ini. Peta Jalur Rahasia. Terowongan ini tembus langsung ke basement laboratorium."),
            ("Arganta", "Kalau kalian butuh masuk ke lab tanpa ketahuan — ini jalannya. Per Nonno."),
        ],

        # ── Dialog setelah quest selesai — muncul SEKALI saat kembali mengobrol ──
        'after_complete_dialog': [
            (None,      "Arganta sedang mengukir sesuatu di tanah pasir dengan ranting. Peta improvisasi."),
            ("Arganta", "Ah, kamu. Duduk — aku baru ingat sesuatu dari catatan Nonno."),
            ("Arganta", "Ada menara pantai di ujung timur. Nonno catat itu sebagai 'punto di osservazione' — titik observasi."),
            ("Arganta", "Dari sana bisa lihat seluruh pulau. Kalau ada sesuatu yang perlu dipantau — itu tempatnya."),
            (None,      "Arganta menggenggam kompasnya sejenak, lalu menatap cakrawala."),
            ("Arganta", "Keluargaku meninggal untuk pulau ini. Aku tidak akan membiarkan pengorbanan mereka sia-sia. Capisci?"),
        ],
    },

    'ignatius': {
        'name':             'Ignatius Forgers',
        'title':            'Insinyur Jenius',
        'available_chapter': 3,
        'location':          'basement',
        'sidequest_id':      'sq_ignatius',
        'sidequest_title':   'Proyek EMP',
        'required_items':    ['Kapasitor Besar', 'Relay Switch', 'Copper Coil'],
        'required_item':     None,
        'required_action':   None,
        'reward_item':       'EMP Device',
        'reward_flag':       'ignatius_sidequest_done',
        'main_quest_impact': 'Menonaktifkan sistem keamanan elektronik (wajib untuk boss Ch4)',
        'chapter_unlock':    4,

        # ── Dialog pertama kali ketemu ──────────────────────────────────────
        'intro_dialog': [
            (None,      "Ruang basement penuh kabel dan komponen elektronik berserakan. Di tengahnya, seorang anak berumur 12 tahun bekerja tanpa henti."),
            ("Ignatius", "Oh! Ada tamu. Tunggu — jangan sentuh apapun. Serius."),
            (None,      "Dia melepas kacamata, mengusap tangan di baju, lalu mengulurkan tangan."),
            ("Ignatius", "Ignatius Forgers. Insinyur berbakat. Juara lomba sains tiga tahun berturut-turut."),
            ("Ignatius", "Mereka menangkapku karena penemuanku. Generator pulsa elektromagnetik mini. Mereka mau menggunakannya sebagai senjata."),
            ("Ignatius", "Aku tolak. Jadi mereka taruh aku di sini. Kesalahan besar dari pihak mereka."),
            (None,      "Dia tersenyum lebar dan menunjuk panel listrik besar di dinding."),
            ("Ignatius", "Mereka menaruhku di sebelah seluruh infrastruktur listrik pulau ini. Waktunya bekerja!"),
        ],

        # ── Dialog saat assign sidequest ────────────────────────────────────
        'quest_dialog': [
            ("Ignatius", "Aku mau membangun perangkat EMP yang bisa melumpuhkan semua sistem keamanan elektronik."),
            ("Ignatius", "Semua kunci magnetis, semua alarm, semua kamera — mati sekaligus. Selama 5 menit."),
            ("Ignatius", "Tapi aku butuh komponen yang tidak ada di basement ini."),
            (None,      "Ignatius menyerahkan daftar yang ditulis dengan cepat namun rapi."),
            ("Ignatius", "Satu: Kapasitor Besar — ada di ruang penyimpanan mansion lantai 2."),
            ("Ignatius", "Dua: Relay Switch — cek ruang generator di ujung selatan basement."),
            ("Ignatius", "Tiga: Copper Coil — ada di peralatan radio lama di backstage teater."),
            ("Ignatius", "Bawa ketiga komponen itu ke sini, dan dalam 20 menit aku selesaikan perangkat EMP-nya."),
            ("Ignatius", "Dengan itu, kalian bisa melumpuhkan boss berikutnya sebelum dia sempat memanggil bantuan. Logis!"),
        ],

        # ── Dialog saat quest selesai ────────────────────────────────────────
        'complete_dialog': [
            ("Ignatius", "Sempurna! Semua komponen lengkap. Mundur dulu — ini butuh konsentrasi penuh."),
            (None,      "Ignatius bekerja dengan kecepatan luar biasa. Tangannya bergerak seperti sudah hafal setiap langkah."),
            ("Ignatius", "Selesai. 18 menit 43 detik. Rekor pribadi."),
            (None,      "Sebuah perangkat kecil berwarna abu-abu dengan tombol merah di tengahnya diletakkan di tanganmu."),
            ("Ignatius", "Tekan tombol merah ini dalam radius 50 meter dari target. Jangkauan efektif: 30 meter."),
            ("Ignatius", "Efek: semua sistem elektronik mati selama 4–6 menit. Termasuk senjata listrik penjaga."),
            ("Ignatius", "Gunakan tepat sebelum konfrontasi dengan Agen Maxwell. Waktu adalah segalanya!"),
        ],

        # ── Dialog setelah quest selesai — muncul SEKALI saat kembali mengobrol ──
        'after_complete_dialog': [
            (None,      "Ignatius sedang membongkar panel listrik lain, tampaknya sedang mengerjakan sesuatu yang baru."),
            ("Ignatius", "Oh! Pas banget. Aku bikin peningkatan kecil untuk EMP itu."),
            (None,      "Dia menyerahkan sepotong kecil komponen tambahan."),
            ("Ignatius", "Perluasan jangkauan. Sekarang efektif 40 meter, bukan 30. Selesai dalam 11 menit."),
            ("Ignatius", "Satu lagi — kalau kamu pakai EMP di dekat air, interferensinya dobel. Berguna untuk situasi tertentu."),
            ("Ignatius", "Tips rekayasa gratis. Tagihannya nanti. Bercanda. ...Mungkin."),
        ],
    },

    'vio': {
        'name':             'Vio',
        'title':            'Peretas & Pakar Enkripsi',
        'available_chapter': 3,
        'location':          'mansion',
        'sidequest_id':      'sq_vio',
        'sidequest_title':   'USB Kebenaran',
        'required_item':     'USB Security Drive',
        'required_action':   None,
        'reward_item':       'USB Evidence Drive',
        'reward_flag':       'vio_sidequest_done',
        'main_quest_impact': 'Bukti inti untuk konfrontasi final Ch6 — WAJIB untuk ending',
        'chapter_unlock':    6,

        # ── Dialog pertama kali ketemu ──────────────────────────────────────
        'intro_dialog': [
            (None,      "Di ruang server mansion, layar komputer masih menyala. Seseorang sedang mengetik cepat."),
            ("Vio",     "Eh, tunggu — kamu bukan penjaga."),
            (None,      "Pemuda berambut merah dengan jaket hoodie berbalik, mata kritisnya menilaimu sekilas."),
            ("Vio",     "Vio. Umur 13. Spesialis enkripsi, dan... terpaksa jadi peretas etis sekarang."),
            ("Vio",     "Aku di sini karena ketidaksengajaan murni. Lagi mengerjakan sesuatu, tiba-tiba diculik."),
            ("Vio",     "Tapi mereka menaruhku di sebelah server farm mereka. Kesalahan terbesar yang pernah mereka buat."),
            (None,      "Dia menunjuk layar yang penuh baris kode dan enkripsi."),
            ("Vio",     "Sistem enkripsi mereka pakai AES-256. Lumayan. Tapi ada celah di implementasinya."),
            ("Vio",     "Beri aku perangkat keras yang tepat dan aku bisa ekstrak semua yang ada di server ini."),
        ],

        # ── Dialog saat assign sidequest ────────────────────────────────────
        'quest_dialog': [
            ("Vio",     "Aku butuh USB Security Drive — tipe spesifik dengan chip enkripsi hardware."),
            ("Vio",     "Kepala penjaga punya satu di sakunya. Dia pikir aman karena ada kata sandi 16 karakter."),
            ("Vio",     "...Aku bisa bajak kata sandi 16 karakter dalam 3 menit. Itu bukan kesombongan. Itu fakta."),
            (None,      "Vio kembali mengetik tanpa melihat keyboard."),
            ("Vio",     "Ambil USB itu dari kepala penjaga. Cara apapun — aku tidak tanya."),
            ("Vio",     "Dengan perangkat itu aku bisa tembus enkripsi server dan unduh: daftar tamu, catatan pembayaran, rekaman."),
            ("Vio",     "Itu bukan sekadar bukti. Itu senjata nuklir informasi. Kalau ini keluar... banyak orang berkuasa yang hancur."),
            ("Vio",     "Dan itulah alasan kita membutuhkannya."),
        ],

        # ── Dialog saat quest selesai ────────────────────────────────────────
        'complete_dialog': [
            ("Vio",     "USB-nya ada. Oke, mulai bekerja."),
            (None,      "Vio mencolokkan USB ke port server, jarinya bergerak cepat menavigasi sistem."),
            ("Vio",     "Menembus lapisan enkripsi pertama... melewati autentikasi... mengunduh..."),
            (None,      "Layar berkedip-kedip. Bilah progres mengisi perlahan."),
            ("Vio",     "Selesai. 47 GB data. Daftar tamu dari tahun 1995 sampai sekarang. Catatan pembayaran. Rekaman pengawasan."),
            ("Vio",     "Dan... ada satu folder khusus. Labelnya 'INSURANCE'. Isinya... lebih dari yang aku bayangkan."),
            (None,      "Vio melepas USB dan memegangnya dengan hati-hati."),
            ("Vio",     "Ini bukan sekadar bukti kejahatan di pulau ini. Ini bukti siapa saja yang terlibat. Secara global."),
            ("Vio",     "Jaga ini seperti nyawa kalian. Karena secara harfiah — inilah yang akan menyelamatkan semua orang."),
            (None,      "Kamu menerima [USB Evidence Drive] — senjata paling berbahaya di pulau ini."),
        ],

        # ── Dialog setelah quest selesai — muncul SEKALI saat kembali mengobrol ──
        'after_complete_dialog': [
            (None,      "Vio sedang membaca data di layar, tapi ekspresinya jauh lebih serius dari biasanya."),
            ("Vio",     "Oh. Kamu. Aku... baru menemukan sesuatu di folder yang aku unduh tadi."),
            ("Vio",     "Ada daftar nama. Ratusan. Bukan cuma politisi atau selebriti. Ada... orang biasa juga."),
            (None,      "Dia terdiam sebentar, menatap layar dengan berat."),
            ("Vio",     "Aku tahu data adalah data. Tapi ini berbeda. Ini nyata. Ini orang-orang nyata."),
            ("Vio",     "...USB itu harus keluar dari pulau ini dengan selamat. Apapun yang terjadi pada kita."),
            ("Vio",     "Semoga kita berhasil."),
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  FUNGSI DISPLAY DIALOG
# ─────────────────────────────────────────────────────────────────────────────

def _print_dialog_line(speaker, line, delay=0.035):
    """Print satu baris dialog dengan format yang sesuai."""
    try:
        if speaker is None:
            # Narasi / action
            print(f"\n  {Warna.ABU_GELAP}[{line}]{Warna.RESET}")
        else:
            # Dialog karakter
            print(f"\n  {Warna.KUNING + Warna.TERANG}{speaker}{Warna.RESET}{Warna.KUNING}: {Warna.RESET}", end="")
            for char in line:
                print(char, end="", flush=True)
                time.sleep(delay)
            print()
        time.sleep(0.3)
    except (IOError, OSError, KeyboardInterrupt):
        if speaker is None:
            print(f"\n  [{line}]")
        else:
            print(f"\n  {speaker}: {line}")


def _display_npc_header(npc_data, header_text="PERTEMUAN"):
    """Tampilkan header NPC interaction."""
    separator('═')
    name  = npc_data.get('name', '???')
    title = npc_data.get('title', '')
    print(f"{Warna.CYAN + Warna.TERANG}{header_text} — {name}{Warna.RESET}".center(80))
    if title:
        print(f"{Warna.ABU_GELAP}{title.center(80)}{Warna.RESET}")
    separator('═')
    print()


def display_npc_intro(npc_id, game_state=None):
    # Menampilkan dialog pertemuan awal dengan NPC (hanya sekali)
    """
    Tampilkan dialog intro NPC — dipanggil saat pertama kali player bertemu NPC.
    Hanya ditampilkan SEKALI seumur hidup (via intro_flag di story_flags).
    """
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return False

    # Cek flag — jika sudah pernah ditampilkan, skip sepenuhnya
    intro_flag = f"{npc_id}_intro_shown"
    if game_state and game_state.story_flags.get(intro_flag):
        return False

    clear_screen()
    _display_npc_header(npc_data, "PERTEMUAN PERTAMA")

    for speaker, line in npc_data.get('intro_dialog', []):
        _print_dialog_line(speaker, line)

    print()
    separator()
    wait_input()

    if game_state:
        game_state.story_flags[intro_flag] = True
        # Auto-trigger sidequest jika chapter sudah cukup
        current_chapter = game_state.story_flags.get('current_chapter', 1)
        try:
            current_chapter = int(current_chapter)
        except (ValueError, TypeError):
            current_chapter = 1
        if current_chapter >= npc_data['available_chapter']:
            game_state.story_flags[f"{npc_id}_quest_available"] = True

    return True


def display_npc_quest_briefing(npc_id, game_state=None):
    # Menampilkan briefing sidequest dari NPC (hanya sekali)
    """
    Tampilkan dialog sidequest NPC — hanya SEKALI saat player pertama menerima quest.
    Setelah ditampilkan, quest_briefing_flag di-set dan tidak akan muncul lagi.
    """
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return False

    # Guard: jangan tampilkan ulang jika sudah pernah
    briefing_flag = f"{npc_id}_briefing_shown"
    if game_state and game_state.story_flags.get(briefing_flag):
        return False

    clear_screen()
    _display_npc_header(npc_data, "SIDEQUEST")
    print(f"  {Warna.KUNING}Quest:{Warna.RESET} {npc_data.get('sidequest_title', '')}")
    print(f"  {Warna.ABU_GELAP}Dampak: {npc_data.get('main_quest_impact', '')}{Warna.RESET}")
    separator()
    print()

    for speaker, line in npc_data.get('quest_dialog', []):
        _print_dialog_line(speaker, line)

    print()
    separator()

    # Tampilkan objective dengan [S] icon
    print(f"\n  {Warna.KUNING + Warna.TERANG}[S] SIDEQUEST OBJECTIVE{Warna.RESET}")
    if npc_data.get('required_items'):
        print(f"  {Warna.KUNING}Kumpulkan item berikut:{Warna.RESET}")
        for item in npc_data['required_items']:
            print(f"    {Warna.CYAN}◆ {item}{Warna.RESET}")
    elif npc_data.get('required_item'):
        print(f"  {Warna.KUNING}Temukan:{Warna.RESET} {Warna.CYAN}◆ {npc_data['required_item']}{Warna.RESET}")
    elif npc_data.get('required_action'):
        action_labels = {
            'defeat_theater_guard': 'Kalahkan Penjaga Theater (Backstage)',
        }
        label = action_labels.get(npc_data['required_action'], npc_data['required_action'])
        print(f"  {Warna.KUNING}Lakukan:{Warna.RESET} {Warna.CYAN}◆ {label}{Warna.RESET}")
    else:
        print(f"  {Warna.ABU_GELAP}(Tidak ada syarat khusus — bicara dengan NPC kembali){Warna.RESET}")

    print(f"\n  {Warna.HIJAU}◈ Reward: {npc_data.get('reward_item', '???')}{Warna.RESET}")
    print()
    separator()
    wait_input()

    if game_state:
        game_state.story_flags[f"{npc_id}_quest_active"] = True
        game_state.story_flags[briefing_flag] = True   # Tandai sudah tampil — tidak akan muncul lagi
    return True


def display_npc_completion(npc_id, game_state=None):
    """
    Tampilkan dialog completion NPC dan berikan reward item.

    PENTING — urutan operasi:
      1. Set story_flags + add_item DULU sebelum dialog mulai
         → Kalau Ctrl+C saat dialog, state sudah tersimpan, tidak ada duplikasi
      2. Baru tampilkan dialog dan reward UI
    """
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return False, None

    reward_flag  = npc_data.get('reward_flag', f"{npc_id}_sidequest_done")
    reward_item  = npc_data.get('reward_item')

    if game_state and game_state.story_flags.get(reward_flag):
        return False, None  # Idempoten — sudah pernah selesai

    # ── STEP 1: Commit state ke game_state SEBELUM dialog ───────────────────
    # Jika pemain Ctrl+C di tengah dialog, item sudah masuk dan flag sudah set.
    # Saat load ulang, guard `reward_flag` di atas akan skip fungsi ini → tidak duplikat.
    if game_state:
        game_state.story_flags[reward_flag]                  = True
        game_state.story_flags[f"{npc_id}_quest_active"]    = False
        game_state.story_flags[f"{npc_id}_quest_done"]      = True
        done_count = game_state.story_flags.get('sidequests_completed', 0)
        game_state.story_flags['sidequests_completed']       = done_count + 1

        # Berikan reward item (idempoten — cek dulu sebelum add)
        if reward_item and reward_item not in game_state.inventory:
            game_state.add_item(reward_item)

        # Consume required items yang dipakai untuk quest ini
        req_items = npc_data.get('required_items', [])
        if not req_items and npc_data.get('required_item'):
            req_items = [npc_data['required_item']]
        for item in req_items:
            game_state.remove_item(item)

    # ── STEP 2: Tampilkan dialog completion (state sudah aman) ──────────────
    clear_screen()
    _display_npc_header(npc_data, "SIDEQUEST SELESAI \u2713")

    for speaker, line in npc_data.get('complete_dialog', []):
        _print_dialog_line(speaker, line)

    print()
    separator()
    print(f"\n  {Warna.HIJAU + Warna.TERANG}[ REWARD DITERIMA ]{Warna.RESET}")
    print(f"  {Warna.KUNING}+{Warna.RESET} {reward_item}")
    print(f"\n  {Warna.ABU_GELAP}Dampak ke main quest:{Warna.RESET}")
    print(f"  {npc_data.get('main_quest_impact', '')}")
    print()
    separator()
    wait_input()

    return True, reward_item


def display_npc_repeat_talk(npc_id, game_state=None):
    """
    Dialog saat player kembali berbicara dengan NPC setelah quest selesai.

    State machine:
      1. after_complete_dialog — ditampilkan SEKALI (lengkap, ada narasi)
      2. brief 'done' line — ditampilkan setiap kunjungan berikutnya (satu baris)
    """
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return

    name = npc_data.get('name', npc_id.capitalize())
    after_flag = f"{npc_id}_after_complete_shown"

    # ── State 1: after_complete_dialog (sekali) ─────────────────────────────
    if game_state and not game_state.story_flags.get(after_flag):
        after_dialog = npc_data.get('after_complete_dialog', [])
        if after_dialog:
            clear_screen()
            _display_npc_header(npc_data, "PERCAKAPAN")
            for speaker, line in after_dialog:
                _print_dialog_line(speaker, line)
            print()
            separator()
            wait_input()
            game_state.story_flags[after_flag] = True
            return

    # ── State 2: brief done line (setiap kunjungan setelahnya) ──────────────
    brief_done_lines = {
        'haikaru': "Cari polanya. Setiap sistem punya celah. Temukan saja.",
        'aolinh':  "♪ Kita akan pulang. Aku percaya itu. ♪",
        'arganta': "La via è sempre avanti. Jalan selalu ada di depan.",
        'ignatius':"Otak insinyur tidak pernah berhenti. Kalau butuh sesuatu — tanya.",
        'vio':     "USB aman? Bagus. Kita hampir sampai.",
    }
    line = brief_done_lines.get(npc_id, f"{name}: Semoga berhasil.")

    clear_screen()
    _display_npc_header(npc_data, "PERCAKAPAN")
    print()
    _print_dialog_line(name, line)
    print()
    wait_input()


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER — CEK STATUS SIDEQUEST
# ─────────────────────────────────────────────────────────────────────────────

def can_trigger_sidequest(npc_id, game_state):
    """Return True jika sidequest NPC bisa dimulai sekarang."""
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return False
    reward_flag = npc_data.get('reward_flag', f"{npc_id}_sidequest_done")
    if game_state.story_flags.get(reward_flag):
        return False  # Sudah selesai
    current_chapter = int(game_state.story_flags.get('current_chapter', 1))
    return current_chapter >= npc_data['available_chapter']


def is_sidequest_complete(npc_id, game_state):
    """Return True jika semua syarat sidequest NPC sudah terpenuhi (siap redeem reward)."""
    npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
    if not npc_data:
        return False
    # Cek syarat item
    if npc_data.get('required_items'):
        return all(item in game_state.inventory for item in npc_data['required_items'])
    if npc_data.get('required_item'):
        return npc_data['required_item'] in game_state.inventory
    if npc_data.get('required_action'):
        return game_state.story_flags.get(npc_data['required_action'], False)
    return False


def get_npc_display_name(npc_id):
    """Nama tampilan NPC dengan fallback yang aman.
    
    Terlebih dahulu mengecek NPC_SIDEQUEST_DATA, lalu cek game_state cache,
    kemudian fallback ke capitalize() sebagai pilihan terakhir.
    
    CATATAN: Jika NPC baru ditambah ke constants.py tapi lupa di NPC_SIDEQUEST_DATA,
    sistem ini masih akan menampilkan nama dengan benar (meski tidak ideal).
    """
    # Priority 1: Check NPC_SIDEQUEST_DATA
    data = NPC_SIDEQUEST_DATA.get(npc_id)
    if data:
        return data.get('name', npc_id.capitalize())
    
    # Priority 2: Fallback ke capitalize() jika NPC belum terdaftar
    # (ini untuk NPC baru yang belum ditambah ke NPC_SIDEQUEST_DATA)
    return npc_id.capitalize()


def get_sidequest_summary(game_state):
    """
    Kembalikan list ringkasan status semua sidequest untuk quest tracker.
    Format: [{'npc': id, 'name': str, 'status': 'done'|'active'|'available'|'locked'}]
    
    Safe version: handles current_chapter as either string or int, with fallback.
    """
    result = []
    
    # Safe chapter retrieval: handles both string and int values
    current_chapter_raw = game_state.story_flags.get('current_chapter', 1)
    try:
        current_chapter = int(current_chapter_raw) if current_chapter_raw else 1
    except (ValueError, TypeError):
        current_chapter = 1  # Fallback to chapter 1 if conversion fails
    
    for npc_id, data in NPC_SIDEQUEST_DATA.items():
        reward_flag = data.get('reward_flag', f"{npc_id}_sidequest_done")
        if game_state.story_flags.get(reward_flag):
            status = 'done'
        elif game_state.story_flags.get(f"{npc_id}_quest_active"):
            status = 'active'
        elif current_chapter >= data.get('available_chapter', 1):
            status = 'available'
        else:
            status = 'locked'
        result.append({
            'npc':    npc_id,
            'name':   data.get('name', npc_id),
            'title':  data.get('sidequest_title', ''),
            'status': status,
            'impact': data.get('main_quest_impact', ''),
        })
    return result
