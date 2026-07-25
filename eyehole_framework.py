import os
import time
import sys
import json
import random
import shutil

# ANSI Color Codes
CYAN = '\033[96m'
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

CONFIG_FILE = "eyehole_tools.json"
HAS_STARTED = False

ASCII_ART = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢀⢀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⡴⠰⠞⠿⠛⠁⠓⠖⠲⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⠆⢁⠶⠿⠇⠹⠁⠸⠷⠏⣈⡀⢰⠀⠈⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡁⠴⠛⢀⡀⠀⠀⢀⠀⠀⠀⠀⡀⠀⠀⠂⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠠⠀⢠⣴⣿⠀⠄⠈⠉⠀⠀⢀⠀⢻⡗⠀⠀⠐⠡⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⠒⢺⣿⣿⣆⠙⠄⢤⠠⠔⠘⢢⣞⠋⠀⢀⣰⣧⣬⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠪⡅⠲⢿⢽⣿⣿⣶⣶⣦⣶⣿⠇⠴⠋⠍⢉⣹⣿⠿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⠆⠁⠀⢈⠉⠹⣹⠈⠁⠀⠆⢰⢆⢀⣾⣾⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠃⠷⠀⠄⣤⡀⠀⣠⠠⣤⠄⠼⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

def play_audio(filename, async_play=True):
    path = os.path.join(os.path.dirname(__file__), "assets", filename)
    if not os.path.exists(path):
        sys.stdout.write('\a')
        sys.stdout.flush()
        return

    if os.name == 'nt':
        if filename.endswith(".wav"):
            try:
                import winsound
                flags = winsound.SND_FILENAME
                if async_play:
                    flags |= winsound.SND_ASYNC
                winsound.PlaySound(path, flags)
            except:
                pass
        else:
            try:
                import ctypes
                alias = f"sfx_{hash(filename) % 10000}"
                ctypes.windll.winmm.mciSendStringW(f'close {alias}', None, 0, None)
                ctypes.windll.winmm.mciSendStringW(f'open "{path}" alias {alias}', None, 0, None)
                ctypes.windll.winmm.mciSendStringW(f'play {alias}', None, 0, None)
            except:
                pass
    else:
        # termux/linux fallback
        bg = "&" if async_play else ""
        os.system(f"termux-media-player play '{path}' > /dev/null 2>&1 {bg} || play -q '{path}' > /dev/null 2>&1 {bg}")

def play_typing():
    play_audio("sfx_typing.wav", async_play=True)

def play_glitch():
    play_audio("sfx_glitch.wav", async_play=True)

def play_startup():
    play_audio("watch-dogs-2-sound-effect-starting-a-mission.mp3", async_play=True)

def stop_audio():
    if os.name == 'nt':
        try:
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
            import ctypes
            ctypes.windll.winmm.mciSendStringW('close all', None, 0, None)
        except:
            pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_horizontal_padding(text_length):
    cols = shutil.get_terminal_size().columns
    return " " * max(0, (cols - text_length) // 2)

def get_vertical_padding(num_lines):
    rows = shutil.get_terminal_size().lines
    return "\n" * max(0, (rows - num_lines) // 2)

def typewriter_effect(text, speed=0.02, sound=False):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if sound and random.random() < 0.2: 
            play_typing()
        time.sleep(speed)
    print()

def typewriter_centered(text, color="", speed=0.02, sound=False):
    padding = get_horizontal_padding(len(text))
    sys.stdout.write(padding + color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if sound and random.random() < 0.2: 
            play_typing()
        time.sleep(speed)
    print(RESET)

def full_screen_glitch_exit(duration=2.5):
    start_time = time.time()
    terminal_size = shutil.get_terminal_size()
    characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/\\~`0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    colors = [CYAN, RED, GREEN, BOLD]
    
    play_glitch()
    while time.time() - start_time < duration:
        clear_screen()
        for _ in range(terminal_size.lines - 1):
            line = "".join(random.choice(characters) for _ in range(terminal_size.columns))
            print(f"{random.choice(colors)}{line}{RESET}")
        time.sleep(0.05)
    
    stop_audio()
    clear_screen()
    sys.exit(0)

def center_glitch_effect(duration=1.5, use_sfx=True):
    start_time = time.time()
    characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    ascii_lines = ASCII_ART.split('\n')
    line_len = max(len(line) for line in ascii_lines)
    
    h_pad = get_horizontal_padding(line_len)
    v_pad = get_vertical_padding(len(ascii_lines) + 6)
    
    if use_sfx:
        play_glitch()
        
    while time.time() - start_time < duration:
        clear_screen()
        print(v_pad, end="")
        for line in ascii_lines:
            glitched_line = ""
            for char in line:
                if char.strip() and random.random() < 0.15:
                    glitched_line += f"{RED}{random.choice(characters)}{CYAN}"
                else:
                    glitched_line += char
            print(f"{h_pad}{CYAN}{glitched_line}{RESET}")
        time.sleep(0.1)
    
    if use_sfx:
        stop_audio()
        
    clear_screen()
    print(v_pad, end="")
    for line in ascii_lines:
        print(f"{h_pad}{CYAN}{line}{RESET}")

def startup_sequence():
    global HAS_STARTED
    if HAS_STARTED:
        return
    clear_screen()
    time.sleep(0.5)
    
    # Trigger the new MP3 sound instead of the wav glitch noise!
    play_startup()
    center_glitch_effect(duration=2.0, use_sfx=False)
    print("\n")
    
    typewriter_centered("JOIN YES?   Y=YES   N=NO", color=f"{RED}{BOLD}", speed=0.04, sound=True)
    
    h_pad = get_horizontal_padding(2)
    sys.stdout.write(h_pad + f"{CYAN}> {RESET}")
    choice = input().strip().upper()
    
    if choice != 'Y':
        full_screen_glitch_exit(duration=2.5)
        
    typewriter_centered("ACCESS GRANTED.", color=f"{GREEN}{BOLD}", speed=0.04, sound=True)
    time.sleep(1)
    HAS_STARTED = True

def load_tools():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_tools(tools):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(tools, f, indent=4)

def add_tool(tools):
    print(f"\n{CYAN}[+] ADD NEW MODULE{RESET}")
    name = input(f"{RED}Module Name: {RESET}").strip()
    if not name:
        return
    
    print(f"\n{GREEN}[TIP] Use {CYAN}{{INPUT}}{GREEN} in your command if the tool needs a username, IP, or phone number.")
    print(f"[TIP] Use {CYAN}{{TARGET_IMAGE}}{GREEN} if the tool needs the photo you auto-grabbed.{RESET}")
    print(f"Example 1: {CYAN}python tools/sherlock/sherlock.py {{INPUT}}{RESET}")
    print(f"Example 2: {CYAN}exiftool {{TARGET_IMAGE}}{RESET}\n")
    
    command = input(f"{RED}Execution Command: {RESET}").strip()
    if not command:
        return

    tools[name] = command
    save_tools(tools)
    typewriter_effect(f"{GREEN}[SUCCESS] Module '{name}' linked successfully.{RESET}", sound=True)
    time.sleep(1)

def grab_latest_photo():
    print(f"\n{CYAN}[+] INITIATING AUTO-GRAB PROTOCOL{RESET}")
    play_typing()
    time.sleep(0.5)
    
    camera_dir = os.path.expanduser("~/storage/dcim/Camera/")
    if os.name == 'nt':
        camera_dir = os.path.expanduser("~\\Pictures\\Camera Roll\\")
    
    typewriter_effect(f"{CYAN}[*] Scanning local device storage: {camera_dir}{RESET}", sound=True)
    
    if not os.path.exists(camera_dir):
        print(f"{RED}[ERROR] Storage directory not found.{RESET}")
        time.sleep(2)
        return None

    try:
        files = [os.path.join(camera_dir, f) for f in os.listdir(camera_dir) if os.path.isfile(os.path.join(camera_dir, f))]
    except Exception as e:
        print(f"{RED}[ERROR] Cannot access storage: {e}{RESET}")
        time.sleep(2)
        return None
    
    if not files:
        print(f"{RED}[!] No photos found in device storage.{RESET}")
        time.sleep(2)
        return None
        
    latest_file = max(files, key=os.path.getmtime)
    
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        
    destination = os.path.join(tools_dir, "target_image.jpg")
    try:
        shutil.copy(latest_file, destination)
        typewriter_effect(f"{GREEN}[SUCCESS] Intercepted latest photo: {os.path.basename(latest_file)}{RESET}", sound=True)
        typewriter_effect(f"{GREEN}[SUCCESS] Saved to: tools/target_image.jpg{RESET}", sound=True)
    except Exception as e:
        print(f"{RED}[ERROR] Failed to copy image: {e}{RESET}")
    
    time.sleep(2)
    return destination

def execute_tool(name, command):
    clear_screen()
    play_typing()
    print(f"{CYAN}{'='*50}{RESET}")
    typewriter_effect(f"{BOLD}Executing Module: {name}{RESET}", speed=0.03, sound=True)
    print(f"{CYAN}{'='*50}{RESET}\n")
    
    if "{INPUT}" in command:
        user_val = input(f"{RED}Enter Target: {RESET}")
        command = command.replace("{INPUT}", user_val)
        
    if "{TARGET_IMAGE}" in command:
        img_path = os.path.join(os.path.dirname(__file__), "tools", "target_image.jpg")
        if not os.path.exists(img_path):
            print(f"{RED}[ERROR] No target image found! Run the Auto-Grab [G] first.{RESET}")
            time.sleep(2)
            return
        command = command.replace("{TARGET_IMAGE}", img_path)
    
    try:
        os.system(command)
    except Exception as e:
        print(f"\n{RED}[ERROR] Failed to execute: {e}{RESET}")
    
    play_typing()
    input(f"\n{CYAN}[Press Enter to return to main menu...]{RESET}")

def main_menu():
    startup_sequence()
    clear_screen()
    for line in ASCII_ART.split('\n'):
        print(f"{CYAN}{line}{RESET}")
        
    print(f"{CYAN}{'='*50}{RESET}")
    print(f"{BOLD}ctOS Central Interface - Extensible Framework{RESET}")
    print(f"{CYAN}{'='*50}{RESET}")
    
    tools = load_tools()
    
    print(f"[{RED}A{RESET}] Add New Module")
    print(f"[{RED}G{RESET}] Auto-Grab Target Photo")
    print(f"[{RED}0{RESET}] Exit System")
    print(f"{CYAN}-{'-'*48}-{RESET}")
    
    if not tools:
        print(f"{RED}[!] System empty. Use [A] to add tools.{RESET}")
    else:
        for idx, (name, _) in enumerate(tools.items(), 1):
            print(f"[{RED}{idx}{RESET}] {name}")
    
    print(f"{CYAN}{'='*50}{RESET}")
    
    choice = input(f"\n{RED}root@EyeHole:~# {RESET}").strip()
    play_typing()
    
    if choice.upper() == 'A':
        add_tool(tools)
    elif choice.upper() == 'G':
        grab_latest_photo()
    elif choice == '0':
        typewriter_effect(f"{RED}Disconnecting from mainframe...{RESET}", sound=True)
        sys.exit(0)
    elif choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(tools):
            tool_name = list(tools.keys())[idx-1]
            tool_command = tools[tool_name]
            execute_tool(tool_name, tool_command)
        else:
            print(f"{RED}[ALERT] Invalid selection.{RESET}")
            time.sleep(1)
    else:
        print(f"{RED}[ALERT] Unrecognized command.{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Force exit detected. Shutting down...{RESET}")
        sys.exit(0)
