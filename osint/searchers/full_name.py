import sys
import random
import time
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

def search_full_name(full_name):
    query = f'"{full_name}" address phone'
    search_results = list(search(query, num_results=10))
    
    address = "Address not found"
    phone = "Number not found"
    
    # Créer un générateur d'User-Agents aléatoires
    ua = UserAgent()
    
    # Liste de User-Agents de secours au cas où fake_useragent échoue
    backup_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    ]
    
    session = requests.Session()
    
    # Ajouter des cookies et d'autres en-têtes pour paraître plus légitime
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    })
    
    # Définir les sites qui nécessitent Selenium (pages dynamiques)
    dynamic_sites = ['remax.com', 'realtor.com', 'zillow.com', 'trulia.com', 'homes.com']
    
    for result in search_results:
        try:
            print(f"Analyzing {result}")
            
            # Décider si on doit utiliser Selenium basé sur l'URL
            use_selenium = any(site in result for site in dynamic_sites)
            
            if use_selenium:
                data = fetch_dynamic_data(result)
                if data.get('address') and data.get('address') != "Not found":
                    address = data['address']
                if data.get('phone') and data.get('phone') != "Not found":
                    phone = data['phone']
            else:
                # Rotation d'User-Agent pour chaque requête
                try:
                    current_ua = ua.random
                except:
                    current_ua = random.choice(backup_user_agents)
                
                session.headers['User-Agent'] = current_ua
                
                # Ajouter un délai aléatoire pour simuler un comportement humain
                time.sleep(random.uniform(1, 3))
                
                response = session.get(result, timeout=15)
                
                # Si on reçoit un 403, essayer avec un autre User-Agent
                if response.status_code == 403:
                    print(f"❌ Access forbidden (403) for {result}. Trying with different headers...")
                    for _ in range(3):  # Essayer jusqu'à 3 fois
                        try:
                            session.headers['User-Agent'] = random.choice(backup_user_agents)
                            # Ajouter un délai plus long pour réduire les soupçons
                            time.sleep(random.uniform(3, 5))
                            response = session.get(result, timeout=15)
                            if response.status_code == 200:
                                break
                        except:
                            continue
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Adaptations pour différents sites
                    if "rocketreach.co" in result:
                        address_tag = soup.select_one(".history p, .location-info")
                        phone_tag = soup.select(".teaser.revealed a, .contact-info a[href^='tel:']")
                    elif "whitepages.com" in result:
                        address_tag = soup.select_one(".address-card, .address-info, .address")
                        phone_tag = soup.select_one(".phone-card, .phone-info, .phone")
                    elif "spokeo.com" in result:
                        address_tag = soup.select_one(".address, .location")
                        phone_tag = soup.select_one(".phone, .contact")
                    else:
                        # Sélecteurs génériques qui peuvent fonctionner sur divers sites
                        address_tag = soup.select_one("address, .address, .location, [itemprop='address'], .contact-info p")
                        phone_tag = soup.select_one(".phone, [itemprop='telephone'], a[href^='tel:'], .contact-info a")
                    
                    if address == "Address not found" and address_tag:
                        address = address_tag.text.strip()
                    
                    if phone == "Number not found" and phone_tag:
                        phone = phone_tag.text.strip()
        
        except Exception as e:
            print(f"❌ Error retrieving data from {result}: {str(e)}")
            continue
        
        # Vérifier si on a trouvé les deux informations
        if address != "Address not found" and phone != "Number not found":
            break
    
    result_text = (
        f"📌 First name: {' '.join(full_name.split()[:-1])}\n"
        f"📌 Last name: {full_name.split()[-1]}\n"
        f"📍 Address: {address}\n"
        f"📞 Number: {phone}\n"
    )
    
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(result_text)
    
    # print(result_text)
    print("💾 Saved in result.txt")
    return result_text

def fetch_dynamic_data(url):
    """Récupère des données d'une page web dynamique en utilisant Selenium avec une meilleure gestion des attentes."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Ajouter un User-Agent aléatoire
    ua = UserAgent()
    try:
        user_agent = ua.random
    except:
        user_agent = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
        ])
    
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    result = {"address": "Not found", "phone": "Not found"}
    
    try:
        driver.get(url)
        
        # Attendre que la page soit chargée (maximum 10 secondes)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Liste de sélecteurs CSS pour les adresses (du plus spécifique au plus générique)
        address_selectors = [
            ".d-address-link p",
            ".d-text.d-header-office-address p",
            ".contact-address",
            ".address",
            "[itemprop='address']",
            ".location-info",
            "address",
            ".contact-info p"
        ]
        
        # Liste de sélecteurs CSS pour les numéros de téléphone
        phone_selectors = [
            ".d-text.d-bio-phone-numbers p",
            ".contact-phone",
            ".phone",
            "[itemprop='telephone']",
            "a[href^='tel:']",
            ".contact-info a"
        ]
        
        # Essayer chaque sélecteur jusqu'à ce qu'un élément soit trouvé
        for selector in address_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                result["address"] = elements[0].text.strip()
                break
        
        for selector in phone_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                result["phone"] = elements[0].text.strip()
                break
        
    except Exception as e:
        print(f"❌ Error retrieving dynamic data from {url}: {str(e)}")
    finally:
        driver.quit()
    
    return result

