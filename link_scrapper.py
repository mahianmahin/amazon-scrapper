import requests
from bs4 import BeautifulSoup

has_next = False

url = "https://www.amazon.com/s?k=earbuds&i=electronics-accessories&ref=nb_sb_noss"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.amazon.com/',
    'Connection': 'keep-alive',
    # Add any other headers you need
}

response = requests.get(url, headers=headers)
# print(response.content)

soup = BeautifulSoup(response.content, "html.parser")

product_list = []

# to list all the present products title
items = soup.find_all('h2', class_=['a-size-mini a-spacing-none a-color-base s-line-clamp-2'])

for item in items:
    dict = {}

    product_url = item.find("a", 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
    product_title = item.find("a", 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').text 

    dict["product url"] = product_url
    dict["product title"] = product_title

    product_list.append(dict)

print(product_list)
