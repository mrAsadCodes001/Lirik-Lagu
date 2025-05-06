import time
from threading import Thread, Lock
import sys

lock = Lock()

COLOR_MAP = {
    '🌸': (255, 105, 180),
    '💎': (0, 255, 255),
    '💖': (255, 0, 0),
    '🌍': (0, 128, 0),
    '💄': (255, 182, 193),
    '🔥': (255, 69, 0),
    '💌': (255, 192, 203),
    '💫': (255, 255, 255)
}

def get_target_color(text):
    for c in reversed(text):
        if c in COLOR_MAP:
            return COLOR_MAP[c]
    return (255, 255, 255)

def animate_text(text, delay=0.1):
    with lock:
        text = text.strip('\n')
        target_color = get_target_color(text)
        total_chars = len(text)
        start_time = time.time()
        
        # Simpan posisi kursor
        sys.stdout.write("\0337")
        sys.stdout.flush()
        
        while True:
            elapsed = time.time() - start_time
            current_char = int(elapsed // delay)
            
            if current_char >= total_chars:
                break
                
            line = []
            for i in range(current_char + 1):
                time_since = max(elapsed - i*delay, 0)
                ratio = time_since / (total_chars*delay - i*delay)
                ratio = max(0, min(ratio, 1))
                
                r = int(255 - (255 - target_color[0]) * ratio)
                g = int(255 - (255 - target_color[1]) * ratio)
                b = int(255 - (255 - target_color[2]) * ratio)
                
                line.append(f"\033[38;2;{r};{g};{b}m{text[i]}\033[0m")
            
            # Hapus baris lalu gambar ulang
            sys.stdout.write("\0338\033[2K")
            sys.stdout.write("".join(line))
            sys.stdout.flush()
            time.sleep(delay/10)
        
        # Tampilkan hasil akhir dengan jarak
        sys.stdout.write("\0338\033[2K")
        sys.stdout.write("".join([
            f"\033[38;2;{target_color[0]};{target_color[1]};{target_color[2]}m{c}\033[0m"
            for c in text
        ]) + "\n\n")  # <-- Perubahan: Menambahkan 2 newline
        sys.stdout.flush()

def sing_lyric(lyric, delay):
    time.sleep(delay)
    animate_text(lyric)

def sing_song():
    lyrics = [
        ("Karna kamu cantik 🌸", 0.3),
        ("Kan kuberi segalanya 💎 apa yang kupunya", 3.2),
        ("Dan hatimu baik 💖", 6.8),
        ("Sempurnalah duniaku 🌍 saat kau di sisiku", 10.5),
        ("Bukan karna make up 💄 di wajahmu", 14.0),
        ("Atau lipstik merah 🔥 itu", 17.5),
        ("Lembut hati tutur kata 💌", 21.5),
        ("Terciptalah cinta yang 💫 kupuja", 24.0),
    ]
    
    threads = []
    for lyric_text, lyric_delay in lyrics:
        t = Thread(target=sing_lyric, args=(lyric_text, lyric_delay))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()