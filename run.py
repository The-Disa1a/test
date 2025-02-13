import os
import subprocess
import time
import shutil

# Set unattended access password
RUSTDESK_PASSWORD = "thedisala"

# Install XFCE Desktop Environment
def install_xfce():
    print("\n[+] Installing XFCE Desktop Environment...")
    os.system("export DEBIAN_FRONTEND=noninteractive")
    os.system("apt update && apt install --assume-yes xfce4 desktop-base xfce4-terminal")
    os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
    os.system("apt remove --assume-yes gnome-terminal")
    os.system("apt install --assume-yes xscreensaver")
    os.system("apt purge --assume-yes light-locker")
    os.system("apt install --reinstall --assume-yes xfce4-screensaver")
    os.system("systemctl disable lightdm.service")
    print("[+] XFCE Installed & Configured.")

# Change Wallpaper
def change_wallpaper():
    print("\n[+] Changing Wallpaper...")
    os.system("curl -s -L -k -o xfce-verticals.png https://gitlab.com/chamod12/changewallpaper-win10/-/raw/main/CachedImage_1024_768_POS4.jpg")
    shutil.copy("xfce-verticals.png", "/usr/share/backgrounds/xfce/")
    print("[+] Wallpaper Changed.")

# Install RustDesk with dependency handling
def install_rustdesk():
    print("\n[+] Installing RustDesk...")
    os.system("wget https://github.com/rustdesk/rustdesk/releases/download/1.3.7/rustdesk-1.3.7-x86_64.deb -O rustdesk.deb")

    # Retry loop for missing dependencies
    for _ in range(3):  # Try up to 3 times
        os.system("dpkg -i rustdesk.deb")
        missing_packages = subprocess.getoutput("apt --fix-broken install -y")
        
        if "depends on" in missing_packages:
            print("\n[!] Missing dependencies detected, attempting to install...")
        else:
            break  # Exit loop if installation is successful
    
    print("[+] RustDesk installation complete.")

# Enable unattended access for RustDesk
def configure_unattended_access():
    print("\n[+] Configuring unattended access for RustDesk...")
    os.makedirs("/root/.config/rustdesk", exist_ok=True)
    with open("/root/.config/rustdesk/passwd", "w") as f:
        f.write(RUSTDESK_PASSWORD)
    os.system("chmod 600 /root/.config/rustdesk/passwd")
    print("[+] Unattended access enabled.")

# Start RustDesk manually
def start_rustdesk():
    print("\n[+] Starting RustDesk in the background...")
    os.system("nohup rustdesk > /dev/null 2>&1 &")
    time.sleep(5)  # Give RustDesk time to start

# Loop to fetch RustDesk ID
def get_rustdesk_id():
    print("\n[+] Fetching RustDesk ID...")
    while True:
        output = subprocess.getoutput("timeout 10 rustdesk --get-id")
        if output:
            print(f"[+] Your RustDesk ID: {output.strip()}")
            break  # Exit loop once ID is found
        else:
            print("[-] RustDesk ID not found. Retrying in 5 seconds...")
            time.sleep(5)

# Infinite loop to keep Colab session alive
def keep_alive():
    print("\n[+] Keeping session alive. Do NOT close this Colab cell.")
    while True:
        time.sleep(60)  # Prevents Colab from disconnecting

# Run setup
install_xfce()
change_wallpaper()
install_rustdesk()
configure_unattended_access()
start_rustdesk()
get_rustdesk_id()
keep_alive()
