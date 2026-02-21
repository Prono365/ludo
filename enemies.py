# Database musuh dan boss

from sprites import Warna
import random


ENEMIES = {
    "guard_novice": {
        "id": "guard_novice",
        "name": "Security Guard - Novice",
        "level": 1,
        "hp": 85,       # Balance: Tier 1 enemy
        "max_hp": 85,
        "attack": 14,   # buffed dari 12
        "defense": 9,   # buffed dari 8
        "speed": 13,    # buffed dari 12
        "xp": 28,
        "dollars": 15,
        "desc": "Nervous rookie guard",
        "sprite": "G",
        "ai_style": "defensive",
        "loot": ["Health Potion", "Keycard Level 1", "Flashlight"],
        "dialog": {
            "encounter": "Hey! Stop right there, kid!",
            "defeat": "I'm just doing my job..."
        }
    },
    
    "guard_veteran": {
        "id": "guard_veteran",
        "name": "Security Guard - Veteran",
        "level": 3,
        "hp": 110,      # Balance: Tier 2 enemy
        "max_hp": 110,
        "attack": 19,   # buffed dari 16
        "defense": 16,  # buffed dari 14
        "speed": 17,    # buffed dari 15
        "xp": 55,
        "dollars": 25,
        "desc": "Experienced guard",
        "sprite": "G",
        "ai_style": "balanced",
        "loot": ["Med Kit", "Keycard Level 2", "Stun Baton"],
        "dialog": {
            "encounter": "You kids aren't going anywhere!",
            "defeat": "How did... you're just children..."
        }
    },
    
    "guard_elite": {
        "id": "guard_elite",
        "name": "Elite Security Guard",
        "level": 5,
        "hp": 140,      # Balance: Tier 3 enemy
        "max_hp": 125,
        "attack": 23,   # buffed dari 20
        "defense": 23,  # buffed dari 20
        "speed": 21,    # buffed dari 18
        "xp": 80,
        "dollars": 40,
        "desc": "Elite military background guard",
        "sprite": "G",
        "ai_style": "aggressive",
        "loot": ["Armor Vest", "Keycard Level 3", "Tactical Knife"],
        "dialog": {
            "encounter": "Kids? Doesn't matter. You're not leaving.",
            "defeat": "Impossible... defeated by children..."
        }
    },
    
    "mercenary_thug": {
        "id": "mercenary_thug",
        "name": "Mercenary Thug",
        "level": 2,
        "hp": 95,       # Balance: Tier 1-2 enemy
        "max_hp": 95,
        "attack": 23,   # buffed dari 20
        "defense": 12,  # buffed dari 10
        "speed": 18,    # buffed dari 16
        "xp": 40,
        "dollars": 30,
        "desc": "Hired muscle",
        "sprite": "M",
        "ai_style": "reckless",
        "loot": ["Baseball Bat", "Cash $50", "Bandage"],
        "dialog": {
            "encounter": "Boss says no one leaves.",
            "defeat": "Damn it..."
        }
    },
    
    "mercenary_sniper": {
        "id": "mercenary_sniper",
        "name": "Mercenary Sniper",
        "level": 4,
        "hp": 105,      # Balance: Tier 2 ranged
        "max_hp": 105,
        "attack": 21,
        "defense": 12,
        "speed": 20,
        "xp": 65,
        "dollars": 40,
        "desc": "Long-range specialist",
        "sprite": "S",
        "ai_style": "patient",
        "loot": ["Scope", "Rifle Parts", "Med Kit"],
        "dialog": {
            "encounter": "Target acquired.",
            "defeat": "Mission... failed..."
        }
    },
    
    "scientist": {
        "id": "scientist",
        "name": "Corrupted Scientist",
        "level": 3,
        "hp": 85,       # Balance: Tier 1 non-combatant
        "max_hp": 85,
        "attack": 17,
        "defense": 15,
        "speed": 14,
        "xp": 55,
        "dollars": 30,
        "desc": "Researcher in dark experiments",
        "sprite": "R",
        "ai_style": "tactical",
        "loot": ["Research Notes", "Serum", "Lab Keycard"],
        "dialog": {
            "encounter": "Test subjects escaping!",
            "defeat": "My research..."
        }
    },
    
    "mansion_guard": {
        "id": "mansion_guard",
        "name": "Mansion Security",
        "level": 2,
        "hp": 95,       # Balance: Tier 2 enemy
        "max_hp": 95,
        "attack": 17,
        "defense": 12,
        "speed": 14,
        "xp": 40,
        "dollars": 25,
        "desc": "Regular mansion security patrol",
        "sprite": "G",
        "ai_style": "balanced",
        "loot": ["Med Kit", "Keycard Level 2", "Walkie Talkie"],
        "dialog": {
            "encounter": "Intruder in the mansion!",
            "defeat": "Backup... need backup..."
        }
    },
    
    "tech_guard": {
        "id": "tech_guard",
        "name": "Tech Security",
        "level": 3,
        "hp": 105,      # Balance: Tier 2 enemy
        "max_hp": 105,
        "attack": 19,
        "defense": 15,
        "speed": 16,
        "xp": 55,
        "dollars": 35,
        "desc": "Guard protecting server room",
        "sprite": "T",
        "ai_style": "defensive",
        "loot": ["Access Card", "Laptop Charger", "Med Kit"],
        "dialog": {
            "encounter": "Server room is restricted!",
            "defeat": "How did you... bypass the system..."
        }
    }
}


# Data boss
BOSSES = {
    "maxwell_enforcer": {
        "id": "maxwell_enforcer",
        "name": "Maxwell - Head of Security",
        "level": 8,
        "hp": 230,      # Balance: Boss HP ~210-250
        "max_hp": 230,
        "attack": 24,
        "defense": 18,
        "speed": 22,
        "xp": 150,
        "dollars": 150,
        "desc": "Former military, Epstein's head enforcer",
        "sprite": "M",
        "boss": True,
        "ai_style": "boss_tactical",
        "loot": ["Master Keycard", "Maxwell's Badge", "Encrypted USB"],
        "skills": {
            "intimidate": {
                "name": "Intimidating Shout",
                "power": 40,
                "effect": "Reduces party defense 20% for 2 turns"
            },
            "tactical_strike": {
                "name": "Tactical Strike",
                "power": 60,
                "effect": "High damage, ignores 50% defense"
            },
            "call_backup": {
                "name": "Call Backup",
                "power": 0,
                "effect": "Summons 2 guards",
                "uses": 1
            }
        },
        "dialog": {
            "encounter": [
                "Maxwell: Five kids. Made it farther than expected.",
                "Maxwell: But this ends here. Mr. Epstein pays well.",
                "Maxwell: And I always deliver."
            ],
            "phase2": [
                "Maxwell: *Grits teeth* Tougher than you look...",
                "Maxwell: But I was Special Forces!"
            ],
            "defeat": [
                "Maxwell: No... can't lose to kids...",
                "*Maxwell collapses. His radio crackles.*"
            ]
        }
    },
    
    "doctor_rousseau": {
        "id": "doctor_rousseau",
        "name": "Dr. Rousseau - Lead Researcher",
        "level": 9,
        "hp": 215,      # Balance: Boss HP ~210-250
        "max_hp": 210,
        "attack": 20,
        "defense": 15,
        "speed": 25,
        "xp": 180,
        "dollars": 180,
        "desc": "Twisted scientist conducting experiments",
        "sprite": "R",
        "boss": True,
        "ai_style": "boss_tricky",
        "loot": ["Experimental Serum", "Lab Master Key", "Research Data"],
        "skills": {
            "neurotoxin": {
                "name": "Neurotoxin Gas",
                "power": 30,
                "effect": "Poison - 15 damage per turn for 3 turns"
            },
            "enhancement_serum": {
                "name": "Enhancement Serum",
                "power": 0,
                "effect": "Boosts ATK/DEF 40% for 3 turns"
            },
            "release_subjects": {
                "name": "Release Test Subjects",
                "power": 0,
                "effect": "Summons 3 enhanced subjects",
                "uses": 1
            }
        },
        "dialog": {
            "encounter": [
                "Dr. Rousseau: Fascinating! Remarkable resilience!",
                "Dr. Rousseau: How does it feel to defy your captors?",
                "Dr. Rousseau: Let's make this a proper experiment!"
            ],
            "phase2": [
                "Dr. Rousseau: *Laughs maniacally* This data is incredible!",
                "Dr. Rousseau: Your survival instincts are off the charts!"
            ],
            "defeat": [
                "Dr. Rousseau: No... the experiment...",
                "Dr. Rousseau: You've ruined everything...",
                "*She collapses among broken test tubes.*"
            ]
        }
    },
    
    "ghislaine_maxwell": {
        "id": "ghislaine_maxwell",
        "name": "Ghislaine Maxwell - The Facilitator",
        "level": 10,
        "hp": 230,      # Balance: Boss HP ~210-250
        "max_hp": 250,
        "attack": 23,
        "defense": 20,
        "speed": 26,
        "xp": 200,
        "dollars": 200,
        "desc": "Epstein's right hand, recruited countless victims",
        "sprite": "G",
        "boss": True,
        "ai_style": "boss_manipulative",
        "loot": ["Little Black Book", "Private Island Keys", "Incriminating Photos"],
        "skills": {
            "manipulation": {
                "name": "Manipulative Lies",
                "power": 35,
                "effect": "Confusion + fear debuff"
            },
            "summon_guards": {
                "name": "Call Elite Guards",
                "power": 0,
                "effect": "Summons 3 elite guards",
                "uses": 2
            },
            "desperate_strike": {
                "name": "Desperate Attack",
                "power": 65,
                "effect": "High damage when cornered"
            }
        },
        "dialog": {
            "encounter": [
                "Ghislaine: Little children playing hero.",
                "Ghislaine: I've groomed hundreds like you.",
                "Ghislaine: You think you're special? You're not.",
                "Ghislaine: Jeffrey will never let you leave this island."
            ],
            "phase2": [
                "Ghislaine: *Furious* I've spent decades building this!",
                "Ghislaine: You can't destroy what we've created!",
                "Ghislaine: The network is too powerful!"
            ],
            "defeat": [
                "Ghislaine: No... my immunity deal... my connections...",
                "Ghislaine: They promised... I'd be protected...",
                "Ghislaine: *Falls* Jeffrey... you failed me...",
                "*Her phone contains thousands of contacts.*"
            ]
        }
    },
    
    "prince_andrew": {
        "id": "prince_andrew",
        "name": "Prince Andrew - The Royal Predator",
        "level": 10,
        "hp": 230,      # Balance: Boss HP ~210-250
        "max_hp": 235,
        "attack": 25,
        "defense": 18,
        "speed": 24,
        "xp": 220,
        "dollars": 220,
        "desc": "Duke of York, frequent island visitor, protected by crown",
        "sprite": "P",
        "boss": True,
        "ai_style": "boss_entitled",
        "loot": ["Royal Seal", "Private Photos", "Incriminating Documents"],
        "skills": {
            "royal_immunity": {
                "name": "Royal Immunity Claim",
                "power": 0,
                "effect": "Reduces damage taken by 50% for 3 turns"
            },
            "privileged_strike": {
                "name": "Privileged Strike",
                "power": 55,
                "effect": "High damage, thinks he's untouchable"
            },
            "deny_everything": {
                "name": "Deny Everything",
                "power": 30,
                "effect": "Confusion attack + attempt to gaslight"
            }
        },
        "dialog": {
            "encounter": [
                "Prince Andrew: I don't recall... I don't sweat...",
                "Prince Andrew: You have no proof I was ever here!",
                "Prince Andrew: I have diplomatic immunity! You can't touch me!",
                "Prince Andrew: The crown will protect me. It always has."
            ],
            "phase2": [
                "Prince Andrew: This is preposterous!",
                "Prince Andrew: I was at Pizza Express in Woking!",
                "Prince Andrew: My lawyers will bury you!"
            ],
            "defeat": [
                "Prince Andrew: The photographs... my alibi...",
                "Prince Andrew: This will ruin everything...",
                "Prince Andrew: *Falls* The Queen will... disown me...",
                "*His phone falls, showing damning text messages.*"
            ]
        }
    },
    
    "bill_clinton": {
        "id": "bill_clinton",
        "name": "Bill Clinton - The Former President",
        "level": 11,
        "hp": 250,      # Balance: Boss HP ~210-250
        "max_hp": 260,
        "attack": 27,
        "defense": 19,
        "speed": 24,
        "xp": 240,
        "dollars": 250,
        "desc": "Ex-president, frequent flyer on Lolita Express",
        "sprite": "B",
        "boss": True,
        "ai_style": "boss_political",
        "loot": ["Flight Logs", "Secret Service Records", "Burner Phone"],
        "skills": {
            "political_spin": {
                "name": "Political Spin",
                "power": 35,
                "effect": "Confuse + reduce party attack"
            },
            "executive_order": {
                "name": "Executive Power",
                "power": 60,
                "effect": "Command guards, massive damage"
            },
            "deny_plausibly": {
                "name": "Plausible Deniability",
                "power": 0,
                "effect": "Dodge attacks, claim innocence"
            }
        },
        "dialog": {
            "encounter": [
                "Clinton: I did not have relations with that island.",
                "Clinton: My trips were purely humanitarian work.",
                "Clinton: You can't prove anything. The records are sealed.",
                "Clinton: I'm a former president. Touch me and face consequences."
            ],
            "phase2": [
                "Clinton: *Furious* You think you can take ME down?",
                "Clinton: I've survived worse scandals!",
                "Clinton: The deep state protects its own!"
            ],
            "defeat": [
                "Clinton: The flight logs... oh god, the flight logs...",
                "Clinton: 26 times... they said it was just once...",
                "Clinton: *Collapses* My legacy... ruined...",
                "*His briefcase opens, revealing classified documents.*"
            ]
        }
    },
    

    "warden_elite": {
        "id": "warden_elite",
        "name": "Warden Elite - Kepala Penjaga",
        "level": 7,
        "hp": 215,      # Balance: Boss HP ~210-250
        "max_hp": 215,
        "attack": 20,
        "defense": 15,
        "speed": 18,
        "xp": 130,
        "dollars": 120,
        "desc": "Penjaga kepala yang blokir jalur keluar penjara",
        "sprite": "W",
        "boss": True,
        "loot": ["Master Key Penjara", "Walkie-Talkie Penjaga"],
        "dialog": {
            "encounter": [
                "Warden: Kamu mau kemana, tahanan?",
                "Warden: Tidak ada yang pernah keluar hidup-hidup dari sini.",
                "Warden: Rencana apapun yang kamu punya... sudah aku antisipasi."
            ],
            "defeat": [
                "Warden: Im-imposibel... tidak ada yang pernah...",
                "*Warden jatuh. Kunci master terlepas dari sabuknya.*"
            ]
        }
    },
    
    "theater_master": {
        "id": "theater_master",
        "name": "Theater Master - Penguasa Panggung",
        "level": 7,
        "hp": 215,      # Balance: Boss HP ~210-250
        "max_hp": 210,
        "attack": 18,
        "defense": 14,
        "speed": 22,
        "xp": 120,
        "dollars": 110,
        "desc": "Pengelola teater yang menjaga Jiejie",
        "sprite": "T",
        "boss": True,
        "loot": ["Kunci Ruang Belakang", "Tiket Backstage"],
        "dialog": {
            "encounter": [
                "Theater Master: Kamu mengacaukan pertunjukanku!",
                "Theater Master: Perempuan itu? Oh, dia koleksi pribadiku.",
                "Theater Master: Tidak akan ada yang menyelamatkannya."
            ],
            "defeat": [
                "Theater Master: K-kamu... merusak segalanya...",
                "*Theater Master roboh di atas panggungnya sendiri.*",
                "Dari balik pintu backstage: 'Aolinh...? Aolinh, itu kamu?'"
            ]
        }
    },
    
    "harbor_captain": {
        "id": "harbor_captain",
        "name": "Harbor Captain - Kapten Pelabuhan",
        "level": 7,
        "hp": 215,      # Balance: Boss HP ~210-250
        "max_hp": 220,
        "attack": 21,
        "defense": 16,
        "speed": 16,
        "xp": 140,
        "dollars": 130,
        "desc": "Kapten yang jaga jalur keluar dermaga",
        "sprite": "C",
        "boss": True,
        "loot": ["Kunci Dermaga", "Peta Jalur Laut"],
        "dialog": {
            "encounter": [
                "Captain: Ha! Bocah nyasar di pelabuhan-ku.",
                "Captain: Tidak ada kapal yang keluar tanpa izin-ku.",
                "Captain: Dan kamu... tidak punya izin."
            ],
            "defeat": [
                "Captain: Accidenti...! Chi sei tu...?",
                "*Kapten terjatuh. Kunci dermaga menggelinding ke kakimu.*"
            ]
        }
    },
    
    "security_bot": {
        "id": "security_bot",
        "name": "AmBOTukam Mk II",
        "level": 8,
        "hp": 230,      # Balance: Boss HP ~210-250
        "max_hp": 240,
        "attack": 22,
        "defense": 20,
        "speed": 14,
        "xp": 150,
        "dollars": 140,
        "desc": "Robot keamanan penjaga generator utama basement",
        "sprite": "R",
        "boss": True,
        "loot": ["Generator Key", "Circuit Fragments"],
        "dialog": {
            "encounter": [
                "AMBOTUKAM MK II: INTRUDER DETECTED.",
                "AMBOTUKAM MK II: INITIATING THREAT ELIMINATION PROTOCOL.",
                "AMBOTUKAM MK II: RESISTANCE IS FUTILE."
            ],
            "defeat": [
                "AMBOTUKAM MK II: SYSTEM FAIL... CORE BREACH...",
                "*Robot berhenti bergerak. Lampu merahnya mati perlahan.*",
                "Ignatius: Satu EMP tepat sasaran. Seperti yang sudah kuhitung."
            ]
        }
    },

    "kepala_penjaga": {
        "id": "kepala_penjaga",
        "name": "Kepala Penjaga",
        "level": 10,
        "hp": 350,
        "max_hp": 350,
        "attack": 22,
        "defense": 15,
        "speed": 12,
        "xp": 300,
        "dollars": 80,
        "desc": "Kepala Penjaga pulau yang memblokir jalan utama",
        "sprite": "K",
        "boss": True,
        "loot": ["Kunci Master Penjara", "Walkie-Talkie Penjaga"],
        "dialog": {
            "encounter": [
                "Kepala Penjaga memblokir jalan kalian.",
                "'Kamu pikir bisa kabur? Pulau ini penjara sempurna.'",
                "'Tidak ada yang pernah berhasil keluar.'",
            ],
            "defeat": [
                "Kepala Penjaga jatuh. Kunci master-nya terlepas dari sakunya.",
                "Jalan menuju chapter berikutnya terbuka.",
            ]
        }
    },

    "agen_maxwell": {
        "id": "agen_maxwell",
        "name": "Maxwell's Agent",
        "level": 13,
        "hp": 530,
        "max_hp": 530,
        "attack": 35,
        "defense": 22,
        "speed": 18,
        "xp": 500,
        "dollars": 150,
        "desc": "Agen Maxwell yang menjaga laboratorium dengan instruksi tanpa ampun",
        "sprite": "A",
        "boss": True,
        "loot": ["Kartu Akses Lab", "Encrypted Files"],
        "dialog": {
            "encounter": [
                "Maxwell's Agent berdiri di tengah laboratorium.",
                "'Anak-anak kecil yang mana coba berani masuk ke sini.'",
                "'Maxwell sudah kasih instruksi jelas: tidak ada saksi.'",
            ],
            "defeat": [
                "Agent jatuh. Sistem keamanan lab tidak merespons lagi.",
                "Kartu akses ke vault dokumen kini ada di tanganmu.",
            ]
        }
    },

    "epstein_boss": {
        "id": "epstein_boss",
        "name": "Jeffrey Epstein",
        "level": 15,
        "hp": 400,      # Balance: Final Boss HP
        "max_hp": 400,
        "attack": 34,
        "defense": 25,
        "speed": 28,
        "xp": 1000,
        "desc": "The predator. The monster. The man who must be stopped.",
        "sprite": "E",
        "boss": True,
        "final_boss": True,
        "ai_style": "final_boss",
        "phases": 3,
        "loot": ["Master Key to Island", "Complete Black Book", "All Evidence USB", "Offshore Account Access"],
        "skills": {
            "corruption": {
                "name": "Corrupting Influence",
                "power": 45,
                "effect": "Massive debuff - all stats -30% for 2 turns"
            },
            "power_play": {
                "name": "Power Play",
                "power": 80,
                "effect": "Massive single target damage"
            },
            "network_summon": {
                "name": "Summon The Network",
                "power": 0,
                "effect": "Summons elite enemies",
                "uses": 2
            },
            "last_resort": {
                "name": "Desperate Gambit",
                "power": 100,
                "effect": "Huge damage but leaves vulnerable"
            }
        },
        "dialog": {
            "encounter": [
                "Epstein: So you're the ones causing trouble.",
                "Epstein: Five children think they can bring me down?",
                "Epstein: I've destroyed people far more powerful than you.",
                "Epstein: Presidents, royalty, billionaires - they all owe me.",
                "Epstein: Let me teach you how the real world works."
            ],
            "phase2": [
                "Epstein: *Breathing heavily* Persistent little brats...",
                "Epstein: But I always win. ALWAYS.",
                "Epstein: I have too much power, too many connections!",
                "Epstein: You can't possibly win!"
            ],
            "phase3": [
                "Epstein: ENOUGH! *Rage* I will NOT lose to children!",
                "Epstein: I am JEFFREY EPSTEIN! I am UNTOUCHABLE!",
                "Epstein: Even if you kill me, the network survives!",
                "Epstein: There are others! Worse than me!",
                "Epstein: You'll never expose them all!"
            ],
            "defeat": [
                "Epstein: No... no... this isn't... possible...",
                "Epstein: I'm... Jeffrey Epstein... I can't... lose...",
                "Epstein: My connections... my power... everything...",
                "Epstein: *Gasping* The evidence... in my safe... destroy it...",
                "Epstein: Please... I'll tell you everything... just—",
                "",
                "*He collapses. The monster is defeated.*",
                "",
                "Around the island, alarms begin to shut down.",
                "The security systems fail. The doors unlock.",
                "You did it. You actually did it.",
                "",
                f"{Warna.HIJAU + Warna.TERANG}The island is free.{Warna.RESET}",
                f"{Warna.KUNING}And you have all the evidence to expose the entire network.{Warna.RESET}"
            ]
        }
    }
}

# create_enemy_instance: lihat definisi lengkap di bawah (dengan chapter scaling)


def create_boss_instance(boss_id):
    """Create boss instance"""
    boss = BOSSES.get(boss_id)
    return boss.copy() if boss else None

def get_enemy_for_location(location, chapter=1):
    """Get appropriate enemy for location based on chapter progression"""
    
    if chapter == 1:
        location_enemies = {
            "island":       ["guard_novice", "guard_novice"],         # +1 extra patrol
            "prison_north": ["guard_novice", "guard_novice"],
            "prison_south": ["guard_novice"],
            "mansion":      ["guard_novice", "mansion_guard", "guard_novice"],  # +1 extra
            "dock":         ["guard_novice", "mansion_guard"],
            "theater":      ["guard_novice"],
            "beach":        ["guard_novice"],
            "basement":     ["guard_novice", "tech_guard"],           # +tech_guard
        }
    elif chapter == 2:
        location_enemies = {
            "island":       ["guard_novice", "guard_veteran", "guard_veteran"],  # +1 extra
            "prison_north": ["guard_novice", "guard_veteran"],
            "prison_south": ["guard_novice", "guard_veteran", "mercenary_thug"],  # +merc
            "mansion":      ["mansion_guard", "guard_veteran", "tech_guard", "guard_elite"],  # +elite
            "dock":         ["guard_veteran", "mercenary_thug", "guard_veteran"],  # +1 extra
            "theater":      ["guard_veteran", "mercenary_thug"],      # +merc
            "beach":        ["guard_veteran", "guard_veteran"],       # +1 extra
            "basement":     ["guard_veteran", "tech_guard", "guard_elite"],  # +elite
        }
    else:
        location_enemies = {
            "island":       ["guard_veteran", "mercenary_thug", "guard_elite"],  # +elite
            "prison_north": ["guard_veteran", "guard_elite"],
            "prison_south": ["guard_veteran", "mercenary_thug"],      # +merc
            "mansion":      ["guard_veteran", "guard_elite", "tech_guard", "mercenary_sniper"],  # +sniper
            "dock":         ["guard_elite", "mercenary_sniper", "guard_elite"],  # +extra
            "laboratory":   ["scientist", "guard_elite", "scientist"],  # +scientist
        }
    
    enemies = location_enemies.get(location, ["guard_novice"])
    return random.choice(enemies)

def get_boss_for_location(location):
    """Get boss for specific location"""
    boss_map = {
        "dock": "maxwell_enforcer",
        "laboratory": "doctor_rousseau",
        "mansion_west": "ghislaine_maxwell",
        "mansion_east": "prince_andrew",
        "yacht": "bill_clinton",
        "mansion_final": "epstein_boss"
    }
    
    return boss_map.get(location)

# Probabilitas spawn musuh per lokasi per chapter
SPAWN_RATES = {
    1: {
        "island":       0.10,   # naik dari 0.08
        "prison_north": 0.12,   # naik dari 0.10
        "prison_south": 0.12,
        "mansion":      0.15,   # naik dari 0.12
        "dock":         0.15,
        "theater":      0.12,
        "beach":        0.10,
        "basement":     0.15,
    },
    2: {
        "island":       0.15,   # naik dari 0.12
        "prison_north": 0.18,
        "prison_south": 0.18,
        "mansion":      0.22,   # naik dari 0.18
        "dock":         0.25,   # naik dari 0.20
        "theater":      0.18,
        "beach":        0.15,
        "basement":     0.22,
    },
    3: {
        "island":       0.18,   # naik dari 0.15
        "prison_north": 0.23,
        "prison_south": 0.23,
        "mansion":      0.28,   # naik dari 0.25
        "dock":         0.35,   # naik dari 0.30
        "laboratory":   0.32,
    }
}

def should_spawn_enemy(location, chapter=1):
    """Check if enemy should spawn based on chapter"""
    # Safe zone adalah area aman — tidak ada enemy yang spawn di sini
    if location == 'safe_zone':
        return False
    chapter_rates = SPAWN_RATES.get(chapter, SPAWN_RATES[1])
    spawn_rate = chapter_rates.get(location, 0.10)
    return random.random() < spawn_rate

def get_all_boss_ids():
    """Get list of all boss IDs"""
    return list(BOSSES.keys())

def get_boss_count():
    """Get total number of bosses"""
    return len(BOSSES)



def scale_enemy_for_chapter(enemy, chapter, player_level=1):
    # Balance: Regular enemy scale with player level; boss HP fixed (no level scale)
    import copy
    e = copy.deepcopy(enemy)
    is_boss = e.get('boss', False)

    ch_factor = 1.0 + (max(1, int(chapter)) - 1) * 0.12
    if is_boss:
        # Boss: chapter scale only, no player_level scaling (HP already tuned)
        total = ch_factor
    else:
        # Regular enemy: scale with player level (+8% per level above 1)
        lv_factor = 1.0 + (max(1, int(player_level)) - 1) * 0.08
        total     = ch_factor * lv_factor

    e['hp']      = max(e.get('hp', 50),      int(e['hp'] * total))
    e['max_hp']  = e['hp']
    e['attack']  = max(e.get('attack', 10),  int(e['attack'] * total))
    e['defense'] = max(e.get('defense', 5),  int(e['defense'] * total))
    e['speed']   = max(e.get('speed', 10),   int(e['speed'] * total))
    e['xp']      = int(e.get('xp', 10) * (ch_factor if is_boss else total))
    return e


def create_enemy_instance(enemy_id, chapter=1, player_level=1):
    # Public: create enemy instance with chapter/level scaling + Hard Mode 1.2x
    if enemy_id in ENEMIES:
        base = ENEMIES[enemy_id].copy()
    elif enemy_id in BOSSES:
        base = BOSSES[enemy_id].copy()
    else:
        return None
    # Tambah variance kecil ±10%
    import random
    variance = random.uniform(0.90, 1.10)
    base['hp']     = int(base.get('hp', 50)     * variance)
    base['max_hp'] = base['hp']
    # Scale berdasarkan chapter/level
    return scale_enemy_for_chapter(base, chapter, player_level)



# Secret NPC Candala
CANDALA_NPC = {
    "id": "candala",
    "name": "Candala",
    "title": "The Witness in the Shadows",
    "intro": [
        "Candala: '...Saya sudah menunggu seseorang yang mau mendengar.'",
        "Candala: 'Saya tahu segalanya tentang tempat ini. Saya pernah bekerja di sini.'",
        "Candala: 'Telepon itu... kamu menemukannya. Berarti kamu sudah lihat.'",
        "Candala: 'Nama-nama dalam kontak itu... simpan baik-baik. Dunia perlu tahu.'",
    ],
    "secret_dialog": [
        "Candala: 'Ada ruangan yang tidak ada di peta resmi. Basement sub-level 2.'",
        "Candala: 'Di sana tersimpan semua rekaman asli. Jangan dibiarkan hancur.'",
        "Candala: 'Satu lagi... jika kamu bertemu seseorang bernama Maxwell di luar...'",
        "Candala: '...beritahu dia bahwa Candala masih ingat segalanya.'",
        "Candala: 'Sekarang pergi. Sebelum dia kembali.'",
        "*Candala menghilang ke sudut gelap. Hanya bayangan yang tersisa.*",
    ],
    "reward_flag": "candala_secret_obtained",
    "reward_item": "Rekaman Candala",
}
