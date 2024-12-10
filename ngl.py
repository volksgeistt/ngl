import random
import string
import requests
import os
import time
import uuid
import hashlib
from typing import Optional, Dict

class volksgeistt:
    def __init__(self):
        self._user_agents = self._load_resource('user-agents.txt')
        self._proxies = self._load_resource('proxies.txt')

    def _load_resource(self, filename: str) -> list:
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Continuing without.")
            return []

    def _generate_token(self) -> str:
        base_token = ''.join([
            uuid.uuid4().hex,
            str(time.time()),
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        ])
        return hashlib.sha256(base_token.encode()).hexdigest()[:32]

    def _get_proxy(self) -> Optional[Dict[str, str]]:
        return {'http': random.choice(self._proxies), 'https': random.choice(self._proxies)} if self._proxies else None

    def _get_user_agent(self) -> str:
        return random.choice(self._user_agents) if self._user_agents else (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

    def spam(self, username: str, message: str, count: int = 10, delay: float = 1.0, use_proxy: bool = False):
        print(f"\n[*] Targeting: {username}")
        
        for attempt in range(count):
            token = self._generate_token()
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://ngl.link',
                'Referer': f'https://ngl.link/{username}',
                'User-Agent': self._get_user_agent(),
                'X-Requested-With': 'XMLHttpRequest',
            }
            payload = {
                'username': username,
                'question': message,
                'deviceId': token,
                'gameSlug': '',
                'referrer': '',
            }
            try:
                proxies = self._get_proxy() if use_proxy else None
                
                response = requests.post(
                    'https://ngl.link/api/submit', 
                    headers=headers, 
                    data=payload, 
                    proxies=proxies,
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"[+] {attempt + 1} :: Sent to {username}")
                else:
                    print(f"[-] Failed to send message. Status: {response.status_code}")
                time.sleep(delay)
            
            except requests.RequestException as e:
                print(f"[!] Request error: {e}")

    def interactive_mode(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("NGL - By @volksgeistt\n")
        username = input("[>] Target Username: ")
        message = input("[>] Message Content: ")
        count = int(input("[>] Number of Messages: "))
        delay = float(input("[>] Delay between messages (seconds): "))
        use_proxy = input("[>] Use Proxy? (y/n): ").lower() == 'y'
        
        self.spam(username, message, count, delay, use_proxy)

def main():
    try:
        volksgeistt().interactive_mode()
    except KeyboardInterrupt:
        print("\n[!] Operation Cancelled")

if __name__ == "__main__":
    main()
