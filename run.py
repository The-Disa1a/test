import os
import subprocess
import shutil
import time

# User details
username = "user"
password = "root"

# RustDesk unattended access password
RUSTDESK_PASSWORD = "thedisala"

# System setup
os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

class RustDeskSetup:
    def __init__(self, user):
        os.system("apt update")
        self.installRustDesk()
        self.enableUnattendedAccess()
        self.enableAutostart()
        self.getRustDeskID()
        self.installDesktopEnvironment()
        self.changeWallpaper()
        self.installGoogleChrome()
        self.installTelegram()
        self.installQbittorrent()
        print("\n[+] RustDesk setup complete!")

    @staticmethod
    def installRustDesk():
        print("\n[+] Installing RustDesk...")
        os.system("wget https://github.com/rustdesk/rustdesk/releases/latest/download/rustdesk-deb.zip -O rustdesk.zip")
        os.system("unzip rustdesk.zip && sudo dpkg -i rustdesk-*.deb")
        os.system("sudo apt --fix-broken install -y")
        print("[+] RustDesk installed successfully.")

    @staticmethod
    def enableUnattendedAccess():
        print("\n[+] Configuring unattended access for RustDesk...")
        os.system(f"echo -n '{RUSTDESK_PASSWORD}' | sudo tee /etc/rustdesk/passwd")
        os.system("sudo systemctl restart rustdesk")
        print("[+] Unattended access enabled.")

    @staticmethod
    def enableAutostart():
        print("\n[+] Setting RustDesk to start on boot...")
        os.system("mkdir -p ~/.config/autostart")
        os.system("cp /usr/share/applications/rustdesk.desktop ~/.config/autostart/")
        os.system("sudo systemctl enable rustdesk")
        os.system("sudo systemctl start rustdesk")
        print("[+] RustDesk will now start on boot.")

    @staticmethod
    def getRustDeskID():
        print("\n[+] Fetching RustDesk ID...")
        time.sleep(5)  # Wait for RustDesk to initialize
        rustdesk_id_file = os.path.expanduser("~/.config/rustdesk/id")

        if os.path.exists(rustdesk_id_file):
            with open(rustdesk_id_file, "r") as file:
                rustdesk_id = file.read().strip()
                print(f"[+] Your RustDesk ID: {rustdesk_id}")
        else:
            print("[-] RustDesk ID not found. Ensure RustDesk is running.")

    @staticmethod
    def installDesktopEnvironment():
        print("\n[+] Installing XFCE4 Desktop Environment...")
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("sudo apt purge light-locker")
        os.system("sudo apt install --reinstall xfce4-screensaver")
        os.system("systemctl disable lightdm.service")
        print("[+] XFCE4 Desktop Environment installed!")

    @staticmethod
    def installGoogleChrome():
        print("\n[+] Installing Google Chrome...")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])
        print("[+] Google Chrome installed!")

    @staticmethod
    def installTelegram():
        print("\n[+] Installing Telegram...")
        subprocess.run(["apt", "install", "--assume-yes", "telegram-desktop"])
        print("[+] Telegram installed!")

    @staticmethod
    def installQbittorrent():
        print("\n[+] Installing Qbittorrent...")
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "-y", "qbittorrent"])
        print("[+] Qbittorrent installed!")

    @staticmethod
    def changeWallpaper():
        print("\n[+] Changing desktop wallpaper...")
        os.system(f"curl -s -L -k -o xfce-verticals.png https://gitlab.com/chamod12/changewallpaper-win10/-/raw/main/CachedImage_1024_768_POS4.jpg")
        current_directory = os.getcwd()
        custom_wallpaper_path = os.path.join(current_directory, "xfce-verticals.png")
        destination_path = '/usr/share/backgrounds/xfce/'
        shutil.copy(custom_wallpaper_path, destination_path)
        print("[+] Wallpaper changed!")

# Start the setup
try:
    RustDeskSetup(username)
    while True:
        pass  # Keeps the script running
except Exception as e:
    print(f"[-] An error occurred: {e}")
