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
# image_url_list = []
main_url_image_list = []


page = 1
while page <= 4:
    try:
        # 2nd step use requists library to fetch the URL
        result = requests.get(
            f"https://enjoyceramicart.com/collections/all?page={page}"
        )

        # 3rd step save page content
        src = result.content

        # 4th step create Soup object to parse content
        soup = BeautifulSoup(src, "lxml")

        # 5th step find the elements containing info we need
        # name , price , rate, description,image

        titles = soup.find_all("h3", {"class": "card__heading h5"})
        price = soup.find_all("span", {"class": "price-item price-item--regular"})
        item_links = soup.find_all("h3", {"class": "card__heading h5"})
        main_url_images = soup.find_all(
            "div",
            {"class": "card__media"},
        )

        # # 6th step Loop over returned lists to extract needed text info into other lists

        for i in range(len(titles)):
            titles_list.append(titles[i].text.strip())
            price_list.append(price[i].text.replace("\n", "").strip())
            main_url_image = main_url_images[i].contents[1].find("img").attrs["src"]

            item_link = item_links[i].contents[1].attrs["href"]
            full_link = "https://enjoyceramicart.com/" + item_link

            item_link_list.append(full_link)
            main_url_image_list.append(main_url_image)

        page += 1
        print("page swiched")
    except:

        print("error")


# # # The Inner Pages
for link in item_link_list:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # 5th step find the elements containing info we need
    # description,images
    description1 = (
        soup.find("div", {"class": "product__description rte quick-add-hidden"})
        .text.strip()
        .replace("\n", "")
    )

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
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/pottery and Ceramic/ceramic cups enjoy.csv",
    "w",
    newline="",
    encoding="utf-8",
) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
    wr.writerows(exported)


# one page
# # 2nd step use requists library to fetch the URL
# result = requests.get(
#     f"https://enjoyceramicart.com/collections/all?page=1"
# )

# # 3rd step save page content
# src = result.content

# # 4th step create Soup object to parse content
# soup = BeautifulSoup(src, "lxml")

# # 5th step find the elements containing info we need
# # name , price , rate, description,image


# titles = soup.find_all("h3", {"class": "card__heading h5"})
# price = soup.find_all("span", {"class": "price-item price-item--regular"})
# item_links=soup.find_all("h3",{"class":"card__heading h5"})
# main_url_images = (soup.find_all("div",{"class": "card__media"},))
# # item_links=soup.find_all("div",{"class":"product-info-inner"})

# # # 6th step Loop over returned lists to extract needed text info into other lists

# for i in range(len(titles)):
#     titles_list.append(titles[i].text.strip())
#     price_list.append(price[i].text.replace("\n", "").strip())
#     main_url_image=main_url_images[i].contents[1].find("img").attrs["src"]

#     item_link=item_links[i].contents[1].attrs["href"]
#     full_link = "https://enjoyceramicart.com/" + item_link


#     item_link_list.append(full_link)
#     main_url_image_list.append(
#         main_url_image
#     )


# # # # The Inner Pages
# for link in item_link_list:
#     result = requests.get(link)
#     src = result.content
#     soup = BeautifulSoup(src, "lxml")
#     # 5th step find the elements containing info we need
#     # description,images
#     description1 = soup.find(
#         "div", {"class": "product__description rte quick-add-hidden"}
#     ).text.strip().replace("\n", "")

#     description_list.append(description1)
# print(description_list[-1])


# # # # csv
# # file_list = [
# #     titles_list,
# #     price_list,
# #     item_link_list,
# #     description_list,
# #     main_url_image_list,
# # ]
# # exported = zip_longest(*file_list)

# # with open(
# #     "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping/ceramic3.csv",
# #     "w",
# #     newline="",encoding="utf-8"
# # ) as myfile:
# #     wr = csv.writer(myfile)
# #     wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
# #     wr.writerows(exported)
