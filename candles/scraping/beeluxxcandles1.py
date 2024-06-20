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


page = 1
while page <= 7:
    try:
        # 2nd step use requists library to fetch the URL
        result = requests.get(
            f"https://beeluxxcandles.com/collections/pillar-plain-beeswax-candles?page={page}"
        )

        # 3rd step save page content
        src = result.content

        # 4th step create Soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        # 5th step find the elements containing info we need
        # name , price , rate, description,image
        titles = soup.find_all("a", {"class": "product-grid-item"})
        price = soup.find_all("span", {"class": "h1 medium--left"})
        item_links = soup.find_all("a", {"class": "product-grid-item"})
        main_url_images = soup.find_all(
            "div",
            {"class": "product-grid-image--centered"},
        )
        # item_links=soup.find_all("div",{"class":"product-info-inner"})

        # # # 6th step Loop over returned lists to extract needed text info into other lists

        for i in range(len(titles)):
            titles_list.append(titles[i].find("p").text.strip())
            price_list.append(price[i].contents[3].text.strip())
            main_url_image = main_url_images[i].find("img").attrs["data-src"]

            item_link = item_links[i].attrs["href"]

            item_link = "https://beeluxxcandles.com/" + item_link
            full_link = item_link.strip()
            item_link_list.append(full_link)
            main_url_image_list.append(main_url_image)

        page += 1
        print("page swiched")
    except:
        print("error")


# # The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # 5th step find the elements containing info we need
    # description,images
    description1 = soup.find("div", {"class": "product-description rte"}).text.strip()

    description_list.append(description1)

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
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/candles/beeswax candles1.csv",
    "w",
    newline="",
    encoding="utf-8",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
    wr.writerows(exported)
