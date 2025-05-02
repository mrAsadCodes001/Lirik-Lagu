import sys
import time
from threading import Thread, Lock

lock = Lock()
start_time = time.time()

def animate_text(text, delay=0.1):
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def sing_lyric(lyric, start_at, speed):
    now = time.time()
    wait_time = start_at - (now - start_time)
    if wait_time > 0:
        time.sleep(wait_time)
    animate_text(lyric, speed)

def sing_song():
    lyrics = [
    ("Yang datang dan pergi\n", 0.08, 0.0),
    ("Semua yang harus dilalui\n", 0.08, 2.8),
    ("Kadang kita perlu tersakikti\n", 0.08, 6.2),
    ("Tuk menjadi manusia\n", 0.08, 10.0),
]

    threads = []
    for lyric, speed, start_at in lyrics:
        t = Thread(target=sing_lyric, args=(lyric, start_at, speed))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()