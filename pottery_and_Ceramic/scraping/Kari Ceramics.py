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
result = requests.get(f"https://kariceramics.com/collections/unique-handmade-ceramics")

# 3rd step save page content
src = result.content

# 4th step create Soup object to parse content
soup = BeautifulSoup(src, "lxml")

# 5th step find the elements containing info we need
# name , price , rate, description,image


titles = soup.find_all("span", {"class": "prod-title"})
price = soup.find_all("span", {"class": "price-item price-item--regular"})
item_links = soup.find("div", {"class": "product-info-inner"}).contents[1].attrs["href"]
main_url_images = soup.find_all(
    "div",
    {"class": "reveal m_reveal_img--height"},
)
item_links = soup.find_all("div", {"class": "product-info-inner"})


# # 6th step Loop over returned lists to extract needed text info into other lists

for i in range(len(titles)):
    titles_list.append(titles[i].text)
    price_list.append(price[i].text.replace("\n", ""))
    main_url_image = main_url_images[i].contents[1].find("img").attrs["data-original"]

    item_link = item_links[i].contents[1].attrs["href"]

    item_link = "https://kariceramics.com/" + item_link
    full_link = item_link.strip()
    item_link_list.append(full_link)
    main_url_image_list.append(main_url_image)


# # The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # 5th step find the elements containing info we need
    # description,images
    description1 = (
        soup.find(
            "div",
            {"class": "product__section--desc product__description-container rte"},
        )
        .text.strip()
        .replace("\n", "")
    )

    description_list.append(description1)
print(len(description_list))


# # csv
file_list = [
    titles_list,
    price_list,
    item_link_list,
    description_list,
    main_url_image_list,
]
exported = zip_longest(*file_list)

with open(
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/pottery and Ceramic/ceramic3.csv",
    "w",
    newline="",
    encoding="utf-8",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
    wr.writerows(exported)
