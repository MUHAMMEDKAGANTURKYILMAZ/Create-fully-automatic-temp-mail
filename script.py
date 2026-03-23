import requests
import random
import string
import threading
import sys
import time
from user_agent import generate_user_agent
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FinalTurbo:
    def __init__(self):
        self.domains = ["mail.gw", "mail.tm", "mail.be", "mail.po", "mail.ee"]
        self.output = "accounts.txt"
        self.proxy_file = "proxies.txt"
        self.lock = threading.Lock()
        self.success = 0
        self.proxies = self.load_proxies()
        self.p_index = 0

    def load_proxies(self):
        try:
            with open(self.proxy_file, "r") as f:
                p = [line.strip() for line in f if line.strip()]
            if not p:
                print("[!] ERROR: proxies.txt is empty!"); sys.exit()
            return p
        except:
            print("[!] ERROR: proxies.txt not found!"); sys.exit()

    def get_proxy(self):
        with self.lock:
            proxy = self.proxies[self.p_index]
            self.p_index = (self.p_index + 1) % len(self.proxies)
            return {"http": proxy, "https": proxy}

    def gen_str(self, size=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))

    def worker(self):
        while True:
            s = requests.Session()
            s.proxies = self.get_proxy()
            base = f"https://api.{random.choice(self.domains)}"

            try:
                d = s.get(f"{base}/domains", timeout=3).json()['hydra:member'][0]['domain']
                user = self.gen_str()
                email = f"{user}@{d}"
                pw = self.gen_str(16)

                reg = s.post(f"{base}/accounts", json={"address":email,"password":pw}, timeout=4)
                if reg.status_code == 201:
                    tk = s.post(f"{base}/token", json={"address":email,"password":pw}, timeout=4).json().get("token")
                    if tk:
                        with self.lock:
                            with open(self.output, "a") as f:
                                f.write(f"{email}|{pw}|{tk}\n")
                            self.success += 1
                            sys.stdout.write(f"\r[+] [ACCOUNTS CREATED 🚀🔥]: {self.success} | Latest: {email}")
                            sys.stdout.flush()
            except:
                continue

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     ███████╗██╗███╗   ██╗ █████╗ ██╗     ██╗████████╗███████╗    ║
    ║     ██╔════╝██║████╗  ██║██╔══██╗██║     ██║╚══██╔══╝██╔════╝    ║
    ║     █████╗  ██║██╔██╗ ██║███████║██║     ██║   ██║   █████╗      ║
    ║     ██╔══╝  ██║██║╚██╗██║██╔══██║██║     ██║   ██║   ██╔══╝      ║
    ║     ██║     ██║██║ ╚████║██║  ██║███████╗██║   ██║   ███████╗    ║
    ║     ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   ╚══════╝    ║
    ║                                                                  ║
    ║              ⚡ FINAL TURBO ACCOUNT GENERATOR ⚡                  ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝

    💰 Support Development:
    ┌─────────────────────────────────────────────────────────────────┐
    │  Donate with Solana: 2R8s8z7cEiUVs44BGq5dsz3XhnvyXpirqk7bLieC2q4y │
    └─────────────────────────────────────────────────────────────────┘

    🌐 Follow: https://github.com/MUHAMMEDKAGANTURKYILMAZ
    """
    print(banner)
    time.sleep(1)

if __name__ == "__main__":
    print_banner()

    bot = FinalTurbo()

    print(f"\n{'─' * 60}")
    print(f"  [⚙️]  THREAD COUNT: 85")
    print(f"  [🌐]  PROXIES LOADED: {len(bot.proxies)}")
    print(f"  [💾]  OUTPUT FILE: {bot.output}")
    print(f"{'─' * 60}\n")

    print("[*] Initializing workers...")
    time.sleep(0.5)

    for i in range(85):
        t = threading.Thread(target=bot.worker)
        t.daemon = True
        t.start()

    print("[✓] All threads started! Press CTRL+C to stop.\n")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n\n[!] Stopped by user")
        print(f"{'═' * 60}")
        print(f"  [📊] TOTAL ACCOUNTS CREATED: {bot.success}")
        print(f"{'═' * 60}")
