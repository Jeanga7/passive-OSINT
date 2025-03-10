import requests

from utils.utils import get_session

SOCIAL_NETWORKS = {
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitHub": "https://github.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Threads": "https://www.threads.net/@{}"
}

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def search_username(username):
    """Recherche un username sur plusieurs réseaux sociaux"""
    found_networks = []
    session = get_session()

    for network, url in SOCIAL_NETWORKS.items():
        profile_url = url.format(username)
        try:
            response = session.get(profile_url, timeout=5)
            if response.status_code == 200:
                found_networks.append(f"✅ {network}: {GREEN}YES{RESET} {profile_url}")
            else:
                found_networks.append(f"❌ {network}: {RED}NO{RESET} {profile_url}")
        except requests.RequestException:
            found_networks.append(f"❌ {network}: {RED}NO{RESET} {profile_url}")

    result_message = f"\n🎯 Résultat pour '{username}':\n\n"
    result_message += "\n".join(found_networks)
    result_message += f"\n\n🔍 {len([n for n in found_networks if '✅' in n])} profils trouvés."

    return result_message
