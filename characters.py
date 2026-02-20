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
                "desc": "Hack sistem pertahanan musuh: DEF musuh -50% selama 3 giliran",
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
                "desc": "Jamming sinyal serangan: ATK musuh -40% selama 3 giliran",
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
                "desc": "RNG blessed! Random: ATK buff / DEF buff / Heal HP / Regen Energy",
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
                "desc": "Injeksi data berlebih: kartu berikutnya damage ×2 + debuff DEF musuh -30%",
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
                "desc": "Analisis kelemahan musuh: DEF -35% + ATK -20% selama 2 giliran",
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
                "desc": "Konsentrasi penuh: ATK diri sendiri +55% selama 2 giliran",
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
                "desc": "Korbankan 20 HP → ATK +65% + +30 Energy selama 2 giliran",
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
                "desc": "Baca pola kartu: hand berikutnya Straight bisa terbentuk dari 4 kartu!",
                "effect": "buff_four_straight",
                "target": "self",
                "level_bonus": 0
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
                "desc": "Melodi penyembuh: pulihkan 40-60 HP diri sendiri",
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
                "desc": "Perisai harmoni: DEF diri sendiri +50% selama 3 giliran",
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
                "desc": "Irama semangat: ATK +35% selama 3 giliran + pulihkan 20 HP",
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
                "desc": "Irama baru: pulihkan 1 slot discard + langsung draw 2 kartu tambahan",
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
                "desc": "Satu langkah ke bayangan: 70% dodge serangan musuh giliran ini",
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
                "desc": "Insting bertahan: pulihkan 25 HP + regen 25 Energy",
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
                "desc": "Tandai target: ATK musuh -45% selama 3 giliran",
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
                "desc": "Keluar dari bayangan: kartu berikutnya ×2 damage + otomatis STUN musuh!",
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
                "desc": "Pulse elektromagnetik: musuh di-stun, skip serangan 1 giliran",
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
                "desc": "Overclocking sistem: ATK diri sendiri +60% + regen 20 Energy selama 2 giliran",
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
                "desc": "Perbaikan darurat: pulihkan 40 HP + bersihkan semua debuff",
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
                "desc": "Korbankan 15 HP → kartu berikutnya ×2 DAMAGE! (Overload circuit)",
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


# NPC spesial (Candala, Joker, Phone Call)
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
    },
    
    "balatro_joker": {
        "name": "The Joker",
        "title": "Master of Cards",
        "age": "???",
        "gender": "Unknown",
        "desc": "Mysterious figure yang master dalam card games",
        "sprite": ("🃏", Warna.UNGU + Warna.TERANG, ""),
        "backstory": "Figura misterius yang muncul saat poker hand dimainkan dengan sempurna. Konon dia adalah representasi dari 'luck' itu sendiri.",
        "dialog": [
            "Joker: *appears with a flourish of cards* Impressive hand, young one...",
            "Joker: In the grand casino of life, you're playing your cards well.",
            "Joker: The house always wins? Not if you know the game!",
            "Joker: Here's a secret: sometimes the joker is wild, sometimes it's wisdom.",
            "Joker: *scatters into playing cards* Remember: every hand is a new chance!",
            "Joker: FLUSH FIVE activated! MEGA BOOST!",
            "Joker: HIGH CARD into STRAIGHT FLUSH? That's MY kind of play!",
            "Joker: Ride the Chaos! Let's MULTIPLY those chips!"
        ],
        "encounter_chance": 0.05,
        "location": "combat_special",
        "can_join": False,
        "bonus": {
            "mult": 1.5,
            "chips": 100,
            "buff": "Lucky Joker: +50% damage next turn"
        }
    },
    
    "prabowo_phone": {
        "name": "???",
        "title": "Mysterious Phone Call",
        "age": "???",
        "gender": "Male",
        "desc": "Suara familiar yang terdengar dari ruang komunikasi...",
        "sprite": ("📞", Warna.HIJAU + Warna.TERANG, ""),
        "backstory": "Sebuah phone call yang tidak disengaja Dia dengar di communication room pulau...",
        "dialog": [
            "*Phone ringing... someone picks up*",
            "Voice 1: \"Jeffrey, the shipment is delayed. My contacts in Jakarta are getting nervous.\"",
            "Voice 2 (Epstein): \"Relax, my friend. The operation has been running smoothly for years.\"",
            "Voice 1: \"Those kids you requested... they'll arrive next week. Very discreet.\"",
            "Voice 2: \"Excellent. And the offshore accounts?\"",
            "Voice 1: \"All clean. Nobody will trace anything back to either of us.\"",
            "Voice 2: \"That's why I work with you. Always reliable, always powerful.\"",
            "Voice 1: \"Just keep your end clean. If this goes public—\"",
            "Voice 2: \"It won't. We have friends in very high places. Even presidents.\"",
            "*Footsteps approaching... you quickly hide*",
            "*The voices fade as the call ends*",
            "",
            f"{Warna.MERAH}[You've uncovered something dark... This information could change everything.]{Warna.RESET}",
            f"{Warna.ABU_GELAP}[Evidence recorded in your memory. This could expose the whole network...]{Warna.RESET}"
        ],
        "encounter_chance": 0.02,
        "location": "mansion_communication_room",
        "can_join": False,
        "unlocks": "secret_evidence"
    }
}

# QUEST UTAMA PER KARAKTER
# Tiap chapter punya boss unik sesuai karakter.
# Boss ch.3 terakhir selalu Epstein (final boss).
# Quest utama per karakter per chapter
CHARACTER_MAIN_QUESTS = {
    # VIO
    "vio": {
        1: {
            "id":     "vio_ch1_main",
            "title":  "Hack the Mansion",
            "objective": "Akses server room dan kalahkan Maxwell Enforcer",
            "boss_id":   "maxwell_enforcer",
            "boss_name": "Maxwell Enforcer",
            "steps": [
                "Akses terminal komputer di server room mansion",
                "Kumpulkan 'USB Security Drive' dari Security Room",
                "Kalahkan Maxwell Enforcer — penjaga jaringan Epstein",
            ],
            "completion_flag": "vio_ch1_complete",
            "next_chapter_msg": "Data terenkripsi berhasil di-crack! Jaringan mulai terbuka...",
        },
        2: {
            "id":     "vio_ch2_main",
            "title":  "Island Network Takeover",
            "objective": "Kalahkan Mercenary Commander dan Corrupted Warden",
            "boss_id":   "mercenary_commander",
            "boss_name": "Mercenary Commander",
            "steps": [
                "Kalahkan 'Mercenary Commander' di pulau (boss 1)",
                "Kalahkan 'Corrupted Warden' di penjara selatan (boss 2)",
            ],
            "completion_flag": "vio_ch2_complete",
            "next_chapter_msg": "Kontrol pulau diambil alih. Saatnya konfrontasi final!",
        },
        3: {
            "id":     "vio_ch3_main",
            "title":  "The Final Upload — Expose Epstein",
            "objective": "Kalahkan Dr. Rousseau, Benefactor, dan Epstein",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Kalahkan Dr. Rousseau — ilmuwan jaringan (boss 1)",
                "Kalahkan Mysterious Benefactor (boss 2)",
                "Kalahkan Epstein — upload semua bukti ke dunia!",
            ],
            "completion_flag": "vio_ch3_complete",
        },
    },
    # HAIKARU
    "haikaru": {
        1: {
            "id":     "haikaru_ch1_main",
            "title":  "Rencana Sempurna: Kabur dari Penjara",
            "objective": "Eksekusi rencana pelarian — kalahkan Warden Elite",
            "boss_id":   "warden_elite",
            "boss_name": "Warden Elite",
            "steps": [
                "Amati pola patroli dan temukan blind spot (30 detik window)",
                "Ambil kunci tersembunyi dari Wing-C penjara",
                "Kalahkan Warden Elite yang memblokir pintu utama",
            ],
            "completion_flag": "haikaru_ch1_complete",
            "next_chapter_msg": "Semua kalkulasi tepat. Penjara teratasi. Target berikutnya: pulau.",
        },
        2: {
            "id":     "haikaru_ch2_main",
            "title":  "Tactical Sweep: Bersihkan Pulau",
            "objective": "Kalahkan 2 boss dengan strategi optimal",
            "boss_id":   "mercenary_commander",
            "boss_name": "Mercenary Commander",
            "steps": [
                "Kalahkan 'Mercenary Commander' di pulau (boss 1)",
                "Kalahkan 'Corrupted Warden' di penjara selatan (boss 2)",
            ],
            "completion_flag": "haikaru_ch2_complete",
            "next_chapter_msg": "Pulau terkendali. Fase terakhir: checkmate Epstein.",
        },
        3: {
            "id":     "haikaru_ch3_main",
            "title":  "Checkmate — Akhiri Jaringan",
            "objective": "Kalahkan trio boss terakhir dan Epstein",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Kalahkan Dr. Rousseau (boss 1)",
                "Kalahkan Mysterious Benefactor (boss 2)",
                "Checkmate Epstein — final boss!",
            ],
            "completion_flag": "haikaru_ch3_complete",
        },
    },
    # AOLINH
    "aolinh": {
        1: {
            "id":     "aolinh_ch1_main",
            "title":  "Musik dan Kebebasan: Temukan Jiejie",
            "objective": "Selamatkan Jiejie — kalahkan Theater Master",
            "boss_id":   "theater_master",
            "boss_name": "Theater Master",
            "steps": [
                "Telusuri teater — temukan jejak Jiejie",
                "Ambil 'Kunci Ruang Belakang' dari loker penjaga teater",
                "Kalahkan Theater Master dan bebaskan Jiejie!",
            ],
            "completion_flag": "aolinh_ch1_complete",
            "next_chapter_msg": "Jiejie bebas! 我们一起！ Musik memberi kekuatan untuk maju.",
        },
        2: {
            "id":     "aolinh_ch2_main",
            "title":  "Sound of Hope: Bawa Damai ke Pulau",
            "objective": "Kalahkan 2 boss penjaga pulau dengan melodi harapan",
            "boss_id":   "mercenary_commander",
            "boss_name": "Mercenary Commander",
            "steps": [
                "Kalahkan 'Mercenary Commander' di pulau (boss 1)",
                "Kalahkan 'Corrupted Warden' di penjara selatan (boss 2)",
            ],
            "completion_flag": "aolinh_ch2_complete",
            "next_chapter_msg": "Pulau mulai tenang. Satu langkah lagi menuju kebebasan.",
        },
        3: {
            "id":     "aolinh_ch3_main",
            "title":  "Final Crescendo — Akhiri Segalanya",
            "objective": "Kalahkan boss final dan Epstein dengan kekuatan musik",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Kalahkan Dr. Rousseau (boss 1)",
                "Kalahkan Mysterious Benefactor (boss 2)",
                "Kalahkan Epstein — nyanyikan lagu kebebasan terakhir!",
            ],
            "completion_flag": "aolinh_ch3_complete",
        },
    },
    # ARGANTA
    "arganta": {
        1: {
            "id":     "arganta_ch1_main",
            "title":  "La Via Avanti: Kabur dari Pantai",
            "objective": "Temukan rute pelarian — kalahkan Harbor Captain",
            "boss_id":   "harbor_captain",
            "boss_name": "Harbor Captain",
            "steps": [
                "Jelajahi pantai — temukan rute ke dermaga tersembunyi",
                "Cari 'Kompas Nonno Arganta' di gudang pantai barat",
                "Kalahkan Harbor Captain yang menjaga pintu dermaga",
            ],
            "completion_flag": "arganta_ch1_complete",
            "next_chapter_msg": "Dermaga dikuasai. La via è sempre avanti, Nonno.",
        },
        2: {
            "id":     "arganta_ch2_main",
            "title":  "Per La Famiglia: Tegakkan Keadilan",
            "objective": "Lanjutkan misi balas dendam — kalahkan 2 boss",
            "boss_id":   "mercenary_commander",
            "boss_name": "Mercenary Commander",
            "steps": [
                "Kalahkan 'Mercenary Commander' di pulau (boss 1)",
                "Kalahkan 'Corrupted Warden' di penjara selatan (boss 2)",
            ],
            "completion_flag": "arganta_ch2_complete",
            "next_chapter_msg": "Niente è reale. Saatnya konfrontasi dengan bos tertinggi.",
        },
        3: {
            "id":     "arganta_ch3_main",
            "title":  "Requiescat in Pace — Akhiri Segalanya",
            "objective": "Selesaikan misi keluarga — kalahkan Epstein",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Kalahkan Dr. Rousseau (boss 1)",
                "Kalahkan Mysterious Benefactor (boss 2)",
                "Requiescat in pace — kalahkan Epstein!",
            ],
            "completion_flag": "arganta_ch3_complete",
        },
    },
    # IGNATIUS
    "ignatius": {
        1: {
            "id":     "ignatius_ch1_main",
            "title":  "Engineering Time: Sabotase Sistem",
            "objective": "Kumpulkan komponen EMP — kalahkan Security Bot Mk-II",
            "boss_id":   "security_bot",
            "boss_name": "Security Bot Mk-II",
            "steps": [
                "Kumpulkan 'Kapasitor Besar' dari panel listrik basement",
                "Kumpulkan 'Relay Switch' dan 'Copper Coil' di storage room",
                "Kalahkan Security Bot Mk-II yang menjaga generator utama",
            ],
            "completion_flag": "ignatius_ch1_complete",
            "next_chapter_msg": "SISTEM DIRETAS! Generator down. EZ hack. Let's blow this joint!",
        },
        2: {
            "id":     "ignatius_ch2_main",
            "title":  "System Override: Ambil Alih Pulau",
            "objective": "Overload sistem keamanan — kalahkan 2 boss",
            "boss_id":   "mercenary_commander",
            "boss_name": "Mercenary Commander",
            "steps": [
                "Kalahkan 'Mercenary Commander' di pulau (boss 1)",
                "Kalahkan 'Corrupted Warden' di penjara selatan (boss 2)",
            ],
            "completion_flag": "ignatius_ch2_complete",
            "next_chapter_msg": "Grid keamanan pulau offline. Final circuit break: Epstein.",
        },
        3: {
            "id":     "ignatius_ch3_main",
            "title":  "Final Circuit Break — Shutdown Epstein",
            "objective": "Kalahkan boss final dan matikan jaringan Epstein",
            "boss_id":   "epstein_boss",
            "boss_name": "Jeffrey Epstein",
            "steps": [
                "Kalahkan Dr. Rousseau (boss 1)",
                "Kalahkan Mysterious Benefactor (boss 2)",
                "FINAL SHUTDOWN — kalahkan Epstein!",
            ],
            "completion_flag": "ignatius_ch3_complete",
        },
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
        "desc": "Fumika tidak mau bergerak tanpa buku catatannya. "
                "Buku itu disita penjaga dan disimpan di Guard Station Wing-B penjara.",
        "objective": "Ambil [Buku Catatan Fumika] dari Guard Station Wing-B",
        "required_item": "Buku Catatan Haikaru",
        "required_action": None,
        "unlock_location": "prison_north",
        "reward_dialog": [
            "Fumika: '...Kamu mengambilnya? Hmph. Efisien.'",
            "Fumika: 'Semua data observasiku ada di sini. 17 posisi guard, 8 blind spot, 3 jalur keluar.'",
            "Fumika: 'Aku bergabung dengan timmu. Tapi ikuti rencanaku. Deviasi tidak diperbolehkan.'"
        ]
    },
    "aolinh": {
        "chapter": 2,
        "name": "Biola di Balik Panggung",
        "desc": "Ao Lin dikurung di ruang ganti teater oleh seorang penjaga. "
                "Kalahkan penjaga tersebut untuk membebaskannya.",
        "objective": "Kalahkan [Theater Guard Brenin] di backstage teater",
        "required_item": None,
        "required_action": "defeat_theater_guard",
        "unlock_location": "theater",
        "reward_dialog": [
            "Ao Lin: '*memeluk biola-nya* 谢谢！ Xiè xie! Makasih banget!'",
            "Ao Lin: 'Aku harus cari Jiejie-ku — kakakku. Tapi sendirian aku tidak berani.'",
            "Ao Lin: 'Aku ikut sama kamu ya? 我们一起！ Kita bersama! Let's stay positive! ♪'"
        ]
    },
    "arganta": {
        "chapter": 2,
        "name": "Kompas yang Hilang",
        "desc": "Amerigo Arganta terjebak di pantai tanpa kompas kakeknya. "
                "Kompas itu diambil penjaga dermaga dan disimpan di gudang pelabuhan.",
        "objective": "Cari [Kompas Nonno Arganta] di gudang barat dermaga",
        "required_item": "Kompas Nonno Arganta",
        "required_action": None,
        "unlock_location": "beach",
        "reward_dialog": [
            "Amerigo: 'Il mio compasso! Kamu menemukannya!'",
            "Amerigo: 'Kompas ini... Nonno-ku memberikannya sebelum mereka membunuhnya di laut.'",
            "Amerigo: 'Aku berutang padamu. Sekarang aku ikut. Bersama kita akan keluar dari pulau terkutuk ini.'"
        ]
    },
    "ignatius": {
        "chapter": 3,
        "name": "Komponen EMP",
        "desc": "Ignatius butuh 3 komponen untuk menyelesaikan alat EMP-nya. "
                "Komponen tersebar di berbagai ruangan mansion.",
        "objective": "Kumpulkan [Kapasitor Besar], [Relay Switch], dan [Copper Coil] di mansion",
        "required_items": ["Kapasitor Besar", "Relay Switch", "Copper Coil"],
        "required_item": None,
        "required_action": None,
        "unlock_location": "basement",
        "reward_dialog": [
            "Ignatius: 'YES! Semua komponen lengkap! Ini yang aku butuhkan!'",
            "Ignatius: 'Dengan ini aku bisa buat EMP pulse yang matiin semua sistem keamanan pulau.'",
            "Ignatius: 'Aku gabung sama tim kamu. Engineering time! Let's blow this joint!'"
        ]
    },
    "vio": {
        "chapter": 3,
        "name": "USB Drive Terenkripsi",
        "desc": "Vio menemukan file penting tapi perlu USB drive khusus dari ruang keamanan. "
                "Ambilkan USB itu dan dia akan berbagi semua data yang sudah di-crack.",
        "objective": "Ambil [USB Security Drive] dari Security Room mansion lantai 2",
        "required_item": "USB Security Drive",
        "required_action": None,
        "unlock_location": "mansion",
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
    """
    Get random dialog for card play based on character and hand type.
    Returns:
        str — dialog, atau default string dari fallback jika tidak ada
    """

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
