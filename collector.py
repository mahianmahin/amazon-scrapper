import re

import requests
from bs4 import BeautifulSoup

url = ["https://www.ebay.com/itm/204469237044?hash=item2f9b50f534:g:jCEAAOSw-aVlCnQz&amdata=enc%3AAQAIAAAAwI3wzGPnc2bKVEemS%2F0%2BuXPrm0sotfwEM8DEFZD6iCiFJqLLyLZjwSvsPVzbCLsyb5T07Ltr4MMmfP7DtkrnhxQF49cOTXiBwrIA%2B9EGGqyCgNOGGQkka9hlg7jN7Z6XeD%2Bzsx6S3hfqg%2B8s53E%2FYi80DI%2FzIuWP%2FIUxKvsYgMVIkvrtGe86uskR7k4dW1OMJHjyolKX2QtzVgl%2B0QsIzMpIq6Qm%2FzDC5jZmqNZtbSnqnM76DPfVoNTVHEzldS449w%3D%3D%7Ctkp%3ABk9SR6yQ5birYw"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.ebay.com/',
    'Connection': 'keep-alive',
}

def extract_numbers(text):
    numbers = re.findall(r'\d+\.\d+', text)
    if numbers:
        return numbers[0]
    return None

product_list = []

for item in url:
    product = {}
    product["Product Link"] = item
    product["Title"] = ""
    product["Price"] = ""
    product["Image"] = ""
    product["Gallery Images"] = ""
    product["Brand"] = ""
    product["Color"] = ""
    product["Model"] = ""
    product["Model Name"] = ""
    product["Features"] = ""
    product["Description"] = ""


    response = requests.get(item, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    # finding the title for the product
    try:
        title_div = soup.find('div', class_=['vim x-item-title'])
        product["Title"] = (title_div.text).strip()
    except:
        print(f"[!] Could not find the title for this product! - {item}")

    # finding the price for the product
    try:
        price_div = soup.find('div', 'x-price-primary')
        product["Price"] = extract_numbers(price_div.text)
    except:
        print(f"[!] Could not find the price for this product! - {item}")

    # finding the main image for the product
    try:
        main_image_div = soup.find('div', class_=['ux-image-carousel-item', 'image-treatment', 'active', 'image'])
        main_image = main_image_div.find('img')
        product["Image"] = main_image.get('src')
    except:
        print(f"[!] Could not find the main image for this product! - {item}")
    
    # finding the gellary images for the product
    try:
        gallery_images_div = soup.find('div', class_=['ux-image-grid-container', 'filmstrip', 'filmstrip-x'])
        image_set = gallery_images_div.find_all('img')

        gallery_list = []

        for image in image_set:
            gallery_list.append(image.get('src'))

        filtered_list = [item for item in gallery_list if item is not None]

        product["Gallery Images"] = filtered_list

    except:
        print(f"[!] Could not find the gallery images for this product! - {item}")

    # finding the specification info

    try:
        specification_part = soup.find('div', 'vim x-about-this-item')
        specification_pair = specification_part.find_all('div', 'ux-layout-section-evo__col')

        for pair in specification_pair:
            label = pair.find('div', 'ux-labels-values__labels')
            values = pair.find('div', 'ux-labels-values__values')
            
            if label.text == "Brand":
                product['Brand'] = values.text
            if label.text == "Color":
                product['Color'] = values.text
            if label.text == "Model":
                product['Model'] = values.text
            if label.text == "Model Name":
                product['Model Name'] = values.text
            if label.text == "Features":
                product['Features'] = values.text

    except:
        pass

    # finding description for the product
    try:
        description_div = soup.find('div', 'vim d-item-description')
        frame = description_div.find('iframe')

        frame_src = frame.get('src')
        frame_response = requests.get(frame_src)
        frame_content = BeautifulSoup(frame_response.text, "html.parser")

        product["Description"] = str(frame_content)

    except:
        print(f"[!] could not find the description for the product! - {item}")


    product_list.append(product)

print(product_list)
    

"""

SKU add kora baki ache - random SKU diye dite hobe
Stock count randomly diye dite hobe
In Stock boolean all true kore dite hobe

"""

    


