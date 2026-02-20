"""
MODE DEMO UNTUK PRESENTASI ATAU UJICOBA MUNGKIN BIARKAN SAJA FILE INI
"""

import sys
import time
import random


try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


try:
    from sprites import Warna
    from characters import PLAYABLE_CHARACTERS, get_card_dialog
    from combat import (
        evaluate_hand, calculate_kerusakan, make_hp_bar,
        Card, SUITS, run_combat,
    )
    from enemies import (
        ENEMIES, BOSSES,
        create_enemy_instance, create_boss_instance,
    )
    from utils import clear_screen as clear, wait_input as wait, separator
except ImportError as e:
    print(f"\nERROR: {e}")
    print("Pastikan semua file game ada di folder yang sama dengan demo.py\n")
    sys.exit(1)




CHAR_COLOR = {
    "vio":      Warna.MERAH,
    "haikaru":  Warna.CYAN,
    "aolinh":   Warna.UNGU,
    "arganta":  Warna.PUTIH,
    "ignatius": Warna.KUNING,
}

CHAR_QUOTE = {
    "vio":
        "Pity counter gue udah 87... tinggal 3 lagi guaranteed SSR...\n"
        "     ...anyway, sistem keamanan pulau ini kayak game gacha bad RNG. Gampang.",
    "haikaru":
        "Shift guard berganti jam 06:00 dan 18:00. Window 15 menit.\n"
        "     Data tidak pernah bohong. Saatnya eksekusi rencana.",
    "aolinh":
        "\u266a Selama masih ada musik, aku bisa tetap kuat. \u266a\n"
        "     Kakak... tunggu aku. Aku pasti datang.",
    "arganta":
        "Koordinat sekitar 20\u00b0N, 65\u00b0W. Dermaga di utara.\n"
        "     Kompas kakek tidak pernah salah. Navigation mode: ON!",
    "ignatius":
        "Lock elektronik model 2015. Outdated. Vulnerable AF.\n"
        "     Panel listrik, alarm, CCTV \u2014 semuanya satu grid. EZ hack.",
}

HAND_SEQUENCE = [
    ("High Card",       [('A', '\u2660')]),
    ("One Pair",        [('K', '\u2660'), ('K', '\u2665')]),
    ("Two Pair",        [('A', '\u2660'), ('A', '\u2665'), ('K', '\u2666'), ('K', '\u2663')]),
    ("Three of a Kind", [('Q', '\u2660'), ('Q', '\u2665'), ('Q', '\u2666')]),
    ("Straight",        [('9','\u2660'),('10','\u2665'),('J','\u2666'),('Q','\u2663'),('K','\u2663')]),
    ("Flush",           [('2','\u2660'),('5','\u2660'),('8','\u2660'),('J','\u2660'),('A','\u2660')]),
    ("Full House",      [('A','\u2660'),('A','\u2665'),('A','\u2666'),('K','\u2660'),('K','\u2665')]),
    ("Four of a Kind",  [('A', s) for s in SUITS]),
    ("Straight Flush",  [('9','\u2660'),('10','\u2660'),('J','\u2660'),('Q','\u2660'),('K','\u2660')]),
]




def pilih_karakter():
    char_list = list(PLAYABLE_CHARACTERS.items())

    while True:
        clear()
        separator('\u2550')
        print(f"{Warna.CYAN + Warna.TERANG}{'PILIH KARAKTER'.center(70)}{Warna.RESET}")
        separator('\u2550')
        print()

        for i, (char_id, data) in enumerate(char_list, 1):
            c = CHAR_COLOR.get(char_id, Warna.PUTIH)
            s = data['stats']
            print(
                f"  {c + Warna.TERANG}[{i}] {data['name']:<10}{Warna.RESET}"
                f"  {Warna.ABU_GELAP}{data['title']}{Warna.RESET}"
            )
            print(
                f"      {Warna.ABU_GELAP}"
                f"HP {s['hp']:>3}  "
                f"ATK {s['attack']:>2}  "
                f"DEF {s['defense']:>2}  "
                f"SPD {s['speed']:>2}"
                f"{Warna.RESET}"
            )
            print()

        separator()
        print(f"  {Warna.MERAH}[0] Keluar{Warna.RESET}")
        print()

        try:
            pilihan = input(f"  {Warna.CYAN}> {Warna.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            return None

        if pilihan == '0':
            return None

        try:
            idx = int(pilihan) - 1
            if 0 <= idx < len(char_list):
                return char_list[idx][0]
        except ValueError:
            pass




def demo_showcase(char_id):
    # Menampilkan showcase karakter dengan stats dan info
    data = PLAYABLE_CHARACTERS[char_id]
    c    = CHAR_COLOR.get(char_id, Warna.PUTIH)
    s    = data['stats']

    clear()
    separator('\u2550')
    print(f"{c + Warna.TERANG}{('◈  ' + data['name'].upper() + '  ◈').center(70)}{Warna.RESET}")
    separator('\u2550')
    print()

    print(f"  {Warna.ABU_GELAP}{data['title']}{Warna.RESET}")
    print(f"  {Warna.ABU_GELAP}Umur {data['age']} | {data['gender']} | {data['desc']}{Warna.RESET}")
    print()

    bar = make_hp_bar(s['hp'], 120, length=20)
    print(
        f"  HP  {bar} {s['hp']:>3}    "
        f"ATK {Warna.MERAH}{s['attack']:>2}{Warna.RESET}  "
        f"DEF {Warna.BIRU}{s['defense']:>2}{Warna.RESET}  "
        f"SPD {Warna.HIJAU}{s['speed']:>2}{Warna.RESET}"
    )
    print()

    separator('\u2500')
    print(f"  {Warna.KUNING + Warna.TERANG}SKILLS{Warna.RESET}")
    separator('\u2500')
    for skill in data['skills'].values():
        print(
            f"  {c}{skill['name']:<22}{Warna.RESET}"
            f"  Power {skill['power']:>2}  Cost {skill['cost']:>2} HP"
        )
        print(f"  {Warna.ABU_GELAP}  {skill['desc']}{Warna.RESET}")
        print()

    separator('\u2500')
    print(f"  {Warna.UNGU + Warna.TERANG}PASSIVE{Warna.RESET}")
    separator('\u2500')
    print(f"  {Warna.UNGU}{data['passive']}{Warna.RESET}")
    print()

    separator('\u2500')
    quote = CHAR_QUOTE.get(char_id, "")
    if quote:
        print(f"  {c}\"{quote}\"{Warna.RESET}")
    print()

    wait()




def demo_combat(char_id):
    # Menjalankan demo pertarungan karakter melawan musuh random
    data  = PLAYABLE_CHARACTERS[char_id]
    c     = CHAR_COLOR.get(char_id, Warna.PUTIH)
    s     = data['stats']

    player = {
        "name": data['name'], "hp": s['hp'], "max_hp": s['hp'],
        "attack": s['attack'], "defense": s['defense'], "level": 1
    }
    enemy = {
        "name": "Security Guard \u2013 Veteran",
        "hp": 120, "max_hp": 120,
        "attack": 40, "defense": 18,
    }

    clear()
    separator('\u2550')
    print(f"{Warna.KUNING + Warna.TERANG}{'DEMO SISTEM PERTARUNGAN'.center(70)}{Warna.RESET}")
    separator('\u2550')
    print()
    print(f"  {Warna.ABU_GELAP}Karakter: {c}{data['name']}{Warna.ABU_GELAP}  |  "
          f"Semakin tinggi kombinasi \u2192 semakin besar damage{Warna.RESET}")
    print()

    print(f"  {Warna.MERAH}MUSUH:{Warna.RESET} {enemy['name']}")
    print(f"  HP: {make_hp_bar(enemy['hp'], enemy['max_hp'], 25)} "
          f"{enemy['hp']}/{enemy['max_hp']}")
    print()
    print(f"  {c}PEMAIN:{Warna.RESET} {player['name']} (Lv.{player['level']})")
    print(f"  HP: {make_hp_bar(player['hp'], player['max_hp'], 25)} "
          f"{player['hp']}/{player['max_hp']}")
    separator('\u2500')

    print(f"\n  {'KOMBINASI':<22} {'KARTU':<38} {'DAMAGE':>6}")
    separator('\u2500')

    for hand_name, pairs in HAND_SEQUENCE:
        cards     = [Card(r, suit) for r, suit in pairs]
        hand_type, hand_score = evaluate_hand(cards)
        dmg       = calculate_kerusakan(hand_type, hand_score, player['attack'], player['level'])
        dmg_final = max(5, dmg - enemy['defense'])
        card_str  = " ".join(str(card) for card in cards)

        if dmg_final >= 40:
            dmg_color = Warna.MERAH + Warna.TERANG
        elif dmg_final >= 20:
            dmg_color = Warna.KUNING
        else:
            dmg_color = Warna.PUTIH

        print(
            f"  {Warna.CYAN}{hand_name:<22}{Warna.RESET}"
            f"{card_str:<46}"
            f"{dmg_color}{dmg_final:>4} dmg{Warna.RESET}"
        )
        time.sleep(0.1)

    separator('\u2500')
    print()

    print(f"  {Warna.KUNING}Aksi lain dalam pertarungan:{Warna.RESET}\n")
    for key, col, desc in [
        ("S \u2013 Skill",     Warna.CYAN,      "Gunakan skill karakter (cost HP, damage tinggi)"),
        ("A \u2013 Ally Help", Warna.UNGU,      "Minta bantuan party (skill / kirim kartu kuat)"),
        ("D \u2013 Discard",   Warna.KUNING,    "Buang kartu buruk, tarik kartu baru dari deck"),
        ("I \u2013 Item",      Warna.HIJAU,     "Pakai Health Potion / Bomb dari inventory"),
        ("F \u2013 Flee",      Warna.MERAH,     "25% berhasil kabur; 75% gagal = kena 25 damage"),
        ("P \u2013 Pass",      Warna.ABU_GELAP, "Lewati giliran"),
    ]:
        print(f"  {col}[{key}]{Warna.RESET}  {desc}")

    print()
    wait()




def _build_player_stats(char_id):
    """Bangun dict player_stats dari data PLAYABLE_CHARACTERS untuk dipass ke run_combat."""
    data = PLAYABLE_CHARACTERS[char_id]
    s    = data['stats']
    return {
        "name":         data['name'],
        "hp":           s['hp'],
        "max_hp":       s['hp'],
        "attack":       s['attack'],
        "defense":      s['defense'],
        "speed":        s['speed'],
        "level":        1,
        "character_id": char_id,
        "skills":       data.get('skills', {}),
    }

def _handle_combat_result(result):
    """
    run_combat bisa return tuple (True/False, player, inventory)
    atau string 'fled'. Normalkan keduanya ke string 'victory'/'defeat'/'fled'.
    """
    if result == 'fled':
        return 'fled'
    if isinstance(result, tuple):
        won, _, _ = result
        return 'victory' if won else 'defeat'
    return 'defeat'

def _show_encounter_dialog(enemy_data):
    """Tampilkan dialog encounter enemy/boss sebelum battle."""
    dialog = enemy_data.get('dialog', {})
    lines  = dialog.get('encounter', [])
    if not lines:
        return

    c = CHAR_COLOR.get('haikaru', Warna.MERAH)
    print()
    for line in lines:
        print(f"  {Warna.KUNING}{line}{Warna.RESET}")
        time.sleep(0.6)
    print()
    time.sleep(0.5)

def _show_defeat_dialog(enemy_data):
    """Tampilkan dialog defeat enemy/boss setelah dikalahkan."""
    dialog = enemy_data.get('dialog', {})
    lines  = dialog.get('defeat', [])
    if not lines:
        return
    print()
    for line in lines:
        if line:
            print(f"  {Warna.ABU_GELAP}{line}{Warna.RESET}")
        else:
            print()
        time.sleep(0.5)
    print()

def _result_screen(result_str, enemy_name):
    """Layar hasil pertarungan — menang, kalah, atau kabur."""
    clear()
    separator('\u2550')
    if result_str == 'victory':
        print(f"{Warna.HIJAU + Warna.TERANG}{'MENANG!'.center(70)}{Warna.RESET}")
    elif result_str == 'defeat':
        print(f"{Warna.MERAH + Warna.TERANG}{'KALAH...'.center(70)}{Warna.RESET}")
    else:
        print(f"{Warna.KUNING + Warna.TERANG}{'KABUR!'.center(70)}{Warna.RESET}")
    separator('\u2550')
    print()
    if result_str == 'victory':
        print(f"  {Warna.HIJAU}Kamu mengalahkan {enemy_name}!{Warna.RESET}")
    elif result_str == 'defeat':
        print(f"  {Warna.MERAH}Kamu dikalahkan oleh {enemy_name}...{Warna.RESET}")
    else:
        print(f"  {Warna.KUNING}Kamu berhasil kabur dari {enemy_name}.{Warna.RESET}")
    print()
    wait()




def _menu_pilih_enemy():
    """Pilih enemy biasa dari daftar ENEMIES."""
    enemy_list = list(ENEMIES.items())

    while True:
        clear()
        separator('\u2550')
        print(f"{Warna.KUNING + Warna.TERANG}{'PILIH MUSUH'.center(70)}{Warna.RESET}")
        separator('\u2550')
        print()

        for i, (eid, data) in enumerate(enemy_list, 1):
            print(
                f"  {Warna.MERAH}[{i}]{Warna.RESET} {data['name']:<35}"
                f"  {Warna.ABU_GELAP}Lv.{data['level']}  "
                f"HP {data['hp']}  ATK {data['attack']}{Warna.RESET}"
            )
        print()
        separator()
        print(f"  {Warna.MERAH}[0] Kembali{Warna.RESET}")
        print()

        try:
            pilihan = input(f"  {Warna.CYAN}> {Warna.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            return None

        if pilihan == '0':
            return None
        try:
            idx = int(pilihan) - 1
            if 0 <= idx < len(enemy_list):
                return enemy_list[idx][0]
        except ValueError:
            pass

def demo_lawan_enemy(char_id):
    """Pilih enemy dari daftar, lalu langsung masuk combat sungguhan."""
    enemy_id = _menu_pilih_enemy()
    if enemy_id is None:
        return

    enemy = create_enemy_instance(enemy_id)
    if not enemy:
        return

    player_stats = _build_player_stats(char_id)
    inventory    = ['Health Potion', 'Health Potion', 'Molotov Cocktail']


    clear()
    separator('\u2550')
    print(f"{Warna.MERAH + Warna.TERANG}{'PERTARUNGAN!'.center(70)}{Warna.RESET}")
    separator('\u2550')
    enc = enemy.get('dialog', {})
    enc_line = enc.get('encounter', '')
    if enc_line:
        print(f"\n  {Warna.KUNING}{enc_line}{Warna.RESET}")
    time.sleep(1.2)

    result = run_combat(player_stats, enemy, inventory)
    result_str = _handle_combat_result(result)

    if result_str == 'victory':
        _show_defeat_dialog(enemy)

    _result_screen(result_str, enemy['name'])




def _menu_pilih_boss():
    """Pilih boss dari daftar BOSSES."""
    boss_list = list(BOSSES.items())

    while True:
        clear()
        separator('\u2550')
        print(f"{Warna.MERAH + Warna.TERANG}{'PILIH BOSS'.center(70)}{Warna.RESET}")
        separator('\u2550')
        print()

        for i, (bid, data) in enumerate(boss_list, 1):
            is_final = data.get('final_boss', False)
            tag = f"  {Warna.MERAH + Warna.TERANG}[FINAL]{Warna.RESET}" if is_final else ""
            print(
                f"  {Warna.MERAH}[{i}]{Warna.RESET} {data['name']:<38}"
                f"  {Warna.ABU_GELAP}Lv.{data['level']}  "
                f"HP {data['hp']}{Warna.RESET}{tag}"
            )

            print(f"       {Warna.ABU_GELAP}{data['desc']}{Warna.RESET}")
            print()

        separator()
        print(f"  {Warna.MERAH}[0] Kembali{Warna.RESET}")
        print()

        try:
            pilihan = input(f"  {Warna.CYAN}> {Warna.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            return None

        if pilihan == '0':
            return None
        try:
            idx = int(pilihan) - 1
            if 0 <= idx < len(boss_list):
                return boss_list[idx][0]
        except ValueError:
            pass

def demo_lawan_boss(char_id):
    """Pilih boss, tampilkan encounter dialog dramatis, lalu masuk combat sungguhan."""
    boss_id = _menu_pilih_boss()
    if boss_id is None:
        return

    boss = create_boss_instance(boss_id)
    if not boss:
        return

    player_stats = _build_player_stats(char_id)
    inventory    = ['Health Potion', 'Health Potion', 'Health Potion', 'Molotov Cocktail']
    c            = CHAR_COLOR.get(char_id, Warna.PUTIH)


    clear()
    separator('\u2550')
    is_final = boss.get('final_boss', False)
    title = 'BOSS FINAL — ' + boss['name'] if is_final else 'BOSS — ' + boss['name']
    color = Warna.MERAH + Warna.TERANG
    print(f"{color}{title.center(70)}{Warna.RESET}")
    separator('\u2550')
    print()

    print(
        f"  {Warna.ABU_GELAP}Level {boss['level']}  |  "
        f"HP {boss['hp']}  |  ATK {boss['attack']}  |  DEF {boss['defense']}{Warna.RESET}"
    )
    print(f"  {Warna.ABU_GELAP}{boss['desc']}{Warna.RESET}")
    print()


    _show_encounter_dialog(boss)

    separator('\u2500')
    print(f"\n  {c}Kamu: Aku tidak akan menyerah!{Warna.RESET}\n")
    time.sleep(1)
    wait("  [ENTER untuk mulai pertarungan] ")

    result = run_combat(player_stats, boss, inventory)
    result_str = _handle_combat_result(result)

    if result_str == 'victory':
        _show_defeat_dialog(boss)

    _result_screen(result_str, boss['name'])




def menu_karakter(char_id):
    data  = PLAYABLE_CHARACTERS[char_id]
    c     = CHAR_COLOR.get(char_id, Warna.PUTIH)

    items = [
        ("1", "Showcase Karakter", lambda: demo_showcase(char_id)),
        ("2", "Demo Combat",       lambda: demo_combat(char_id)),
        ("3", "Lawan Enemy",       lambda: demo_lawan_enemy(char_id)),
        ("4", "Lawan Boss",        lambda: demo_lawan_boss(char_id)),
        ("5", "Semua (urut)",      None),
        ("0", "Ganti Karakter",    None),
    ]

    while True:
        clear()
        separator('\u2550')
        print(
            f"{c + Warna.TERANG}"
            f"{'CURSED ISLAND ESCAPE  \u2014  ' + data['name'].upper()}"
            .center(70) + Warna.RESET
        )
        print(f"{Warna.ABU_GELAP}{'MODE DEMO'.center(70)}{Warna.RESET}")
        separator('\u2550')
        print()

        for key, label, _ in items:
            col = Warna.MERAH if key == "0" else Warna.KUNING
            print(f"  {col}[{key}]{Warna.RESET}  {label}")

        separator()

        try:
            pilihan = input(f"\n  {Warna.CYAN}> {Warna.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            return

        if pilihan == '0':
            return

        if pilihan == '5':
            demo_showcase(char_id)
            demo_combat(char_id)
            demo_lawan_enemy(char_id)
            demo_lawan_boss(char_id)
            clear()
            separator('\u2550')
            print(f"{Warna.HIJAU + Warna.TERANG}{'DEMO SELESAI!'.center(70)}{Warna.RESET}")
            separator('\u2550')
            print(
                f"\n  {Warna.ABU_GELAP}Jalankan {Warna.RESET}"
                f"{Warna.CYAN}python main.py{Warna.RESET}"
                f"{Warna.ABU_GELAP} untuk memulai game lengkap.{Warna.RESET}\n"
            )
            wait()
            return

        for key, _, fn in items:
            if pilihan == key and fn is not None:
                fn()
                break




def main():
    # Entry point untuk mode demo
    if sys.version_info < (3, 6):
        print("Python 3.6+ dibutuhkan.")
        sys.exit(1)

    try:
        while True:
            char_id = pilih_karakter()
            if char_id is None:
                break
            menu_karakter(char_id)

        clear()
        print(f"\n  {Warna.CYAN}Terima kasih sudah menonton demo!{Warna.RESET}")
        print(f"  {Warna.ABU_GELAP}Jalankan python main.py untuk memulai game.{Warna.RESET}\n")

    except KeyboardInterrupt:
        clear()
        print(f"\n  {Warna.CYAN}Interrupted.{Warna.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {Warna.MERAH}Error: {e}{Warna.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
