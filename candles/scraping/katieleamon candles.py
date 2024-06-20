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
    f"https://katieleamon.com/c/candles/?_gl=1*rui890*_up*MQ..*_ga*NDA3NTMxMTc5LjE3MTgzNDU2ODc.*_ga_X8JTEFMZ6X*MTcxODM1MzAzNC4yLjEuMTcxODM1MzA1NC4wLjAuMA.."
)

# 3rd step save page content
src = result.content

# 4th step create Soup object to parse content
soup = BeautifulSoup(src, "lxml")

# 5th step find the elements containing info we need
# name , price , rate, description,image


titles = soup.find_all("h2", {"class": "woocommerce-loop-product__title"})
price = soup.find_all("bdi")
item_links = soup.find_all(
    "a", {"class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"}
)
main_url_images = soup.find_all(
    "a",
    {"class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"},
)

# # 6th step Loop over returned lists to extract needed text info into other lists

for i in range(len(titles)):
    titles_list.append(titles[i].text)
    price_list.append(price[i].text.replace("\n", ""))

    item_link = item_links[i].attrs["href"]
    full_link = item_link.strip()
    item_link_list.append(full_link)
    # main_url_image = main_url_images[i].contents[1].find("img").attrs["src"]
    # main_url_image_list.append(main_url_image)


# # # The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # 5th step find the elements containing info we need
    # description,images
    description1 = soup.find(
        "div", {"class": "woocommerce-product-details__short-description"}
    )

    description_list.append(description1.text.replace("\n", "").replace("\xa0", ""))


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
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/candles/katieleamon_soy_candles2.csv",
    "w",
    newline="",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
    wr.writerows(exported)
