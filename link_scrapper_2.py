import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.amazon.com/s?k=earbuds&i=electronics-accessories&ref=nb_sb_noss"

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
options.add_extension("./extensions/Fingerprint.crx")
options.add_extension("./extensions/Random.crx")

driver = webdriver.Chrome(options=options)
driver.get(url)

def scroll(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", element)

def decorate(element, mode):
    if mode == "highlight":
        driver.execute_script("arguments[0].style.border = '4px #fa9805 dashed';", element)
    if mode == "click":
        driver.execute_script("arguments[0].style.border = '4px #0584fa dashed';", element)

while True:
    product_list = []

    try:
        elements = driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
    except:
        print("\n[-] some error occured!")

    for item in elements:
        dict = {}
        
        scroll(item)
        decorate(item, "highlight")

        dict["product_url"] = item.get_property("href")
        dict["product_title"] = item.text
        
        product_list.append(dict)

    next_btn = driver.find_element(By.XPATH, "//*[contains(@class, 's-pagination-item') and contains(@class, 's-pagination-previous')]")
    scroll(next_btn)

    if next_btn.get_attribute("aria-disabled") == None:
        decorate(next_btn, "click")
        next_btn.click()
        driver.refresh()
    else:
        break


print("[*] scrapping completed!")