import random
import requests
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

PROXY_URL = "https://www.sslproxies.org/"

def get_random_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except:
        backup_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    ]
        return random.choice(backup_user_agents)

def get_session():
    session = requests.Session()

    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
        'User-Agent': get_random_user_agent()
    })

    """ working_proxies = get_working_proxies()
    if not working_proxies:
        print("❌ Aucun proxy fonctionnel trouvé !")
        return session

    chosen_proxy = random.choice(working_proxies)
    session.proxies.update({"http": chosen_proxy, "https": chosen_proxy}) """

    return session

def get_working_proxies():
    """
    Récupère et teste une liste de proxies gratuits, puis retourne uniquement ceux qui fonctionnent.
    """
    print("🔍 Récupération des proxies gratuits...")
    proxies = get_free_proxies()
    print(f"📌 {len(proxies)} proxies trouvés. Test en cours...")

    working_proxies = [proxy for proxy in proxies if test_proxy(proxy)]
    print(f"✅ {len(working_proxies)} proxies fonctionnels trouvés !")

    return working_proxies


def get_free_proxies(limit=100):
    """
    Récupère une liste de proxies gratuits depuis sslproxies.org
    """
    response = requests.get(PROXY_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []

    # Extraction des proxies depuis le tableau
    for row in soup.select("table tbody tr"):
        columns = row.find_all("td")

        if len(columns) < 2:
            continue

        ip = columns[0].text.strip()
        port = columns[1].text.strip()

        if ip and port:
            proxy = f"http://{ip}:{port}"
            proxies.append(proxy)

    return proxies[:limit]


def test_proxy(proxy):
    """
    Vérifie si un proxy fonctionne en essayant une requête vers un site de test.
    """
    try:
        response = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def save_result_to_file(result_text, base_filename="result.txt"):
    # Séparation du nom et de l'extension
    name_part, ext_part = os.path.splitext(base_filename)
    
    filename = base_filename
    counter = 1
    
    while os.path.exists(filename):
        counter += 1
        filename = f"{name_part}{counter}{ext_part}"
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(result_text)
    
    print(f"💾 Saved in {filename}")
    return filename

