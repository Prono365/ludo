import os
import time

# tempat save file
SAVE_FILE = "data.txt"

def save_progress(scene_id):
    with open(SAVE_FILE, "w") as f:
        f.write(scene_id)

def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return f.read().strip()
        except:
            pass
    return "prolog"

# tampilan
def slow_print(text, delay=0.01):
    """
    Mencetak teks seperti mesin tik.
    Untuk efek membaca novel yang santai.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Database Cerita
story = {
    # --- PROLOG: AWAL PERTEMUAN ---
    "prolog": {
        "bab": "PROLOG: IKATAN EMAS",
        "text": "Kesadaranmu kembali perlahan, seperti seseorang yang terbangun dari mimpi panjang yang tak berujung. Bukan di atas kasur yang empuk, melainkan di lantai batu yang dingin dan lembab. Udara di tempat ini terasa berat, membawa aroma logam berkarat dan bau tanah yang tertutup hujan. \n\nSaat kamu mencoba menggerakkan tangan kananmu, kau merasakan beban yang aneh. Ada tali halus namun sangat kuat yang melilit di pergelangan tanganmu. Saat kau lihat, ada tangan pucat yang terlilit benang emas yang terhubung ke tanganmu. Candala. \n\nTangan kananmu terasa berat sekali. Tangan itu bukan milikmu. Tangan itu terikat pada pemiliknya yang kini terbaring lemah di sampingmu.",
        "candala": "Candala terbaring lemah di lantai. Matanya tertutup rapat. Napasnya tidak teratur.",
        "choices": ["Angkat tubuh Candala dan bantu dia berdiri", "Tanya apakah ada jalan pintas"],
        "next": ["bab1_angkat", "prolog_tanya"]
    },
    "prolog_tanya": {
        "bab": "PROLOG: JALAN PINTAS",
        "text": "Joel muncul dari bayangan. 'Jalan pintas? Di tempat ini? Satu-satunya jalan pintas adalah kematian. Dan kamu belum sepayah itu.'",
        "candala": "Update Sanity -5 (Rasa putus asa awal)",
        "choices": ["Terima kenyataan dan angkat Candala"],
        "next": ["bab1_angkat"]
    },

    # --- BAB 1: HUTAN KABEL (IGNATIUS - LOGIC) ---
    "bab1_angkat": {
        "bab": "BAB I: HUTAN KABEL",
        "text": "Kau mengangkat tubuh ringan Candala. Dia meringis pelan. Tanganmu terasa terbakar oleh benang emas itu. Perjalanan dimulai. \n\nKau berjalan menyusuri lorong batu yang sempit. Ujung lorong membuka pada sebuah hutan yang aneh. Ini bukan hutan dengan pepohonan hijau. Ini adalah hutan kabel. Kabel-kabel tembaga tebal saling melilit seperti akar pohon raksasa. Suara denging listrik memekakkan telinga, seperti ribuan serangga yang berdengung. \n\nDi antara rimbun kabel itu, seorang pria berkacamata tebal sedang duduk di atas tumpukan server tua. Ignatius.",
        "candala": "Candala memeluk erat tanganmu. Dia takut.",
        "choices": ["Sapa Ignatius dan tanya jalan keluar", "Cari jalan sendiri"],
        "next": ["bab1_sapa", "bab1_cari"]
    },
    "bab1_sapa": {
        "bab": "BAB I: HUTAN KABEL (PERTEMUAN)",
        "text": "Kau mendekati Ignatius. Pria itu sedang menempelkan kabel ke kepalanya sendiri. Saat ia melihatmu dan Candala, ia berhenti menulis. \n\n'Kau tersesat di algoritma,' kata Ignatius dengan suara berat. 'Probabilitas kau bertahan hidup di sini adalah 0.0001%. Tapi ada anomali.' \nIgnatius menunjuk Candala di tanganmu. 'Dia. Dia merusak perhitungan alam semesta. Error dalam kode.'",
        "candala": "Candala menangis kecil di balik bahunmu.",
        "choices": ["'Maksudmu dia kutukan?'", "'Dia bukan kutukan. Dia pasanganku.'"],
        "next": ["bab1_kutukan", "bab1_pasangan"]
    },
    "bab1_kutukan": {
        "bab": "BAB I: BAGIAN DARI KODE",
        "text": "Ignatius tertawa. 'Kutukan? Kata yang terlalu mistis untuk dunia digital ini. Dia adalah virus. Dan kau... kau adalah hostnya.' \n\nIgnatius berdiri dan menatapmu dengan mata merah, vena di dahinya menonjol. 'Jangan biarkan sistem memformat dia.' \n\nCandala menangis makin kencang. Nino tertawa semakin keras. Suara itu menusuk telinga.",
        "candala": "Candala: 'Papa... sakit...'",
        "choices": ["Bisikkan pada Candala untuk tenang"],
        "next": ["bab1_tenang"]
    },
    "bab1_pasangan": {
        "bab": "BAB I: PARASIT YANG ROMANTIS",
        "text": "Ignatius menghentikan tawanya. 'Pasangan? Menarik. Menjaga virus agar tidak mati... itu bentuk cinta baru.' \n\nIgnatius: 'Baiklah. Lalu apakah kau bersedia 'diinfeksi' selamanya demi dia?'",
        "candala": "Candala menatapmu penuh harapan.",
        "choices": ["'Selamanya.'", "'Hanya sampai pintu keluar.'"],
        "next": ["bab1_terima", "bab1_tolak"]
    },
    "bab1_cari": {
        "bab": "BAB I: TERSESAT DI ALGORITMA",
        "text": "Kau memutuskan mencari jalan sendiri. Kau menembus semak-semak kabel. \n\nTernyata, sistem lebih rumit dari yang kira. Kabel-kabel itu bergerak sendiri, menghalangi jalanmu, dan kadang memberikan sengatan listrik yang menyengatkan kulit. Kau tersesat. \n\nIgnatius muncul dari belakang. 'Aku bilang, ini bukan tempat random. Ini adalah server terpusat. Jalan keluarnya hanya satu.'",
        "candala": "Candala gemetar.",
        "choices": ["Minta Ignatius menunjukkan jalan"],
        "next": ["bab1_jalan"]
    },
    "bab1_jalan": {
        "bab": "BAB I: KELUAR",
        "text": "Ignatius menunjuk ke sebuah lorong gelap di sisi timur hutan. 'Lewati situ. Tapi hati-hati. Di sana ada labirin perhitungan.'",
        "candala": "Candala memegang tanganmu erat.",
        "choices": ["Masuk ke lorong gelap"],
        "next": ["bab2_taman"]
    },
    "bab1_tenang": {
        "bab": "BAB I: KEHANGATAN",
        "text": "Kau membelai rambut Candala. Dia tenang, tapi benang emas itu makin mengecut dan mencekik pergelangan tanganmu. \n\nRasa sakit itu nyata. Bukan ilusi.",
        "candala": "Candala: 'Terima kasih.'",
        "choices": ["Lanjut jalan"],
        "next": ["bab2_taman"]
    },
    "bab1_terima": {
        "bab": "BAB I: INFEKSI",
        "text": "Ignatius mengangguk. 'Fanatisme. Level 99. Lanjutkan. Jangan biarkan sistem memformat dia.' \n\nKau merasa sedikit aneh di dalam tubuhmu, seolah ada data asing yang mengalir.",
        "candala": "Candala tersenyum tipis.",
        "choices": ["Lanjut jalan"],
        "next": ["bab2_taman"]
    },
    "bab1_tolak": {
        "bab": "BAB I: PENOLAKAN",
        "text": "Ignatius meludah ke tanah (digital). 'Hypocrite. Manusia memang begitu. Manfaatkan lalu buang.' \n\nDia menunjuk jalan dengan kasar.",
        "candala": "Candala menatapmu dengan tatapan putus asa.",
        "choices": ["Lanjut jalan (Menyesal)"],
        "next": ["bab2_taman"]
    },

    # --- BAB 2: TAMAN DURI (AOLINH - EMPATHY) ---
    "bab2_taman": {
        "bab": "BAB II: TAMAN DURI",
        "text": "Lorong membawa kalian ke sebuah taman yang indah namun mengerikan. Bunganya terbuat dari daging segar. Batangnya adalah tulang putih. \n\nDi tengah taman, Aolinh sedang duduk memeluk sebuah bunga matahari yang menjerit. Aolinh... nama itu terasa begitu akrab, namun kau tidak ingat di mana pernah mendengarnya.",
        "candala": "Candala memegang tanganmu. Dia tampak tenang di tempat ini.",
        "choices": ["Mendekati Aolinh", "Biarkan Aolinh sendiri"],
        "next": ["bab2_dekat", "bab2_biarkan"]
    },
    "bab2_dekat": {
        "bab": "BAB II: KEBUNAN DALAM JIWA",
        "text": "Kau mendekati Aolinh. Wanita itu berbalik. Wajahnya penuh luka sayatan. \n\n'Kakak... apakah kakak suka bungaku? Bibirnya manis...' Aolinh menunjuk bunga yang berdarah di tangannya. \n\nKau melihat lebih dekat. Bunga itu terbuat dari bola mata yang menyatu. Sungguh mengerikan.",
        "candala": "Candala menunduk takut melihat bola mata itu.",
        "choices": ["'Itu bukan bunga, Aolinh. Itu daging.'", "'Sangat indah. Bagus sekali.'"],
        "next": ["bab2_jujur", "bab2_dustur"]
    },
    "bab2_biarkan": {
        "bab": "BAB II: DIAM DALAM SUNYI",
        "text": "Kau memutuskan untuk tidak mengganggu. Namun, dari jauh, kau bisa mendengar tangisannya. \n\n'Kenapa... kenapa kakak meninggalkan aku...?'",
        "candala": "Candala memeluk tanganmu, merasa bersedih karena Aolinh.",
        "choices": ["Akhirnya mendekati dan bertanya"],
        "next": ["bab2_tanya"]
    },
    "bab2_jujur": {
        "bab": "BAB II: KEJUJURAN",
        "text": "Kau berkata jujur. Bunga di tangan Aolinh hancur. \n\nAolinh menjerit histeris. 'Kakak jahat! Kakak tidak mau mengerti!' \n\nCandala di tanganmu gemetar. Dia takut dengan tangisan itu.",
        "candala": "Candala: 'Papa... peluk aku...'",
        "choices": ["Jelaskan bahwa itu demi kebaikannya"],
        "next": ["bab2_mengerti"]
    },
    "bab2_dustur": {
        "bab": "BAB II: PENGHANCURAN",
        "text": "Kau memuji Aolinh. Aolinh tersenyum lebar. Bibirnya sobek. \n\n'Kakak suka? Aku punya banyak lagi di dalam perutku...' \n\nAolinh menunjuk ke arah perutnya. Tindikasi yang ada di sana sangat menyeramkan. \n\nCandala bergetar hebat.",
        "candala": "Candala: 'Jangan... jangan melihat ke arah itu!'",
        "choices": ["Lari menjauh dari Aolinh"],
        "next": ["bab3_jembatan"]
    },
    "bab2_tanya": {
        "bab": "BAB II: KONFRONTASI",
        "text": "Aolinh menghentikan tangisannya. Dia menatapmu dengan mata sayu namun dalam. \n\n'Apa yang menyakitkanmu, Kakak? Aku... aku ditinggalkan.'",
        "candala": "Candala menatapmu, meminta belas kasih.",
        "choices": ["'Aku tersesat di sini, sama sepertimu.'"],
        "next": ["bab2_mengerti"]
    },
    "bab2_mengerti": {
        "bab": "BAB II: KOMPENSI",
        "text": "Kau memeluk Aolinh. Dia berhenti menangis. Air matanya menetes ke bahu bajumu. \n\nAolinh memberimu sebuah bunga berduri yang kering. \n\n'Untuk kakak... dan nona pucat itu. Jangan lupa disiram air mata ya.'",
        "candala": "Candala tersenyum kecil.",
        "choices": ["Terima bunga dan lanjut"],
        "next": ["bab3_jembatan"]
    },

    # --- BAB 3: JEMBATAN CERMIN (HAIKARU & VIO - MORAL) ---
    "bab3_jembatan": {
        "bab": "BAB III: JEMBATAN CERMIN",
        "text": "Kau meninggalkan taman aneh itu. Menemukan sebuah jembatan yang melayang di atas jurang tak berdasar. Lantainya cermin. Setiap kali melangkah, kau melihat wajahmu sendiri yang mengerikan di bawah. \n\nDi tengah jembatan, berdiri dua sosok. Haikaru (bersenjatakan pedang) dan Vio (bersenjatakan belati). Mereka tidak saling menyerang, melainkan menusuk diri sendiri dengan senjata yang sama.",
        "candala": "Candala memelukmu erat. Dia tidak menyukai tempat ini.",
        "choices": ["Lari melewati mereka", "Hadapi mereka"],
        "next": ["bab3_lari", "bab3_hadapi"]
    },
    "bab3_lari": {
        "bab": "BAB III: LARIAN TANPA TUJU",
        "text": "Kau berlari. Tapi jembatan itu memanjang. Mereka selalu ada di depan, menusuk diri sendiri berulang-ulang. \n\nLari... lari... lari... tapi tidak kemana-mana. Kelelahan mental menyerang.",
        "candala": "Candala: 'Papa... kita tersesat...'",
        "choices": ["Berhenti dan berteriak"],
        "next": ["bab3_teriak"]
    },
    "bab3_teriak": {
        "bab": "BAB III: KEPUTUSASAAN",
        "text": "Jeritanmu memecahkan cermin di bawah. Jembatan runtuh. Kau jatuh... tapi mendarat di tempat yang sama. \n\nHaikaru dan Vio tertawa di atas runtuhanmu. 'Lihat? Bukti ketiadaanmu!'",
        "candala": "Candala menunduk malu.",
        "choices": ["Bangkit dan lanjut"],
        "next": ["bab4_perpus"]
    },
    "bab3_hadapi": {
        "bab": "BAB III: KONFRONTASI",
        "text": "Kau berdiri di depan mereka. Mereka berhenti menusuk dan menatapmu. \n\nHaikaru: 'Kau berani berhenti?' \nVio: 'Atau kau hanya sudah menyerah?' \n\nMereka berdua bersatu menjadi satu sosok bayangan. Bayangan hitam yang menyerap cahaya.",
        "candala": "Candala menangis pelan.",
        "choices": ["''Jika aku lelah, aku beristirahat. Bukan menyerah.'", "''Apa yang ingin kalian berdua dariku?'"],
        "next": ["bab3_tenang", "bab3_tanya"]
    },
    "bab3_tenang": {
        "bab": "BAB III: DAMAI DALAM BADAI",
        "text": "Sosok bayangan itu tersenyum dan menghilang. Jembatan menjadi pendek. \n\nHaikaru: 'Kelelahan adalah kebenaran,' bisik suara di angin. Vio: 'Kita membutuhkan pengorbanan agar jembatan ini stabil.' \n\nCandala menatapmu. 'Kau kuat,' katanya. 'Kau melindungi aku.'",
        "candala": "Candala merasa lebih aman.",
        "choices": ["Lanjut jalan"],
        "next": ["bab4_perpus"]
    },
    "bab3_tanya": {
        "bab": "BAB III: TANYA JAWAB",
        "text": "Kau bertanya pada mereka. \n\n''Apakah satu-satunya cara menstabilkan jembatan ini adalah pengorbanan? Tidak ada cara lain?' \n\nHaikaru tertawa. Vio menangis.",
        "candala": "Candala tidak tahu harus mendukung yang mana.",
        "choices": ["Terima pengorbanan agar jembatan stabil", "Lawan mereka untuk membebaskan Candala"],
        "next": ["bab3_korban", "bab3_lawan"]
    },
    "bab3_korban": {
        "bab": "BAB III: KORBAN",
        "text": "Kau menerima pengorbanan. Haikaru dan Vio menangis dan menghilang menjadi debu. Jembatan menjadi kokoh. \n\nKau menyeberangi jembatan itu. Tapi ada bekas luka di jiwa.",
        "candala": "Candala melihatmu iba.",
        "choices": ["Lanjut"],
        "next": ["bab4_perpus"]
    },
    "bab3_lawan": {
        "bab": "BAB III: PERTEMPURAN",
        "text": "Kau berdiri tegak melawan bayangan hitam itu. 'Kita tidak akan menjadi budak sistem!' \n\nPertempuran hebat terjadi. Bayangan itu pecah menjadi serpihan api. Kau terluka bakar. Namun, cahaya itu memusnahkan jembatan. Kau dan Candala jatuh.",
        "candala": "Candala menjerit pelan.",
        "choices": ["Bangkit dan lanjut"],
        "next": ["bab4_perpus"]
    },

    # --- BAB 4: PERPUSTAKAAN (ARGANTA - KAFKA) ---
    "bab4_perpus": {
        "bab": "BAB IV: PERPUSTAKAAN KAFKA",
        "text": "Kau tiba di sebuah perpustakaan tua. Tidak ada ujung. Rak bukunya menjulang tinggi sampai ke langit yang tak terlihat. \n\nDi tengah ruangan, Arganta duduk di kursi kayu tua, membaca sebuah buku yang sangat tebal. Judulnya terukir jelas: **'The Trial' (Proses) - Franz Kafka**.",
        "candala": "Candala terdiam di belakangmu.",
        "choices": ["'Apa yang sedang kau baca?'", "'Mengapa aku terikat di sini?'"],
        "next": ["arganta_jelaskan", "arganta_ikat"]
    },
    "arganta_jelaskan": {
        "bab": "BAB IV: PROSES PENGADILAN",
        "text": "Arganta menutup bukunya. \n\n'Buku ini menceritakan seorang pria, Jose K., yang ditangkap dan dihukum tanpa pernah tahu kesalahannya.' \n\nArganta menunjuk ke arahmu. 'Sama seperti kalian. Kau hidup, kau menderita karena {dosa}, lalu kau mati. Pengadilan ini tidak akan pernah memberi vonis adil.' \n\nArganta: 'Josef K. mati 'seperti anjing'. Kau mau mati seperti apa?'",
        "candala": "Candala mendengarkan dengan seksama.",
        "choices": ["'Aku tidak mau mati seperti sampah.'", "'Aku tidak peduli vonisnya.'"],
        "next": ["arganta_marah", "arganta_pasrah"]
    },
    "arganta_ikat": {
        "bab": "BAB IV: BELITAN TAKDIR",
        "text": "Arganta menatapmu, lalu menatap Candala. \n\n'Candala di tanganmu... dia sudah mati sejak lama. Kau hanya membawa bangkai.' \n\nArganta: 'Tapi ada detak jantung... bukan di dadanya. Tapi di dalam benang emas yang mengikat kalian.' \n\nArganta: 'Sungguh parasit yang romantis.'",
        "candala": "Candala menatapmu dengan mata kosong.",
        "choices": ["''Aku akan terus membawanya, sampai detak itu berhenti di akupun.'"],
        "next": ["bab5_akhir"]
    },
    "arganta_marah": {
        "bab": "BAB IV: HUKUMAN",
        "text": "Arganta tersenyum mengejek. 'Kau punya harga diri? Di tempat ini?' \n\nArganta: 'Karena kau punya harga diri, penghukumanmu akan lebih lama. Bawa Candala ke ruang eksekusi.'",
        "candala": "Candala menangis.",
        "choices": ["Gandeng tangan Candala menuju ruang eksekusi"],
        "next": ["bab5_akhir"]
    },
    "arganta_pasrah": {
        "bab": "BAB IV: PASRAH",
        "text": "Arganta berdiri. 'Pasrah. Kebanyakan manusia memilih jalan ini.' \n\nArganta: 'Kalau begitu, pergilah. Jangan ganggu pengadilan dengan tangisanmu.'",
        "candala": "Candala hanya diam.",
        "choices": ["Gandeng tangan Candala menuju ruang akhir"],
        "next": ["bab5_akhir"]
    },

    # --- BAB 5: FINAL (THE TRIAL & CONFESSION) ---
    "bab5_akhir": {
        "bab": "BAB V: RUANG PENGADILAN",
        "text": "Di ruang terakhir, tidak ada algojo. Hanya ada kursi kosong. Dan di tengahnya, tiang gantungan. \n\nSuara (Arganta?): 'Hakimnya tidak ada. Juri tidak ada. Hanya kalian dan rasa bersalah {dosa}.' \n\nCandala berdiri sendiri (untuk pertama kalinya). Benang emas itu renggang. \n\nCandala: 'Ini akhirnya...'",
        "candala": "Candala: 'Apa yang harus kulakukan?'",
        "choices": ["'Lari bersama Candala (Rebel)'", "'Biarkan Candala digantung (Void)'", "'Mengakui dosa & menebusnya (Confession)'"],
        "next": ["rebel_ending", "void_ending", "confession_route"]
    },

    # --- ROUTE: CONFESSION (PENGAKUAN) ---
    "confession_route": {
        "bab": "PENGAKUAN: RUANG BACA",
        "text": "Kau berdiri di tengah ruang putih. Ini bukan pengadilan. Ini adalah ruang baca. \n\n'Pengakuan,' bisik suara di sekelilingmu. 'Hanya di sini, kau bisa membersihkan dirimu dari beban dosa sebelum pergi ke ke tempat tujuan.' \n\nKau melihat meja kayu tua. Di atasnya ada pena dan kertas kosong.",
        "candala": "Candala menunggu.",
        "choices": ["Tuliskan pengakuan dosa di kertas"],
        "next": ["tulis_pengakuan"]
    },
    "tulis_pengakuan": {
        "bab": "PENGAKUAN: TINTA PEMBEBAS",
        "text": "Kau mengambil pena. Kau mulai menulis tentang {dosa}. \n\nKau menuangkan semua penyesalan, rasa sakit, dan keinginan untuk berubah. Saat tinta terakhir kering, kertas itu bersinar terang. \n\nSuara (Tuhan? Arganta?): 'Pengakuan yang tulus melepaskan rantai. Namun, konsekuensi tetap ada. Pilihlah jalur akhirmu dengan bijak.'",
        "candala": "Candala tersenyum.",
        "choices": [
            "Pergi ke Surga (Redemption)",
            "Pergi ke Neraka (Judgment)",
            "Lingkaran Terus (Purgatory)"
        ],
        "next": ["confession_surga", "confession_neraka", "confession_loop"]
    },
    "confession_surga": {
        "bab": "ENDING: PENGAMPUNAN",
        "text": "Pintu ke Surga terbuka. Cahaya menyilaukan. \n\nKau dan Candala masuk. Rasa bersalah telah hilang, digantikan dengan kedamaan. \n\nENDING: REDEMPTION",
        "candala": "",
        "choices": ["Selesai"],
        "next": ["selesai"]
    },
    "confession_neraka": {
        "bab": "ENDING: HUKUMAN",
        "text": "Pintu ke Neraka terbuka. Panas yang menyengatkan. \n\nKau harus menjalani hukuman karena dosa masa lalu yang tidak kau perbaiki dengan sungguh-sungguh saat hidup. \n\nENDING: JUDGMENT",
        "candala": "",
        "choices": ["Selesai"],
        "next": ["selesai"]
    },
    "confession_loop": {
        "bab": "ENDING: SIKLUS PEMBAHARAN",
        "text": "Tidak ada pintu yang terbuka. Kau dan Candala dikirim kembali ke prolog. \n\nKau harus mengulang kehidupan untuk membersihkan dosamu sedikit demi sedikit. \n\nENDING: PURGATORY LOOP",
        "candala": "",
        "choices": ["Mulai Ulang"],
        "next": ["prolog"]
    },

    # --- ENDINGS LAIN ---
    "rebel_ending": {
        "bab": "ENDING: THE TRIAL ENDS",
        "text": "Kau memegang tangan Candala dan berlari menabrak dinding putih. Dinding itu retak. \n\nDi baliknya, bukan kebebasan. Tapi hutan kabel lagi. \n\nCandala: 'Kita tidak akan pernah keluar, [Nama]. Kau tahu. Ayo kita berjalan lagi.' \n\nKau tersenyum lelah. 'Aku tahu. Ayo kita berjalan lagi.'",
        "candala": "LOOP INFINIT DIMULAI...",
        "choices": ["Main Ulang"],
        "next": ["reset"]
    },
    "void_ending": {
        "bab": "ENDING: SOLITUDE CONFINEMENT",
        "text": "Kau melepaskan tangan Candala. Dia naik ke tiang gantungan sendiri. Tali itu terikat lehermu sendiri. \n\nCandala: 'Terima kasih... telah melepaskanku dari rasa sakit...' (Tapi matanya menyalahkanmu). \n\nKau sendirian di ruang putih. Sunyi. Abadi.",
        "candala": "",
        "choices": ["Reset"],
        "next": ["reset"]
    },

    # Sistem
    "reset": {
        "bab": "SYSTEM",
        "text": "Menghapus memori...",
        "choices": ["Mulai"],
        "next": ["prolog"]
    },
    "selesai": {
        "bab": "SYSTEM",
        "text": "Cerita selesai.",
        "candala": "",
        "choices": ["Keluar"],
        "next": ["selesai_exit"]
    },
    "selesai_exit": {
        "bab": "SYSTEM",
        "text": "Terima kasih.",
        "candala": "",
        "choices": ["Selesai"],
        "next": ["selesai_exit"]
    }
}

# Variabel
nama_player = "Unknown"
latar_dosa = "Unknown Crime"

def intro_player():
    global nama_player, latar_dosa
    clear_screen()
    print("=" * 40)
    print("CANDALA")
    print("   (Novel Interaktif Full Story)")
    print("=" * 40)
    print("\n[Info]: Program ini adalah novel teks panjang.")
    print("[Info]: Gunakan headphone untuk pengalaman terbaik.")
    
    nama_player = input("\nSiapa nama pengelana? : ")
    latar_dosa = input("Apa satu dosa yang sangat menyesakkanmu? : ")
    
    print("\n[Memulai narasi...]")
    time.sleep(2)

def format_text(text):
    return text.replace("{nama}", nama_player).replace("{dosa}", latar_dosa)

def main():
    intro_player()
    scene = "prolog"
    
    while True:
        clear_screen()
        data = story[scene]
        
        print("-" * 60)
        # Tampilkan Judul Bab
        print(f">>> {data['bab']} <<<")
        print("-" * 60)
        
        # Tampilkan Narasi (Slow Print)
        narrative_text = format_text(data['text'])
        slow_print(narrative_text)
        print()
        
        # Tampilkan Dialog Candala
        if 'candala' in data:
            candala_text = format_text(data['candala'])
            if candala_text:
                print(f"   {candala_text}")
        print("-" * 60)
        
        # Tampilkan Pilihan
        choices = data['choices']
        for i, c in enumerate(choices, 1):
            print(f"{i}. {c}")
            
        try:
            pil = int(input("\nPilihan Bab Selanjutnya: "))
            idx = pil - 1
            if 0 <= idx < len(choices):
                next_scene = data['next'][idx]
                
                # Simpan Progress
                save_progress(next_scene)
                scene = next_scene
                
            else:
                print("Halaman ini tidak ada dalam buku.")
                time.sleep(1)
        except ValueError:
            print("Input salah.")
            time.sleep(1)

if __name__ == "__main__":
    main()