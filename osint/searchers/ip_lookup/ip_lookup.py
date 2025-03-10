import time
import random
from utils.utils import get_session

def search_ip_address(ip):
    """
    Recherche les informations associées à une adresse IP.
    Retourne des infos comme la ville et le fournisseur d'accès internet.
    """
    session = get_session()
    
    apis = [
        f"http://ip-api.com/json/{ip}",
        f"https://ipapi.co/{ip}/json/",
        f"https://ipinfo.io/{ip}/json"
    ]
    
    city = "City not found"
    isp = "ISP not found"
    country = "Country not found"
    region = "Region not found"
    latitude = "Latitude not found"
    longitude = "Longitude not found"
    
    for api_url in apis:
        try:
            time.sleep(random.uniform(1, 2))
            
            response = session.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if "ip-api.com" in api_url:
                    if data.get("status") == "success":
                        city = data.get("city", city)
                        isp = data.get("isp", isp)
                        country = data.get("country", country)
                        region = data.get("regionName", region)
                        latitude = data.get("lat", latitude)
                        longitude = data.get("lon", longitude)
                
                elif "ipapi.co" in api_url:
                    city = data.get("city", city)
                    isp = data.get("org", isp)
                    country = data.get("country_name", country)
                    region = data.get("region", region)
                    latitude = data.get("latitude", latitude)
                    longitude = data.get("longitude", longitude)
                
                elif "ipinfo.io" in api_url:
                    city = data.get("city", city)
                    isp = data.get("org", isp)
                    country = data.get("country", country)
                    region = data.get("region", region)
                    latitude = data.get("loc").split(',')[0] if "loc" in data else "Lat not found"
                    longitude = data.get("loc").split(',')[1] if "loc" in data else "Lon not found"
                
                if city != "City not found" and isp != "ISP not found":
                    break
                    
        except Exception as e:
            print(f"Erreur avec l'API {api_url}: {e}")
            continue
    
    result_text = (
        f"🌐 IP Address: {ip}\n"
        f"🏙️ City: {city}\n"
        f"🌍 Region: {region}\n"
        f"🏳️ Country: {country}\n"
        f"🖥️ ISP: {isp}\n"
        f"🧭 City Lat/Lon: ({latitude})/({longitude})\n"
    )
    
    return result_text



