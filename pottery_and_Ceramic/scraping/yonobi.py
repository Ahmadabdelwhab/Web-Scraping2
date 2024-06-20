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
while page <= 4:
    try:
        # 2nd step use requists library to fetch the URL
        result = requests.get(
            f"https://yonobi.com/collections/all-products?page={page}"
        )

        # 3rd step save page content
        src = result.content

        # 4th step create Soup object to parse content
        soup = BeautifulSoup(src, "lxml")

        # 5th step find the elements containing info we need
        # name , price , rate, description,image
        titles = soup.find_all(
            "div", {"class": "ProductItem__Info ProductItem__Info--center"}
        )
        price = soup.find_all(
            "div", {"class": "ProductItem__Info ProductItem__Info--center"}
        )
        item_links = soup.find_all("a", {"class": "ProductItem__ImageWrapper"})
        # main_url_images = (soup.find_all("noscript"))
        # # # 6th step Loop over returned lists to extract needed text info into other lists
        for i in range(len(titles)):
            titles_list.append(
                titles[i].find("p").text.strip()
                + " "
                + titles[i].find("h2").text.strip()
            )
            price_list.append(
                price[i].contents[2].text.replace("\n", "").split("kr")[0]
            )
            # main_url_image=main_url_images[i].contents[1].attrs["src"]

            item_link = item_links[i].attrs["href"]
            full_link = "https://yonobi.com/" + item_link

            item_link_list.append(full_link)
            # main_url_image_list.append(
            #     main_url_image
            # )

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
    main_url_images = (
        soup.find("div", {"class": "AspectRatio AspectRatio--withFallback"})
        .contents[1]
        .attrs["data-original-src"]
    )
    main_url_image_list.append(main_url_images)
    description1 = (
        soup.find("div", {"class": "ProductMeta__Description"})
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
    "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping2/pottery and Ceramic/ceramic yonobi.csv",
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
#     f"https://yonobi.com/collections/all-products?page=2"
# )

# # 3rd step save page content
# src = result.content

# # 4th step create Soup object to parse content
# soup = BeautifulSoup(src, "lxml")

# # 5th step find the elements containing info we need
# # name , price , rate, description,image
# titles = soup.find_all("div", {"class": "ProductItem__Info ProductItem__Info--center"})
# price = soup.find_all("div", {"class": "ProductItem__Info ProductItem__Info--center"})
# item_links=soup.find_all("a",{"class":"ProductItem__ImageWrapper"})
# # main_url_images = (soup.find_all("noscript"))
# # # # 6th step Loop over returned lists to extract needed text info into other lists
# for i in range(len(titles)):
#     titles_list.append(titles[i].find("p").text.strip() + " "+ titles[i].find("h2").text.strip())
#     price_list.append(price[i].contents[2].text.replace("\n", "").split("kr")[0])
#     # main_url_image=main_url_images[i].contents[1].attrs["src"]

#     item_link=item_links[i].attrs["href"]
#     full_link = "https://yonobi.com/" + item_link


#     item_link_list.append(full_link)
#     # main_url_image_list.append(
#     #     main_url_image
#     # )


# # # The Inner Pages
# for link in item_link_list:
#     result = requests.get(link)
#     src = result.content
#     soup = BeautifulSoup(src, "lxml")
#     # 5th step find the elements containing info we need
#     # description,images
#     main_div=soup.find("div",{"class":"Product__SlideItem Product__SlideItem--image Carousel__Cell is-selected"})
#     if main_div:
#         # Find all <img> tags within this div
#         img_tags = main_div.find_all('img')

#         # Extract and print the src attributes of the <img> tags
#         for img in img_tags:
#             src = img.get('data-original-src')
#             if src:
#                 main_url_image_list.append(src)

#     description1 = soup.find(
#         "div", {"class": "ProductMeta__Description"}
#     ).text.strip().replace("\n", "")

#     description_list.append(description1)


# # # # csv
# file_list = [
#     titles_list,
#     price_list,
#     item_link_list,
#     description_list,
#     main_url_image_list,
# ]
# exported = zip_longest(*file_list)

# with open(
#     "C:/Users/Qebaa/OneDrive/Desktop/Web Scraping/ceramic yonobi4.csv",
#     "w",
#     newline="",encoding="utf-8"
# ) as myfile:
#     wr = csv.writer(myfile)
#     wr.writerow(["Title", "Price", "Link", "Description", "Main image"])
#     wr.writerows(exported)


# import requests
# from bs4 import BeautifulSoup
# import lxml
# import csv
# from itertools import zip_longest


# titles_list = []
# price_list = []
# item_link_list = []
# description_list = []
# image_url_list = []
# # image_url_list = []
# main_url_image_list = []
