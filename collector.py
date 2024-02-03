import csv
import random
import re
import string

import requests
from bs4 import BeautifulSoup

category = input("Please insert the category >> ")
url_file = input("Input filename >> ")
output_file = input("Output filename >> ")

url = []

print("\n")

def open_source(file_path):
    result_list = []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            result_list = list(reader)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return result_list

source_file = open_source(url_file)

with open(url_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
        
    if "Product URL" in reader.fieldnames:
        for row in reader:
            url.append(row["Product URL"])
            count += 1
            print(f"Listed {count} product urls...", end='\r')
    else:
        print("Error: 'Product URL' column not found in the CSV file.")

# url = ["https://www.ebay.com/itm/373234320363?hash=item56e67fc3eb:g:vTEAAOSwrgVfbYn5&amdata=enc%3AAQAIAAAAwEUGGO0OooKLmD5jeRtkx3Doguixk406Ge0pgMT%2Fws6w0%2FSu2Tjcxis5eXYHdAfvNP5iBsc6C7cAW2smkv1%2FNYxaFm3cWowk2sL%2BAmSbG7ocw26VCA8e2up9feNBwoiXjrw3IRnmH2pNWhbeQLlDbhPSPVw6jQk8JyDpHXJwK%2F5CAlpoAZhGJysbwNEcL9fF40JAt3JjMCVRUA21vexrjWYZVoY0eZn1Xtp4GamSkGruefmGVnnnjIyGSZ3rfJi7tA%3D%3D%7Ctkp%3ABk9SR46u_bGrYw"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.ebay.com/',
    'Connection': 'keep-alive',
}



def generate_random_sku(length=8, prefix="SKU"):
    """Generate a random SKU for products."""
    alphanumeric_characters = string.ascii_uppercase + string.digits
    random_suffix = ''.join(random.choice(alphanumeric_characters) for _ in range(length))
    sku = f"{prefix}-{random_suffix}"
    return sku

def extract_numbers(text):
    numbers = re.findall(r'\d+\.\d+', text)
    if numbers:
        return numbers[0]
    return None



def format_description(input_dict):

    # print(input_dict)

    html_list = "<h4>Specifications of the product:</h4><br><span>This product comes with all these below specifications and conditions</span><br><ul>"
    
    for key, value in input_dict.items():
        html_list += f"<li><strong>{key.capitalize()}: </strong> {str(value)}</li>"

    html_list += "</ul>"

    # Remove specified words in a case-insensitive manner
    words_to_remove = ["read", "more", "about", "moreabout"]
    for word in words_to_remove:
        html_list = re.sub(fr'\b{re.escape(word)}\b', "", html_list, flags=re.IGNORECASE)

    # Remove specified characters
    characters_to_remove = ";,#$@&%'\""
    html_list = re.sub(f"[{re.escape(characters_to_remove)}]", " ", html_list)

    # print("==========\n\n", html_list)

    return html_list

product_list = []

def init_csv(file_name):
    fieldnames = ['ID', 'Type', 'SKU', 'Product Link', 'Name', 'Published', 'Is Featured', 'Visibility in catalog',
                  'Regular price', 'Images', 'Tax status', 'In stock?', 'Stock', 'Categories', 'Allow customer reviews',
                  'Brand', 'Color', 'Model', 'Model Name', 'Features', 'Description']

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

appended_products = []

def append_to_csv(file_name, data):
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.values())
        appended_products.append(data)

init_csv(output_file)

print("\n")

for item in url:
    # print(f"[*] Total went through {len(product_list)} products...", end='\r')
    print(f"[*] Scrapped {len(appended_products)} products...", end='\r')

    product = {}
    specification_dict = {}

    product["ID"] = source_file[url.index(item)]["ID"]
    product["Type"] = "simple"
    product["SKU"] = generate_random_sku()
    product["Product Link"] = item
    product["Name"] = ""
    product["Published"] = 1
    product["Is featured?"] = 0
    product["Visibility in catalog"] = "visible"
    product["Regular price"] = ""
    product["Images"] = ""
    product["Tax status"] = "taxable"
    product["In stock?"] = 1
    product["Stock"] = random.randint(1, 50)
    product["Categories"] = category
    product["Allow customer reviews"] = 1
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
        product["Name"] = (title_div.text).strip()
    except:
        pass

    # finding the price for the product
    try:
        price_div = soup.find('div', 'x-price-primary')
        product["Regular price"] = extract_numbers(price_div.text)
    except:
        pass
    
    # finding the gellary images for the product

    try:
        gallery_images_div = soup.find('div', class_=['ux-image-grid-container', 'filmstrip', 'filmstrip-x'])
        image_set = gallery_images_div.find_all('img')

        main_image_div = soup.find('div', class_=['ux-image-carousel-item', 'image-treatment', 'active', 'image'])
        main_image_section = main_image_div.find('img')
        main_image = main_image_section.get('src')

        gallery_list = []

        # URL to skip
        skip_image_url = "https://i.ebayimg.com/images/g/DOcAAOSw8NplLtwK/s-l960.webp"
        skip_image_url_2 = "https://i.ebayimg.com/images/g/DOcAAOSw8NplLtwK/s-l960.jpg"
        skip_image_url_3 = "https://i.ebayimg.com/images/g/DOcAAOSw8NplLtwK/s-l960.png"
        skip_image_url_4 = "https://i.ebayimg.com/images/g/DOcAAOSw8NplLtwK/s-l960.gif"

        for image in image_set:
            image_source = image.get('src')
            # Allow webp images in the gallery_list
            if image_source and image_source != skip_image_url:
                # Replace the size part in the image URL using regular expression
                modified_image_source = re.sub(r'/s-l\d+', '/s-l960', image_source)
                gallery_list.append(modified_image_source)

        # Main image will remain unchanged
        filtered_list = [item for item in gallery_list if item is not None]
        filtered_list.append(main_image)
        try:
            filtered_list.remove(skip_image_url)
        except:
            pass

        try:
            filtered_list.remove(skip_image_url_2)
        except:
            pass
        
        try:
            filtered_list.remove(skip_image_url_3)
        except:
            pass
        
        try:
            filtered_list.remove(skip_image_url_4)
        except:
            pass

        joined_images = ', '.join(item for item in filtered_list)

        product["Images"] = joined_images

    except:
        pass


    # finding the specification info

    try:
        specification_part = soup.find('div', 'vim x-about-this-item')
        # specification_part = soup.find('div', 'ux-layout-section-evo ux-layout-section--features')
        specification_pair = specification_part.find_all('div', 'ux-layout-section-evo__col')

        # labels = specification_part.find_all('div', 'ux-labels-values__labels')
        # values = specification_part.find_all('div', 'ux-labels-values__values')
        
        labels = specification_part.find_all('div', 'ux-labels-values__labels-content')
        values = specification_part.find_all('div', 'ux-labels-values__values-content')

        exclude_words = ["manufacturer", "mpn", "country", "part number", "ean", "upc"]

        for label, value in zip(labels, values):
            specification_dict[label.text] = value.text
        
            if label.text == "Brand":
                product['Brand'] = value.text
            elif label.text == "Color":
                product['Color'] = value.text
            elif label.text == "Model":
                product['Model'] = value.text
            elif label.text == "Model Name":
                product['Model Name'] = value.text
            elif label.text == "Features":
                product['Features'] = value.text

        specification_dict = {key: value for key, value in specification_dict.items() if not any(word in key.lower() for word in exclude_words)}

        product["Description"] = format_description(specification_dict)

    except:
        pass

    product_list.append(product)
    append_to_csv(output_file, product)


print("Done")



