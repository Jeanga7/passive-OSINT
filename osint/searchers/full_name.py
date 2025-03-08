import sys
from googlesearch import search
from bs4 import BeautifulSoup
import requests

def search_full_name(full_name):
    query = f'"{full_name}" address phone'
    search_results = search(query, num_results=5)
    
    address = "Address not found"
    phone = "Number not found"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    session = requests.Session()
    
    for result in search_results:
        try:
            response = session.get(result, headers=headers, timeout=10)
            print(f"result {result}")
            
            if response.status_code == 403:
                print(f"❌ Access forbidden (403) for {result}. Trying with different headers...")
                headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
                response = session.get(result, headers=headers, timeout=10)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if "rocketreach.co" in result:
                address_tag = soup.select_one(".history p")
                if address_tag:
                    address = address_tag.text.strip()

                phone_tags = soup.select(".teaser.revealed a")
                if phone_tags:
                    phone = ", ".join([tag.text.strip() for tag in phone_tags])
                    print(f"📞 Phone numbers found: {phone}")
                else:
                    print("❌ No phone numbers found on this page.") 
            
            elif "contactout.com" in result:
                address_tag = soup.select_one(".history p")
                phone_tag = None
            else:
                address_tag = soup.select_one(".bi-address")
                phone_tag = soup.select_one(".bi-phone")
            
            # Mettre à jour l'adresse uniquement si elle n'est pas déjà trouvée
            if address == "Address not found" and address_tag:
                address = address_tag.text.strip()
            
            # Mettre à jour le numéro de téléphone uniquement s'il n'est pas déjà trouvé
            if phone == "Number not found" and phone_tag:
                phone = phone_tag.text.strip()
            
            # Si les deux informations sont trouvées, on arrête la boucle
            if address != "Address not found" and phone != "Number not found":
                break
        except requests.exceptions.RequestException as e:
            print(f"❌ Error retrieving data from {result}: {e}")
            continue
    
    result = (
        f"📌 First name: {' '.join(full_name.split()[:-1])}\n"
        f"📌 Last name: {full_name.split()[-1]}\n"
        f"📍 Address: {address}\n"
        f"📞 Number: {phone}\n"
    )

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(result)

    print(result)
    print("💾 Saved in result.txt")
