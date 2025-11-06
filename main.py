#!/usr/bin/env python3
import sys, os, threading, queue, time, shutil

KEY_Q = queue.Queue()

def start_input_thread():
    if os.name == "nt":
        import msvcrt
        def loop():
            while True:
                ch = msvcrt.getwch()
                KEY_Q.put(ch)
    else: # hey i dont know if this code actually works uh oh
        import tty, termios, select
        def loop():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                while True:
                    r, _, _ = select.select([fd], [], [], 0.1)
                    if r:
                        ch = sys.stdin.read(1)
                        KEY_Q.put(ch)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
    t = threading.Thread(target=loop, daemon=True)
    t.start()

# terminal helpers yippee
def clear_screen():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

def hide_cursor():
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()

def get_term_size():
    return shutil.get_terminal_size(fallback=(80, 24))

def draw_static_lane(rows=12): # idk what i should name this?
    cols, term_rows = get_term_size()
    clear_screen()
    print("rhybol - v0.1 (dev) - game(not) - press q to quit")
    print("-" * 40) # top 10 python moments
    for r in range(rows):
        if r >= rows- 2:
            print("|                                      | =")
        else:
            print("|                                      |")
    print("-" * 40)
    sys.stdout.flush()

def main():
    start_input_thread()
    hide_cursor()
    print("game running. press q to quit?")
    try:
        while True:
            draw_static_lane(rows=12)
            while not KEY_Q.empty():
                k = KEY_Q.get()
                if k in ("q", "Q"):
                    return
            time.sleep(0.2)
    finally:
        show_cursor()
        clear_screen()

if __name__ == "__main__":
    main()