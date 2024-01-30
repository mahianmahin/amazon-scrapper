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

url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=earbuds&_sacat=0&_pgn=3"

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

    with open(str(file_name), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            if all(item.values()):
                writer.writerow({"Product URL": item["product_url"], "Product Title": item["product_title"]})

def current_date_time():
    now = datetime.now()
    formatted_date_time = now.strftime("%d/%m/%Y-%H_%M_%S")
    return str(formatted_date_time)


ELEMENT_CLASS = "s-item__info clearfix"

product_list = []

while True:
    try:
        elements = driver.find_elements(By.XPATH, f"//*[@class='{ELEMENT_CLASS}']")

        for item in elements:
            dict = {}

            try:
                a_element = item.find_element(By.TAG_NAME, "a")
                dict["product_url"] = a_element.get_property('href')

                title_element = item.find_element(By.CLASS_NAME, "s-item__title")
                dict["product_title"] = title_element.text

                scroll(title_element)
                decorate(title_element, "highlight")

                product_list.append(dict)

            except:
                print(f"[!] Couldn't find any a tag or title for {item} product!")
                continue

        try:
            next_btn = driver.find_element(By.XPATH, "//*[contains(@class, 'pagination__next')]")
            scroll(next_btn)

            if next_btn.get_attribute("aria-disabled") == None:
                decorate(next_btn, "click")
                next_btn.click()
            else:
                break
        except:
            print("[!] Couldn't find any previous or next button!")

    except:
        print("[!] Couldn't find any product listing element!")


date_time = current_date_time()
write_to_csv(product_list, f"products_list.csv")

print("[+] made it to the end without any error! :)")

input()