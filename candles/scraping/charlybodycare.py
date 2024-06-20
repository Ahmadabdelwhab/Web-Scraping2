import requests
from bs4 import BeautifulSoup
import lxml
import csv
from itertools import zip_longest


titles_list = []
price_list = []
item_link_list = []
description_list = []
image_url_list = []
main_url_image_list = []


# 2nd step use requists library to fetch the URL
result = requests.get(
    f"https://charlybodycare.com/collections/soy-candles/type_decorative?sort_by="
)

# 3rd step save page content
src = result.content

# 4th step create Soup object to parse content
soup = BeautifulSoup(src, "lxml")

# 5th step find the elements containing info we need
# name , price , rate, description,image


titles = soup.find_all("a", {"class": "product-grid-item__title font-heading"})
price = soup.find_all("a", {"class": "product-grid-item__price price"})
main_url_image = soup.find(
    "deferred-loading",
    {"class": "product__media__hover product__media__hover--fade-in"},
)

# 6th step Loop over returned lists to extract needed text info into other lists

for i in range(len(titles)):
    titles_list.append(titles[i].text)
    price_list.append(price[i].text.replace("\n", ""))

    item_link = titles[i].attrs["href"]
    full_link =  item_link.strip()
    item_link_list.append(full_link)
    main_url_image_list.append(
        main_url_image.contents[1].find("img").attrs["src"].replace("'", "")
    )


# The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # 5th step find the elements containing info we need
    # description,images
    description1 = soup.find(
        "div", {"class": "product__block product__description rte"}
    )

    # description_list.append(description1.text.replace("\n", "").replace("\xa0", ""))
print(description1)


# csv
file_list = [
    titles_list,
    price_list,
    item_link_list,
    description_list,
    main_url_image_list,
]
exported = zip_longest(*file_list)

with open(
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/candles/charlybodycare_soy_candles_decorative2.csv",
    "w",
    newline="",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
    wr.writerows(exported)
