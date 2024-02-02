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

def sanitize_description(soup):
    symbols_to_skip = {',', ';', '-', ':'}

    # Extract tags with text, excluding those with specified symbols
    tags_with_text = [
        tag for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'ul', 'ol', 'li'])
        if tag.get_text(strip=True) and not any(symbol in tag.get_text(strip=True) for symbol in symbols_to_skip)
    ]

    extracted_html = ''.join(str(tag) for tag in tags_with_text)

    return extracted_html


def create_csv(data, file_name):
    fieldnames = data[0].keys()

    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


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

def extract_text(soup):
    # Define tags to consider
    tags_to_extract = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'ul', 'ol', 'li']

    # Extract text content from selected tags
    unique_lines = set()
    for tag in soup.find_all(tags_to_extract):
        text = tag.get_text(strip=True).replace(',', ' ')
        unique_lines.add(text)

    # Join lines with <br> tags
    text_content = '<br>'.join(unique_lines)

    return 

def format_description(input_dict):
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

    return html_list

product_list = []

def init_csv(file_name):
    fieldnames = ['ID', 'Type', 'SKU', 'Product Link', 'Name', 'Published', 'Is Featured', 'Visibility in catalog',
                  'Regular price', 'Images', 'Tax status', 'In stock?', 'Stock', 'Categories', 'Allow customer reviews',
                  'Brand', 'Color', 'Model', 'Model Name', 'Features', 'Description']

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def append_to_csv(file_name, data):
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.values())

init_csv(output_file)

print("\n")

for item in url:
    print(f"[*] Scrapped {len(product_list)} products...", end='\r')

    product = {}
    specification_dict = {}

    product["ID"] = random.randint(500, 900000)
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
        specification_pair = specification_part.find_all('div', 'ux-layout-section-evo__col')

        for pair in specification_pair:
            label = pair.find('div', 'ux-labels-values__labels')
            values = pair.find('div', 'ux-labels-values__values')

            if "manufacturer" not in (label.text).lower():
                specification_dict[label.text] = values.text
            elif "mpn" not in (label.text).lower():
                specification_dict[label.text] = values.text
            elif "country" not in (label.text).lower():
                specification_dict[label.text] = values.text
            elif "part number" not in (label.text).lower():
                specification_dict[label.text] = values.text

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

        product["Description"] = format_description(specification_dict)

    except:
        pass

    # finding description for the product
    try:
        description_div = soup.find('div', 'vim d-item-description')
        frame = description_div.find('iframe')

        frame_src = frame.get('src')
        frame_response = requests.get(frame_src)
        frame_content = BeautifulSoup(frame_response.text, "html.parser")

        sanitized_description = sanitize_description(frame_content)
        extracted_text = extract_text(frame_content)
        # product["Description"] = str(extracted_text)

        # print(product["Description"])

    except:
        # print(f"[!] could not find the description for the product! - {item}")
        pass

    product_list.append(product)
    append_to_csv(output_file, product)


print("Done")



