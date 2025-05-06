import time
from threading import Thread, Lock
import sys

lock = Lock()

COLOR_MAP = {
    '🧠': (255, 105, 180),
    '💔': (255, 0, 0),
    '💫': (255, 255, 153),
    '😊': (152, 251, 152),
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
        ["Aku dah lupa, tak ingat lagi 🧠", 0.0],
        ["Nama kau pun jauh dari hati 💔", 2.5],
        ["Aku move on, hidup sendiri, 💫", 5.0],
        ["Tak perlu kau, aku happy 😊", 7.5],
        ["Aku dah lupa, tak ingat lagi 🧠", 10.0],
        ["Nama kau pun jauh dari hati 💔", 12.5],
        ["Aku move on, hidup sendiri, 💫", 15.0],
        ["Tak perlu kau, aku happy. 😊", 17.5],
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