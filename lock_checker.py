import threading
import time
import ctypes
from PIL import Image, ImageDraw, ImageFont
import pystray

# Windows API
GetKeyState = ctypes.windll.user32.GetKeyState
VK_CAPITAL = 0x14  # CapsLock
VK_NUMLOCK = 0x90  # NumLock

# Font
try:
    font = ImageFont.truetype("arial.ttf", 48)
except:
    font = ImageFont.load_default()

# Create icon with single letter
def create_icon(letter, state_on):
    img = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(img)

    color = "black" if state_on else "white"
    draw.text((16, 8), letter, font=font, fill=color)

    return img

# Two tray icons
icon_caps = pystray.Icon("CapsChecker")
icon_num = pystray.Icon("NumChecker")

def update_caps():
    while True:
        caps_on = GetKeyState(VK_CAPITAL) & 1
        icon_caps.icon = create_icon("C", caps_on)
        icon_caps.title = f"CapsLock: {'ON' if caps_on else 'OFF'}"
        time.sleep(0.5)

def update_num():
    while True:
        num_on = GetKeyState(VK_NUMLOCK) & 1
        icon_num.icon = create_icon("N", num_on)
        icon_num.title = f"NumLock: {'ON' if num_on else 'OFF'}"
        time.sleep(0.5)

# Start both icons
threading.Thread(target=update_caps, daemon=True).start()
threading.Thread(target=update_num, daemon=True).start()

threading.Thread(target=lambda: icon_caps.run(), daemon=True).start()
icon_num.run()
