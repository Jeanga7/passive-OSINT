import requests
import time

from utils.utils import get_session

SOCIAL_NETWORKS = {
    "Instagram": {
        "url": "https://www.instagram.com/{}",
        "verification": lambda r: not "Sorry, this page isn't available." in r.text
    },
    "GitHub": {
        "url": "https://github.com/{}",
        "verification": lambda r: not "Not Found" in r.text
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "verification": lambda r: not "Sorry, nobody on Reddit goes by that name" in r.text
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "verification": lambda r: not "Couldn't find this account" in r.text
    },
    "Threads": {
        "url": "https://www.threads.net/@{}",
        "verification": lambda r: not ("Page not found" in r.text or "Page not available" in r.text)
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{}",
        "verification": lambda r: not ("Page not found" in r.text or "profile you're looking for isn't available" in r.text)
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{}",
        "verification": lambda r: not "This page isn't available" in r.text
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "verification": lambda r: not ("Page not found" in r.text or "Cette page n'est pas disponible" in r.text)
    },
    "Medium": {
        "url": "https://medium.com/@{}",
        "verification": lambda r: "404" not in r.text
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{}",
        "verification": lambda r: not "Sorry. Unless you've got a time machine" in r.text
    },
    "Snapchat": {
        "url": "https://www.snapchat.com/add/{}",
        "verification": lambda r: "snapcode-img" in r.text
    },
    "StackOverflow": {
        "url": "https://stackoverflow.com/users/{}",
        "verification": lambda r: not "Page not found" in r.text
    }
}

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def search_username(username):
    """Recherche un username sur plusieurs réseaux sociaux avec une vérification améliorée"""
    found_networks = []
    session = get_session()
    
    for network, info in SOCIAL_NETWORKS.items():
        profile_url = info["url"].format(username)
        verification_func = info["verification"]
        
        try:
            print(f"🔍 Analyse de {network}...", end="\r")

            time.sleep(1)
            response = session.get(profile_url, timeout=10)
            
            if response.status_code == 200 and verification_func(response):
                found_networks.append(f"✅ {network}: {GREEN}YES{RESET} {profile_url}")
            else:
                found_networks.append(f"❌ {network}: {RED}NO{RESET} {profile_url}")
                
        except requests.RequestException as e:
            found_networks.append(f"❌ {network}: {RED}NO (Error: {str(e)[:30]}...){RESET} {profile_url}")
    
    result_message = f"\n🎯 Résultat pour '{username}':\n\n"
    result_message += "\n".join(found_networks)
    result_message += f"\n\n🔍 {len([n for n in found_networks if '✅' in n])} profils found.\n"
    
    return result_message
