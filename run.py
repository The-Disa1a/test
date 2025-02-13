import os
import subprocess
import time

# Set unattended access password
RUSTDESK_PASSWORD = "thedisala"

# Install RustDesk with dependency handling
def install_rustdesk():
    print("\n[+] Installing RustDesk on Colab...")
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

# Enable unattended access
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

# Run setup
install_rustdesk()
configure_unattended_access()
start_rustdesk()
get_rustdesk_id()
