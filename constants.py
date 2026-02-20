"""
CONSTANTS - Global constants untuk menghindari inkonsistensi data
"""

# Currency System
CURRENCY_NAME = "Dollars"
CURRENCY_SINGULAR = "Dollar"
CURRENCY_PLURAL = "Dollars"
CURRENCY_SHORT = "$"

# Monster Drops
BASE_MONEY_DROP = 10  # Base dollars dropped per enemy
BASE_XP_DROP = 25     # Base XP dropped per enemy

# Combat System
BASE_ATTACK = 10
BASE_DEFENSE = 10
BASE_SPEED = 10
BASE_HP = 100
BASE_ENERGY = 30

# Leveling System
BASE_XP_TO_LEVEL = 100
LEVEL_UP_HP_GAIN = 12
LEVEL_UP_ATTACK_GAIN = 2
LEVEL_UP_DEFENSE_GAIN = 2
LEVEL_UP_SPEED_GAIN = 1
LEVEL_UP_ENERGY_GAIN = 5
XP_SCALE_FACTOR = 1.15

# Terminal & Display
MIN_TERMINAL_WIDTH = 80
MIN_TERMINAL_HEIGHT = 24
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 24

# Game Settings
GAME_VERSION = "0.3"
SAVE_FILE = "data.txt"
CONFIG_FILE = "card_dialogs.json"

# Chapter System — 6 chapter total
MAX_CHAPTERS = 6
BOSS_CHAPTERS = [2, 4, 6]   # Chapter dengan boss battle
FINAL_CHAPTER = 6

# Boss identifiers per chapter
CHAPTER_BOSSES = {
    2: "kepala_penjaga",     # Head Guard — Ch2
    4: "agen_maxwell",       # Maxwell's Agent / Lieutenant — Ch4
    6: "epstein_boss",       # Jeffrey Epstein — Ch6 Final (matches enemies.py key)
}

# NPC Sidequest System (menggantikan party system)
# NPC tidak join party — mereka kasih KEY ITEM yang dibutuhkan main quest
NPC_IDS = ['haikaru', 'aolinh', 'arganta', 'ignatius', 'vio']
SIDEQUESTS_NEEDED_FOR_CH4 = 2   # Min sidequest selesai sebelum bisa ke Ch4
SIDEQUESTS_NEEDED_FOR_CH6 = 4   # Min sidequest selesai sebelum Ch6

# Party System — dipertahankan minimal untuk backward compat save file
MAX_PARTY_SIZE = 5
DEFAULT_PARTY_MEMBER_HP = 100

# Dialog & UI
FALLBACK_CARD_DIALOGS = {
    "attack": "Serang!",
    "defend": "Pertahanan!",
    "heal": "Pulihkan!",
    "special": "Kekuatan khusus!",
    "flee": "Melariiiii!",
    "default": "Aksi!",
}
