import random
import os
import sys
import time
from itertools import product
from sprites import Warna, SPRITES
from characters import get_character_intro, get_character_data
from constants import (LEVEL_UP_HP_GAIN, LEVEL_UP_ATTACK_GAIN,
                       LEVEL_UP_DEFENSE_GAIN, LEVEL_UP_SPEED_GAIN)

#  Exploration system - map navigation, enemy encounters, location tracking


try:
    from utils import clear_screen, flush_input
except ImportError:
    from contextlib import suppress
    
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def flush_input():
        with suppress(Exception):
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)


def _direction_arrow(px, py, tx, ty):
    #  Calculate 8-direction arrow from player to target
    """Kembalikan simbol panah 8-arah dari posisi player ke target."""
    dx = tx - px
    dy = ty - py
    if dx == 0 and dy == 0:
        return "●"
    ax, ay = abs(dx), abs(dy)
    if ax > ay * 2:
        return "→" if dx > 0 else "←"
    if ay > ax * 2:
        return "↓" if dy > 0 else "↑"
    if dx > 0 and dy < 0:
        return "↗"
    if dx > 0 and dy > 0:
        return "↘"
    return "↖" if dx < 0 and dy < 0 else "↙"


def _manhattan(px, py, tx, ty):
    #  Calculate Manhattan distance
    return abs(tx - px) + abs(ty - py)


def _distance_label(dist):
    if dist <= 3:
        return "sangat dekat!"
    if dist <= 7:
        return f"~{dist} langkah"
    return f"~{dist} langkah" if dist <= 12 else f"~{dist} langkah (jauh)"


class MapTile:
    def __init__(self, tile_type, walkable=True, description=""):
        self.type = tile_type
        self.walkable = walkable
        self.description = description


class GameMap:
    def __init__(self, map_id, width=25, height=18, current_player_char=None):
        self.map_id = map_id
        self.width = width
        self.height = height
        self.current_player_char = current_player_char
        self.tiles = [[MapTile(0, True, "Floor") for _ in range(width)] for _ in range(height)]
        self.player_x = width // 2
        self.player_y = height // 2
        self.enemies    = []
        self.npcs       = []
        self.items      = []
        self.exits      = []
        self.boss_doors = []
        self.discovered = {(self.player_x, self.player_y)}
        self.enemy_counter = 0

    def _validate_spawn_point(self, x, y):
        """
        Cari tile walkable terdekat dari (x, y).
        Dibatasi MAX_SEARCH_RADIUS=8 untuk cegah loop besar yang hang CPU.
        """
        MAX_SEARCH_RADIUS = 8  # Cukup untuk semua map 25x18
        if 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x].walkable:
            return x, y
        for radius in range(1, MAX_SEARCH_RADIUS + 1):
            for dx, dy in product(range(-radius, radius + 1), repeat=2):
                if abs(dx) != radius and abs(dy) != radius:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and self.tiles[ny][nx].walkable:
                    return nx, ny
        # Fallback mutlak: tengah peta
        return self.width // 2, self.height // 2


    def generate_island(self):
        for y in range(self.height):
            for x in range(self.width):
                if x < 2 or x >= self.width - 2 or y < 2 or y >= self.height - 2:
                    self.tiles[y][x] = MapTile(7, False, "Ocean")
                elif x < 3 or x >= self.width - 3 or y < 3 or y >= self.height - 3:
                    self.tiles[y][x] = MapTile(0, True, "Beach")
                else:
                    self.tiles[y][x] = MapTile(8 if random.random() < 0.25 else 0, True, "Path")

        self.create_path(self.width // 2, 3, self.width // 2, self.height - 3)
        self.create_path(3, self.height // 2, self.width - 3, self.height // 2)

        self.place_exit(7,  7,  "prison_north", "Penjara Utara")
        self.place_exit(18, 7,  "prison_south", "Penjara Selatan")
        self.place_exit(7,  13, "mansion",       "Mansion")
        self.place_exit(18, 13, "dock",          "Dermaga")
        self.place_exit(12, 5,  "safe_zone",     "Safe Zone - Toko Bran")
        # Exit ke area baru (chapter 2+)
        self.place_exit(12, 15, "theater",       "Teater")
        self.place_exit(3,  9,  "beach",         "Pantai")

        self.add_enemy_patrol(6,  6,  "guard_novice",  [(6,6),  (9,6),  (9,9),  (6,9)])
        self.add_enemy_patrol(19, 6,  "guard_veteran", [(19,6), (22,6), (22,9), (19,9)])

        # Di island hub (chapter 2), karakter lain mungkin terlihat
        # Haikaru di penjara utara, Aolinh di teater — jangan spawn di island
        self.place_item(10, 8, "Health Potion")
        self.place_item(15, 8, "Keycard Level 1")

        self.player_x, self.player_y = self._validate_spawn_point(12, 12)


    def generate_prison(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = MapTile(1, False, "Wall")
                else:
                    self.tiles[y][x] = MapTile(0, True, "Floor")

        for x in range(5, self.width - 5, 5):
            for y in range(5, self.height - 5, 5):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    self.tiles[y][x] = MapTile(6, False, "Pillar")

        for x in range(8, 17):
            if 0 < x < self.width - 1:
                self.tiles[9][x] = MapTile(1, False, "Cell")

        self.place_exit(12, 1, "island", "Keluar")
        self.add_enemy_patrol(8, 8, "guard_novice", [(8,8), (16,8), (16,10), (8,10)])
        # Haikaru ada di prison_north sebagai NPC untuk karakter lain
        # (place_npc() sudah otomatis skip jika npc_id == current_player_char)
        self.place_npc(10, 9, "haikaru")
        self.place_item(15, 9, "Med Kit")           # Haikaru: blind spot #1
        self.place_item(5,  4, "Keycard Level 1")   # Haikaru: blind spot #2
        self.place_item(18, 4, "Buku Catatan")       # Haikaru: blind spot #3

        self.player_x, self.player_y = self._validate_spawn_point(12, 3)


    def generate_mansion(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = MapTile(1, False, "Wall")
                elif x % 4 == 0 and y % 3 == 0:
                    if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                        self.tiles[y][x] = MapTile(6, False, "Column")
                else:
                    self.tiles[y][x] = MapTile(0, True, "Floor")

        self.place_exit(12, 1, "island", "Keluar")
        # Boss akan di-spawn setelah main quest chapter selesai (bukan saat map generate)

        self.add_enemy_patrol(8,  10, "guard_elite",       [(8,10),  (16,10)])
        self.add_enemy_patrol(16, 6,  "mercenary_sniper",  [(16,6),  (16,10)])

        self.place_item(18, 8, "Armor Vest")
        self.place_item(8,  6, "Keycard Level 1")    # Vio hack_terminal objective
        self.place_item(18, 12, "Access Card")        # Vio hack_terminal objective (ke-2)
        self.place_npc(10, 8, "ignatius")

        self.player_x, self.player_y = self._validate_spawn_point(12, 3)


    def generate_safe_zone(self):
        """
        Safe Zone — area aman tanpa musuh.
        Ada toko Bran Edwards dan beberapa item gratis.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = MapTile(1, False, "Tembok")
                elif (x in (4, self.width - 5)) or (y in (4, self.height - 5)):
                    self.tiles[y][x] = MapTile(8, True, "Tanaman")  # dekorasi
                else:
                    self.tiles[y][x] = MapTile(0, True, "Lantai Aman")

        # Blok counter / toko di tengah atas
        for x in range(9, 16):
            self.tiles[3][x] = MapTile(6, False, "Konter Toko")

        self.place_exit(12, self.height - 2, "island", "Kembali ke Pulau")

        # Bran Edwards — penjual
        self.npcs.append({'x': 12, 'y': 4, 'id': 'bran_edwards'})

        # Beberapa item gratis di safe zone
        self.place_item(5,  8,  "Health Potion")
        self.place_item(19, 8,  "Bandage")
        self.place_item(12, 12, "Info Pulau")

        self.player_x, self.player_y = self._validate_spawn_point(12, self.height - 4)


    def generate_dock(self):
        """
        Dock — area pelabuhan dengan musuh.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x < 10:
                    self.tiles[y][x] = MapTile(0, True, "Dock")
                    if y in (0, self.height - 1):
                        self.tiles[y][x] = MapTile(1, False, "Fence")
                else:
                    self.tiles[y][x] = MapTile(7, False, "Water")

        self.place_exit(1, self.height // 2, "island", "Keluar")

        self.place_item(4, 8,  "Health Potion")
        self.place_item(4, 10, "Med Kit")
        self.place_npc(5, 9, "arganta")

        self.player_x, self.player_y = self._validate_spawn_point(3, self.height // 2)


    def generate_theater(self):
        """Teater — lokasi Ao Lin. Berbeda dari penjara."""
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = MapTile(1, False, "Dinding Teater")
                else:
                    self.tiles[y][x] = MapTile(0, True, "Lantai")

        # Panggung di bagian atas
        for x in range(4, self.width - 4):
            for y in range(2, 6):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    self.tiles[y][x] = MapTile(0, True, "Panggung")
        for x in range(4, self.width - 4):
            if 0 < x < self.width - 1:
                self.tiles[6][x] = MapTile(6, False, "Tepi Panggung")

        # Kursi penonton
        for row_y in (8, 10, 12):
            for x in range(3, self.width - 3, 3):
                if 0 < x < self.width - 1 and row_y < self.height - 1:
                    self.tiles[row_y][x] = MapTile(6, False, "Kursi")

        self.place_exit(12, self.height - 2, "island", "Keluar Teater")
        # Aolinh berada di panggung teater — NPC bagi karakter non-Aolinh
        self.place_npc(12, 4, "aolinh")
        self.add_enemy_patrol(8, 13, "guard_novice",
                              [(8, 13), (16, 13), (16, 15), (8, 15)])
        self.place_item(3, 4,  "Health Potion")
        self.place_item(21, 4, "Bandage")
        self.player_x, self.player_y = self._validate_spawn_point(12, 9)


    def generate_beach(self):
        """Pantai — lokasi Arganta."""
        for y in range(self.height):
            for x in range(self.width):
                if y >= self.height - 4:
                    self.tiles[y][x] = MapTile(7, False, "Laut")
                elif y >= self.height - 6:
                    self.tiles[y][x] = MapTile(0, True, "Pantai Pasir")
                elif x == 0 or x == self.width - 1 or y == 0:
                    self.tiles[y][x] = MapTile(1, False, "Tebing")
                else:
                    self.tiles[y][x] = MapTile(8 if random.random() < 0.15 else 0, True, "Hutan Pantai")

        for px, py in [(2, 10), (3, 10), (2, 11), (3, 11)]:
            if 0 < px < self.width - 1 and 0 < py < self.height - 4:
                self.tiles[py][px] = MapTile(6, False, "Reruntuhan Perahu")

        self.place_exit(12, 1, "island", "Masuk Pulau")
        # Arganta di pantai — NPC bagi karakter non-Arganta
        self.place_npc(6, 10, "arganta")
        self.place_item(6, 9, "Health Potion")
        if self.current_player_char != "arganta":
            self.place_item(15, 9, "Kompas Nonno Arganta")
        self.add_enemy_patrol(10, 5, "guard_novice", [(10, 5), (18, 5), (18, 8), (10, 8)])
        self.player_x, self.player_y = self._validate_spawn_point(3, self.height - 6)


    def generate_basement(self):
        """Ruang elektrik bawah tanah — lokasi Ignatius."""
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = MapTile(1, False, "Beton")
                elif (x % 6 == 0 and y % 5 == 0 and
                      0 < x < self.width - 1 and 0 < y < self.height - 1):
                    self.tiles[y][x] = MapTile(6, False, "Panel Listrik")
                else:
                    self.tiles[y][x] = MapTile(0, True, "Lantai Beton")

        self.create_path(1, self.height // 2, self.width - 2, self.height // 2)
        self.create_path(self.width // 2, 1, self.width // 2, self.height - 2)

        self.place_exit(12, 1, "mansion", "Naik ke Mansion")
        # Ignatius ada di basement — NPC bagi karakter non-Ignatius
        self.place_npc(4, 4, "ignatius")
        self.place_item(4, 7, "Kapasitor Besar")
        self.place_item(20, 4, "Relay Switch")
        self.place_item(4, 12, "Copper Coil")
        self.place_item(18, 10, "EMP Prototype")     # Ignatius: sabotage_alarm_panel trigger
        self.add_enemy_patrol(10, 8, "guard_novice", [(10, 8), (14, 8)])
        self.player_x, self.player_y = self._validate_spawn_point(12, 3)


    def create_path(self, x1, y1, x2, y2):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= y < self.height and 0 <= x1 < self.width:
                    self.tiles[y][x1] = MapTile(0, True, "Path")
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= y1 < self.height and 0 <= x < self.width:
                    self.tiles[y1][x] = MapTile(0, True, "Path")


    def place_exit(self, x, y, dest, desc):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = MapTile(2, True, desc)
            self.exits.append({
                'x': x, 'y': y,
                'destination': dest,
                'locked': False, 'key': None,
                'description': desc
            })

    def place_boss_door(self, x, y, boss_id, desc):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = MapTile(9, True, desc)
            self.boss_doors.append({
                'x': x, 'y': y,
                'boss_id': boss_id,
                'locked': False,
                'description': desc
            })

    def _spawn_boss_for_chapter(self, chapter, char_id, gs):
        """Spawn bosses based on chapter and character.
        BUG FIX: ch1 boss sekarang selalu di-spawn di map yang sesuai (tidak butuh flag).
        Boss disesuaikan dengan CHARACTER_MAIN_QUESTS boss_id per karakter.
        """
        # Boss ch1 per karakter — sesuai dengan CHARACTER_MAIN_QUESTS
        CH1_BOSSES = {
            "vio":      ("maxwell_enforcer",  8, self.height // 2, "Maxwell Enforcer"),
            "haikaru":  ("warden_elite",      12, self.height - 3, "Warden Elite"),
            "aolinh":   ("theater_master",    12, 4,               "Theater Master"),
            "arganta":  ("harbor_captain",    8,  self.height // 2, "Harbor Captain"),
            "ignatius": ("security_bot",      12, self.height - 3, "Security Bot Mk-II"),
        }
        
        if chapter == 1:
            # BUG FIX: Selalu spawn boss ch1 — tidak perlu flag apapun
            # Cek map_id cocok dengan karakter (jangan spawn di map yang salah)
            CHAR_START_MAP = {
                "vio": "mansion", "haikaru": "prison_north",
                "aolinh": "theater", "arganta": "beach", "ignatius": "basement",
            }
            if char_id in CH1_BOSSES and self.map_id == CHAR_START_MAP.get(char_id):
                boss_id, boss_x, boss_y, boss_desc = CH1_BOSSES[char_id]
                if not any(d['boss_id'] == boss_id for d in self.boss_doors):
                    self.place_boss_door(boss_x, boss_y, boss_id, boss_desc)
        elif chapter == 2:
            if gs.story_flags.get('ch2_bosses_available', False):
                for boss_id, (boss_x, boss_y) in {('island_mid_boss', (11, 9)), ('prison_south_boss', (12, 14))}:
                    if all(d['boss_id'] != boss_id for d in self.boss_doors):
                        self.place_boss_door(boss_x, boss_y, boss_id, "BOSS")
        elif chapter == 3:
            if gs.story_flags.get('final_bosses_available', False):
                for boss_id, (boss_x, boss_y) in {('doctor_rousseau', (10, 7)), ('mysterious_benefactor', (14, 11))}:
                    if all(d['boss_id'] != boss_id for d in self.boss_doors):
                        self.place_boss_door(boss_x, boss_y, boss_id, "BOSS")
                if all(d['boss_id'] != 'epstein_boss' for d in self.boss_doors):
                    self.place_boss_door(self.width // 2, self.height // 2, "epstein_boss", "FINAL BOSS")

    def check_and_spawn_bosses(self, gs):
        """Check and spawn bosses based on chapter and character."""
        char_id = gs.player_character
        chapter = int(gs.story_flags.get('current_chapter', 1))
        self._spawn_boss_for_chapter(chapter, char_id, gs)

    def add_enemy_patrol(self, x, y, enemy_id, path=None):
        """Tambahkan enemy yang DIAM di tempat (stay). Path diabaikan untuk cegah bug render."""
        sx, sy = self._validate_spawn_point(x, y)
        self.enemies.append({
            'x': sx, 'y': sy,
            'id': enemy_id,
            'path': [],       # Selalu kosong — musuh STAY, tidak patrol
            'path_index': 0,
            'counter': 0
        })

    def place_npc(self, x, y, npc_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.current_player_char and npc_id == self.current_player_char:
                return
            # Validate that NPC is not placed on unwalkable tile
            if self.tiles[y][x].walkable:
                self.npcs.append({'x': x, 'y': y, 'id': npc_id})
            else:
                # If placement invalid, find nearest valid spot
                valid_spot = self._validate_spawn_point(x, y)
                if valid_spot:
                    self.npcs.append({'x': valid_spot[0], 'y': valid_spot[1], 'id': npc_id})

    def place_item(self, x, y, item):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.items.append({'x': x, 'y': y, 'item': item})


    def attempt_move(self, dx, dy, gs):
        nx = self.player_x + dx
        ny = self.player_y + dy

        if not (0 <= nx < self.width and 0 <= ny < self.height):
            return None

        if not self.tiles[ny][nx].walkable:
            return None

        for exit_data in self.exits:
            if (nx, ny) == (exit_data['x'], exit_data['y']):
                self.player_x, self.player_y = nx, ny
                self.discovered.add((nx, ny))
                return {
                    'type': 'exit',
                    'destination': exit_data['destination'],
                    'locked': exit_data['locked'],
                    'key': exit_data['key']
                }

        for door in self.boss_doors:
            if (nx, ny) == (door['x'], door['y']):
                self.player_x, self.player_y = nx, ny
                self.discovered.add((nx, ny))
                return {'type': 'boss', 'boss_id': door['boss_id'], 'locked': door['locked']}

        for npc in self.npcs:
            if (nx, ny) == (npc['x'], npc['y']):
                self.player_x, self.player_y = nx, ny
                self.discovered.add((nx, ny))
                return {'type': 'npc', 'npc_id': npc['id']}

        for item in list(self.items):
            if (nx, ny) == (item['x'], item['y']):
                self.items.remove(item)
                self.player_x, self.player_y = nx, ny
                self.discovered.add((nx, ny))
                return {'type': 'item', 'item': item['item']}

        for enemy in self.enemies:
            if (nx, ny) == (enemy['x'], enemy['y']):
                from enemies import create_enemy_instance
                if ei := create_enemy_instance(enemy['id']):
                    self.player_x, self.player_y = nx, ny
                    self.discovered.add((nx, ny))
                    return {'type': 'enemy', 'enemy': ei}

        self.player_x, self.player_y = nx, ny
        self.discovered.add((nx, ny))

        return {'type': 'move'}


    def add_boss_enemy(self, x, y, enemy_id):
        """Tambahkan boss enemy yang diam (stay) — tidak patrol, tidak chase."""
        self.enemies.append({
            'x': x, 'y': y,
            'id': enemy_id,
            'path': [],         # kosong = tidak patrol
            'path_index': 0,
            'counter': 0,
            'is_boss': True,    # boss: stay only, tidak chase
        })

    def update_enemies(self):
        """
        AI musuh: STAY sistem.
        - Semua musuh DIAM di tempat (tidak patrol, tidak chase)
        - Return None karena tidak ada gerakan aktif musuh
        - Encounter hanya terjadi saat player bergerak menuju musuh (via attempt_move)
        """
        # Musuh sepenuhnya statis — tidak ada gerakan, tidak ada chase
        # Ini mencegah bug render posisi ganda dan memudahkan tracking no-respawn
        return None


    def _build_main_quest_lines(self, main_quests, gs=None):
        """Build main quest display lines.
        
        Untuk Ch1 quest: tampilkan SEMUA objective dengan progress bar masing-masing
        (baca dari story_flags agar akurat terlepas urutan pengumpulan item).
        Untuk chapter lain: tampilkan step linear seperti biasa.
        """
        if not main_quests:
            return []
        mq       = main_quests[0]
        quest_id = mq.get('id', '')

        lines = [("quest", f"[M] {mq['title']}")]

        # ── Ch1: per-objective progress dari story_flags ─────────────────────
        _current_chapter = int(gs.story_flags.get('current_chapter', 1))
        if _current_chapter == 1 and gs is not None:
            try:
                from character_routes import get_ch1_objective_status
                obj_statuses = get_ch1_objective_status(gs)
                if obj_statuses:
                    for obj_id, desc, cur, tot, done in obj_statuses:
                        bar    = '■' * cur + '□' * max(0, tot - cur)
                        prefix = '✓' if done else '◐'
                        color_tag = "done" if done else "prog"
                        lines.append((color_tag, f"  └ {prefix} {desc}"))
                        lines.append((color_tag, f"      [{bar}] {cur}/{tot}"))
                    return lines
            except Exception:
                pass

        # ── Fallback: tampilkan step linear berdasarkan progress ──────────────
        prog   = mq.get("progress", 0)
        total  = mq.get("total", 1)
        bar    = "■" * prog + "□" * (total - prog)
        targets = mq.get("targets", [])
        if targets and prog < len(targets):
            current_step = targets[prog]
        elif targets and prog >= len(targets):
            current_step = targets[-1] + " ✓"
        else:
            current_step = mq.get("objective", "")
        lines.append(("prog", f"  └ {current_step}"))
        lines.append(("prog", f"    [{bar}] {prog}/{total}"))
        return lines

    def _build_tracker_lines(self, gs):
        """
        Quest Tracker HUD:
        - Main quest (per karakter/chapter) + progress step
        - Sidequest NPC aktif dengan label [S]
        - Target terdekat (boss, NPC, item, pintu)
        """
        lines = []
        chapter_obj = gs.get_chapter_objective()
        lines.append(("obj", chapter_obj))

        main_quests = [q for q in gs.active_quests if q.get("quest_type") != "side"]
        side_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
        
        lines.extend(self._build_main_quest_lines(main_quests, gs=gs))

        # Sidequest NPC aktif — semua pakai [S]
        for sq in side_quests[:2]:
            sq_prog  = sq.get("progress", 0)
            sq_total = sq.get("total", 1)
            sq_bar   = "■" * sq_prog + "□" * (sq_total - sq_prog)
            lines.extend([
                ("side", f"[S] {sq['title']}  [{sq_bar}] {sq_prog}/{sq_total}"),
                ("prog", f"  └ {sq['objective']}")
            ])

        # Target terdekat
        targets = []

        for npc in self.npcs:
            dist = _manhattan(self.player_x, self.player_y, npc['x'], npc['y'])
            arrow = _direction_arrow(self.player_x, self.player_y, npc['x'], npc['y'])
            try:
                from characters import get_character_name
                name = get_character_name(npc['id'])
            except Exception:
                name = npc['id'].capitalize()
            targets.append((dist, "npc", f"{arrow} NPC: {name} ({_distance_label(dist)})"))

        for door in self.boss_doors:
            dist  = _manhattan(self.player_x, self.player_y, door['x'], door['y'])
            arrow = _direction_arrow(self.player_x, self.player_y, door['x'], door['y'])
            targets.append((dist, "boss", f"{arrow} BOSS: {door.get('description','?')} ({_distance_label(dist)})"))

        for item in self.items:
            dist  = _manhattan(self.player_x, self.player_y, item['x'], item['y'])
            arrow = _direction_arrow(self.player_x, self.player_y, item['x'], item['y'])
            targets.append((dist, "item", f"{arrow} Item: {item['item']} ({_distance_label(dist)})"))

        for exit_d in self.exits:
            dist  = _manhattan(self.player_x, self.player_y, exit_d['x'], exit_d['y'])
            arrow = _direction_arrow(self.player_x, self.player_y, exit_d['x'], exit_d['y'])
            targets.append((dist, "exit", f"{arrow} Pintu: {exit_d['description']} ({_distance_label(dist)})"))

        targets.sort(key=lambda t: t[0])
        lines.extend((kind, label) for _, kind, label in targets[:4])

        return lines


    def render(self, gs):
        """Render peta + Quest Tracker HUD."""
        # Check apakah boss perlu di-spawn berdasarkan quest completion
        self.check_and_spawn_bosses(gs)
        
        clear_screen()

        vw, vh = 23, 15
        cx = max(0, min(self.player_x - vw // 2, self.width  - vw))
        cy = max(0, min(self.player_y - vh // 2, self.height - vh))

        map_name = self.map_id.upper().replace('_', ' ')
        hp_bar_filled = max(0, int((gs.hp / max(gs.max_hp, 1)) * 10))
        hp_bar = f"{Warna.HIJAU}{'█' * hp_bar_filled}{Warna.MERAH}{'░' * (10 - hp_bar_filled)}{Warna.RESET}"
        
        energy      = getattr(gs, 'energy', 0)
        max_energy  = getattr(gs, 'max_energy', 20)
        en_filled   = max(0, int((energy / max(max_energy, 1)) * 10))
        en_bar      = f"{Warna.CYAN}{'█' * en_filled}{Warna.ABU_GELAP}{'░' * (10 - en_filled)}{Warna.RESET}"

        chapter  = int(gs.story_flags.get('current_chapter', 1))
        sq_done  = len(getattr(gs, 'completed_quests', []))
        sq_total    = 5  # Total NPC sidequest tersedia
        print(f"\n{Warna.CYAN + Warna.TERANG}{map_name}{Warna.RESET}  "
              f"HP:{hp_bar}{gs.hp}/{gs.max_hp}  "
              f"{Warna.CYAN}EN:{en_bar}{energy}/{max_energy}{Warna.RESET}  "
              f"Lv:{Warna.KUNING}{gs.level}{Warna.RESET}  "
              f"Ch:{Warna.KUNING}{chapter}{Warna.RESET}  "
              f"[S]:{Warna.CYAN}{sq_done}/{sq_total}{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{'─' * 65}{Warna.RESET}")
        print()

        for y in range(cy, min(cy + vh, self.height)):
            print("  ", end="")
            for x in range(cx, min(cx + vw, self.width)):
                if x == self.player_x and y == self.player_y:
                    print(f"{Warna.HIJAU + Warna.TERANG}@ {Warna.RESET}", end="")
                    continue

                rendered = False

                for enemy in self.enemies:
                    if x == enemy['x'] and y == enemy['y']:
                        print(f"{Warna.MERAH}E {Warna.RESET}", end="")
                        rendered = True
                        break

                if not rendered:
                    for npc in self.npcs:
                        if x == npc['x'] and y == npc['y']:
                            print(f"{Warna.CYAN}N {Warna.RESET}", end="")
                            rendered = True
                            break

                if not rendered:
                    for item in self.items:
                        if x == item['x'] and y == item['y']:
                            print(f"{Warna.KUNING}I {Warna.RESET}", end="")
                            rendered = True
                            break

                if not rendered:
                    for exit_d in self.exits:
                        if x == exit_d['x'] and y == exit_d['y']:
                            print(f"{Warna.HIJAU}>{Warna.RESET} ", end="")
                            rendered = True
                            break

                if not rendered:
                    for door in self.boss_doors:
                        if x == door['x'] and y == door['y']:
                            print(f"{Warna.MERAH}B {Warna.RESET}", end="")
                            rendered = True
                            break

                if not rendered:
                    tile = self.tiles[y][x]
                    if tile.type in SPRITES:
                        char, color, _ = SPRITES[tile.type]
                        print(f"{color}{char[0]} {Warna.RESET}", end="")
                    else:
                        print("  ", end="")
            print()

        print(f"\n{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}")

        tracker_lines = self._build_tracker_lines(gs)

        COLOR_MAP = {
            "obj":       Warna.KUNING + Warna.TERANG,
            "quest":     Warna.PUTIH,
            "prog":      Warna.ABU_GELAP,
            "done":      Warna.HIJAU,
            "side":      Warna.HIJAU + Warna.TERANG,
            "side_prog": Warna.ABU_GELAP,
            "npc":       Warna.CYAN,
            "boss":      Warna.MERAH + Warna.TERANG,
            "item":      Warna.KUNING,
            "exit":      Warna.HIJAU,
        }

        PROXIMITY_KINDS = {"npc", "boss", "item", "exit"}

        print(f"{Warna.KUNING + Warna.TERANG}◈ QUEST TRACKER{Warna.RESET}  "              f"{Warna.ABU_GELAP}[M]=Main Quest  [S]=Sidequest NPC{Warna.RESET}")
        if tracker_lines:
            # Pisahkan baris quest (obj/quest/prog/done/side) dari proximity (npc/boss/item/exit)
            quest_lines     = [(k, v) for k, v in tracker_lines if k not in PROXIMITY_KINDS]
            proximity_lines = [(k, v) for k, v in tracker_lines if k in PROXIMITY_KINDS]

            for kind, label in quest_lines:
                col = COLOR_MAP.get(kind, Warna.PUTIH)
                if kind == "obj":
                    print(f"  {col}✦ [O] {label}{Warna.RESET}")
                elif kind in ("quest", "side"):
                    print(f"  {col}└ {label}{Warna.RESET}")
                else:
                    print(f"  {col}{label}{Warna.RESET}")

            if proximity_lines:
                print(f"  {Warna.ABU_GELAP}Terdekat:{Warna.RESET}")
                for kind, label in proximity_lines[:4]:
                    col = COLOR_MAP.get(kind, Warna.PUTIH)
                    print(f"    {col}{label}{Warna.RESET}")

        print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}")

        legend = (
            f"{Warna.HIJAU}@{Warna.RESET}=Kamu "
            f"{Warna.CYAN}N{Warna.RESET}=NPC "
            f"{Warna.KUNING}I{Warna.RESET}=Item "
            f"{Warna.MERAH}E{Warna.RESET}=Musuh "
            f"{Warna.MERAH}B{Warna.RESET}=Boss "
            f"{Warna.HIJAU}>{Warna.RESET}=Pintu"
        )
        print(f"  {legend}")
        print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}")


def create_game_map(map_id, gs=None):
    # Membuat instance peta game berdasarkan map_id
    """Buat map berdasarkan ID."""
    current_char = gs.player_character if gs else None
    gm = GameMap(map_id, current_player_char=current_char)

    if map_id == "island":
        gm.generate_island()
    elif map_id in ("prison_north", "prison_south"):
        gm.generate_prison()
    elif map_id == "mansion":
        gm.generate_mansion()
    elif map_id == "dock":
        gm.generate_dock()
    elif map_id == "safe_zone":
        gm.generate_safe_zone()
    elif map_id == "theater":
        gm.generate_theater()
    elif map_id == "beach":
        gm.generate_beach()
    elif map_id == "basement":
        gm.generate_basement()
    else:
        gm.generate_island()

    if gs and gs.story_flags.get('start_x') is not None:
        sx = gs.story_flags['start_x']
        sy = gs.story_flags['start_y']
        if (0 <= sx < gm.width and 0 <= sy < gm.height
                and gm.tiles[sy][sx].walkable):
            gm.player_x = sx
            gm.player_y = sy
        del gs.story_flags['start_x']
        del gs.story_flags['start_y']

    # Filter musuh yang sudah dikalahkan agar tidak respawn
    if gs:
        defeated_set = set(gs.defeated_enemies) if isinstance(gs.defeated_enemies, list) else gs.defeated_enemies
        gm.enemies = [
            e for e in gm.enemies
            if f"{map_id}:{e['x']}:{e['y']}" not in defeated_set
        ]

    return gm


def loop_eksplorasi(gs, gm):
    # Menjalankan loop eksplorasi utama (navigasi, encounter, interaksi)
    """Loop utama eksplorasi — handle movement dan interaksi."""

    taken_key = f"items_taken_{gm.map_id}"
    taken_items = set(gs.story_flags.get(taken_key, []))
    gm.items = [it for it in gm.items if f"{it['x']},{it['y']}" not in taken_items]

    # Selalu inisialisasi quest — add_quest() sudah cek duplikat secara internal
    # Ini memastikan main quest chapter baru langsung muncul setelah advance chapter
    _init_location_quests(gs, gm.map_id)

    # Input ghosting prevention: buffer clearing + consistent frame timing
    FRAME_TIME = 0.05  # ~20 FPS for input responsiveness
    last_frame_time = time.time()

    while True:
        try:
            # Frame timing to prevent input buildup
            current_time = time.time()
            elapsed = current_time - last_frame_time
            if elapsed < FRAME_TIME:
                time.sleep(FRAME_TIME - elapsed)
            last_frame_time = time.time()

            gm.render(gs)
            if triggered := gm.update_enemies():
                from enemies import create_enemy_instance
                if ei := create_enemy_instance(triggered['id']):
                    ghost_result = {'type': 'enemy', 'enemy': ei}
                    if ret := handle_hasil(ghost_result, gs, gm):
                        return ret
                    continue

            print(f"\n{Warna.ABU_GELAP}W/A/S/D=Gerak | I=Barang | Q=Quest NPC | B=Toko Bran | X=Simpan | ESC=Keluar{Warna.RESET}")

            # Clear input buffer BEFORE reading to prevent ghosting
            flush_input()
            cmd = input(f"{Warna.CYAN}> {Warna.RESET}").strip().lower()

            if not cmd:
                continue

            hasil = None
            if cmd == 'w':
                hasil = gm.attempt_move(0, -1, gs)
            elif cmd == 's':
                hasil = gm.attempt_move(0, 1, gs)
            elif cmd == 'a':
                hasil = gm.attempt_move(-1, 0, gs)
            elif cmd == 'd':
                hasil = gm.attempt_move(1, 0, gs)
            if hasil and hasil.get('type') == 'item':
                coord_key = f"{gm.player_x},{gm.player_y}"
                taken_items.add(coord_key)
                gs.story_flags[taken_key] = list(taken_items)
                if gs.update_quest_progress("collect_items"):
                    gs.complete_quest("collect_items")

            if hasil:
                if ret := handle_hasil(hasil, gs, gm):
                    return ret

            if cmd == 'i':
                tampilkan_inventory(gs)
            elif cmd == 'q':
                tampilkan_npc_quests(gs)
            elif cmd == 'b':
                # Bran's Shop — bisa diakses dari mana saja via radio/signal
                _buka_toko_bran_remote(gs)
            elif cmd == 'x':
                save_menu(gs)
            elif cmd in ('esc', 'e'):
                if konfirmasi_quit():
                    return 'quit'

        except KeyboardInterrupt:
            if konfirmasi_quit():
                return 'quit'
        except Exception as e:
            print(f"{Warna.MERAH}Error: {e}{Warna.RESET}")
            time.sleep(1)


def _init_location_quests(gs, gm_map_id):
    """
    Inisialisasi quest berdasarkan progress karakter.
    - Main quest: dari CHARACTER_MAIN_QUESTS — tiap chapter ada boss unik
    - Sidequest NPC: dikelola oleh npc_interactions.py saat player bertemu NPC
    """
    try:
        from characters import CHARACTER_MAIN_QUESTS
    except ImportError:
        CHARACTER_MAIN_QUESTS = {}

    chapter = gs.story_flags.get("current_chapter", 1)
    try:
        chapter = int(chapter)
    except (ValueError, TypeError):
        chapter = 1

    char_id = gs.player_character
    char_quests = CHARACTER_MAIN_QUESTS.get(char_id, {})
    if quest_data := char_quests.get(chapter):
        steps = quest_data.get("steps", [quest_data["objective"]])
        gs.add_quest(
            quest_data["id"],
            quest_data["title"],
            quest_data["objective"],
            targets=steps,
            location=gm_map_id,
            quest_type="main",
        )
    else:
        # Fallback jika karakter tidak ada di dict
        gs.add_quest(
            f"ch{chapter}_escape",
            f"Chapter {chapter}: Bertahan dan maju",
            "Kalahkan boss di chapter ini untuk lanjut",
            targets=["boss"],
            location=gm_map_id,
            quest_type="main",
        )

    # Sync HUD progress untuk Ch1 agar akurat bahkan setelah load game
    if chapter == 1:
        try:
            from character_routes import sync_ch1_quest_hud
            sync_ch1_quest_hud(gs)
        except Exception:
            pass

    # Sidequest NPC dikelola sepenuhnya oleh npc_interactions.py.
    # Quest muncul di HUD saat player pertama kali bertemu NPC (via interaksi_npc).


def _add_recruit_quest_on_meet(gs, npc_id):
    """
    DEPRECATED — sistem rekrutmen party sudah dihapus.
    NPC hanya hadir dalam story dan memberi sidequest reward.
    Fungsi ini dipertahankan sebagai stub untuk backward compat save file.
    """
    pass  # No-op: party recruitment removed


def handle_hasil(hasil, gs, gm):
    """Handle hasil dari movement dan interaksi."""
    if not hasil:
        return None

    try:
        if hasil['type'] == 'enemy':
            from combat import run_combat
            from characters import get_character_name, get_character_data

            char_data = get_character_data(gs.player_character) or {}
            player_stats = {
                'name':         get_character_name(gs.player_character),
                'hp':           gs.hp,
                'max_hp':       gs.max_hp,
                'attack':       gs.attack,
                'defense':      gs.defense,
                'speed':        gs.speed,
                'level':        gs.level,
                'character_id': gs.player_character,
                # FIX: skill dari karakter, bukan story_flags yang selalu kosong
                'skills':       char_data.get('skills', {}),
                'energy':       getattr(gs, 'energy', 20),
                'max_energy':   getattr(gs, 'max_energy', 20),
                'bonus_discard_tokens': gs.story_flags.pop('bonus_discard_tokens', 0),
                'stats': {
                    'hp':       gs.hp,
                    'max_hp':   gs.max_hp,
                    'attack':   gs.attack,
                    'defense':  gs.defense,
                    'speed':    gs.speed
                }
            }

            # FIX: konversi party_members (list ID string) → list dict yang dibutuhkan combat
            party_dicts = []
            for mid in gs.party_members:
                if mid in gs.party_data:
                    pd = gs.party_data[mid]
                    party_dicts.append({
                        'name':    pd.get('name', mid),
                        'hp':      pd.get('hp', pd.get('max_hp', 100)),
                        'max_hp':  pd.get('max_hp', 100),
                        'attack':  pd.get('attack', 10),
                        'defense': pd.get('defense', 10),
                        'speed':   pd.get('speed', 10),
                        'skills':  pd.get('skills', {}),
                        'stats': {
                            'hp':      pd.get('max_hp', 100),
                            'attack':  pd.get('attack', 10),
                            'defense': pd.get('defense', 10),
                        },
                        '_id': mid,
                    })

            ret = run_combat(player_stats, hasil['enemy'], gs.inventory, party_dicts)

            # HP dan energy di-sync balik setelah combat
            gs.hp = max(0, player_stats.get('hp', gs.hp))
            if hasattr(gs, 'energy'):
                gs.energy = max(0, player_stats.get('energy', gs.energy))

            if ret == 'victory':
                gs.battles_won += 1
                # Hapus enemy yang sudah kalah dari peta supaya tidak bisa fight lagi
                px, py = gm.player_x, gm.player_y
                gm.enemies = [
                    e for e in gm.enemies
                    if (e['x'] != px or e['y'] != py)
                ]
                # Simpan key agar tidak respawn saat map dibuat ulang
                defeat_key = f"{gm.map_id}:{px}:{py}"
                if defeat_key not in gs.defeated_enemies:
                    gs.defeated_enemies.append(defeat_key)

                # Update kill counter untuk quest "kalahkan musuh"
                enemy_id = hasil['enemy'].get('id', '')
                gs.story_flags[f'kill_{enemy_id}'] = gs.story_flags.get(f'kill_{enemy_id}', 0) + 1
                gs.story_flags['total_kills'] = gs.story_flags.get('total_kills', 0) + 1
                # Aolinh sidequest: kalahkan penjaga theater (enemy apapun di map theater)
                if gm.map_id == 'theater' or 'theater' in gm.map_id.lower():
                    gs.story_flags['defeat_theater_guard'] = True
                # Update quest progress jika ada quest kill aktif
                if gs.update_quest_progress("defeat_enemies"):
                    gs.complete_quest("defeat_enemies")
                if gs.update_quest_progress(f"defeat_{enemy_id}"):
                    gs.complete_quest(f"defeat_{enemy_id}")

                # Ch1 combat objective tracking
                if int(gs.story_flags.get('current_chapter', 1)) == 1:
                    try:
                        from character_routes import (
                            get_ch1_quest, update_ch1_objective,
                            check_ch1_objective_progress, display_ch1_completion,
                            sync_ch1_quest_hud,
                            get_ch1_objective_complete_dialog,
                            get_ch1_next_objective_dialog,
                            get_ch1_next_incomplete_objective,
                        )
                        q_data = get_ch1_quest(gs.player_character)
                        if q_data:
                            for obj in q_data['objectives']:
                                if obj.get('type') == 'combat':
                                    pre_cur, tot = check_ch1_objective_progress(gs, obj['id'])
                                    if pre_cur < tot:
                                        update_ch1_objective(gs, obj['id'], 1)
                                        cur2, tot2 = check_ch1_objective_progress(gs, obj['id'])
                                        bar = '■' * cur2 + '□' * max(0, tot2 - cur2)

                                        # Dialog progres per karakter
                                        _win_dialogs = {
                                            'vio':      f"Vio: Penjaga dinetralisir. {cur2}/{tot2}.",
                                            'haikaru':  f"Haikaru: {cur2}/{tot2} penjaga dinetralkan. Sesuai kalkulasi.",
                                            'aolinh':   f"Aolinh: Aku bisa melakukan ini! {cur2}/{tot2} ✓",
                                            'arganta':  f"Arganta: Per Nonno. {cur2}/{tot2} patroli dilumpuhkan.",
                                            'ignatius': f"Ignatius: {cur2}/{tot2} down.",
                                        }
                                        msg = _win_dialogs.get(gs.player_character, f"{cur2}/{tot2} dikalahkan")
                                        icon = '✓' if cur2 >= tot2 else '◐'
                                        print(f"\n  {Warna.KUNING}{msg}{Warna.RESET}")
                                        print(f"  {Warna.CYAN}{icon} {obj['desc']}: [{bar}] {cur2}/{tot2}{Warna.RESET}")
                                        time.sleep(1.2)

                                        # Objective baru selesai?
                                        if cur2 >= tot2:
                                            comp_dialogs = get_ch1_objective_complete_dialog(
                                                gs.player_character, obj['id'])
                                            if comp_dialogs:
                                                print()
                                                for line in comp_dialogs:
                                                    print(f"  {Warna.HIJAU}{line}{Warna.RESET}")
                                                time.sleep(1.5)

                                            from character_routes import check_ch1_complete
                                            if check_ch1_complete(gs):
                                                display_ch1_completion(gs)
                                            else:
                                                next_obj_id, _ = get_ch1_next_incomplete_objective(gs)
                                                if next_obj_id:
                                                    next_dialogs = get_ch1_next_objective_dialog(
                                                        gs.player_character, next_obj_id)
                                                    if next_dialogs:
                                                        print()
                                                        for line in next_dialogs:
                                                            print(f"  {Warna.KUNING}{line}{Warna.RESET}")
                                                        time.sleep(1.5)
                                        break
                    except Exception:
                        pass

                xp_gain = hasil['enemy'].get('xp', 10)
                if leveled := gs.gain_xp(xp_gain):
                    # Tampilkan gains per-karakter (bukan flat constants)
                    gains = getattr(gs, 'level_up_gains', {})
                    hp_g  = gains.get('hp',      LEVEL_UP_HP_GAIN)
                    atk_g = gains.get('attack',  LEVEL_UP_ATTACK_GAIN)
                    def_g = gains.get('defense', LEVEL_UP_DEFENSE_GAIN)
                    spd_g = gains.get('speed',   LEVEL_UP_SPEED_GAIN)
                    print(f"\n{Warna.KUNING}{'═' * 50}{Warna.RESET}")
                    print(f"{Warna.KUNING + Warna.TERANG}  ⭐ LEVEL UP! ⭐  Sekarang Level {gs.level}{Warna.RESET}")
                    print(f"{Warna.HIJAU}  HP Maks: +{hp_g}  ATK: +{atk_g}  DEF: +{def_g}  SPD: +{spd_g}{Warna.RESET}")
                    print(f"{Warna.CYAN}  Stats baru: HP {gs.max_hp} | ATK {gs.attack} | DEF {gs.defense} | SPD {gs.speed}{Warna.RESET}")
                    print(f"{Warna.KUNING}{'═' * 50}{Warna.RESET}")
                    time.sleep(2.5)

                # Reward Dollar
                dollar_drop = hasil['enemy'].get('dollars', 0)
                if dollar_drop > 0:
                    bonus = random.randint(0, dollar_drop // 3)  # sedikit random bonus
                    earned = dollar_drop + bonus
                    # Cek lucky charm aktif
                    if gs.story_flags.pop('luck_boost_active', False):
                        earned = int(earned * 1.25)
                        print(f"  {Warna.KUNING}🍀 Lucky Charm aktif! Bonus dollar!{Warna.RESET}")
                    gs.dollars += earned
                    print(f"  {Warna.KUNING}💵 +${earned} (Total: ${gs.dollars}){Warna.RESET}")
                    time.sleep(1)

            elif ret == 'player_dead':
                return 'game_over'

            from characters import check_candala_encounter
            check_candala_encounter(gs)

        elif hasil['type'] == 'npc':
            interaksi_npc(hasil['npc_id'], gs, gm)

        elif hasil['type'] == 'item':
            item_name = hasil['item']
            gs.add_item(item_name)
            print(f"\n{Warna.HIJAU}✓ Dapat: {item_name}!{Warna.RESET}")
            time.sleep(0.5)

            # Ch1: cek apakah item ini trigger objective progress
            if int(gs.story_flags.get('current_chapter', 1)) == 1:
                try:
                    from character_routes import (
                        get_ch1_item_objective, update_ch1_objective,
                        check_ch1_objective_progress, get_ch1_quest,
                        display_ch1_completion, sync_ch1_quest_hud,
                        get_ch1_objective_complete_dialog,
                        get_ch1_next_objective_dialog,
                        get_ch1_next_incomplete_objective,
                    )
                    result = get_ch1_item_objective(gs.player_character, item_name)
                    if result:
                        obj_id, obj_dialog = result

                        # Baca progress SEBELUM update untuk deteksi "baru selesai"
                        q_data = get_ch1_quest(gs.player_character)
                        obj_def = next(
                            (o for o in q_data['objectives'] if o['id'] == obj_id), None
                        ) if q_data else None
                        pre_cur = gs.story_flags.get(f"ch1_obj_{obj_id}", 0)
                        pre_done = obj_def and pre_cur >= obj_def['target']

                        # Dialog karakter saat ambil item
                        print(f"\n  {Warna.KUNING}{obj_dialog}{Warna.RESET}")
                        time.sleep(1.2)

                        # Update progress + sync HUD
                        quest_done = update_ch1_objective(gs, obj_id, 1)

                        # Tampilkan progress bar objective ini
                        if obj_def:
                            cur, tot = check_ch1_objective_progress(gs, obj_id)
                            bar = '■' * cur + '□' * max(0, tot - cur)
                            icon = '✓' if cur >= tot else '◐'
                            print(f"  {Warna.CYAN}{icon} {obj_def['desc']}: "
                                  f"[{bar}] {cur}/{tot}{Warna.RESET}")
                            time.sleep(0.8)

                        # Cek apakah objective ini BARU SAJA selesai
                        post_cur = gs.story_flags.get(f"ch1_obj_{obj_id}", 0)
                        just_done = (not pre_done) and obj_def and (post_cur >= obj_def['target'])

                        if just_done:
                            # Dialog completion objective
                            comp_dialogs = get_ch1_objective_complete_dialog(
                                gs.player_character, obj_id)
                            if comp_dialogs:
                                print()
                                for line in comp_dialogs:
                                    print(f"  {Warna.HIJAU}{line}{Warna.RESET}")
                                time.sleep(1.5)

                            # Jika seluruh quest belum selesai, tampilkan intro objective berikut
                            if not quest_done:
                                next_obj_id, _ = get_ch1_next_incomplete_objective(gs)
                                if next_obj_id:
                                    next_dialogs = get_ch1_next_objective_dialog(
                                        gs.player_character, next_obj_id)
                                    if next_dialogs:
                                        print()
                                        for line in next_dialogs:
                                            print(f"  {Warna.KUNING}{line}{Warna.RESET}")
                                        time.sleep(1.5)

                        if quest_done:
                            display_ch1_completion(gs)
                except Exception:
                    pass

        elif hasil['type'] == 'exit':
            if hasil['locked']:
                print(f"\n{Warna.MERAH}Terkunci! Perlu: {hasil['key']}{Warna.RESET}")
                time.sleep(1)
            else:
                dest = hasil['destination']
                # Cek akses berdasarkan chapter
                from character_routes import can_access_location
                chapter = int(gs.story_flags.get('current_chapter', 1))
                if not can_access_location(gs.player_character, dest, chapter):
                    # Tentukan chapter berapa lokasi ini terbuka
                    from character_routes import get_chapter_locations
                    unlock_ch = None
                    for ch in (1, 2, 3):
                        locs = get_chapter_locations(ch)
                        all_locs = locs.get('all', locs.get(gs.player_character, []))
                        if dest in all_locs:
                            unlock_ch = ch
                            break
                    if unlock_ch:
                        print(f"\n{Warna.MERAH}✗ Akses terkunci!{Warna.RESET}")
                        print(f"  {Warna.KUNING}Selesaikan Chapter {unlock_ch - 1} dulu untuk membuka lokasi ini.{Warna.RESET}")
                    else:
                        print(f"\n{Warna.MERAH}✗ Lokasi '{dest}' belum terbuka.{Warna.RESET}")
                    time.sleep(2)
                else:
                    gs.current_location = dest
                    gs.visited_locations.add(dest)
                    if gs.update_quest_progress("escape_start"):
                        gs.complete_quest("escape_start")
                    return 'map_change'

        elif hasil['type'] == 'boss':
            if hasil['locked']:
                print(f"\n{Warna.MERAH}Pintu boss terkunci!{Warna.RESET}")
                time.sleep(1)
            else:
                from enemies import create_boss_instance
                from contextlib import suppress
                if boss := create_boss_instance(hasil['boss_id']):
                    # Pre-boss dialog ch1 (ditampilkan 1x per boss per karakter)
                    boss_id_key  = hasil['boss_id']
                    preboss_flag = f'preboss_shown_{boss_id_key}'
                    chapter      = int(gs.story_flags.get('current_chapter', 1))
                    if chapter == 1 and not gs.story_flags.get(preboss_flag):
                        try:
                            from character_routes import get_ch1_pre_boss_dialog
                            from utils import clear_screen
                            pre_lines = get_ch1_pre_boss_dialog(gs.player_character, boss_id_key)
                            if pre_lines:
                                clear_screen()
                                CHAR_THEME = {
                                    'vio':      Warna.MERAH + Warna.TERANG,
                                    'haikaru':  Warna.CYAN + Warna.TERANG,
                                    'aolinh':   Warna.UNGU + Warna.TERANG,
                                    'arganta':  Warna.PUTIH + Warna.TERANG,
                                    'ignatius': Warna.KUNING + Warna.TERANG,
                                }
                                tc = CHAR_THEME.get(gs.player_character, Warna.KUNING + Warna.TERANG)
                                print(f"\n{tc}{'─' * 58}{Warna.RESET}")
                                print(f"{tc}  ⚔  BOSS ENCOUNTER{Warna.RESET}")
                                print(f"{tc}{'─' * 58}{Warna.RESET}\n")
                                time.sleep(0.4)
                                for kind, text in pre_lines:
                                    if kind == 'narasi':
                                        print(f"  {Warna.ABU_GELAP}{text}{Warna.RESET}")
                                        time.sleep(0.38)
                                    elif kind == 'dialog':
                                        print(f"  {tc}{text}{Warna.RESET}")
                                        time.sleep(0.45)
                                    elif kind == 'inner':
                                        print(f"  {Warna.DIM}{Warna.CYAN}{text}{Warna.RESET}")
                                        time.sleep(0.32)
                                    elif kind == 'system':
                                        print(f"  {Warna.HIJAU + Warna.TERANG}{text}{Warna.RESET}")
                                        time.sleep(0.3)
                                print(f"\n{tc}{'─' * 58}{Warna.RESET}")
                                input(f"\n{Warna.ABU_GELAP}[ ENTER untuk mulai pertarungan ] {Warna.RESET}")
                                gs.story_flags[preboss_flag] = True
                        except Exception:
                            pass

                    with suppress(Exception):
                        from story import play_boss_confrontation
                        play_boss_confrontation(hasil['boss_id'])

                    from combat import run_combat
                    from characters import get_character_name, get_character_data

                    char_data = get_character_data(gs.player_character) or {}
                    player_stats = {
                        'name':         get_character_name(gs.player_character),
                        'hp':           gs.hp,
                        'max_hp':       gs.max_hp,
                        'attack':       gs.attack,
                        'defense':      gs.defense,
                        'speed':        gs.speed,
                        'level':        gs.level,
                        'character_id': gs.player_character,
                        # FIX: skill dari karakter, bukan story_flags
                        'skills':       char_data.get('skills', {}),
                        'energy':       getattr(gs, 'energy', 20),
                        'max_energy':   getattr(gs, 'max_energy', 20),
                        'stats': {
                            'hp':       gs.hp,
                            'max_hp':   gs.max_hp,
                            'attack':   gs.attack,
                            'defense':  gs.defense,
                            'speed':    gs.speed
                        }
                    }

                    # FIX: konversi party_members (list ID) → list dict untuk combat
                    boss_party_dicts = []
                    for mid in gs.party_members:
                        if mid in gs.party_data:
                            pd = gs.party_data[mid]
                            boss_party_dicts.append({
                                'name':    pd.get('name', mid),
                                'hp':      pd.get('hp', pd.get('max_hp', 100)),
                                'max_hp':  pd.get('max_hp', 100),
                                'attack':  pd.get('attack', 10),
                                'defense': pd.get('defense', 10),
                                'speed':   pd.get('speed', 10),
                                'skills':  pd.get('skills', {}),
                                'stats': {
                                    'hp':      pd.get('max_hp', 100),
                                    'attack':  pd.get('attack', 10),
                                    'defense': pd.get('defense', 10),
                                },
                                '_id': mid,
                            })

                    ret = run_combat(player_stats, boss, gs.inventory, boss_party_dicts)

                    # HP dan energy di-sync setelah boss combat
                    gs.hp = max(1, player_stats.get('hp', gs.hp))
                    if hasattr(gs, 'energy'):
                        gs.energy = max(0, player_stats.get('energy', gs.energy))

                    if ret == 'player_dead':
                        return 'game_over'
                    elif ret == 'victory':
                        # Check if this is a final boss
                        if boss.get('final_boss') or boss.get('id') == 'epstein_boss':
                            return 'victory'
                        
                        # Set special flags based on boss ID for character quests
                        boss_id = boss.get('id', '')
                        if boss_id == 'theater_master' or 'theater' in boss_id.lower():
                            gs.story_flags['defeat_theater_guard'] = True
                        
                        gs.bosses_defeated += 1

                        char_id = gs.player_character
                        chapter = int(gs.story_flags.get('current_chapter', 1))

                        # Ambil data quest utama chapter ini
                        try:
                            from characters import CHARACTER_MAIN_QUESTS
                            quest_data = CHARACTER_MAIN_QUESTS.get(char_id, {}).get(chapter)
                        except Exception:
                            quest_data = None

                        # Update progress main quest character
                        quest_id = (quest_data["id"]
                                    if quest_data
                                    else f"defeat_{char_id}_boss")
                        # Cek progress sebelum update, untuk dialog step completion
                        _prog_before = next((q.get('progress',0) for q in gs.active_quests if q.get('id')==quest_id), 0)
                        quest_done = gs.update_quest_progress(quest_id)
                        _prog_after = next((q.get('progress',0) for q in gs.active_quests if q.get('id')==quest_id), _prog_before+1)
                        # Dialog objektif selesai
                        if quest_data and _prog_after > _prog_before:
                            _targets = quest_data.get('steps', [])
                            _step_done = _targets[_prog_before] if _prog_before < len(_targets) else ""
                            if _step_done:
                                print(f"\n{Warna.KUNING}{'★'*55}{Warna.RESET}")
                                print(f"  {Warna.HIJAU + Warna.TERANG}✓ OBJEKTIF SELESAI:{Warna.RESET} {_step_done}")
                                if not quest_done and _prog_after < len(_targets):
                                    print(f"  {Warna.CYAN}▶ Selanjutnya:{Warna.RESET} {_targets[_prog_after]}")
                                print(f"{Warna.KUNING}{'★'*55}{Warna.RESET}")
                                time.sleep(2.5)
                        if quest_done:
                            gs.complete_quest(quest_id)

                            # Tandai completion flag di story_flags
                            if quest_data:
                                gs.story_flags[quest_data["completion_flag"]] = True
                                next_msg = quest_data.get("next_chapter_msg", "")

                            # Naikan chapter — sistem 6 chapter
                            from character_routes import advance_chapter, check_chapter_unlock
                            next_ch = chapter + 1
                            can_advance, reason = check_chapter_unlock(gs, next_ch)

                            if chapter == 1:
                                gs.story_flags['current_chapter'] = 2
                                gs.story_flags['ch2_bosses_available'] = True
                                gs.active_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
                                print(f"\n{Warna.KUNING}{'═'*60}{Warna.RESET}")
                                print(f"  {Warna.KUNING + Warna.TERANG}★  CHAPTER 1 SELESAI!  ★{Warna.RESET}")
                                if quest_data:
                                    print(f"  {quest_data.get('next_chapter_msg','')}")
                                print(f"  {Warna.HIJAU}Chapter 2 dimulai — Eksplorasi Pulau!{Warna.RESET}")
                                print(f"{Warna.KUNING}{'═'*60}{Warna.RESET}")
                                time.sleep(3)

                            elif chapter == 2:
                                gs.story_flags['current_chapter'] = 3
                                gs.active_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
                                print(f"\n{Warna.KUNING}{'═'*60}{Warna.RESET}")
                                print(f"  {Warna.KUNING + Warna.TERANG}★  CHAPTER 2 SELESAI!  ★{Warna.RESET}")
                                if quest_data:
                                    print(f"  {quest_data.get('next_chapter_msg','')}")
                                print(f"  {Warna.CYAN}Chapter 3 — Selidiki mansion & temui NPC!{Warna.RESET}")
                                print(f"{Warna.KUNING}{'═'*60}{Warna.RESET}")
                                time.sleep(3)

                            elif chapter == 3:
                                # Ch3→4 butuh 2 sidequest
                                sq_done = sum(1 for nid in ['haikaru','aolinh','arganta','ignatius','vio']
                                              if gs.story_flags.get(f'sidequest_{nid}_complete'))
                                if sq_done >= 2:
                                    gs.story_flags['current_chapter'] = 4
                                    gs.active_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
                                    print(f"\n{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                    print(f"  {Warna.MERAH + Warna.TERANG}★  CHAPTER 3 SELESAI!  ★{Warna.RESET}")
                                    print(f"  {Warna.MERAH}Chapter 4 — Konfrontasi Maxwell's Agent!{Warna.RESET}")
                                    print(f"{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                    time.sleep(3)
                                else:
                                    print(f"\n{Warna.KUNING}Selesaikan minimal 2 sidequest NPC untuk lanjut ke Ch.4!{Warna.RESET}")
                                    print(f"  Quest selesai: {sq_done}/2")
                                    time.sleep(3)

                            elif chapter == 4:
                                gs.story_flags['current_chapter'] = 5
                                gs.active_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
                                print(f"\n{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                print(f"  {Warna.MERAH + Warna.TERANG}★  CHAPTER 4 SELESAI!  ★{Warna.RESET}")
                                print(f"  {Warna.CYAN}Chapter 5 — Kumpulkan semua bukti!{Warna.RESET}")
                                print(f"{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                time.sleep(3)

                            elif chapter == 5:
                                # Ch5→6 butuh 4 sidequest + USB
                                sq_done = sum(1 for nid in ['haikaru','aolinh','arganta','ignatius','vio']
                                              if gs.story_flags.get(f'sidequest_{nid}_complete'))
                                has_usb = 'USB Evidence Drive' in gs.inventory
                                if sq_done >= 4 and has_usb:
                                    gs.story_flags['current_chapter'] = 6
                                    gs.active_quests = [q for q in gs.active_quests if q.get("quest_type") == "side"]
                                    print(f"\n{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                    print(f"  {Warna.MERAH + Warna.TERANG}★  CHAPTER 5 SELESAI!  ★{Warna.RESET}")
                                    print(f"  {Warna.MERAH}CHAPTER 6 — EPSTEIN MENUNGGU! FINAL BOSS!{Warna.RESET}")
                                    print(f"{Warna.MERAH}{'═'*60}{Warna.RESET}")
                                    time.sleep(3)
                                else:
                                    msgs = []
                                    if sq_done < 4:
                                        msgs.append(f"Quest NPC: {sq_done}/4 selesai")
                                    if not has_usb:
                                        msgs.append("USB Evidence Drive belum dimiliki!")
                                    print(f"\n{Warna.MERAH}Belum bisa lanjut ke Chapter 6!{Warna.RESET}")
                                    for m in msgs:
                                        print(f"  {Warna.KUNING}→ {m}{Warna.RESET}")
                                    time.sleep(3)

                            # Backward compat — quest generic
                            if gs.update_quest_progress("defeat_bosses"):
                                gs.complete_quest("defeat_bosses")
                            if gs.update_quest_progress("defeat_final_boss"):
                                gs.complete_quest("defeat_final_boss")

                            # Reward Dollar Boss
                            dollar_drop = boss.get('dollars', 0)
                            if dollar_drop > 0:
                                if gs.story_flags.pop('luck_boost_active', False):
                                    dollar_drop = int(dollar_drop * 1.25)
                                gs.dollars += dollar_drop
                                print(f"\n  {Warna.KUNING}💵 BOSS DEFEATED! +${dollar_drop} "
                                      f"(Total: ${gs.dollars}){Warna.RESET}")
                                time.sleep(1.5)

                            # Hapus boss door dari peta setelah dikalahkan
                            px, py = gm.player_x, gm.player_y
                            gm.boss_doors = [
                                d for d in gm.boss_doors
                                if (d['x'] != px or d['y'] != py)
                            ]

                            try:
                                from story import get_route_chapter_at, display_route_chapter
                                # chapter_index: 0=ch1 selesai, 1=ch2 selesai, dst
                                chapter_index = chapter - 1  # 0-based sesuai chapter yang baru selesai
                                ch_id = get_route_chapter_at(gs.player_character, chapter_index)
                                if ch_id:
                                    clear_screen()
                                    displayed = display_route_chapter(ch_id)
                                    if displayed:
                                        input(f"\n{Warna.ABU_GELAP}[ENTER untuk lanjut]{Warna.RESET} ")
                            except KeyError:
                                pass  # Story chapter tidak ditemukan — skip tanpa crash
                            except Exception:
                                pass  # Abaikan error story display, jangan interrupt gameplay

    except Exception as e:
        print(f"{Warna.MERAH}Error: {e}{Warna.RESET}")
        time.sleep(1)

    return None



# ══════════════════════════════════════════════════════════════════════════════
# BRAN EDWARDS SHOP

BRAN_SHOP_ITEMS = [
    {"name": "Health Potion",     "desc": "Restore 40 HP",                   "price": 30,  "effect": "heal_40"},
    {"name": "Med Kit",           "desc": "Restore 80 HP",                   "price": 60,  "effect": "heal_80"},
    {"name": "Antidote",          "desc": "Sembuhkan status efek negatif",   "price": 45,  "effect": "cure"},
    {"name": "Energy Drink",      "desc": "ATK +5 permanent",                "price": 80,  "effect": "atk_up"},
    {"name": "Armor Padding",     "desc": "DEF +5 permanent",                "price": 80,  "effect": "def_up"},
    {"name": "Discard Token",     "desc": "+1 slot discard untuk 1 combat",  "price": 50,  "effect": "discard_token"},
    {"name": "Lucky Charm",       "desc": "25% bonus dollar dari musuh berikutnya", "price": 100, "effect": "luck_boost"},
    {"name": "Explosive Charge",  "desc": "Senjata sekali pakai, 60 damage", "price": 120, "effect": "explosive"},
]

BRAN_DIALOG = [
    "Bran Edwards: *휘파람 불며* Oh hey, survivor!",
    "Bran Edwards: Name's Bran. Don't ask how I got here.",
    "Bran Edwards: I got supplies. You got dollars.",
    "Bran Edwards: Let's make a deal, yeah?",
]


def _buka_toko_bran_remote(gs):
    """
    Akses toko Bran dari mana saja via radio/walkie-talkie.
    Pertama kali: kasih hadiah gratis (Health Potion + Bandage).
    """
    clear_screen()
    first_visit = not gs.story_flags.get('bran_shop_visited', False)

    print(f"\n{Warna.KUNING + Warna.TERANG}╔══════════════════════════════════════════════════╗{Warna.RESET}")
    print(f"{Warna.KUNING + Warna.TERANG}║          BRAN EDWARDS — RADIO SHOP               ║{Warna.RESET}")
    print(f"{Warna.KUNING + Warna.TERANG}╚══════════════════════════════════════════════════╝{Warna.RESET}")

    if first_visit:
        # Dialog dan hadiah pertama kali
        print(f"\n  {Warna.CYAN}*krssshh* Walkie-talkie berbunyi...{Warna.RESET}")
        time.sleep(1)
        print(f"\n  {Warna.KUNING + Warna.TERANG}Bran{Warna.RESET}{Warna.KUNING}: {Warna.RESET}", end="")
        for c in "Hei hei! Kamu bisa dengar aku? Bran Edwards di sini. Island Surplus Store — mobile edition.":
            print(c, end="", flush=True)
            time.sleep(0.03)
        print()
        time.sleep(0.5)
        print(f"\n  {Warna.KUNING + Warna.TERANG}Bran{Warna.RESET}{Warna.KUNING}: {Warna.RESET}", end="")
        for c in "Pertama kali hubungi aku? Ini, welcome gift dari Bran. Gratis. Jangan tanya dari mana asalnya.":
            print(c, end="", flush=True)
            time.sleep(0.03)
        print()
        time.sleep(0.5)

        # Berikan hadiah gratis
        gifts = ["Health Potion", "Bandage"]
        print(f"\n  {Warna.HIJAU + Warna.TERANG}[ HADIAH PERTAMA KALI ]{Warna.RESET}")
        for gift in gifts:
            gs.add_item(gift)
            print(f"  {Warna.HIJAU}✓ Dapat: {gift}{Warna.RESET}")
        time.sleep(0.5)

        print(f"\n  {Warna.KUNING + Warna.TERANG}Bran{Warna.RESET}{Warna.KUNING}: {Warna.RESET}", end="")
        for c in "Oke, sekarang belanja apa? Dollar kamu yang bicara.":
            print(c, end="", flush=True)
            time.sleep(0.03)
        print()
        time.sleep(1)

        gs.story_flags['bran_shop_visited'] = True
    else:
        print(f"\n  {Warna.CYAN}*krssshh*{Warna.RESET}")
        print(f"  {Warna.KUNING + Warna.TERANG}Bran{Warna.RESET}{Warna.KUNING}: {Warna.RESET}Kamu lagi. Good, berarti masih hidup. Mau beli apa?")
        time.sleep(1)

    # BUG FIX: recursive call removed — shop menu langsung di sini
    while True:
        clear_screen()
        print(f"\n{Warna.KUNING + Warna.TERANG}╔══════════════════════════════════════════════════╗{Warna.RESET}")
        print(f"{Warna.KUNING + Warna.TERANG}║     BRAN EDWARDS — ISLAND SURPLUS STORE          ║{Warna.RESET}")
        print(f"{Warna.KUNING + Warna.TERANG}╚══════════════════════════════════════════════════╝{Warna.RESET}")
        print(f"\n  {Warna.ABU_GELAP}\"Semua barang garansi asli. Mungkin.\" — Bran{Warna.RESET}")
        print(f"\n  {Warna.KUNING}💵 Dollar kamu: ${gs.dollars}{Warna.RESET}\n")
        print(f"  {Warna.ABU_GELAP}{'─' * 52}{Warna.RESET}")

        for i, item in enumerate(BRAN_SHOP_ITEMS, 1):
            can_afford = gs.dollars >= item['price']
            price_color = Warna.HIJAU if can_afford else Warna.MERAH
            print(f"  {Warna.CYAN}[{i}]{Warna.RESET} {Warna.TERANG}{item['name']:<20}{Warna.RESET} "
                  f"{price_color}${item['price']:>4}{Warna.RESET}  "
                  f"{Warna.ABU_GELAP}{item['desc']}{Warna.RESET}")

        print(f"\n  {Warna.ABU_GELAP}[0] Keluar dari toko{Warna.RESET}")
        print(f"  {Warna.ABU_GELAP}{'─' * 52}{Warna.RESET}")

        try:
            pilihan = input(f"\n  {Warna.CYAN}Beli apa? > {Warna.RESET}").strip()
            if pilihan == '0':
                print(f"\n  {Warna.ABU_GELAP}Bran Edwards: \"Balik lagi kapanpun, friend!\"{Warna.RESET}")
                time.sleep(1.5)
                break

            idx = int(pilihan) - 1
            if not (0 <= idx < len(BRAN_SHOP_ITEMS)):
                print(f"\n  {Warna.MERAH}Pilihan tidak valid.{Warna.RESET}")
                time.sleep(1)
                continue

            item = BRAN_SHOP_ITEMS[idx]

            if gs.dollars < item['price']:
                print(f"\n  {Warna.MERAH}Dollar tidak cukup! Perlu ${item['price']}, punya ${gs.dollars}.{Warna.RESET}")
                print(f"  {Warna.ABU_GELAP}Bran: \"Come back when you have more cash, kid.\"{Warna.RESET}")
                time.sleep(2)
                continue

            # Proses pembelian
            gs.dollars -= item['price']
            effect = item['effect']

            if effect == 'heal_40':
                healed = min(40, gs.max_hp - gs.hp)
                gs.hp = min(gs.hp + 40, gs.max_hp)
                print(f"\n  {Warna.HIJAU}✓ HP +{healed} (sekarang {gs.hp}/{gs.max_hp}){Warna.RESET}")
            elif effect == 'heal_80':
                healed = min(80, gs.max_hp - gs.hp)
                gs.hp = min(gs.hp + 80, gs.max_hp)
                print(f"\n  {Warna.HIJAU}✓ HP +{healed} (sekarang {gs.hp}/{gs.max_hp}){Warna.RESET}")
            elif effect == 'cure':
                gs.story_flags.pop('poisoned', None)
                gs.story_flags.pop('debuffed', None)
                print(f"\n  {Warna.HIJAU}✓ Status efek negatif dihapus.{Warna.RESET}")
            elif effect == 'atk_up':
                gs.attack += 5
                print(f"\n  {Warna.HIJAU}✓ ATK permanent +5 (sekarang {gs.attack}){Warna.RESET}")
            elif effect == 'def_up':
                gs.defense += 5
                print(f"\n  {Warna.HIJAU}✓ DEF permanent +5 (sekarang {gs.defense}){Warna.RESET}")
            elif effect == 'discard_token':
                cur = gs.story_flags.get('bonus_discard_tokens', 0)
                gs.story_flags['bonus_discard_tokens'] = cur + 1
                print(f"\n  {Warna.HIJAU}✓ +1 Discard Token! (Aktif di combat berikutnya){Warna.RESET}")
            elif effect == 'luck_boost':
                gs.story_flags['luck_boost_active'] = True
                print(f"\n  {Warna.HIJAU}✓ Lucky Charm aktif! Bonus dollar musuh berikutnya.{Warna.RESET}")
            elif effect == 'explosive':
                gs.add_item("Explosive Charge")
                print(f"\n  {Warna.HIJAU}✓ Explosive Charge masuk ke inventory!{Warna.RESET}")
            else:
                gs.add_item(item['name'])
                print(f"\n  {Warna.HIJAU}✓ {item['name']} masuk ke inventory!{Warna.RESET}")

            print(f"  {Warna.KUNING}💵 Sisa: ${gs.dollars}{Warna.RESET}")
            print(f"  {Warna.ABU_GELAP}Bran: \"Good choice. Stay alive out there.\"{Warna.RESET}")
            time.sleep(2)

        except (ValueError, IndexError):
            print(f"\n  {Warna.MERAH}Input tidak valid.{Warna.RESET}")
            time.sleep(1)
        except Exception as e:
            print(f"\n  {Warna.MERAH}Error: {e}{Warna.RESET}")
            time.sleep(1)


def interaksi_npc(npc_id, gs, gm):
    """Interaksi NPC — sidequest system (bukan party rekrutmen)."""

    # Bran Edwards — toko khusus
    if npc_id == 'bran_edwards':
        clear_screen()
        print(f"\n{Warna.KUNING + Warna.TERANG}Bran Edwards{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}Pedagang Misterius — Safe Zone{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")
        for line in BRAN_DIALOG:
            print(f"  {line}")
            time.sleep(0.8)
        print()
        print(f"\n  {Warna.KUNING}[1]{Warna.RESET} Masuk ke toko")
        print(f"  {Warna.ABU_GELAP}[2] Pergi{Warna.RESET}")
        pilihan = input(f"\n{Warna.CYAN}> {Warna.RESET}").strip()
        if pilihan == '1':
            _buka_toko_bran_remote(gs)
        return

    cd = get_character_data(npc_id)
    if not cd:
        return

    # Coba gunakan npc_interactions jika tersedia
    try:
        from npc_interactions import (
            NPC_SIDEQUEST_DATA, can_trigger_sidequest, is_sidequest_complete,
            display_npc_intro, display_npc_quest_briefing, display_npc_completion,
            display_npc_repeat_talk
        )
        npc_data = NPC_SIDEQUEST_DATA.get(npc_id)
        use_new_system = npc_data is not None
    except ImportError:
        use_new_system = False

    clear_screen()
    chapter = int(gs.story_flags.get('current_chapter', 1))

    if use_new_system:
        npc_data = NPC_SIDEQUEST_DATA[npc_id]
        sq_flag  = f"sidequest_{npc_id}_complete"
        met_flag = f"met_{npc_id}"

        # Cek apakah sudah pernah bertemu
        already_met = gs.story_flags.get(met_flag, False)

        # Tampilkan intro pertama kali
        if not already_met:
            display_npc_intro(npc_id, gs)
            gs.story_flags[met_flag] = True

        sq_complete  = gs.story_flags.get(sq_flag, False)
        # FIX bug: urutan parameter yang benar — (npc_id, game_state)
        sq_available = can_trigger_sidequest(npc_id, gs)

        if sq_complete:
            # Quest sudah selesai — tampilkan dialog baru sesuai state
            display_npc_repeat_talk(npc_id, gs)
            return

        if not sq_available:
            min_ch = npc_data.get('available_chapter', 2)
            print(f"\n{Warna.CYAN + Warna.TERANG}{cd['name']}{Warna.RESET}")
            print(f"{Warna.ABU_GELAP}{cd.get('title', '')}{Warna.RESET}")
            print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")
            print(f"  {Warna.ABU_GELAP}{cd['name']}: \"Kita bisa bicara lebih lanjut nanti...\"")
            print(f"  {Warna.KUNING}(Sidequest terbuka mulai Chapter {min_ch}){Warna.RESET}")
            time.sleep(2)
            return

        print(f"\n{Warna.CYAN + Warna.TERANG}{cd['name']}{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{cd.get('title', '')}{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")

        # Cek apakah quest sudah dimulai
        sq_started_flag = f"sidequest_{npc_id}_started"
        sq_started      = gs.story_flags.get(sq_started_flag, False)

        if not sq_started:
            # Tampilkan briefing quest — hanya ditampilkan sekali
            display_npc_quest_briefing(npc_id, gs)
            gs.story_flags[sq_started_flag] = True
        else:
            # Quest sudah dimulai — cek apakah sudah selesai
            # FIX bug: urutan parameter yang benar — (npc_id, game_state)
            if is_sidequest_complete(npc_id, gs):
                # Selesai! Reward dari npc_interactions (lebih lengkap)
                gs.story_flags[sq_flag] = True
                gs.complete_quest(f"sidequest_{npc_id}")
                display_npc_completion(npc_id, gs)
                time.sleep(2)
            else:
                # Quest belum selesai — tampilkan progress ringkas
                req_items   = npc_data.get('required_items') or (
                              [npc_data['required_item']] if npc_data.get('required_item') else [])
                req_action  = npc_data.get('required_action')
                print(f"\n  {Warna.KUNING}Quest: {npc_data.get('sidequest_title', 'Sidequest')}{Warna.RESET}")
                print(f"  {Warna.ABU_GELAP}Progress:{Warna.RESET}")
                if req_items:
                    for item in req_items:
                        have = item in gs.inventory
                        chk  = f"{Warna.HIJAU}✓{Warna.RESET}" if have else f"{Warna.MERAH}✗{Warna.RESET}"
                        print(f"    {chk} {item}")
                if req_action:
                    done = gs.story_flags.get(req_action, False)
                    chk  = f"{Warna.HIJAU}✓{Warna.RESET}" if done else f"{Warna.MERAH}✗{Warna.RESET}"
                    action_labels = {'defeat_theater_guard': 'Kalahkan Penjaga Theater Backstage'}
                    print(f"    {chk} {action_labels.get(req_action, req_action)}")
                print()
                input(f"\n{Warna.ABU_GELAP}[ENTER untuk kembali]{Warna.RESET} ")

    else:
        # Fallback: tampilkan backstory dan info karakter saja
        print(f"\n{Warna.CYAN + Warna.TERANG}{cd['name']}{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{cd.get('title', '')}{Warna.RESET}")
        print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")
        if intro := get_character_intro(npc_id):
            for line in intro:
                print(f"  {line}")
                time.sleep(0.7)
        print()
        print(f"  {Warna.ABU_GELAP}[Sidequest akan tersedia setelah chapter yang sesuai]{Warna.RESET}")
        input(f"\n{Warna.ABU_GELAP}[ENTER untuk kembali]{Warna.RESET} ")


def tampilkan_inventory(gs):
    # Menampilkan inventory pemain
    clear_screen()
    print(f"\n{Warna.CYAN}BARANG{Warna.RESET}")
    print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")

    if not gs.inventory:
        print(f"{Warna.ABU_GELAP}Kosong{Warna.RESET}")
    else:
        for i, item in enumerate(gs.inventory, 1):
            print(f"[{i}] {item}")

    input(f"\n{Warna.ABU_GELAP}[ENTER]{Warna.RESET} ")


def tampilkan_npc_quests(gs):
    """Tampilkan status sidequest NPC sebagai ganti party screen."""
    clear_screen()
    chapter = int(gs.story_flags.get('current_chapter', 1))
    print(f"\n{Warna.CYAN + Warna.TERANG}STATUS SIDEQUEST NPC{Warna.RESET}")
    print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")
    print(f"  Chapter saat ini: {Warna.KUNING}Ch.{chapter}{Warna.RESET}\n")

    NPC_LIST = [
        ("haikaru",  "Haikaru Fumika",  2,  "Catatan Sandi Haikaru"),
        ("aolinh",   "Ao Lin",          2,  "Rekaman Distraksi Aolinh"),
        ("arganta",  "Amerigo Arganta", 2,  "Peta Jalur Rahasia"),
        ("ignatius", "Ignatius",        3,  "EMP Device"),
        ("vio",      "Vio",             3,  "USB Evidence Drive"),
    ]

    for npc_id, npc_name, min_ch, reward in NPC_LIST:
        sq_flag      = f"sidequest_{npc_id}_complete"
        started_flag = f"sidequest_{npc_id}_started"
        met_flag     = f"met_{npc_id}"

        sq_done    = gs.story_flags.get(sq_flag, False)
        sq_started = gs.story_flags.get(started_flag, False)
        met        = gs.story_flags.get(met_flag, False)
        locked     = chapter < min_ch

        if sq_done:
            status_str = f"{Warna.HIJAU}✓ SELESAI{Warna.RESET}"
            reward_str = f"  → {Warna.HIJAU}{reward} diperoleh{Warna.RESET}"
        elif locked:
            status_str = f"{Warna.ABU_GELAP}⬜ Terbuka Ch.{min_ch}{Warna.RESET}"
            reward_str = f"  → {Warna.ABU_GELAP}Reward: {reward}{Warna.RESET}"
        elif not met:
            status_str = f"{Warna.ABU_GELAP}⬜ Belum bertemu{Warna.RESET}"
            reward_str = f"  → {Warna.ABU_GELAP}Reward: {reward}{Warna.RESET}"
        elif sq_started:
            status_str = f"{Warna.KUNING}◐ Dalam progress{Warna.RESET}"
            reward_str = f"  → {Warna.KUNING}Reward: {reward}{Warna.RESET}"
        else:
            status_str = f"{Warna.CYAN}○ Siap diterima{Warna.RESET}"
            reward_str = f"  → {Warna.CYAN}Reward: {reward}{Warna.RESET}"

        print(f"  {Warna.TERANG}{npc_name:<18}{Warna.RESET} {status_str}")
        print(f"{reward_str}")
        print()

    # Chapter unlock info
    print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}")
    print(f"  {Warna.KUNING}Syarat unlock chapter:{Warna.RESET}")
    print(f"  Ch.4: min 2 sidequest selesai")
    print(f"  Ch.6: min 4 sidequest + USB Evidence Drive")
    print()

    input(f"{Warna.ABU_GELAP}[ENTER untuk kembali]{Warna.RESET} ")


def tampilkan_party(gs):
    """Backward compat — redirect ke npc quest screen."""
    tampilkan_npc_quests(gs)


def save_menu(gs):
    clear_screen()
    print(f"\n{Warna.CYAN}SIMPAN GAME{Warna.RESET}")
    print(f"{Warna.ABU_GELAP}{'─' * 60}{Warna.RESET}\n")

    try:
        confirm = input(f"{Warna.CYAN}Simpan sekarang? (y/n): {Warna.RESET}").strip().lower()
        if confirm == 'y':
            sukses, msg = gs.save_to_file()
            print(f"\n{Warna.HIJAU if sukses else Warna.MERAH}{msg}{Warna.RESET}")
        else:
            print(f"\n{Warna.ABU_GELAP}Dibatalkan.{Warna.RESET}")
    except Exception as e:
        print(f"\n{Warna.MERAH}Simpan error: {e}{Warna.RESET}")

    time.sleep(2)


def konfirmasi_quit():
    try:
        print(f"\n{Warna.KUNING}Progress belum di-save akan hilang!{Warna.RESET}")
        confirm = input(f"{Warna.CYAN}Keluar? (y/n): {Warna.RESET}").strip().lower()
        return confirm == 'y'
    except (KeyboardInterrupt, EOFError):
        return True
