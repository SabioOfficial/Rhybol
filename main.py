#!/usr/bin/env python3
import sys, os, threading, queue, time

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

def main():
    start_input_thread()
    print("input thread is running i think if i did this correctly. press q to quit?")
    try:
        while True:
            while not KEY_Q.empty():
                k = KEY_Q.get()
                if k in ("q", "Q"):
                    raise KeyboardInterrupt
                print("i fucking got:", repr(k))
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n bye bye i dont miss you")

if __name__ == "__main__":
    main()