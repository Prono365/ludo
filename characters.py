from sprites import Warna
import random
import json
import os
from contextlib import suppress
from constants import FALLBACK_CARD_DIALOGS

def _load_card_dialogs():
    """Muat CARD_PLAY_DIALOGS dari card_dialogs.json dengan validasi ketat."""

    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _candidates = [
        os.path.join(_this_dir, "card_dialogs.json"),
        os.path.join(os.getcwd(), "card_dialogs.json"),
    ]

    for _path in _candidates:
        if os.path.exists(_path):
            try:
                with open(_path, "r", encoding="utf-8") as _f:
                    _raw = json.load(_f)

                # Validate structure: should be dict with character -> hand_type -> dialogs array
                if not isinstance(_raw, dict):
                    raise TypeError(f"card_dialogs.json harus dict, bukan {type(_raw).__name__}")
                
                # Validate that we have character entries with dialog arrays
                _valid_dialogs = {}
                for char_id, hand_dialogs in _raw.items():
                    if not char_id.startswith("_") and isinstance(hand_dialogs, dict):
                        # This is a valid character entry
                        _valid_dialogs[char_id] = hand_dialogs

                if _valid_dialogs:
                    return _valid_dialogs
                # If no valid dialogs found, fall through to fallback
                print(f"⚠️  WARNING: card_dialogs.json tidak memiliki dialog valid di {_path}")
                break
                
            except json.JSONDecodeError as _e:
                print(f"⚠️  WARNING: card_dialogs.json memiliki JSON syntax error: {_e}")
                print(f"           Gunakan fallback dialogs untuk mencegah NPC bisu.")
                break
            except (OSError, TypeError, ValueError) as _e:
                print(f"⚠️  WARNING: card_dialogs.json error ({type(_e).__name__}): {_e}")
                break

    # Fallback ke FALLBACK_CARD_DIALOGS jika terjadi masalah
    print("   Menggunakan fallback dialogs.")
    return FALLBACK_CARD_DIALOGS.copy()

CARD_PLAY_DIALOGS = _load_card_dialogs()

PLAYABLE_CHARACTERS = {
    "vio": {
        "name": "Vio",
        "title": "Gacha Whale & Crypto Expert",
        "age": 13,
        "gender": "Male",
        "desc": "Whaler game mobile gacha dan ahli enkripsi sistem",
        "sprite": ("♂♂", Warna.MERAH + Warna.TERANG, ""),
        "stats": {
            "hp": 88,
            "attack": 16,
            "defense": 11,
            "speed": 21
        },
        "skills": {
            "system_hack": {
                "name": "System Hack",
                "type": "debuff",
                "power": 0,
                "cost": 6,
                "energy_cost": 6,
                "cooldown": 3,
                "duration_turns": 3,
                "desc": "Hack sistem pertahanan musuh: DEF musuh -50% selama 3 turn | CD: 3 turn",
                "effect": "debuff_defense",
                "target": "enemy",
                "level_bonus": 5
            },
            "signal_jam": {
                "name": "Signal Jam",
                "type": "debuff",
                "power": 0,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 3,
                "duration_turns": 3,
                "desc": "Jamming sinyal serangan: ATK musuh -40% selama 3 turn | CD: 3 turn",
                "effect": "debuff_attack",
                "target": "enemy",
                "level_bonus": 5
            },
            "gacha_fortune": {
                "name": "Gacha Fortune",
                "type": "special",
                "power": 0,
                "cost": 3,
                "energy_cost": 3,
                "cooldown": 4,
                "duration_turns": 3,
                "desc": "RNG blessed! Random: ATK buff 3t / DEF buff 3t / Heal HP / Regen Energy | CD: 4 turn",
                "effect": "gacha_buff",
                "target": "self",
                "level_bonus": 5
            },
            "data_overload": {
                "name": "Data Overload",
                "type": "special",
                "power": 0,
                "cost": 7,
                "energy_cost": 7,
                "cooldown": 3,
                "duration_turns": 1,
                "desc": "Injeksi data berlebih: kartu berikutnya damage ×2 + debuff DEF musuh -30% | CD: 3 turn",
                "effect": "buff_card_power",
                "target": "self",
                "level_bonus": 0
            }
        },
        "backstory": "Jenius coding dari Edinburgh, Skotlandia. Sejak usia 10 tahun sudah memenangkan berbagai kompetisi pemrograman tingkat UK. Diculik setelah secara tidak sengaja membobol jaringan keuangan Epstein saat mengikuti CTF challenge online. Meski terjebak, tetap menyembunyikan HP gaming di balik lapisan seragam penjara untuk 'daily login' gacha.",
        "passive": "Gacha Luck: 25% chance untuk double damage atau heal berkat RNG god",
        "starting_location": "mansion",
        "nationality": "Scottish",
        "hometown": "Edinburgh, Skotlandia",
        "personality": "Tenang, analitis, sedikit addict gacha, sarkastik, bangga pada asal Skotlandia",
        "hobby": "Main gacha game, collect SSR characters, CTF hacking competition, flexing pull",
        "favorite_quote": "Pity system is for casuals. True whale goes all-in!",

        "card_dialogs": CARD_PLAY_DIALOGS.get("vio", {})
    },
    
    "haikaru": {
        "name": "Haikaru Fumika",
        "title": "Strategic Observer",
        "age": 12,
        "gender": "Female",
        "desc": "Pengamat tajam dari Kyoto dengan photographic memory dan analisis sempurna",
        "sprite": ("♀♀", Warna.CYAN + Warna.TERANG, ""),
        "stats": {
            "hp": 92,
            "attack": 13,
            "defense": 16,
            "speed": 19
        },
        "skills": {
            "pattern_analysis": {
                "name": "Pattern Analysis",
                "type": "debuff",
                "power": 0,
                "cost": 6,
                "energy_cost": 6,
                "cooldown": 3,
                "duration_turns": 2,
                "desc": "Analisis kelemahan musuh: DEF -35% + ATK -20% selama 2 turn | CD: 3 turn",
                "effect": "debuff_def_atk",
                "target": "enemy",
                "level_bonus": 5
            },
            "focus_mind": {
                "name": "Focus Mind",
                "type": "buff",
                "power": 0,
                "cost": 4,
                "energy_cost": 4,
                "cooldown": 2,
                "duration_turns": 2,
                "desc": "Konsentrasi penuh: ATK diri sendiri +55% selama 2 turn | CD: 2 turn",
                "effect": "buff_attack",
                "target": "self",
                "level_bonus": 5
            },
            "gambit": {
                "name": "Strategic Gambit",
                "type": "special",
                "power": 0,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 4,
                "duration_turns": 2,
                "desc": "Korbankan 20 HP → ATK +65% selama 2 turn + +30 Energy | CD: 4 turn",
                "effect": "power_up",
                "target": "self",
                "level_bonus": 5
            },
            "four_card_read": {
                "name": "Four-Card Read",
                "type": "special",
                "power": 0,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 3,
                "duration_turns": 1,
                "desc": "Analisis pola: hand berikutnya bisa Straight dengan 4 kartu saja | CD: 3 turn",
                "effect": "buff_four_straight",
                "target": "self",
                "level_bonus": 5
            }
        },
        "backstory": "Putri sulung keluarga akademisi dari Kyoto, Jepang. Fumika adalah juara olimpiade matematika tingkat nasional di usia 11 tahun dengan IQ 162 dan photographic memory yang tidak pernah gagal. Diculik ketika secara tidak sengaja menyaksikan transaksi mencurigakan antara anggota jaringan Epstein dan seorang pejabat tinggi di airport Kansai. Selama 2 minggu di pulau, tidak panik — justru mengisi buku catatannya dengan pola penjaga, blind spot CCTV, dan tiga rencana pelarian berlapis.",
        "passive": "Keen Eye: Selalu tahu hand musuh & +20% crit chance",
        "starting_location": "island",
        "nationality": "Japanese",
        "hometown": "Kyoto, Jepang",
        "personality": "Serius, perfeksionis, dingin tapi protektif, sedikit tsundere pada yang dianggap 'kurang efisien'",
        "hobby": "Catur, mencatat pola, membuat strategi berlapis, puzzle logika, origami sebagai meditasi",
        "favorite_quote": "Semua sistem punya celah. Saya hanya perlu 2.7 detik untuk menemukannya.",
        "card_dialogs": CARD_PLAY_DIALOGS.get("haikaru", {})
    },
    
    "aolinh": {
        "name": "Ao Lin",
        "title": "Cheerful Healer & Music Lover",
        "age": 10,
        "gender": "Female",
        "desc": "Gadis ceria dari Chengdu yang musiknya bisa menyembuhkan jiwa",
        "sprite": ("♀♀", Warna.UNGU + Warna.TERANG, ""),
        "stats": {
            "hp": 88,
            "attack": 11,
            "defense": 13,
            "speed": 17
        },
        "skills": {
            "healing_melody": {
                "name": "Healing Melody",
                "type": "heal",
                "power": 45,
                "cost": 6,
                "energy_cost": 6,
                "cooldown": 3,
                "desc": "Melodi penyembuh: pulihkan 40-60 HP diri sendiri | CD: 3 turn",
                "effect": "heal_self",
                "target": "self",
                "level_bonus": 8
            },
            "harmonic_shield": {
                "name": "Harmonic Shield",
                "type": "buff",
                "power": 0,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 3,
                "duration_turns": 3,
                "desc": "Perisai harmoni: DEF diri sendiri +50% selama 3 turn | CD: 3 turn",
                "effect": "buff_defense",
                "target": "self",
                "level_bonus": 5
            },
            "rhythm_boost": {
                "name": "Rhythm Boost",
                "type": "buff",
                "power": 0,
                "cost": 4,
                "energy_cost": 4,
                "cooldown": 3,
                "duration_turns": 3,
                "desc": "Irama semangat: ATK +35% selama 3 turn + pulihkan 20 HP | CD: 3 turn",
                "effect": "buff_atk_heal",
                "target": "self",
                "level_bonus": 5
            },
            "discard_rhythm": {
                "name": "Discard Rhythm",
                "type": "special",
                "power": 0,
                "cost": 4,
                "energy_cost": 4,
                "cooldown": 3,
                "desc": "Irama baru: pulihkan 1 slot discard + langsung draw 2 kartu tambahan | CD: 3 turn",
                "effect": "refresh_discard",
                "target": "self",
                "level_bonus": 0
            }
        },
        "backstory": "Gadis berhati besar dari Chengdu, Sichuan, China. Belajar biola sejak usia 4 tahun di bawah bimbingan Jiejie (kakak perempuannya) yang juga seorang pemain biola berbakat. Keduanya diculik saat mengikuti turnamen musik internasional di Hongkong. Meski ketakutan, Ao Lin tetap memegang biola dan earphone birunya sebagai penghubung keberanian — karena musik ibunya selalu bilang adalah jembatan antara hati yang hancur dan dunia yang lebih baik.",
        "passive": "Musical Spirit: Heal +25% effectiveness & party morale boost (+10% all stats)",
        "starting_location": "prison_south",
        "nationality": "Chinese",
        "hometown": "Chengdu, Sichuan, China",
        "personality": "Ceria, optimis, penyayang, pemberani saat terdesak, sesekali bicara Mandarin saat emosional",
        "hobby": "Biola, mendengarkan musik erhu & pop Cina, memasak masakan Sichuan, membuat playlist, dance",
        "favorite_quote": "音乐能让世界变得更美好！ Musik bisa membuat dunia lebih indah!",
        "favorite_music": "Erhu klassik, C-Pop, Anime OST, EDM",
        "card_dialogs": CARD_PLAY_DIALOGS.get("aolinh", {})
    },
    
    "arganta": {
        "name": "Amerigo Arganta",
        "title": "Pathfinder Scout",
        "age": 13,
        "gender": "Male",
        "desc": "Navigator Italia dan scout dengan insting survival tajam",
        "sprite": ("♂♂", Warna.PUTIH + Warna.TERANG, ""),
        "stats": {
            "hp": 87,
            "attack": 19,
            "defense": 11,
            "speed": 24
        },
        "skills": {
            "shadow_step": {
                "name": "Shadow Step",
                "type": "buff",
                "power": 0,
                "cost": 3,
                "energy_cost": 3,
                "cooldown": 2,
                "duration_turns": 1,
                "desc": "Satu langkah ke bayangan: 70% dodge serangan musuh giliran ini | CD: 2 turn",
                "effect": "buff_evade",
                "target": "self",
                "level_bonus": 5
            },
            "survival_instinct": {
                "name": "Survival Instinct",
                "type": "heal",
                "power": 25,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 2,
                "desc": "Insting bertahan: pulihkan 25 HP + regen 25 Energy | CD: 2 turn",
                "effect": "heal_energy",
                "target": "self",
                "level_bonus": 4
            },
            "scout_mark": {
                "name": "Scout Mark",
                "type": "debuff",
                "power": 0,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 3,
                "duration_turns": 3,
                "desc": "Tandai target: ATK musuh -45% selama 3 turn | CD: 3 turn",
                "effect": "debuff_attack",
                "target": "enemy",
                "level_bonus": 5
            },
            "ambush_strike": {
                "name": "Ambush Strike",
                "type": "special",
                "power": 0,
                "cost": 6,
                "energy_cost": 6,
                "cooldown": 4,
                "duration_turns": 1,
                "desc": "Keluar dari bayangan: kartu berikutnya ×2 damage + STUN musuh 1 turn! | CD: 4 turn",
                "effect": "buff_ambush",
                "target": "self",
                "level_bonus": 0
            }
        },
        "backstory": "Putra keluarga pelaut dari Napoli, Italia. Kakeknya adalah navigator legendaris di Laut Mediterania yang mewariskan kompas antik bertuliskan 'La via è sempre avanti'. Keluarganya berlayar ke Karibia untuk lomba layar internasional ketika perahu mereka dihancurkan oleh anak buah Epstein yang menyamar sebagai tim penyelamat. Tumbuh dengan kisah-kisah leluhur Italia — termasuk legenda Assassini kuno yang katanya pernah beroperasi dari Napoli hingga Firenze — Amerigo percaya bahwa kebenaran selalu bisa ditemukan di balik kepalsuan, dan keadilan harus diperjuangkan sendiri jika sistem gagal.",
        "passive": "Scout's Instinct: First strike dalam combat & +25% evasion",
        "starting_location": "island",
        "nationality": "Italian",
        "hometown": "Napoli, Italia",
        "personality": "Mandiri, resourceful, penuh dendam yang terkendali, bangga akan warisan Italia, sesekali berbisik kata-kata Assassini kuno sebagai mantra",
        "hobby": "Navigasi bintang, peta tangan, parkour di gang-gang Napoli, membaca sejarah assassini Italia, mempertajam pisau lipat",
        "favorite_quote": "Niente è reale, tutto è lecito. La via è sempre avanti.",
        "card_dialogs": CARD_PLAY_DIALOGS.get("arganta", {})
    },
    
    "ignatius": {
        "name": "Ignatius",
        "title": "Engineer Prodigy",
        "age": 12,
        "gender": "Male",
        "desc": "Teknisi jenius dengan gadget DIY yang powerful",
        "sprite": ("♂♂", Warna.KUNING + Warna.TERANG, ""),
        "stats": {
            "hp": 85,
            "attack": 22,
            "defense": 9,
            "speed": 16
        },
        "skills": {
            "emp_stun": {
                "name": "EMP Stun",
                "type": "special",
                "power": 0,
                "cost": 3,
                "energy_cost": 3,
                "cooldown": 4,
                "duration_turns": 1,
                "desc": "Pulse elektromagnetik: musuh di-stun, skip serangan 1 turn | CD: 4 turn",
                "effect": "stun_enemy",
                "target": "enemy",
                "level_bonus": 0
            },
            "overclock": {
                "name": "Overclock",
                "type": "buff",
                "power": 0,
                "cost": 6,
                "energy_cost": 6,
                "cooldown": 3,
                "duration_turns": 2,
                "desc": "Overclocking sistem: ATK diri sendiri +60% selama 2 turn + regen 12 Energy | CD: 3 turn",
                "effect": "buff_atk_energy",
                "target": "self",
                "level_bonus": 5
            },
            "emergency_repair": {
                "name": "Emergency Repair",
                "type": "heal",
                "power": 40,
                "cost": 2,
                "energy_cost": 2,
                "cooldown": 3,
                "desc": "Perbaikan darurat: pulihkan 40 HP + bersihkan semua debuff | CD: 3 turn",
                "effect": "heal_cleanse",
                "target": "self",
                "level_bonus": 8
            },
            "power_surge": {
                "name": "Power Surge",
                "type": "special",
                "power": 0,
                "cost": 5,
                "energy_cost": 5,
                "cooldown": 3,
                "duration_turns": 1,
                "desc": "Korbankan 15 HP → kartu berikutnya ×2 DAMAGE! (Overload circuit) | CD: 3 turn",
                "effect": "buff_overload",
                "target": "self",
                "level_bonus": 0
            }
        },
        "backstory": "Anak yang bisa memperbaiki dan memodifikasi segala macam mesin sejak umur 8 tahun. Panel listrik dan circuit board adalah mainannya.",
        "passive": "Tech Genius: Skill damage +30% & bisa craft item dari junk",
        "starting_location": "mansion",
        "personality": "Energik, curious, suka eksperimen, kadang ceroboh",
        "hobby": "Modding gadget, robotics, gaming hardware",
        "favorite_quote": "If it runs on electricity, I can hack it or break it!",
        "card_dialogs": CARD_PLAY_DIALOGS.get("ignatius", {})
    }
}

# LEVEL-UP STAT GAINS PER KARAKTER
# Setiap karakter punya distribusi stat unik → level-up gains mencerminkan itu.
#
# Referensi base stats:
#   Vio     : HP 88  ATK 16  DEF 11  SPD 21  → ATK/SPD build
#   Haikaru : HP 92  ATK 13  DEF 16  SPD 19  → DEF/HP build
#   Aolinh  : HP 88  ATK 11  DEF 13  SPD 17  → Support/Energy build
#   Arganta : HP 87  ATK 19  DEF 11  SPD 24  → ATK/SPD glass cannon
#   Ignatius: HP 85  ATK 22  DEF  9  SPD 16  → Pure ATK berserker
# Level-up stat gains per karakter
CHARACTER_LEVEL_GAINS = {
    "vio": {
        # Hacker: cepat & menyerang, tapi tipis
        "hp":      10,  # squishy — HP tumbuh pelan
        "attack":   2,  # solid attacker
        "defense":  1,  # pertahanan rendah tetap rendah
        "speed":    2,  # SPD signature — naik cepat
        "energy":   1,  # energy gain per level — lebih sedikit post-buff
        "note": "ATK/SPD scaling — tetap cepat tapi rapuh",
    },
    "haikaru": {
        # Strategist: tanky, analitis, low attack
        "hp":      14,  # paling tinggi — HP-nya tebal
        "attack":   1,  # ATK rendah tetap rendah
        "defense":  3,  # DEF signature — paling tinggi
        "speed":    1,  # SPD biasa
        "energy":   2,
        "note": "DEF/HP scaling — tank sejati yang tidak mati",
    },
    "aolinh": {
        # Healer: support, energy regen, balanced growth
        "hp":      12,  # sedang
        "attack":   1,  # paling lemah
        "defense":  2,  # sedang
        "speed":    1,  # sedang
        "energy":   2,  # healer energy gain (dikurangi)
        "note": "Energy scaling — skill heal makin kuat tiap level",
    },
    "arganta": {
        # Scout: extreme speed & attack, paper-thin defense
        "hp":       9,  # paling kecil — glass cannon murni
        "attack":   3,  # ATK tinggi signature
        "defense":  1,  # DEF tetap rendah
        "speed":    3,  # SPD tertinggi — la via è sempre avanti
        "energy":   2,
        "note": "ATK/SPD glass cannon — hit hard, move fast, die easy",
    },
    "ignatius": {
        # Engineer: berserker ATK, sangat rapuh
        "hp":       8,  # paling rendah — rapuh banget
        "attack":   4,  # paling tinggi — pure damage
        "defense":  1,  # hampir tidak ada defense growth
        "speed":    1,  # SPD biasa
        "energy":   2,  # energy untuk skill gadget
        "note": "Pure ATK scaling — one-shot king dengan HP tipis",
    },
}

# NPC spesial (Candala)
SPECIAL_NPC = {
    "candala": {
        "name": "Candala",
        "title": "The Wish Granter",
        "age": "???",
        "gender": "Female",
        "desc": "Wanita misterius yang pernah bisa mengabulkan semua permintaan",
        "sprite": ("♀♀", Warna.PUTIH + Warna.TERANG + Warna.DIM, ""),
        "backstory": "Seorang wanita yang dulunya memiliki kutukan sekaligus karunia untuk mengabulkan setiap permintaan yang diucapkan di hadapannya.",
        "dialog": [
            "Candala: ...Anak-anak yang terjebak di pulau terkutuk ini...",
            "Candala: Aku pernah seperti kalian. Terikat oleh takdir yang tidak bisa kulawan.",
            "Candala: Tapi kalian... kalian punya yang tidak pernah kumiliki.",
            "Candala: Kalian punya satu sama lain. Jangan sia-siakan itu.",
            "Candala: *menghilang perlahan seperti kabut* ...Semoga kalian menemukan kebebasan yang kuimpikan..."
        ],
        "encounter_chance": 0.03,
        "location": "special_hidden",
        "can_join": False
    }
}

# QUEST UTAMA PER KARAKTER
# Tiap chapter punya boss unik sesuai karakter.
# Boss ch.3 terakhir selalu Epstein (final boss).
# Quest utama per karakter per chapter
CHARACTER_MAIN_QUESTS = {
    "vio": {
        1: {
            "id":     "vio_ch1_main",
            "title":  "Hack & Escape: Ruang Server Mansion",
            "objective": "Tembus 2 terminal server, kalahkan Maxwell Enforcer",
            "boss_id":   "maxwell_enforcer",
            "boss_name": "Maxwell Enforcer",
            "steps": [
                "Tembus 2 terminal server mansion (Keycard/Laptop/Access Card)",
                "Kalahkan Maxwell Enforcer — kepala keamanan jaringan (Boss Ch.1)",
            ],
            "completion_flag": "vio_ch1_complete",
            "next_chapter_msg": "Data terenkripsi mulai terbuka! Pulau menunggu.",
        },
        2: {
            "id":     "vio_ch2_main",
            "title":  "Dominasi Jaringan — Singkirkan Kepala Penjaga",
            "objective": "Hack 2 terminal pulau, kalahkan Kepala Penjaga di Penjara Utara",
            "boss_id":   "kepala_penjaga",
            "boss_name": "Kepala Penjaga",
            "steps": [
                "Hack 2 terminal jaringan di area pulau (Keycard Level 2)",
                "Pergi ke Penjara Utara (PRISON NORTH)",
                "Kalahkan Kepala Penjaga (Boss Ch.2)",
            ],
            "completion_flag": "boss_ch2_defeated",
            "next_chapter_msg": "Kontrol jaringan pulau diambil alih. Saatnya rekrut sekutu!",
        },
        3: {
            "id":     "vio_ch3_main",
            "title":  "Bangun Aliansi Digital — Rekrut Sekutu",
            "objective": "Selesaikan minimal 2 sidequest NPC untuk akses Chapter 4",
            "steps": [
                "Temui NPC di area pulau (Haikaru, Aolinh, Arganta, Ignatius)",
                "Selesaikan minimal 2 sidequest — kumpulkan key item sekutu",
                "Aliansi terbentuk → Chapter 4 terbuka",
            ],
            "completion_flag": "ch3_sidequests_done",
            "next_chapter_msg": "Aliansi siap. Saatnya infiltrasi laboratorium Maxwell.",
        },
        4: {
            "id":     "vio_ch4_main",
            "title":  "Infiltrasi Lab — Jebol Sistem Maxwell",
            "objective": "Masuk ke laboratorium, decrypt file Maxwell, kalahkan Maxwell's Agent",
            "boss_id":   "agen_maxwell",
            "boss_name":  "Maxwell's Agent",
            "steps": [
                "Masuk ke Laboratorium (exit di pulau utama, Ch.4+)",
                "Gunakan EMP Device dari Ignatius untuk lemahkan sistem keamanan",
                "Kalahkan Maxwell's Agent — penjaga rahasia lab (Boss Ch.4)",
            ],
            "completion_flag": "boss_ch4_defeated",
            "next_chapter_msg": "Lab dikuasai! Kartu akses vault ada di tanganmu.",
        },
        5: {
            "id":     "vio_ch5_main",
            "title":  "Deadman Switch — Kumpulkan Semua Bukti",
            "objective": "Selesaikan 4 sidequest NPC, dapatkan USB Evidence Drive",
            "steps": [
                "Selesaikan minimal 4 sidequest NPC (dari total 5)",
                "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
                "Aktifkan deadman switch — bukti tersimpan aman di cloud",
            ],
            "completion_flag": "ch5_evidence_done",
            "next_chapter_msg": "Deadman switch aktif. Saatnya konfrontasi terakhir.",
        },
        6: {
            "id":     "vio_ch6_main",
            "title":  "The Final Upload — Expose Epstein ke Dunia",
            "objective": "Masuk Mansion Timur, kalahkan Epstein, upload semua bukti",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
                "Hadapi Jeffrey Epstein — Final Boss Ch.6",
                "Upload USB Evidence Drive — expose jaringan kejahatan ke dunia",
            ],
            "completion_flag": "vio_ch6_complete",
        },
    },
    "haikaru": {
        1: {
            "id":     "haikaru_ch1_main",
            "title":  "Escape Analysis: Penjara Utara",
            "objective": "Identifikasi 3 blind spot, ambil Kunci Wing-C, kalahkan Warden Elite",
            "boss_id":   "warden_elite",
            "boss_name": "Warden Elite",
            "steps": [
                "Identifikasi 3 blind spot penjaga (ambil item observasi di penjara)",
                "Ambil Kunci Wing-C dari loker tersembunyi di Wing-C",
                "Kalahkan Warden Elite yang memblokir pintu utama (Boss Ch.1)",
            ],
            "completion_flag": "haikaru_ch1_complete",
            "next_chapter_msg": "Semua kalkulasi tepat. Penjara teratasi. Target: pulau.",
        },
        2: {
            "id":     "haikaru_ch2_main",
            "title":  "Taktik Superioritas — Netralkan Kepala Penjaga",
            "objective": "Petakan 2 posisi baru penjaga, kalahkan Kepala Penjaga",
            "boss_id":   "kepala_penjaga",
            "boss_name": "Kepala Penjaga",
            "steps": [
                "Petakan 2 posisi penjaga baru di pulau (item intel/peta)",
                "Pergi ke Penjara Utara (PRISON NORTH)",
                "Kalahkan Kepala Penjaga dengan strategi optimal (Boss Ch.2)",
            ],
            "completion_flag": "boss_ch2_defeated",
            "next_chapter_msg": "Pulau terkendali. Fase rekrutmen dimulai.",
        },
        3: {
            "id":     "haikaru_ch3_main",
            "title":  "Kalkulasi Aliansi — Rekrut Sekutu Strategis",
            "objective": "Selesaikan minimal 2 sidequest NPC untuk akses Chapter 4",
            "steps": [
                "Temui NPC di area pulau — prioritas berdasarkan probabilitas manfaat",
                "Selesaikan minimal 2 sidequest — kumpulkan key item sekutu",
                "Aliansi terkonfirmasi → Chapter 4 terbuka",
            ],
            "completion_flag": "ch3_sidequests_done",
            "next_chapter_msg": "Aliansi siap. Checkmate Maxwell's Agent berikutnya.",
        },
        4: {
            "id":     "haikaru_ch4_main",
            "title":  "Checkmate Maxwell's Agent — Probabilitas 99.9%",
            "objective": "Analisis kelemahan Maxwell's Agent, kalahkan dengan strategi presisi",
            "boss_id":   "agen_maxwell",
            "boss_name":  "Maxwell's Agent",
            "steps": [
                "Masuk ke Laboratorium (exit di pulau utama, Ch.4+)",
                "Analisis kelemahan Maxwell's Agent via intel EMP Ignatius",
                "Kalahkan Maxwell's Agent — eksekusi skenario terbaik (Boss Ch.4)",
            ],
            "completion_flag": "boss_ch4_defeated",
            "next_chapter_msg": "Checkmate! Lab dikuasai. Satu langkah lagi ke Epstein.",
        },
        5: {
            "id":     "haikaru_ch5_main",
            "title":  "Kumpulkan Variabel Bukti — Persiapkan Strategi Final",
            "objective": "Selesaikan 4 sidequest NPC, dapatkan USB Evidence Drive",
            "steps": [
                "Selesaikan minimal 4 sidequest NPC (dari total 5)",
                "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
                "Semua variabel terkumpul — siap konfrontasi Epstein",
            ],
            "completion_flag": "ch5_evidence_done",
            "next_chapter_msg": "Semua kalkulasi lengkap. Langkah ke-61: checkmate Epstein.",
        },
        6: {
            "id":     "haikaru_ch6_main",
            "title":  "Checkmate — Akhiri Jaringan Epstein",
            "objective": "Masuk Mansion Timur, eksekusi rencana final, kalahkan Epstein",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
                "Hadapi Jeffrey Epstein — eksekusi rencana akhir (Final Boss Ch.6)",
                "Upload USB Evidence Drive — checkmate permanen",
            ],
            "completion_flag": "haikaru_ch6_complete",
        },
    },
    "aolinh": {
        1: {
            "id":     "aolinh_ch1_main",
            "title":  "Melodi Kebebasan: Cari Jejak Jiejie",
            "objective": "Temukan 2 jejak Jiejie, kalahkan Theater Master",
            "boss_id":   "theater_master",
            "boss_name": "Theater Master",
            "steps": [
                "Temukan 2 jejak Jiejie di area theater (item clue di panggung)",
                "Kalahkan Theater Master yang mengurung Jiejie (Boss Ch.1)",
            ],
            "completion_flag": "aolinh_ch1_complete",
            "next_chapter_msg": "Jiejie bebas! 我们一起！ Musik memberi kekuatan untuk maju.",
        },
        2: {
            "id":     "aolinh_ch2_main",
            "title":  "Simfoni Kebebasan — Singkirkan Kepala Penjaga",
            "objective": "Cari lokasi Jiejie di pulau, kalahkan Kepala Penjaga",
            "boss_id":   "kepala_penjaga",
            "boss_name": "Kepala Penjaga",
            "steps": [
                "Cari 2 clue lokasi Jiejie di area pulau",
                "Pergi ke Penjara Utara (PRISON NORTH)",
                "Kalahkan Kepala Penjaga dengan melodi harapan (Boss Ch.2)",
            ],
            "completion_flag": "boss_ch2_defeated",
            "next_chapter_msg": "Jalan terbuka! Kini saatnya membangun tim.",
        },
        3: {
            "id":     "aolinh_ch3_main",
            "title":  "Nyanyikan Harapan — Rekrut Sekutu",
            "objective": "Selesaikan minimal 2 sidequest NPC untuk akses Chapter 4",
            "steps": [
                "Temui NPC di area pulau — sapa dengan melodimu",
                "Selesaikan minimal 2 sidequest — kumpulkan key item sekutu",
                "Tim bersatu → Chapter 4 terbuka",
            ],
            "completion_flag": "ch3_sidequests_done",
            "next_chapter_msg": "Musik menyatukan kita. Saatnya tantang Maxwell.",
        },
        4: {
            "id":     "aolinh_ch4_main",
            "title":  "Melodi Perlawanan — Jebol Lab Maxwell",
            "objective": "Gunakan distraksi musik, kalahkan Maxwell's Agent bersama tim",
            "boss_id":   "agen_maxwell",
            "boss_name":  "Maxwell's Agent",
            "steps": [
                "Masuk ke Laboratorium (exit di pulau utama, Ch.4+)",
                "Gunakan Rekaman Distraksi Aolinh untuk buka celah keamanan",
                "Kalahkan Maxwell's Agent — lawan bersama tim (Boss Ch.4)",
            ],
            "completion_flag": "boss_ch4_defeated",
            "next_chapter_msg": "Lab ditaklukkan! Satu langkah lagi menuju kebebasan.",
        },
        5: {
            "id":     "aolinh_ch5_main",
            "title":  "Kumpulkan Bukti untuk Jiejie — Akhiri Penderitaan Ini",
            "objective": "Selesaikan 4 sidequest NPC, dapatkan USB Evidence Drive",
            "steps": [
                "Selesaikan minimal 4 sidequest NPC (dari total 5)",
                "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
                "Semua bukti tersimpan — siap untuk konfrontasi Epstein",
            ],
            "completion_flag": "ch5_evidence_done",
            "next_chapter_msg": "Bukti untuk Jiejie sudah aman. Musik akan berakhir dengan kemenangan.",
        },
        6: {
            "id":     "aolinh_ch6_main",
            "title":  "Final Crescendo — Kalahkan Epstein untuk Semua Anak",
            "objective": "Masuk Mansion Timur, kalahkan Epstein, nyanyikan lagu kebebasan",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
                "Hadapi Jeffrey Epstein — nyanyikan simfoni terakhirmu (Final Boss Ch.6)",
                "Upload USB Evidence Drive — suara korban akhirnya terdengar dunia",
            ],
            "completion_flag": "aolinh_ch6_complete",
        },
    },
    "arganta": {
        1: {
            "id":     "arganta_ch1_main",
            "title":  "Survival Route: Pantai Karibia",
            "objective": "Kumpulkan 2 perlengkapan survival, kalahkan Harbor Captain",
            "boss_id":   "harbor_captain",
            "boss_name": "Harbor Captain",
            "steps": [
                "Kumpulkan 2 perlengkapan survival (item di area pantai)",
                "Kalahkan Harbor Captain yang menjaga dermaga (Boss Ch.1)",
            ],
            "completion_flag": "arganta_ch1_complete",
            "next_chapter_msg": "Dermaga dikuasai. La via è sempre avanti, Nonno.",
        },
        2: {
            "id":     "arganta_ch2_main",
            "title":  "Navigator Memimpin — Singkirkan Kepala Penjaga",
            "objective": "Scout 2 jalur baru di pulau, kalahkan Kepala Penjaga",
            "boss_id":   "kepala_penjaga",
            "boss_name": "Kepala Penjaga",
            "steps": [
                "Scout 2 jalur pelarian baru di pulau (peta atau item navigasi)",
                "Pergi ke Penjara Utara (PRISON NORTH)",
                "Kalahkan Kepala Penjaga lewat jalur yang kamu petakan (Boss Ch.2)",
            ],
            "completion_flag": "boss_ch2_defeated",
            "next_chapter_msg": "Pulau terpetakan. Saatnya membangun aliansi untuk keadilan.",
        },
        3: {
            "id":     "arganta_ch3_main",
            "title":  "Per Famiglia — Rekrut Sekutu untuk Keadilan",
            "objective": "Selesaikan minimal 2 sidequest NPC untuk akses Chapter 4",
            "steps": [
                "Temui NPC di area pulau — tawarkan bantuan sebagai navigator",
                "Selesaikan minimal 2 sidequest — kumpulkan key item sekutu",
                "Aliansi terbentuk → Chapter 4 terbuka",
            ],
            "completion_flag": "ch3_sidequests_done",
            "next_chapter_msg": "Tim siap. La via è sempre avanti — menuju lab Maxwell.",
        },
        4: {
            "id":     "arganta_ch4_main",
            "title":  "Tembus Lab Maxwell — Per Nonno",
            "objective": "Gunakan jalur tersembunyi, kalahkan Maxwell's Agent",
            "boss_id":   "agen_maxwell",
            "boss_name":  "Maxwell's Agent",
            "steps": [
                "Masuk ke Laboratorium lewat jalur rahasia (exit di pulau Ch.4+)",
                "Gunakan Peta Jalur Rahasia untuk bypass keamanan lab",
                "Kalahkan Maxwell's Agent — per famiglia (Boss Ch.4)",
            ],
            "completion_flag": "boss_ch4_defeated",
            "next_chapter_msg": "Niente è reale. Langkah terakhir: Epstein.",
        },
        5: {
            "id":     "arganta_ch5_main",
            "title":  "Requiescat in Pace — Kumpulkan Semua Bukti",
            "objective": "Selesaikan 4 sidequest NPC, dapatkan USB Evidence Drive",
            "steps": [
                "Selesaikan minimal 4 sidequest NPC (dari total 5)",
                "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
                "Semua bukti untuk keadilan keluarga tersimpan aman",
            ],
            "completion_flag": "ch5_evidence_done",
            "next_chapter_msg": "Nonno... ini untukmu. Saatnya mengakhiri semuanya.",
        },
        6: {
            "id":     "arganta_ch6_main",
            "title":  "Vendetta Finale — Kalahkan Epstein untuk Keluargamu",
            "objective": "Masuk Mansion Timur, kalahkan Epstein, tegakkan keadilan",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
                "Hadapi Jeffrey Epstein — per Nonno, per Papà, per Mamma (Final Boss Ch.6)",
                "Upload USB Evidence Drive — keadilan untuk seluruh keluarga Arganta",
            ],
            "completion_flag": "arganta_ch6_complete",
        },
    },
    "ignatius": {
        1: {
            "id":     "ignatius_ch1_main",
            "title":  "Engineering Breakout: Basement Listrik",
            "objective": "Kumpulkan 3 komponen EMP, sabotase panel alarm, kalahkan AmBOTukam Mk II",
            "boss_id":   "security_bot",
            "boss_name": "AmBOTukam Mk II",
            "steps": [
                "Kumpulkan 3 komponen EMP: Kapasitor Besar, Relay Switch, Copper Coil",
                "Sabotase panel alarm utama basement (gunakan Blueprint/EMP Prototype)",
                "Kalahkan AmBOTukam Mk II dengan EMP prototype (Boss Ch.1)",
            ],
            "completion_flag": "ignatius_ch1_complete",
            "next_chapter_msg": "SISTEM DIRETAS! Generator down. Engineering DONE.",
        },
        2: {
            "id":     "ignatius_ch2_main",
            "title":  "Engineering Bergerak — Kepala Penjaga Harus Disingkirkan",
            "objective": "Lokasi 2 node grid listrik di pulau, kalahkan Kepala Penjaga",
            "boss_id":   "kepala_penjaga",
            "boss_name": "Kepala Penjaga",
            "steps": [
                "Lokasi 2 node jaringan listrik di area pulau (panel/generator)",
                "Pergi ke Penjara Utara (PRISON NORTH)",
                "Kalahkan Kepala Penjaga dengan teknik sabotase (Boss Ch.2)",
            ],
            "completion_flag": "boss_ch2_defeated",
            "next_chapter_msg": "Grid pulau dipetakan. Saatnya rekrut tim engineer.",
        },
        3: {
            "id":     "ignatius_ch3_main",
            "title":  "Tim Engineer — Rekrut Sekutu dengan Keahlian Teknis",
            "objective": "Selesaikan minimal 2 sidequest NPC untuk akses Chapter 4",
            "steps": [
                "Temui NPC di area pulau — tawarkan keahlian teknis",
                "Selesaikan minimal 2 sidequest — kumpulkan key item sekutu",
                "Tim teknis terbentuk → Chapter 4 terbuka",
            ],
            "completion_flag": "ch3_sidequests_done",
            "next_chapter_msg": "Tim siap. EMP berikutnya: laboratorium Maxwell.",
        },
        4: {
            "id":     "ignatius_ch4_main",
            "title":  "EMP Total — Matikan Lab Maxwell dengan Teknologimu",
            "objective": "Gunakan EMP Device di lab, kalahkan Maxwell's Agent",
            "boss_id":   "agen_maxwell",
            "boss_name":  "Maxwell's Agent",
            "steps": [
                "Masuk ke Laboratorium (exit di pulau utama, Ch.4+)",
                "Gunakan EMP Device untuk matikan sistem keamanan lab",
                "Kalahkan Maxwell's Agent — teknologi beats tyranny (Boss Ch.4)",
            ],
            "completion_flag": "boss_ch4_defeated",
            "next_chapter_msg": "Lab offline. Satu sistem terakhir yang harus dimatikan.",
        },
        5: {
            "id":     "ignatius_ch5_main",
            "title":  "Blueprint Keadilan — Kumpulkan Semua Bukti Elektronik",
            "objective": "Selesaikan 4 sidequest NPC, dapatkan USB Evidence Drive",
            "steps": [
                "Selesaikan minimal 4 sidequest NPC (dari total 5)",
                "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
                "Semua bukti elektronik terdokumentasi — blueprint keadilan lengkap",
            ],
            "completion_flag": "ch5_evidence_done",
            "next_chapter_msg": "Blueprint selesai. Saatnya blackout total: Epstein.",
        },
        6: {
            "id":     "ignatius_ch6_main",
            "title":  "Blackout Epstein — Matikan Sistem Terakhirnya Selamanya",
            "objective": "Masuk Mansion Timur, kalahkan Epstein, hancurkan infrastrukturnya",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
                "Hadapi Jeffrey Epstein — engineering vs kejahatan (Final Boss Ch.6)",
                "Upload USB Evidence Drive — blackout total jaringan Epstein",
            ],
            "completion_flag": "ignatius_ch6_complete",
        },
    },
}
# CHAPTER QUEST TEMPLATES — chapter 2-6 shared across characters
# Dipanggil dari _init_location_quests dan _build_main_quest_lines
CHAPTER_QUEST_TEMPLATES = {
    2: {
        "id":        "ch2_main_kepala_penjaga",
        "title":     "Bersihkan Jalan — Kalahkan Kepala Penjaga",
        "objective": "Temukan dan kalahkan Kepala Penjaga di Penjara Utara",
        "steps": [
            "Pergi ke Penjara Utara (PRISON NORTH)",
            "Kalahkan Kepala Penjaga (Boss Ch.2)",
        ],
        "completion_flag": "boss_ch2_defeated",
        "next_chapter_msg": "Kepala Penjaga dikalahkan! Akses penuh ke pulau terbuka.",
    },
    3: {
        "id":        "ch3_main_sidequest",
        "title":     "Bangun Aliansi — Rekrut Sekutu NPC",
        "objective": "Bantu 2 NPC selesaikan sidequest untuk maju ke Ch.4",
        "steps": [
            "Temui NPC di pulau — Haikaru, Aolinh, Arganta, Ignatius, atau Vio",
            "Selesaikan minimal 2 sidequest NPC (kumpulkan key item mereka)",
            "Aliansi terbentuk → Chapter 4 terbuka",
        ],
        "completion_flag": "ch3_sidequests_done",
        "next_chapter_msg": "Aliansi terbentuk! Saatnya infiltrasi laboratorium.",
    },
    4: {
        "id":        "ch4_main_agen_maxwell",
        "title":     "Infiltrasi Laboratorium — Kalahkan Maxwell's Agent",
        "objective": "Masuk ke laboratorium dan kalahkan Maxwell's Agent",
        "steps": [
            "Masuk ke Laboratorium (exit di pulau utama, Ch.4+)",
            "Gunakan EMP Device dari Ignatius untuk melemahkan Maxwell's Agent",
            "Kalahkan Maxwell's Agent — Boss Ch.4",
        ],
        "completion_flag": "boss_ch4_defeated",
        "next_chapter_msg": "Maxwell's Agent dikalahkan! Satu langkah lagi menuju Epstein.",
    },
    5: {
        "id":        "ch5_main_evidence",
        "title":     "Kumpulkan Bukti — Persiapan Konfrontasi Final",
        "objective": "Selesaikan 4 sidequest NPC dan dapatkan USB Evidence Drive",
        "steps": [
            "Selesaikan minimal 4 sidequest NPC (dari total 5)",
            "Berikan USB Security Drive ke Vio → terima USB Evidence Drive",
            "Semua bukti terkumpul — siap konfrontasi Epstein",
        ],
        "completion_flag": "ch5_evidence_done",
        "next_chapter_msg": "Semua bukti terkumpul. Saatnya mengakhiri ini — selamanya.",
    },
    6: {
        "id":        "ch6_main_epstein",
        "title":     "Konfrontasi Final — Hentikan Jeffrey Epstein",
        "objective": "Masuk ke Mansion Timur dan kalahkan Jeffrey Epstein",
        "steps": [
            "Pergi ke Mansion Timur (mansion_east) — exit sudut kanan bawah pulau",
            "Hadapi Jeffrey Epstein — Final Boss Ch.6",
            "Upload USB Evidence Drive — akhiri jaringan kejahatan ini",
        ],
        "completion_flag": "boss_ch6_defeated",
        "next_chapter_msg": "EPSTEIN DIKALAHKAN. Kebenaran terungkap ke dunia.",
    },
}
def get_main_quest(char_id, chapter):
    """Kembalikan data quest utama karakter untuk chapter tertentu."""
    return CHARACTER_MAIN_QUESTS.get(char_id, {}).get(chapter)

# Quest rekrutmen NPC
NPC_QUESTS = {
    "haikaru": {
        "chapter": 2,
        "name": "Buku Catatan yang Disita",
        "desc": "Buku catatan Haikaru berisi 312 halaman analisis enkripsi dan peta blind spot. "
                "Disita penjaga dan disimpan di Guard Station Wing-B penjara utara.",
        "objective": "Kalahkan guard veteran di penjara utara — item drop: Buku Catatan Haikaru",
        "steps": [
            "Pergi ke Penjara Utara (PRISON NORTH)",
            "Temukan guard veteran yang berpatroli di koridor timur laut",
            "Kalahkan guard veteran — Buku Catatan Haikaru akan di-drop",
            "Kembalikan buku ke Haikaru — terima kunci info blind spot",
        ],
        "required_item": "Buku Catatan Haikaru",
        "required_action": None,
        "unlock_location": "prison_north",
        "location": "prison_north",
        "reward_item": "Catatan Sandi Haikaru",
        "reward_dialog": [
            "Fumika: '...Kamu mengambilnya? Hmph. Efisien.'",
            "Fumika: 'Semua data observasiku ada di sini. 17 posisi guard, 8 blind spot, 3 jalur keluar.'",
            "Fumika: 'Aku bergabung dengan timmu. Ikuti rencanaku. Deviasi tidak diperbolehkan.'"
        ]
    },
    "aolinh": {
        "chapter": 2,
        "name": "Biola di Balik Panggung",
        "desc": "Ao Lin dikurung di ruang ganti teater oleh penjaga teater yang keras. "
                "Kalahkan penjaga tersebut untuk membebaskan Ao Lin dan biolanya.",
        "objective": "Kalahkan penjaga teater (backstage) untuk bebaskan Ao Lin",
        "steps": [
            "Pergi ke Teater (THEATER)",
            "Temukan area backstage di balik panggung utama",
            "Kalahkan penjaga teater yang mengurung Ao Lin",
            "Bebaskan Ao Lin — terima Rekaman Distraksi sebagai reward",
        ],
        "required_item": None,
        "required_action": "defeat_theater_guard",
        "unlock_location": "theater",
        "location": "theater",
        "reward_item": "Rekaman Distraksi Aolinh",
        "reward_dialog": [
            "Ao Lin: '*memeluk biola-nya* 谢谢！ Xiè xie! Makasih banget!'",
            "Ao Lin: 'Aku harus cari Jiejie-ku — kakakku. Tapi sendirian aku tidak berani.'",
            "Ao Lin: 'Aku ikut sama kamu ya? 我们一起！ Kita bersama! Let's stay positive! ♪'"
        ]
    },
    "arganta": {
        "chapter": 2,
        "name": "Kompas yang Hilang",
        "desc": "Amerigo Arganta terjebak di pantai tanpa kompas warisan kakeknya. "
                "Kompas diambil penjaga dermaga dan tersimpan di sudut barat pantai.",
        "objective": "Kalahkan guard veteran di pantai — item drop: Kompas Nonno Arganta",
        "steps": [
            "Pergi ke Pantai (BEACH)",
            "Temukan guard veteran atau mercenary thug yang patroli di pantai",
            "Kalahkan mereka — Kompas Nonno Arganta akan di-drop",
            "Kembalikan kompas ke Arganta — terima Peta Jalur Rahasia",
        ],
        "required_item": "Kompas Nonno Arganta",
        "required_action": None,
        "unlock_location": "beach",
        "location": "beach",
        "reward_item": "Peta Jalur Rahasia",
        "reward_dialog": [
            "Amerigo: 'Il mio compasso! Kamu menemukannya!'",
            "Amerigo: 'Kompas ini... Nonno-ku memberikannya sebelum mereka membunuhnya di laut.'",
            "Amerigo: 'Aku berutang padamu. Sekarang aku ikut. Bersama kita akan keluar dari pulau terkutuk ini.'"
        ]
    },
    "ignatius": {
        "chapter": 3,
        "name": "Komponen EMP Ignatius",
        "desc": "Ignatius butuh 3 komponen untuk menyelesaikan alat EMP-nya. "
                "Komponen tersebar di basement dan mansion.",
        "objective": "Kalahkan guard elite (mansion), tech guard (pusat kontrol), mansion guard (teater) untuk drop komponen",
        "steps": [
            "Pergi ke Basement atau Mansion",
            "Ambil [Kapasitor Besar] di gudang supply lantai 1 mansion",
            "Ambil [Relay Switch] di ruang komunikasi lantai 2",
            "Ambil [Copper Coil] di ruang generator timur basement",
            "Kumpulkan ke Ignatius — terima EMP Device yang sudah jadi",
        ],
        "required_items": ["Kapasitor Besar", "Relay Switch", "Copper Coil"],
        "required_item": None,
        "required_action": None,
        "unlock_location": "basement",
        "location": "basement",
        "reward_item": "EMP Device",
        "reward_dialog": [
            "Ignatius: 'YES! Semua komponen lengkap! Ini yang aku butuhkan!'",
            "Ignatius: 'Dengan ini aku bisa buat EMP pulse yang matiin semua sistem keamanan pulau.'",
            "Ignatius: 'Aku gabung sama tim kamu. Engineering time! Let's blow this joint!'"
        ]
    },
    "vio": {
        "chapter": 3,
        "name": "USB Drive Terenkripsi",
        "desc": "Vio butuh USB Security Drive dengan chip enkripsi hardware untuk crack file utama. "
                "Item ini ada di security room laboratorium.",
        "objective": "Kalahkan scientist di laboratorium — item drop: USB Security Drive",
        "steps": [
            "Pergi ke Laboratorium (tersedia Ch.4+)",
            "Temukan scientist yang berpatroli di area barat laboratorium",
            "Kalahkan scientist — USB Security Drive akan di-drop",
            "Serahkan ke Vio — terima USB Evidence Drive yang sudah di-decrypt",
        ],
        "required_item": "USB Security Drive",
        "required_action": None,
        "unlock_location": "laboratory",
        "location": "laboratory",
        "reward_item": "USB Evidence Drive",
        "reward_dialog": [
            "Vio: '...Nice. Edinburgh hackers appreciate good teamwork.'",
            "Vio: 'USB ini punya semua guest list dan flight log Epstein. Aku udah crack semua enkripsinya.'",
            "Vio: 'Aku ikut tim kamu. Gacha bisa nunggu, tapi data ini tidak bisa diabaikan.'"
        ]
    }
}
# Intro cerita tiap karakter
CHARACTER_INTROS = {
    "vio": [
        "Dia adalah Vio, hacker elite dari Edinburgh, Skotlandia yang diculik karena membobol jaringan Epstein.",
        "Di sel gelap, Dia tetap sempat check daily login game gacha di HP gaming yang disembunyikan di balik seragam.",
        "'Pity counter gue udah 87... tinggal 3 lagi guaranteed SSR...' - pikir Vio sambil analisis sistem keamanan pulau.",
        "'Sistem keamanan pulau ini... mirip game gacha dengan bad RNG. Ada backdoor di network mereka.'",
        "'Aku bisa jebol. Scottish hackers dinna give up. Keluar dari sini, lanjut pull gacha.'"
    ],
    "haikaru": [
        "Dia adalah Haikaru Fumika, ahli strategi dari Kyoto yang sudah 2 minggu memetakan seluruh pola pulau.",
        "Buku catatannya penuh — penjaga, kamera, celah — semua tercatat dengan presisi seorang juara olimpiade matematik.",
        "'Shift berganti jam 06.00 dan 18.00. Window keluar: 47 detik.' Fumika sudah hitung segalanya.",
        "'Saya bukan orang yang panik. Saya adalah orang yang membuat orang lain panik.' — kata Fumika dalam hati.",
        "'Rencana sudah matang. Yang dibutuhkan hanya satu hal lagi: seseorang yang bisa bergerak cepat.'"
    ],
    "aolinh": [
        "Dia adalah Ao Lin, gadis ceria dari Chengdu, China yang diculik bersama Jiejie-nya saat turnamen musik di Hongkong.",
        "Earphone biru kesayangannya masih ada. Biola warisan ibu masih dalam genggaman.",
        "Meski ketakutan, Ao Lin tahu satu hal: 音乐给我力量 — musik memberinya kekuatan.",
        "'Jiejie... 我来找你。 Aku akan menemukanmu. Jangan menyerah.'",
        "'Selama aku bisa memegang biola ini... aku tidak akan berhenti. 我们一起！ Kita bersama!'"
    ],
    "arganta": [
        "Dia adalah Amerigo Arganta, navigator muda dari Napoli, Italia yang keluarganya dibantai di laut Karibia.",
        "Kompas kakeknya masih di sakunya - warisan dari sang Nonno, navigator legendaris Mediterania.",
        "Di dinding selnya, Dia mengukir kata-kata yang dipelajari dari legenda kota leluhurnya di Italia:",
        "'Niente è reale, tutto è lecito.' Tidak ada yang nyata, segalanya diperbolehkan.",
        "'La via è sempre avanti,' bisiknya sambil menggenggam kompas. 'Requiescat in pace, Nonno. Aku akan selesaikan ini.'"
    ],
    "ignatius": [
        "Dia adalah Ignatius, teknisi yang bisa hack mesin apapun.",
        "Panel listrik di luar selmu bermasalah. Koneksi ground yang lemah.",
        "Lock elektronik pakai sistem lama. Kesalahan mereka. Keuntunganmu.",
        "'Lock elektronik ini... model 2015. Outdated. Vulnerable AF.'",
        "'Panel listrik, alarm, CCTV... semuanya terkoneksi ke satu grid. EZ hack. Let's break it!'"
    ]
}

def get_character_select_screen():
    text = f"\n{Warna.CYAN + Warna.TERANG}╔══════════════════════════════════════════════════════════╗\n"
    text += f"║              PILIH KARAKTER UTAMA                         ║\n"
    text += f"╚══════════════════════════════════════════════════════════╝{Warna.RESET}\n\n"
    
    for i, (char_id, data) in enumerate(PLAYABLE_CHARACTERS.items(), 1):
        name = data["name"]
        title = data["title"]
        desc = data["desc"]
        age = data["age"]
        gender = data["gender"]
        
        stats = data["stats"]
        stat_line = f"HP:{stats['hp']} ATK:{stats['attack']} DEF:{stats['defense']} SPD:{stats['speed']}"
        
        skills = [s["name"] for s in data["skills"].values()]
        skills_preview = ", ".join(skills)
        
        hobby = data.get("hobby", "Unknown")
        
        text += f"{Warna.KUNING + Warna.TERANG}[{i}] {name}{Warna.RESET} - {Warna.CYAN}{title}{Warna.RESET}\n"
        text += f"    {Warna.ABU_GELAP}{gender}, {age} tahun - {desc}{Warna.RESET}\n"
        text += f"    {Warna.PUTIH}Stats: {stat_line}{Warna.RESET}\n"
        text += f"    {Warna.HIJAU}Skills: {skills_preview}{Warna.RESET}\n"
        text += f"    {Warna.UNGU}Passive: {data['passive']}{Warna.RESET}\n"
        text += f"    {Warna.CYAN}Hobby: {hobby}{Warna.RESET}\n"
        text += f"    {Warna.ABU_GELAP}Personality: {data['personality']}{Warna.RESET}\n\n"
    
    text += f"{Warna.CYAN}Setiap karakter punya story path unik dan battle dialogs!{Warna.RESET}\n"
    text += f"{Warna.UNGU}Easter Eggs: Candala, Balatro Joker, Secret Phone Call...{Warna.RESET}\n"
    
    return text

def get_character_intro(char_id):
    if char_id in CHARACTER_INTROS:
        return CHARACTER_INTROS[char_id]
    return ["Dia terbangun di tempat asing yang gelap."]

def get_character_data(char_id):
    return PLAYABLE_CHARACTERS.get(char_id)

def get_special_npc_data(npc_id):
    return SPECIAL_NPC.get(npc_id)

def get_all_character_ids():
    return list(PLAYABLE_CHARACTERS.keys())

def get_character_name(char_id):
    char = PLAYABLE_CHARACTERS.get(char_id)
    return char["name"] if char else "Unknown"

def get_card_dialog(char_id, hand_type):
    

    char_id = char_id.lower().strip()

    char = PLAYABLE_CHARACTERS.get(char_id)
    if not char:
        return FALLBACK_CARD_DIALOGS.get("default", "Aksi!")

    dialogs = char.get("card_dialogs", {})
    if not dialogs:
        return FALLBACK_CARD_DIALOGS.get("default", "Aksi!")

    HAND_KEY_MAP = {
        "high_card":       "high_card",
        "one_pair":        "pair",
        "two_pair":        "two_pair",
        "three_of_a_kind": "three_kind",
        "straight":        "straight",
        "flush":           "flush",
        "full_house":      "full_house",
        "four_of_a_kind":  "four_kind",
        "straight_flush":  "straight_flush",
        "nothing":         "high_card",
    }

    raw_key = hand_type.lower().replace(" ", "_")
    hand_key = HAND_KEY_MAP.get(raw_key, raw_key)

    # Coba ambil dialog sesuai hand_key
    if dialogs.get(hand_key) and len(dialogs[hand_key]) > 0:
        with suppress(Exception):
            return random.choice(dialogs[hand_key])

    # Fallback 1: Coba ambil high_card dialog
    if dialogs.get("high_card") and len(dialogs["high_card"]) > 0:
        with suppress(Exception):
            return random.choice(dialogs["high_card"])

    # Fallback 2: Coba ambil dialog pertama dari entry manapun yang tersedia
    with suppress(Exception):
        for lines in dialogs.values():
            if lines:
                return random.choice(lines)

    # Fallback 3: Gunakan global fallback
    return FALLBACK_CARD_DIALOGS.get("default", "Aksi!")

def safe_get_card_dialog(char_id, hand_key):
    """FIX Bug 3: API aman untuk mengakses dialog kartu dari kode eksternal"""
    
    def _get_dialog_from_char(char, hand_key):
        dialogs = char.get("card_dialogs", {})
        if not dialogs:
            return None
        if dialogs.get(hand_key):
            return random.choice(dialogs[hand_key])
        if dialogs.get("high_card"):
            return random.choice(dialogs["high_card"])
        return next((random.choice(lines) for lines in dialogs.values() if lines), None)
    
    char_id  = char_id.lower().strip()
    hand_key = hand_key.lower().strip()

    with suppress(KeyError, TypeError, AttributeError):
        char = PLAYABLE_CHARACTERS.get(char_id)
        if char:
            return _get_dialog_from_char(char, hand_key)

    return None

def check_candala_encounter(game_state):
    """Check if Candala appears"""
    return hasattr(game_state, 'bosses_defeated') and game_state.bosses_defeated > 0 and random.random() < SPECIAL_NPC["candala"]["encounter_chance"]

def check_balatro_encounter(hand_type, hand_score):
    """Check if Balatro Joker appears on good hands"""
    good_hands = ["Flush", "Full House", "Four of a Kind", "Straight Flush"]
    return hand_type in good_hands and random.random() < SPECIAL_NPC["balatro_joker"]["encounter_chance"]

def check_prabowo_phone_encounter(game_state, location):
    """Check if player finds the secret phone call"""
    return location == "mansion" and "secret_evidence" not in game_state.discovered_secrets and random.random() < SPECIAL_NPC["prabowo_phone"]["encounter_chance"]

import time
from contextlib import suppress

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
