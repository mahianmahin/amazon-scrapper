import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.amazon.com/s?k=earbuds&i=electronics-accessories&ref=nb_sb_noss"
# url = "https://www.amazon.com/s?k=earbuds&i=electronics-accessories"
# url = "https://www.amazon.com/s?k=earbuds&i=movies-tv-intl-ship&ref=nb_sb_noss"

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/14.1.1')
options.add_argument(f"Referer={'https://www.amazon.com/'}")

# options.add_extension("./extensions/Fingerprint.crx")
# options.add_extension("./extensions/Random.crx")

driver = webdriver.Chrome(options=options)
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


product_list = []

while True:
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
