from bs4 import BeautifulSoup

def fetch_static_data(url, session):
    try:
        response = session.get(url, timeout=15)
        if response.status_code != 200:
            return {"address": "Not found", "phone": "Not found"}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = {
            "address": ["address", ".address", ".location", "[itemprop='address']", ".contact-info p"],
            "phone": [".phone", "[itemprop='telephone']", "a[href^='tel:']", ".contact-info a"]
        }
        
        data = {}
        for key, paths in selectors.items():
            for path in paths:
                element = soup.select_one(path)
                if element:
                    data[key] = element.text.strip()
                    break
            data.setdefault(key, "Not found")
        
        return data
    except Exception as e:
        print(f"❌ Error retrieving static data from {url}: {str(e)}")
        return {"address": "Not found", "phone": "Not found"}
