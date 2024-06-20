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


page = 1
while page <= 2:
    try:
        # 2nd step use requists library to fetch the URL
        result = requests.get(
            f"https://moiandko.com/collections/pillar-candles?page={page}"
        )

        # 3rd step save page content
        src = result.content

        # 4th step create Soup object to parse content
        soup = BeautifulSoup(src, "lxml")

        # 5th step find the elements containing info we need
        # name , price , rate, description,image

        titles = soup.find_all("h3", {"class": "t4s-product-title"})
        price = soup.find_all("div", {"class": "t4s-product-price"})

        # 6th step Loop over returned lists to extract needed text info into other lists

        for i in range(len(titles)):
            titles_list.append(titles[i].text)
            price_list.append(price[i].text.replace("\n", ""))

            item_link = titles[i].find("a").attrs["href"]
            full_link = "https://moiandko.com" + item_link.strip()
            item_link_list.append(full_link)
        page += 1
        print("page swiched")
    except:
        print("error")


# The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")

    # 5th step find the elements containing info we need
    # description,images
    description1 = soup.find("div", {"class": "t4s-product__description t4s-rte"})
    image_tags = soup.find_all(
        "img", {"class": "t4s-lz--fadeIn lazyautosizes lazyloadt4sed"}
    )

    # Iterate through each image tag
    for img in image_tags:
        # Get the image URL from the 'src' attribute
        img_url = img.get("src")
        image_url_list.append(img_url)
    description_list.append(description1.text.replace("\n", "").replace("\xa0", ""))

    print(image_url_list)

# find("img",{"class":"t4s-lz--fadeIn lazyautosizes lazyloadt4sed"})

# csv
file_list = [titles_list, price_list, item_link_list, description_list]
exported = zip_longest(*file_list)

with open(
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/candles/moiandko_soy_candles_decorative.csv",
    "w",
    newline="",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description"])
    wr.writerows(exported)
