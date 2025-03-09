from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils.utils import get_random_user_agent

def fetch_dynamic_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    result = {"address": "Not found", "phone": "Not found"}
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        selectors = {
            "address": [".d-address-link p", ".contact-address", ".address", "[itemprop='address']"],
            "phone": [".contact-phone", ".phone", "[itemprop='telephone']", "a[href^='tel:']"]
        }
        
        for key, paths in selectors.items():
            for path in paths:
                elements = driver.find_elements(By.CSS_SELECTOR, path)
                if elements:
                    result[key] = elements[0].text.strip()
                    break
        
    except Exception as e:
        print(f"❌ Error retrieving dynamic data from {url}: {str(e)}")
    finally:
        driver.quit()
    
    return result
