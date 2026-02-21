# Rute dan chapter tiap karakter

from sprites import Warna
from contextlib import suppress
import time

try:
    from story import display_route_chapter
except ImportError:
    def display_route_chapter(chapter_id):
        pass

from constants import (
    MAX_CHAPTERS, BOSS_CHAPTERS, FINAL_CHAPTER, CHAPTER_BOSSES,
    SIDEQUESTS_NEEDED_FOR_CH4, SIDEQUESTS_NEEDED_FOR_CH6,
)

CHAPTER_OBJECTIVES = {
    1: "Kabur dari area starting — selesaikan semua objektif Chapter 1",
    2: "Bersihkan pulau, kalahkan Kepala Penjaga di Penjara Utara",
    3: "Bangun aliansi — selesaikan minimal 2 sidequest NPC",
    4: "Infiltrasi laboratorium — kalahkan Maxwell's Agent",
    5: "Kumpulkan semua bukti — selesaikan 4 sidequest NPC",
    6: "Konfrontasi final — hentikan Jeffrey Epstein di Mansion Timur",
}

CHAPTER_OBJECTIVES_BY_CHAR = {
    "vio": {
        1: "Hack server mansion, jebol sistem keamanan, kabur dari ruang server",
        2: "Dominasi jaringan pulau, singkirkan Kepala Penjaga",
        3: "Rekrut sekutu — kumpulkan item kunci dari NPC",
        4: "Tembus lab Maxwell, ambil data intel, kalahkan Maxwell's Agent",
        5: "Upload deadman switch — kumpulkan semua bukti digital",
        6: "Server final — expose Epstein ke dunia",
    },
    "haikaru": {
        1: "Eksekusi rencana 47 langkah — kabur dari sel penjara",
        2: "Taktik superioritas — netralkan Kepala Penjaga",
        3: "Kalkulasi aliansi — rekrut sekutu strategis",
        4: "Checkmate Maxwell's Agent — probabilitas menang 99.9%",
        5: "Kumpulkan semua variabel bukti — persiapkan strategi final",
        6: "Checkmate Epstein — eksekusi rencana akhir",
    },
    "aolinh": {
        1: "Cari jejak Jiejie di theater, kalahkan penjaga yang mengurungnya",
        2: "Simfoni kebebasan — singkirkan Kepala Penjaga",
        3: "Nyanyikan harapan — rekrut sekutu dengan melodimu",
        4: "Melodi perlawanan — jebol lab Maxwell bersama tim",
        5: "Kumpulkan bukti untuk Jiejie — akhiri penderitaan ini",
        6: "Final crescendo — kalahkan Epstein untuk semua anak yang terjebak",
    },
    "arganta": {
        1: "Survival mode — kumpulkan bekal, buka jalur dermaga",
        2: "Navigator memimpin — singkirkan Kepala Penjaga",
        3: "Per famiglia — rekrut sekutu untuk keadilan",
        4: "La via è sempre avanti — tembus lab Maxwell",
        5: "Requiescat in pace — kumpulkan semua bukti kejahatan",
        6: "Vendetta finale — kalahkan Epstein untuk keluargamu",
    },
    "ignatius": {
        1: "Rekayasa mesin — rakit EMP, sabotase alarm, hancurkan Security Bot",
        2: "Engineering bergerak — Kepala Penjaga harus disingkirkan",
        3: "Tim engineer — rekrut sekutu dengan keahlian teknis",
        4: "EMP total — matikan lab Maxwell dengan teknologimu",
        5: "Blueprint keadilan — kumpulkan semua bukti elektronik",
        6: "Blackout Epstein — matikan sistem terakhirnya selamanya",
    },
}

BOSS_DATA = {
    'kepala_penjaga': {
        'name':       'Kepala Penjaga',
        'chapter':    2,
        'location':   'prison_north',
        'hp':         350,      # Balance: Boss HP +40%
        'attack':     22,
        'defense':    15,
        'speed':      12,
        'reward_xp':  300,
        'reward_dollars': 80,
        'reward_item': 'Kunci Master Penjara',
        'flag_key':   'boss_ch2_defeated',
        'intro': [
            "Kepala Penjaga memblokir jalan kalian.",
            "'Kamu pikir bisa kabur? Pulau ini penjara sempurna.'",
            "'Tidak ada yang pernah berhasil keluar.'",
        ],
        'defeat_text': [
            "Kepala Penjaga jatuh. Kunci master-nya terlepas dari sakunya.",
            "Jalan menuju chapter berikutnya terbuka.",
        ],
    },
    'agen_maxwell': {
        'name':       "Maxwell's Agent",
        'chapter':    4,
        'location':   'laboratory',
        'hp':         530,      # Balance: Boss HP +40%
        'attack':     35,
        'defense':    22,
        'speed':      18,
        'reward_xp':  500,
        'reward_dollars': 150,
        'reward_item': 'Kartu Akses Lab',
        'flag_key':   'boss_ch4_defeated',
        'special': 'Lemah terhadap EMP Device — gunakan sebelum battle',
        'intro': [
            "Maxwell's Agent berdiri di tengah laboratorium.",
            "'Anak-anak kecil yang mana coba berani masuk ke sini.'",
            "'Maxwell sudah kasih instruksi jelas: tidak ada saksi.'",
        ],
        'defeat_text': [
            "Agent jatuh. Sistem keamanan lab tidak merespons lagi.",
            "Kartu akses ke vault dokumen kini ada di tanganmu.",
        ],
    },
    'jeffrey_epstein': {
        'name':       'Jeffrey Epstein',
        'chapter':    6,
        'location':   'mansion_east',
        'hp':         850,      # Balance: Final boss HP +42%
        'attack':     45,
        'defense':    30,
        'speed':      20,
        'reward_xp':  1000,
        'reward_dollars': 0,
        'reward_item': None,
        'flag_key':   'boss_ch6_defeated',
        'special': 'Membutuhkan USB Evidence Drive untuk unlock true ending',
        'intro': [
            "Jeffrey Epstein berdiri di ruang besar mansion.",
            "Senyumnya dingin. Sama sekali tidak takut.",
            "'Kalian pikir kalian satu-satunya yang pernah mencoba?'",
            "'Tapi tidak ada yang bisa sentuh aku. Aku... tidak tersentuh.'",
        ],
        'defeat_text': [
            "Epstein jatuh. Pulau terkutuk ini akhirnya dalam jangkauanmu.",
            "Tapi ini bukan akhir. Ini baru awal kebenaran.",
        ],
    },
}

CH1_ITEM_OBJECTIVE_MAP = {
    'vio': {
        'Keycard Level 1': ('hack_terminal',
            "Vio: Keycard ini bisa bypass firewall terminal pertama. Useful."),
        'Keycard Level 2': ('hack_terminal',
            "Vio: Level 2. Server makin terbuka. Pity counter bisa nunggu."),
        'USB Encrypted':   ('hack_terminal',
            "Vio: USB ini ada data terenkripsi. Perlu di-crack, tapi ini petunjuk besar."),
        'Laptop':          ('hack_terminal',
            "Vio: Laptop dengan akses jaringan lokal. RNG blessed today."),
        'Access Card':     ('hack_terminal',
            "Vio: Access card. Lumayan untuk akses server room utama."),
    },
    'haikaru': {
        'Buku Catatan':         ('find_blind_spots',
            "Haikaru: Catatan tambahan. Blind spot barat laut terkonfirmasi. Update kalkulasi."),
        'Buku Catatan Haikaru': ('find_blind_spots',
            "Haikaru: *menggenggam buku* Ini catatanku yang disita! Sekarang analisa bisa dilanjutkan."),
        'Info Pulau':           ('find_blind_spots',
            "Haikaru: Data baru. Pola patroli teridentifikasi. Efisiensi rencana naik 12%."),
        'Med Kit':              ('find_blind_spots',
            "Haikaru: *melihat posisi loker* Blind spot area ini teridentifikasi dari sini."),
        'Keycard Level 1':      ('find_blind_spots',
            "Haikaru: Layout yang ditunjukkan kartu ini mengkonfirmasi blind spot ketiga."),
        'Kunci Wing-C':         ('find_wingc_key',
            "Haikaru: *menggenggam kunci* Ini yang aku cari. Loker 7, bukan 12. Asumsi awal salah 3%."),
    },
    'aolinh': {
        # Fix: Ao Linh Route — Bandage removed as clue; replaced with narrative items
        'Health Potion':   ('find_jiejie_clues',
            "Aolinh: *menemukan sesuatu* ...Ini pita rambut Jiejie. Dia pernah di sini!"),
        'Gantungan Kunci Musik': ('find_jiejie_clues',
            "Aolinh: *mengangkat gantungan berbentuk not* ...Ini milik Jiejie! Nada favoritnya tergores di sini!"),
        'Tiket Backstage': ('find_jiejie_clues',
            "Aolinh: Tiket backstage! Jiejie pasti dibawa lewat sini. 我找到了！"),
        'Info Pulau':      ('find_jiejie_clues',
            "Aolinh: Peta ini... ada ruangan backstage yang ditandai. Jiejie pasti di sana!"),
    },
    'arganta': {
        'Health Potion':   ('collect_survival_kit',
            "Arganta: Obat-obatan. Per Nonno — bertahan dulu, lawan kemudian."),
        'Bandage':         ('collect_survival_kit',
            "Arganta: Perban. Kit survival makin lengkap. Nonno akan setuju."),
        'Kompas Nonno Arganta': ('collect_survival_kit',
            "Arganta: *menggenggam erat* Il mio compasso! Ini... ini milik Nonno. Ini segalanya."),
        'Med Kit':         ('collect_survival_kit',
            "Arganta: Med kit lengkap. Satu lagi komponen survival terkumpul."),
    },
    'ignatius': {
        'Kapasitor Besar': ('collect_emp_parts_ch1',
            "Ignatius: 200 microfarad kapasitor. PERFECT. Ini komponen utama EMP-ku!"),
        'Relay Switch':    ('collect_emp_parts_ch1',
            "Ignatius: Relay switch! Ini yang trigger pulse-nya. Engineering time!"),
        'Copper Coil':     ('collect_emp_parts_ch1',
            "Ignatius: Copper coil! Induktansi optimal. Satu lagi dan EMP prototype jadi!"),
        'Blueprint':       ('sabotage_alarm_panel',
            "Ignatius: Blueprint sistem alarm! Sekarang aku tahu persis titik lemahnya."),
        'EMP Prototype':   ('sabotage_alarm_panel',
            "Ignatius: EMP prototype aktif! Tinggal tancapkan ke panel alarm ini..."),
    },
}

CH1_PRE_BOSS_DIALOGS = {
    'vio': {
        'maxwell_enforcer': [
            ('narasi', "Server room utama. Di balik pintu besi... langkah kaki berat."),
            ('dialog', "Vio: *menghentikan langkah* Hmm."),
            ('inner',  "[Signature langkah. 90kg+. Sepatu militer. Bukan guard biasa.]"),
            ('dialog', "Vio: Maxwell. Head of Security. Filenya sudah kubaca."),
            ('dialog', "Vio: Former special forces. Bisa bunuh orang dengan tangan kosong."),
            ('inner',  "[Situasi ini... tidak ideal untuk hacker 13 tahun sendirian.]"),
            ('inner',  "[Tapi data di server ini ada jutaan dollar dan ratusan nama. Harus diekspos.]"),
            ('dialog', "Vio: *mengepalkan tangan* Fine. Selalu ada exploit-nya."),
            ('dialog', "Vio: Gacha player tahu satu hal tentang boss — tinggal temukan pattern-nya."),
        ],
    },
    'haikaru': {
        'warden_elite': [
            ('narasi', "Pintu utama penjara. Warden Elite berdiri menghalangi jalan keluar."),
            ('dialog', "Haikaru: *berhenti tepat di ambang pintu*"),
            ('inner',  "[Warden Elite. Reaksi 0.3 detik. Jangkauan 2.1m. Berat estimasi 85kg.]"),
            ('inner',  "[Variabel yang belum diperhitungkan: seberapa cepat dia panggil bantuan.]"),
            ('dialog', "Haikaru: Tidak ada dalam kalkulasi awal saya."),
            ('dialog', "Haikaru: Tapi saya sudah siapkan tiga skenario untuk situasi ini."),
            ('dialog', "Haikaru: Skenario A. Konfrontasi langsung. Efisiensi 73%. Cukup."),
            ('narasi', "Haikaru Fumika melangkah maju dengan presisi yang dingin."),
        ],
    },
    'aolinh': {
        'theater_master': [
            ('narasi', "Backstage teater. Suara langkah berat di balik pintu besi."),
            ('dialog', "Aolinh: *mencengkeram biola* Jiejie... ada di balik pintu itu."),
            ('inner',  "[Theater Master. Yang mengurung Jiejie di sini. Yang memisahkan mereka.]"),
            ('inner',  "[Aolinh takut. Sangat takut. Tangannya gemetar.]"),
            ('dialog', "Aolinh: *berbisik* 妈妈... 给我力量。"),
            ('dialog', "Aolinh: Mama... beri aku kekuatan."),
            ('narasi', "Dia memainkan satu not biola. Pelan. Dalam."),
            ('dialog', "Aolinh: Jiejie menungguku. Aku tidak akan lari."),
            ('narasi', "Aolinh membuka pintu besi itu."),
        ],
    },
    'arganta': {
        'harbor_captain': [
            ('narasi', "Ujung dermaga. Harbor Captain berdiri menghadap laut — punggungnya ke Arganta."),
            ('dialog', "Arganta: *melihat kapal di kejauhan* Itu jalan keluarnya."),
            ('inner',  "[Harbor Captain. Yang menghalangi dermaga. Yang berdiri antara dia dan kebebasan.]"),
            ('inner',  "[Dan keadilan untuk Nonno.]"),
            ('dialog', "Arganta: *memegang kompas* La via è sempre avanti."),
            ('dialog', "Arganta: Jalan selalu ada di depan. Tapi kadang ada yang harus disingkirkan."),
            ('dialog', "Arganta: *mengeluarkan pisau lipat* Niente è reale, tutto è lecito."),
            ('narasi', "Amerigo Arganta melangkah ke pertarungan terakhirnya di chapter ini."),
        ],
    },
    'ignatius': {
        'security_bot': [
            ('narasi', "Generator room utama. AmBOTukam Mk II aktif dan berputar menghadap Ignatius."),
            ('system', ">> AMBOTUKAM MK II: UNAUTHORIZED PERSONNEL DETECTED"),
            ('system', ">> INITIATING ELIMINATION PROTOCOL"),
            ('dialog', "Ignatius: *tersenyum lebar* Oh halo juga, teman lama."),
            ('inner',  "[AmBOTukam Mk II. Model 2019. Weakpoint: central capacitor bank.]"),
            ('inner',  "[Kalau EMP prototype deliver pulse ke capacitor... sistem crash total.]"),
            ('dialog', "Ignatius: Kamu jaga generator. Bagus."),
            ('dialog', "Ignatius: Tapi aku akan matiin kamu pakai generator kamu sendiri."),
            ('dialog', "Ignatius: *menyiapkan EMP prototype* Engineering time!"),
        ],
    },
}

CH1_QUESTS = {
    'vio': {
        'title':       'Hack & Escape: Ruang Server Mansion',
        'description': 'Vio terjebak di ruang server mansion. Tembus sistem enkripsi dan kalahkan Maxwell Enforcer sebelum ketahuan.',
        'location':    'mansion',
        'objectives': [
            {
                'id':     'hack_terminal',
                'desc':   'Tembus 2 terminal server mansion',
                'target': 2,
                'type':   'interact',
                'label':  'Terminal di-hack: {}/{}'
            },
            {
                'id':     'defeat_maxwell_enforcer',
                'desc':   'Kalahkan Maxwell Enforcer — kepala keamanan jaringan (Boss Ch.1)',
                'target': 1,
                'type':   'boss',
                'label':  'Maxwell Enforcer: {}/{}'
            },
        ],
        'completion_flag': 'ch1_vio_complete',
        'reward_item':     'Akses Level 3',
        'reward_flag':     'vio_ch1_reward_given',
        'completion_text': [
            "Server ter-hack. Data jutaan dollar mulai mengalir ke USB-mu.",
            "Maxwell Enforcer sudah dikalahkan. Jalur keluar mansion terbuka.",
            "Kamu menggenggam 'Akses Level 3' — kunci ke area island selanjutnya.",
        ],
        'next_area': 'island',
    },

    'haikaru': {
        'title':       'Escape Analysis: Penjara Utara',
        'description': 'Haikaru sudah 2 minggu kalkulasi rencana kabur. Identifikasi blind spot, ambil kunci Wing-C, kalahkan Warden Elite.',
        'location':    'prison_north',
        'objectives': [
            {
                'id':     'find_blind_spots',
                'desc':   'Identifikasi 3 blind spot penjaga (via item observasi)',
                'target': 3,
                'type':   'interact',
                'label':  'Blind spot terkonfirmasi: {}/{}'
            },
            {
                'id':     'find_wingc_key',
                'desc':   'Ambil Kunci Wing-C dari loker tersembunyi di Wing-C',
                'target': 1,
                'type':   'interact',
                'label':  'Kunci Wing-C: {}/{}'
            },
            {
                'id':     'defeat_warden_elite',
                'desc':   'Kalahkan Warden Elite yang memblokir pintu utama (Boss Ch.1)',
                'target': 1,
                'type':   'boss',
                'label':  'Warden Elite: {}/{}'
            },
        ],
        'completion_flag': 'ch1_haikaru_complete',
        'reward_item':     'Peta Blind Spot Penjara',
        'reward_flag':     'haikaru_ch1_reward_given',
        'completion_text': [
            "Semua blind spot teridentifikasi. Peta mental 100% lengkap.",
            "Kunci Wing-C berhasil diambil — celah dalam sistem dikonfirmasi.",
            "Warden Elite dinetralkan. Waktu eksekusi: tepat sesuai kalkulasi.",
            "Kamu menerima 'Peta Blind Spot Penjara' — keunggulan navigasi chapter berikutnya.",
        ],
        'next_area': 'island',
    },

    'aolinh': {
        'title':       'Melodi Kebebasan: Cari Jejak Jiejie',
        'description': 'Aolinh terjebak di theater. Cari 2 jejak Jiejie, lalu hadapi Theater Master yang mengurungnya.',
        'location':    'theater',
        'objectives': [
            {
                'id':     'find_jiejie_clues',
                'desc':   'Temukan 2 jejak Jiejie di area theater',
                'target': 2,
                'type':   'interact',
                'label':  'Jejak Jiejie ditemukan: {}/{}'
            },
            {
                'id':     'defeat_theater_master',
                'desc':   'Kalahkan Theater Master yang mengurung Jiejie (Boss Ch.1)',
                'target': 1,
                'type':   'boss',
                'label':  'Theater Master: {}/{}'
            },
        ],
        'completion_flag': 'ch1_aolinh_complete',
        'reward_item':     'Tiket Backstage',
        'reward_flag':     'aolinh_ch1_reward_given',
        'completion_text': [
            "Dua jejak Jiejie ditemukan — dia masih di pulau ini!",
            "Theater Master telah dikalahkan. Backstage terbuka.",
            "Kamu menerima 'Tiket Backstage' — izin masuk area tersembunyi.",
            "♪ Jiejie... Aolinh sudah dekat. Musik memberi kekuatan. ♪",
        ],
        'next_area': 'island',
    },

    'arganta': {
        'title':       'Survival Route: Pantai Karibia',
        'description': 'Arganta terdampar di pantai. Kumpulkan perlengkapan survival dan kalahkan Harbor Captain untuk buka jalur dermaga.',
        'location':    'beach',
        'objectives': [
            {
                'id':     'collect_survival_kit',
                'desc':   'Kumpulkan 2 perlengkapan survival (obat, perban, atau bekal)',
                'target': 2,
                'type':   'interact',
                'label':  'Perlengkapan terkumpul: {}/{}'
            },
            {
                'id':     'defeat_harbor_captain',
                'desc':   'Kalahkan Harbor Captain yang menjaga dermaga (Boss Ch.1)',
                'target': 1,
                'type':   'boss',
                'label':  'Harbor Captain: {}/{}'
            },
        ],
        'completion_flag': 'ch1_arganta_complete',
        'reward_item':     'Kompas Aktif',
        'reward_flag':     'arganta_ch1_reward_given',
        'completion_text': [
            "Perlengkapan survival terkumpul. Cukup untuk perjalanan panjang.",
            "Harbor Captain telah dikalahkan. Dermaga terbuka.",
            "Il compasso Nonno menyala — 'Kompas Aktif' menunjuk jalur barat.",
            "Per Nonno. La via è sempre avanti.",
        ],
        'next_area': 'island',
    },

    'ignatius': {
        'title':       'Engineering Breakout: Basement Listrik',
        'description': 'Ignatius di ruang listrik basement — pusat saraf seluruh pulau. Rakit EMP, sabotase alarm, hancurkan Security Bot.',
        'location':    'basement',
        'objectives': [
            {
                'id':     'collect_emp_parts_ch1',
                'desc':   'Kumpulkan 3 komponen EMP: Kapasitor Besar, Relay Switch, Copper Coil',
                'target': 3,
                'type':   'interact',
                'label':  'Komponen EMP terkumpul: {}/{}'
            },
            {
                'id':     'sabotage_alarm_panel',
                'desc':   'Sabotase panel alarm utama basement (gunakan Blueprint/EMP)',
                'target': 1,
                'type':   'interact',
                'label':  'Panel alarm disabotase: {}/{}'
            },
            {
                'id':     'defeat_security_bot',
                'desc':   'Kalahkan AmBOTukam Mk II dengan EMP prototype (Boss Ch.1)',
                'target': 1,
                'type':   'boss',
                'label':  'AmBOTukam Mk II: {}/{}'
            },
        ],
        'completion_flag': 'ch1_ignatius_complete',
        'reward_item':     'EMP Prototype',
        'reward_flag':     'ignatius_ch1_reward_given',
        'completion_text': [
            "Tiga komponen terkumpul dan dirakit menjadi EMP Prototype.",
            "Panel alarm berhasil disabotase — 30% sistem keamanan offline.",
            "AmBOTukam Mk II dihancurkan dengan EMP-nya sendiri. Poetic.",
            "Kamu menerima 'EMP Prototype' — senjata kunci untuk chapter berikutnya.",
            "Engineering time? Engineering DONE.",
        ],
        'next_area': 'island',
    },
}

CHAPTER_REQUIREMENTS = {
    2: {
        'description': 'Selesaikan quest Chapter 1 dan kabur dari area starting',
        'flags':    ['ch1_{char_id}_complete'],  # {char_id} diisi saat runtime
        'items':    [],
        'sidequests_needed': 0,
        'boss_needed': None,
    },
    3: {
        'description': 'Kalahkan Kepala Penjaga (Boss Chapter 2)',
        'flags':    ['boss_ch2_defeated'],
        'items':    [],
        'sidequests_needed': 0,
        'boss_needed': 'kepala_penjaga',
    },
    4: {
        'description': 'Selesaikan minimal 2 sidequest NPC (butuh key item mereka)',
        'flags':    ['boss_ch2_defeated'],
        'items':    [],
        'sidequests_needed': SIDEQUESTS_NEEDED_FOR_CH4,  # 2
        'boss_needed': None,
    },
    5: {
        'description': "Kalahkan Maxwell's Agent (Boss Chapter 4)",
        'flags':    ['boss_ch4_defeated'],
        'items':    [],
        'sidequests_needed': 0,
        'boss_needed': 'agen_maxwell',
    },
    6: {
        'description': 'Selesaikan minimal 4 sidequest + miliki USB Evidence Drive',
        'flags':    ['boss_ch4_defeated'],
        'items':    ['USB Evidence Drive'],
        'sidequests_needed': SIDEQUESTS_NEEDED_FOR_CH6,  # 4
        'boss_needed': None,
    },
}

CHAPTER_LOCATIONS = {
    1: {
        # Ch1: hanya area starting + command_center tidak tersedia
        'vio':      ['mansion'],
        'haikaru':  ['prison_north'],
        'aolinh':   ['theater'],
        'arganta':  ['beach'],
        'ignatius': ['basement', 'mansion'],
    },
    2: {
        'all': ['island', 'prison_north', 'prison_south', 'mansion',
                'dock', 'theater', 'beach', 'basement', 'command_center'],
    },
    3: {
        'all': ['island', 'prison_north', 'prison_south', 'mansion',
                'dock', 'theater', 'beach', 'basement', 'command_center',
                'mansion_west', 'mansion_east'],
    },
    4: {
        'all': ['island', 'prison_north', 'prison_south', 'mansion',
                'dock', 'theater', 'beach', 'basement', 'command_center',
                'mansion_west', 'mansion_east', 'laboratory'],
    },
    5: {
        'all': ['island', 'prison_north', 'prison_south', 'mansion',
                'dock', 'theater', 'beach', 'basement', 'command_center',
                'mansion_west', 'mansion_east', 'laboratory'],
    },
    6: {
        'all': ['island', 'prison_north', 'prison_south', 'mansion',
                'dock', 'theater', 'beach', 'basement', 'command_center',
                'mansion_west', 'mansion_east', 'laboratory'],
    },
}

def get_character_route(char_id):
    # Mengambil konfigurasi route untuk setiap karakter
    """Return route configuration untuk setiap karakter."""
    routes = {
        'vio': {
            'start_location':     'mansion',
            'start_coords':       (12, 3),
            'chapter_1_location': 'mansion',
            'intro': [
                "Kamu terbangun di ruang server mansion.",
                "Layar komputer di depanmu masih menyala.",
                "Ada file terbuka: 'GUEST_LIST.encrypted'",
                "",
                "Skill hacking-mu berguna di sini.",
                "Tapi kamu harus keluar secepatnya!",
            ],
            'starting_items':    ['USB Encrypted', 'Laptop'],
            'special_objective': 'Hack server, kabur dari mansion',
            'difficulty':        'Medium',
            'bonus_stat':        {'attack': +3, 'speed': +2},
        },

        'haikaru': {
            'start_location':     'prison_north',
            'start_coords':       (12, 3),
            'chapter_1_location': 'prison_north',
            'intro': [
                "Kamu terbangun di sel penjara yang dingin.",
                "Sudah 2 minggu kamu mengamati pola penjaga.",
                "47 halaman catatan. 17 posisi guard. 8 blind spot.",
                "",
                "Sekarang jam 5:47 pagi. Shift berganti jam 6:00.",
                "Window 47 detik. Cukup.",
                "Haikaru Fumika tidak pernah salah hitung.",
            ],
            'starting_items':    ['Buku Catatan', 'Pensil'],
            'special_objective': 'Identifikasi blind spot, kabur dari penjara',
            'difficulty':        'Easy',
            'bonus_stat':        {'defense': +5, 'speed': +1},
        },

        'aolinh': {
            'start_location':     'theater',
            'start_coords':       (12, 9),
            'chapter_1_location': 'theater',
            'intro': [
                "Kamu terbangun di atas panggung teater yang gelap.",
                "Biola warisan ibu masih di sampingmu. Earphone biru masih di leher.",
                "Bekas air mata di pipimu belum kering.",
                "",
                "Jiejie-mu... kakakmu... dimana?",
                "Kalian diculik bersama dari Hongkong. Lalu dipisahkan.",
                "音乐给我力量 — Musik memberimu kekuatan. Mari mulai!",
            ],
            'starting_items':    ['Biola', 'Earphone'],
            'special_objective': 'Cari jejak Jiejie, kabur dari theater',
            'difficulty':        'Easy',
            'bonus_stat':        {'max_hp': +8, 'defense': +3},
        },

        'arganta': {
            'start_location':     'beach',
            'start_coords':       (3, 9),
            'chapter_1_location': 'beach',
            'intro': [
                "Kamu terbangun di pantai pulau terkutuk.",
                "Reruntuhan perahu keluargamu... hancur di kejauhan.",
                "'Rescue operation' katanya. Bugiardi. Semua pembohong.",
                "",
                "Il compasso di Nonno masih di sakumu.",
                "'La via è sempre avanti, Amerigo. Jalan selalu ada di depan.'",
                "Suara kakekmu terngiang. Benar, Nonno. Ini bukan akhir.",
                "",
                "Arah barat laut: dermaga. Kesempatanmu kabur.",
                "Per Nonno. Per famiglia. Per la vendetta!",
            ],
            'starting_items':    ['Kompas Nonno Arganta', 'Pisau Lipat'],
            'special_objective': 'Kumpulkan perlengkapan survival, buka jalur dermaga',
            'difficulty':        'Medium',
            'bonus_stat':        {'attack': 4, 'speed': 3},
        },

        'ignatius': {
            'start_location':     'basement',
            'start_coords':       (12, 3),
            'chapter_1_location': 'basement',
            'intro': [
                "Kamu terbangun di ruang elektrik basement.",
                "Panel listrik di depanmu. Generator backup.",
                "Sistem keamanan pulau terhubung ke sini.",
                "",
                "Satu EMP pulse dan semua alarm mati.",
                "Tapi kamu butuh komponen. Cari di sekitar basement.",
                "Engineering time!",
            ],
            'starting_items':    ['Multitool', 'Blueprint'],
            'special_objective': 'Kumpulkan komponen, sabotase alarm sistem',
            'difficulty':        'Hard',
            'bonus_stat':        {'attack': +5, 'defense': +2},
        },
    }
    return routes.get(char_id, routes['haikaru'])


def get_ch1_quest(char_id):
    """Return data quest Chapter 1 untuk karakter yang dipilih."""
    return CH1_QUESTS.get(char_id)

def get_ch1_item_objective(char_id, item_name):
    
    return CH1_ITEM_OBJECTIVE_MAP.get(char_id, {}).get(item_name)

def get_ch1_pre_boss_dialog(char_id, boss_id):
    
    return CH1_PRE_BOSS_DIALOGS.get(char_id, {}).get(boss_id, [])

def init_ch1_quest(game_state):
    # Menginisialisasi quest Chapter 1 ke game_state
    """Inisialisasi quest Chapter 1 ke game_state.active_quests."""
    char_id = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return

    quest_id = f"ch1_{char_id}"
    # Cek sudah ada belum
    for q in game_state.active_quests:
        if q.get('id') == quest_id:
            return

    targets = [obj['desc'] for obj in quest_data['objectives']]
    game_state.add_quest(
        quest_id=quest_id,
        title=quest_data['title'],
        objective=quest_data['description'],
        targets=targets,
        location=quest_data['location'],
        quest_type='main',
    )

def update_ch1_objective(game_state, objective_id, amount=1):
    
    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return False

    obj_flag   = f"ch1_obj_{objective_id}"
    current    = game_state.story_flags.get(obj_flag, 0)
    target_obj = next((o for o in quest_data['objectives'] if o['id'] == objective_id), None)
    if not target_obj:
        return False

    new_val = min(current + amount, target_obj['target'])
    game_state.story_flags[obj_flag] = new_val

    # Sync HUD — pastikan active_quests selalu mencerminkan jumlah objective selesai
    sync_ch1_quest_hud(game_state)

    return check_ch1_complete(game_state)

def check_ch1_objective_progress(game_state, objective_id):
    """Return (current, target) progress untuk satu objective."""
    char_id = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return 0, 1
    obj = next((o for o in quest_data['objectives'] if o['id'] == objective_id), None)
    if not obj:
        return 0, 1
    current = game_state.story_flags.get(f"ch1_obj_{objective_id}", 0)
    return current, obj['target']

def check_ch1_complete(game_state):
    
    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return False

    comp_flag = quest_data['completion_flag']
    if game_state.story_flags.get(comp_flag):
        return True  # Sudah selesai sebelumnya

    # Cek semua objective
    for obj in quest_data['objectives']:
        current = game_state.story_flags.get(f"ch1_obj_{obj['id']}", 0)
        if current < obj['target']:
            return False

    # Semua selesai!
    game_state.story_flags[comp_flag] = True
    game_state.story_flags['chapter_1_complete'] = True

    # Fix: Ao Linh Drop — gunakan add_quest_item agar tidak duplikat
    reward = quest_data.get('reward_item')
    reward_flag = quest_data.get('reward_flag')
    if reward and not game_state.story_flags.get(reward_flag):
        game_state.add_item(reward)  # add_item auto-route ke add_quest_item jika quest item
        if reward_flag:
            game_state.story_flags[reward_flag] = True

    # Complete quest di active_quests
    quest_id = f"ch1_{char_id}"
    game_state.complete_quest(quest_id)

    return True

def sync_ch1_quest_hud(game_state):
    
    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return
    quest_id = f"ch1_{char_id}"
    completed = sum(
        1 for obj in quest_data['objectives']
        if game_state.story_flags.get(f"ch1_obj_{obj['id']}", 0) >= obj['target']
    )
    for q in game_state.active_quests:
        if q.get('id') == quest_id:
            q['progress'] = completed
            q['total']    = len(quest_data['objectives'])
            break

def get_ch1_objective_status(game_state):
    
    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return []
    result = []
    for obj in quest_data['objectives']:
        cur  = game_state.story_flags.get(f"ch1_obj_{obj['id']}", 0)
        done = cur >= obj['target']
        obj_type = obj.get('type', 'interact')
        result.append((obj['id'], obj['desc'], cur, obj['target'], done, obj_type))
    return result

def get_ch1_next_incomplete_objective(game_state):
    """Return (obj_id, obj_def) objective Ch1 pertama yang belum selesai, atau None."""
    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return None, None
    for obj in quest_data['objectives']:
        cur = game_state.story_flags.get(f"ch1_obj_{obj['id']}", 0)
        if cur < obj['target']:
            return obj['id'], obj
    return None, None

CH1_OBJECTIVE_COMPLETE_DIALOGS = {
    'vio': {
        'hack_terminal': [
            "Vio: Terminal berhasil ditembus. Data jaringan mulai terbuka.",
            "Vio: *menutup laptop sebentar* Oke. Tinggal satu hal lagi.",
        ],
        'defeat_maxwell_enforcer': [
            "Vio: Maxwell Enforcer down. Server room bersih.",
            "Vio: *menghembuskan napas* Ada exploit-nya kan. Selalu ada.",
        ],
    },
    'haikaru': {
        'find_blind_spots': [
            "Haikaru: Semua blind spot terkonfirmasi. Peta mental diperbarui.",
            "Haikaru: Efisiensi rute naik 23%. Sesuai proyeksi.",
        ],
        'find_wingc_key': [
            "Haikaru: Kunci Wing-C. Bagian yang hilang dari kalkulasi awal.",
            "Haikaru: *mengangguk* Sekarang satu obstacle tersisa: Warden Elite.",
        ],
        'defeat_warden_elite': [
            "Haikaru: Warden Elite dinetralkan. Waktu: tepat sesuai kalkulasi.",
            "Haikaru: *mengangguk singkat* Probabilitas keberhasilan: 100%. Sesuai.",
        ],
    },
    'aolinh': {
        'find_jiejie_clues': [
            "Aolinh: Aku menemukan jejaknya! Jiejie pernah ada di sini!",
            "Aolinh: *memeluk biola* 我找到了！ Dia masih di pulau ini!",
        ],
        'defeat_theater_master': [
            "Aolinh: Theater Master sudah kalah. Backstage terbuka!",
            "Aolinh: ♪ Jiejie... tunggu aku, Aolinh sudah dekat ♪",
        ],
    },
    'arganta': {
        'collect_survival_kit': [
            "Arganta: Perlengkapan terkumpul. Nonno akan setuju dengan ini.",
            "Arganta: *menggenggam kompas* Per famiglia. Satu lagi.",
        ],
        'defeat_harbor_captain': [
            "Arganta: Harbor Captain dilumpuhkan. Dermaga sekarang milikku.",
            "Arganta: La via è sempre avanti. *melihat kapal di kejauhan*",
        ],
    },
    'ignatius': {
        'collect_emp_parts_ch1': [
            "Ignatius: Semua komponen terkumpul! EMP prototype siap dirakit!",
            "Ignatius: *mata berbinar* Engineering time dimulai sekarang.",
        ],
        'sabotage_alarm_panel': [
            "Ignatius: Panel alarm berhasil disabotase. 30% sistem keamanan offline.",
            "Ignatius: *mengelap tangan* Tinggal satu: AmBOTukam Mk II.",
        ],
        'defeat_security_bot': [
            "Ignatius: AmBOTukam Mk II dihancurkan dengan EMP-nya sendiri. PERFECT.",
            "Ignatius: *tertawa kecil* Kamu jaga generator. Aku pakein generatormu untuk matiin kamu.",
        ],
    },
}

CH1_NEXT_OBJECTIVE_DIALOGS = {
    'vio': {
        'defeat_maxwell_enforcer': [
            "Vio: Maxwell Enforcer masih menghalangi jalan keluar...",
            "Vio: Former special forces. Bisa bunuh dengan tangan kosong.",
            "Vio: *mengepalkan tangan* Semua boss ada exploit-nya. Temukan polanya.",
        ],
    },
    'haikaru': {
        'find_wingc_key': [
            "Haikaru: Ada kunci tersembunyi di Wing-C. Di balik panel listrik ketiga.",
            "Haikaru: Aku sudah kalkulasi posisinya. Estimasi waktu pengambilan: 8 detik.",
        ],
        'defeat_warden_elite': [
            "Haikaru: Warden Elite memblokir pintu keluar. Reaksi 0.3 detik. Jangkauan 2.1m.",
            "Haikaru: Sudah ada tiga skenario untuk ini. Skenario A: konfrontasi langsung. Efisiensi 73%.",
        ],
    },
    'aolinh': {
        'defeat_theater_master': [
            "Aolinh: Theater Master menghalangi backstage... Yang mengurung Jiejie di sini.",
            "Aolinh: *mencengkeram biola* 妈妈... 给我力量。 Aku tidak akan lari.",
        ],
    },
    'arganta': {
        'defeat_harbor_captain': [
            "Arganta: Harbor Captain berdiri di ujung dermaga. Yang menghalangi jalan pulang.",
            "Arganta: *memegang kompas* Niente è reale, tutto è lecito. Per Nonno.",
        ],
    },
    'ignatius': {
        'sabotage_alarm_panel': [
            "Ignatius: Masih ada panel alarm utama yang perlu disabotase.",
            "Ignatius: Lokasi: sudut barat basement. Kalau itu mati, seluruh sistem alarm padam.",
        ],
        'defeat_security_bot': [
            "Ignatius: AmBOTukam Mk II masih aktif dan menjaga generator utama.",
            "Ignatius: *menyiapkan EMP prototype* Kamu jaga generator aku? Aku pakai generatormu untuk matiin kamu.",
        ],
    },
}

def get_ch1_objective_complete_dialog(char_id, obj_id):
    """Return list dialog setelah objective selesai. Empty list jika tidak ada."""
    return CH1_OBJECTIVE_COMPLETE_DIALOGS.get(char_id, {}).get(obj_id, [])

def get_ch1_next_objective_dialog(char_id, next_obj_id):
    """Return list dialog intro untuk objective berikutnya. Empty list jika tidak ada."""
    return CH1_NEXT_OBJECTIVE_DIALOGS.get(char_id, {}).get(next_obj_id, [])

def display_ch1_completion(game_state):
    """Tampilkan teks penyelesaian Ch1 dan transisi ke Ch2."""
    from utils import clear_screen, wait_input, separator

    char_id    = game_state.player_character
    quest_data = get_ch1_quest(char_id)
    if not quest_data:
        return

    clear_screen()
    separator('═')
    print(f"{Warna.HIJAU + Warna.TERANG}  CHAPTER 1 SELESAI!{Warna.RESET}".center(70))
    separator('═')
    print()
    for line in quest_data.get('completion_text', []):
        print(f"  {Warna.KUNING}{line}{Warna.RESET}")
        time.sleep(0.4)
    print()
    reward = quest_data.get('reward_item')
    if reward:
        print(f"  {Warna.HIJAU}[ ITEM DIDAPAT ]{Warna.RESET} {reward}")
    print()
    separator()
    wait_input("Tekan ENTER untuk lanjut ke Chapter 2... ")
    # Auto-advance chapter so the game immediately recognizes Ch2 is available
    try:
        game_state.story_flags['current_chapter'] = 2
        game_state.story_flags['ch2_bosses_available'] = True
        # Keep only side quests in active_quests (main quest completed)
        game_state.active_quests = [q for q in game_state.active_quests if q.get('quest_type') == 'side']
    except Exception:
        pass


def get_current_chapter(game_state):
    """Return current chapter sebagai int."""
    try:
        return int(game_state.story_flags.get('current_chapter', 1))
    except (ValueError, TypeError):
        return 1

def check_chapter_unlock(game_state, target_chapter):
    
    if target_chapter > MAX_CHAPTERS:
        return False, "Chapter tidak ada."

    char_id = game_state.player_character
    reqs = CHAPTER_REQUIREMENTS.get(target_chapter, {})
    reasons = []

    # Cek story flags
    for flag_template in reqs.get('flags', []):
        flag = flag_template.replace('{char_id}', char_id)
        if not game_state.story_flags.get(flag):
            reasons.append(f"Flag belum terpenuhi: {flag}")

    # Cek items
    for item in reqs.get('items', []):
        if item not in game_state.inventory:
            reasons.append(f"Item belum ada: {item}")

    # Cek sidequests
    needed = reqs.get('sidequests_needed', 0)
    done   = game_state.story_flags.get('sidequests_completed', 0)
    if done < needed:
        reasons.append(f"Sidequest kurang: {done}/{needed} selesai")

    # Cek boss
    boss_id = reqs.get('boss_needed')
    if boss_id:
        boss_data = BOSS_DATA.get(boss_id, {})
        flag_key  = boss_data.get('flag_key', '')
        if flag_key and not game_state.story_flags.get(flag_key):
            reasons.append(f"Boss belum dikalahkan: {boss_data.get('name', boss_id)}")

    if reasons:
        return False, " | ".join(reasons)
    return True, "OK"

def advance_chapter(game_state):
    """Maju ke chapter berikutnya. Return True jika berhasil."""
    current = get_current_chapter(game_state)
    if current >= MAX_CHAPTERS:
        return False
    target = current + 1
    can, reason = check_chapter_unlock(game_state, target)
    if can:
        game_state.story_flags['current_chapter'] = target
        return True
    return False

def check_chapter_complete(game_state):
    
    chapter = get_current_chapter(game_state)
    char_id = game_state.player_character

    if chapter == 1:
        return game_state.story_flags.get('chapter_1_complete', False)
    else:
        target = chapter + 1
        if target > MAX_CHAPTERS:
            return game_state.story_flags.get('boss_ch6_defeated', False)
        can, _ = check_chapter_unlock(game_state, target)
        return can

def get_chapter_progress_info(game_state):
    
    chapter = get_current_chapter(game_state)
    char_id = game_state.player_character

    info = {
        'chapter':    chapter,
        'objective':  CHAPTER_OBJECTIVES.get(chapter, ""),
        'is_boss_chapter': chapter in BOSS_CHAPTERS,
        'boss_name':  None,
        'boss_done':  False,
        'next_unlock_reason': "",
        'can_advance': False,
    }

    if chapter in BOSS_CHAPTERS:
        boss_id   = CHAPTER_BOSSES.get(chapter)
        boss_data = BOSS_DATA.get(boss_id, {})
        info['boss_name'] = boss_data.get('name', '???')
        info['boss_done'] = game_state.story_flags.get(boss_data.get('flag_key', ''), False)

    target = chapter + 1
    if target <= MAX_CHAPTERS:
        can, reason = check_chapter_unlock(game_state, target)
        info['can_advance']        = can
        info['next_unlock_reason'] = "" if can else reason
    else:
        info['can_advance'] = game_state.story_flags.get('boss_ch6_defeated', False)

    return info


def display_route_intro(char_id):
    """Tampilkan intro awal Chapter 1 untuk karakter yang dipilih."""
    from utils import clear_screen, wait_input, separator

    route = get_character_route(char_id)
    clear_screen()
    separator('═')
    display_name = "AMERIGO ARGANTA" if char_id == 'arganta' else char_id.upper()
    print(f"{Warna.HIJAU + Warna.TERANG}CHAPTER 1 DIMULAI — {display_name}{Warna.RESET}".center(70))
    separator('═')
    print()
    for line in route['intro']:
        if line:
            print(f"  {Warna.KUNING}{line}{Warna.RESET}")
        else:
            print()
    print()
    separator()
    print(f"  {Warna.CYAN}Objektif: {route['special_objective']}{Warna.RESET}")
    print(f"  {Warna.ABU_GELAP}Kesulitan: {route['difficulty']}{Warna.RESET}")
    separator()
    print()
    wait_input()

def apply_route_bonuses(game_state, char_id):
    # Menerapkan bonus stat dan item sesuai rute karakter
    """Apply stat dan item bonuses sesuai rute karakter. Dipanggil sekali saat new game."""
    if game_state.story_flags.get('route_bonuses_applied'):
        return game_state

    route   = get_character_route(char_id)
    bonuses = route.get('bonus_stat', {})

    if 'max_hp' in bonuses:
        game_state.max_hp += bonuses['max_hp']
        game_state.hp = min(game_state.hp + bonuses['max_hp'], game_state.max_hp)
    if 'attack'  in bonuses: game_state.attack  += bonuses['attack']
    if 'defense' in bonuses: game_state.defense += bonuses['defense']
    if 'speed'   in bonuses: game_state.speed   += bonuses['speed']

    for item in route.get('starting_items', []):
        if item not in game_state.inventory:
            game_state.add_item(item)

    game_state.current_location = route.get('chapter_1_location', 'island')
    if coords := route.get('start_coords'):
        game_state.story_flags['start_x'] = coords[0]
        game_state.story_flags['start_y'] = coords[1]

    game_state.story_flags['route_bonuses_applied'] = True
    game_state.story_flags['current_chapter']       = 1
    game_state.story_flags['sidequests_completed']  = 0
    return game_state

def get_chapter_locations(chapter):
    
    return CHAPTER_LOCATIONS.get(chapter, CHAPTER_LOCATIONS.get(2, {}))

def can_access_location(char_id, location, chapter):
    """Cek apakah karakter bisa akses lokasi di chapter saat ini."""
    chapter_data = CHAPTER_LOCATIONS.get(chapter, CHAPTER_LOCATIONS[2])
    if chapter == 1:
        allowed = chapter_data.get(char_id, [])
    else:
        allowed = chapter_data.get('all', [])
    return location in allowed

def get_boss_for_current_chapter(game_state):
    """Return boss_id jika chapter saat ini adalah boss chapter, else None."""
    chapter = get_current_chapter(game_state)
    return CHAPTER_BOSSES.get(chapter)

def mark_boss_defeated(game_state, boss_id):
    """Tandai boss sebagai sudah dikalahkan dan update bosses_defeated count."""
    boss_data = BOSS_DATA.get(boss_id, {})
    flag_key  = boss_data.get('flag_key', '')
    if flag_key:
        game_state.story_flags[flag_key] = True
    game_state.bosses_defeated = game_state.bosses_defeated + 1
    # Berikan reward item jika ada
    reward = boss_data.get('reward_item')
    if reward and reward not in game_state.inventory:
        game_state.add_item(reward)
    return boss_data

def get_npc_display_name(npc_id):
    """Nama tampilan NPC (wrapper ke npc_interactions jika tersedia)."""
    names = {
        'haikaru':  'Haikaru Fumika',
        'aolinh':   'Ao Lin',
        'arganta':  'Amerigo Arganta',
        'ignatius': 'Ignatius Forgers',
        'vio':      'Vio',
    }
    return names.get(npc_id, npc_id.capitalize())

def check_candala_encounter(game_state):
    
    chapter = int(game_state.story_flags.get('current_chapter', 1))
    if chapter < 2:
        return

    battles = game_state.battles_won
    already_met = game_state.story_flags.get('candala_encountered', False)
    if not already_met and battles >= 5 and chapter >= 2:
        # Trigger dialog misterius
        game_state.story_flags['candala_encountered'] = True
        try:
            from sprites import Warna
            import time
            print(f"\n  {Warna.UNGU}*Sebuah pesan muncul di layar terdekat...{Warna.RESET}")
            time.sleep(0.5)
            print(f"  {Warna.UNGU + Warna.TERANG}??? : \"Kamu lebih jauh dari yang mereka kira. Hati-hati.\"{Warna.RESET}")
            time.sleep(1.5)
        except Exception:
            pass
