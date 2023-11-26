import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def try_retrieve_data(driver, by, value, img=False):
    txt = None
    by = by.lower()
    try:
        if by == "xpath":
            txt = driver.find_element(By.XPATH, value).text
        elif by == "css":
            txt = driver.find_element(By.CSS_SELECTOR, value).text
        elif by == "class":
            txt = driver.find_element(By.CLASS_NAME, value).text
    except:
        pass
    else:
        return txt

def try_retrieve_img_url(wait, value):
    img_urls = []
    imgs = None
    img_url = None
    
    try:
        try:
            imgs = driver.find_elements(By.CSS_SELECTOR, '.pi-image > a > img')
        except:
            pass
        
        try:
            img_url = wait.until(EC.visibility_of_element_located((By.XPATH, value)))
        except:
            pass
    except:
        return img_urls
    else:
        if len(imgs) > 0:
            for img in imgs:
                img_urls.append(img.get_attribute('src'))
        elif img_url:
            img_urls.append(img_url.get_attribute('src'))

    return img_urls    

# options = webdriver.ChromeOptions()
# options.add_argument('--headless=new') # <------------- Telling the webdriver to run headless

chop = webdriver.ChromeOptions()
chop.add_extension('uBlock-Origin.crx')
driver = webdriver.Chrome(options = chop)

wait = WebDriverWait(driver, 2)

characters = []
limit = 250
# driver = webdriver.Chrome()
for i in range(0, 2500, limit):
    url = f"https://gundam.fandom.com/wiki/Special:BrowseData/Characters?limit={limit}&offset={i}&_cat=Characters"
    driver.get(url)

    time.sleep(2)

    names = driver.find_elements(By.CSS_SELECTOR, '.smw-column > ul > li > a[href^="/wiki"]')
    links = [name.get_attribute('href') for name in names]

    for link in links:
        driver.get(link)

        char_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="firstHeading"]'))).text
        img_url = try_retrieve_img_url(wait, '//*[@id="mw-content-text"]/div/aside/figure/a/img')

        character = {"name": char_name, "img_urls": img_url, "wiki": link}

        characters.append(character)
        print(character)

# Format as JSON
characters = json.dumps(characters, indent=4)

# Write JSON to file
with open('gundam_characters.json', 'a') as gundam:
    gundam.write(characters)




    