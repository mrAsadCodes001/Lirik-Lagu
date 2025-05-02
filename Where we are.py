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
        ("Is it all inside of my head?\n", 0.08, 0.5),
        ("Maybe you still think I don't care\n", 0.07, 3.5),
        ("But all I need is you\n", 0.06, 6.8),
        ("Yeah, you know it's true\n", 0.06, 9.0),
        ("Yeah, you know it's true\n", 0.06, 10.5),
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