import csv
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=earbuds&_sacat=0&_odkw=earphones&_osacat=0"

driver.get(url)

def scroll(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", element)

def decorate(element, mode):
    if mode == "highlight":
        driver.execute_script("arguments[0].style.border = '4px #fa9805 dashed';", element)
    if mode == "click":
        driver.execute_script("arguments[0].style.border = '4px #0584fa dashed';", element)

def write_to_csv(data, file_name):
    fieldnames = ["Product URL", "Product Title"]

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({"Product URL": item["product_url"], "Product Title": item["product_title"]})

def current_date_time():
    now = datetime.now()
    formatted_date_time = now.strftime("%d:%m:%Y-%H:%M:%S")
    return formatted_date_time


ELEMENT_CLASS = 's-item__info clearfix'


product_list = []

while True:
    try:
        elements = driver.find_elements(By.XPATH, f"//*[@class='{ELEMENT_CLASS}']")
    except:
        print("\n[-] some error occured!")

    for item in elements:
        dict = {}
        
        scroll(item)
        decorate(item, "highlight")

        dict["product_url"] = item.get_property("href")
        dict["product_title"] = item.text
        
        product_list.append(dict)

    next_btn = driver.find_element(By.XPATH, "//*[contains(@class, 's-pagination-item') and contains(@class, 's-pagination-next')]")
    scroll(next_btn)

    if next_btn.get_attribute("aria-disabled") == None:
        decorate(next_btn, "click")
        next_btn.click()
        driver.refresh()
    else:
        break

date_time = current_date_time()
write_to_csv(product_list, f"amazon_products_{date_time}.csv")

print("[*] scrapping completed!")

input()
