"""
UTILITY
"""
import os
import sys
import time
import shutil
from contextlib import suppress
from sprites import Warna

# Enhanced encoding configuration with fallback
def _setup_encoding():
    # Mengatur encoding terminal ke UTF-8 dengan fallback
    """Setup terminal encoding with UTF-8 fallback"""
    encoding_success = False
    
    with suppress(Exception):
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            encoding_success = True
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    
    return encoding_success

def check_terminal_compatibility():
    # Mengecek apakah terminal memenuhi ukuran minimal (80x24)
    """Check if terminal supports minimal requirements (80x24)"""
    try:
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        if cols < 80 or rows < 24:
            return False, cols, rows
        return True, cols, rows
    except Exception:
        return True, 80, 24  # Assume OK if can't determine

def get_terminal_info():
    # Mengambil informasi terminal untuk debugging
    """Get terminal info for debugging"""
    try:
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        encoding = sys.stdout.encoding or 'unknown'
        return {
            'width': cols,
            'height': rows,
            'encoding': encoding,
            'platform': os.name
        }
    except Exception as e:
        return {'error': str(e)}

# Initialize encoding on module load
_encoding_ok = _setup_encoding()

def clear_screen():
    # Menghapus layar terminal
    """Clear terminal screen"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except OSError:
        print('\n' * 50)

def flush_input():
    # Menghapus buffer input yang tertabung untuk mencegah ghosting
    """
    Buang semua karakter yang tertabung di stdin buffer.
    Mencegah 'ghosting' — input WASD yang tertabung diproses sebagai
    perintah baru di giliran berikutnya.
    Mendukung Windows (msvcrt) dan Linux/Mac (termios).

    BUG FIX: Sebelumnya memanggil tty.setraw() yang mengubah terminal ke
    raw mode tanpa pernah restore — menyebabkan input() tidak bisa baca
    ENTER. Sekarang hanya pakai tcflush() langsung tanpa mengubah mode terminal.
    """
    try:
        if os.name == 'nt':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            # tcflush saja — JANGAN setraw(), itu akan merusak terminal mode
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass

def print_slow(text, delay=0.03, allow_skip=True):
    # Mencetak teks dengan efek typewriter (karakter demi karakter)
    """Print teks dengan efek typewriter (karakter demi karakter).

    Setiap karakter langsung di-flush ke terminal.
    Skip: Windows pakai msvcrt.kbhit(), Unix pakai select().
    Delay == 0 -> langsung print biasa.
    """
    if delay <= 0:
        print(text)
        return

    try:
        skip_mode = False

        for char in text:
            if allow_skip and not skip_mode:
                try:
                    if os.name == 'nt':
                        import msvcrt
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key in (b'\r', b' ', b'\n'):
                                skip_mode = True
                    else:
                        import select
                        rlist, _, _ = select.select([sys.stdin], [], [], 0)
                        if rlist:
                            sys.stdin.readline()
                            skip_mode = True
                except Exception:
                    pass

            sys.stdout.write(char)
            if not skip_mode:
                sys.stdout.flush()
                time.sleep(delay)

        sys.stdout.flush()
        print()

    except (IOError, OSError, UnicodeEncodeError):
        try:
            print(text)
        except Exception:
            pass

def wait_input(prompt="[ENTER untuk lanjut] "):
    # Menunggu input ENTER dari pengguna dengan flush buffer
    """Wait for user to press ENTER (dengan flush buffer dulu).
    Uses adaptive delay to account for terminal speed variations.
    """
    try:
        flush_input()
        time.sleep(0.02)
        input(f"{Warna.ABU_GELAP}{prompt}{Warna.RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

def separator(char=None, length=70):
    # Mencetak garis pemisah
    """Print separator line"""
    if char is None:
        char = '-'  # ASCII fallback default
    print(f"{Warna.ABU_GELAP}{char * length}{Warna.RESET}")

def header(text):
    # Mencetak header dengan garis pemisah
    """Print header with separators"""
    separator()
    print(f"{Warna.CYAN}{text}{Warna.RESET}")
    separator()

def confirm_action(prompt="Yakin? (y/n): "):
    # Meminta konfirmasi yes/no dari pengguna
    """Get yes/no confirmation from user"""
    while True:
        response = input(f"{Warna.KUNING}{prompt}{Warna.RESET}").strip().lower()
        if response in ['y', 'ya', 'yes']:
            return True
        elif response in ['n', 'no', 'tidak']:
            return False
        else:
            print(f"{Warna.MERAH}Masukkan 'y' atau 'n'{Warna.RESET}")

def get_stat(obj, stat_name, default=None):
    # Mengambil stat dari object dengan fallback ke dict stats
    """Get stat from object with fallback to stats dict.
    E.g., get_stat(player, 'attack', 10) → player.get('attack') or player.get('stats', {}).get('attack', 10)
    """
    return obj.get(stat_name) or obj.get('stats', {}).get(stat_name, default) or default
