import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import re

os.makedirs("output", exist_ok=True)
os.makedirs("output_image", exist_ok=True)

url_index = "https://books.toscrape.com/index.html"

def get_soup(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup

def get_book_list_url(url):
    soup = get_soup(url)
    book_list_url = []
    
    for urls in soup.find_all("h3"):
        book_url = urljoin(url,urls.find("a").get("href"))
        book_list_url.append(book_url)

    return book_list_url

def get_book_list_url_all_pages(url):
    soup = get_soup(url)
    book_list_url_all = get_book_list_url(url)
    while soup.find("li", {"class":"next"}):
        url = urljoin(url,soup.find("li", {"class":"next"}).find("a")["href"])
        book_list_url_all = book_list_url_all + get_book_list_url(url)
        soup = get_soup(url)
    return book_list_url_all

def get_book_info(url_book):

    soup = get_soup(url_book)
    title = soup.find("h1").text.strip()
    category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
    description = soup.find("meta", {"name": "description"}).get("content")
    book_image_url = urljoin(url_book,soup.find("img")["src"])

    #EXTRACT BOOK INFO FROM PRODUCT INFO
    tr_balises = soup.find_all("tr")
    tr_content = {}

    for tr in tr_balises :
        product_info = tr.find("th").text
        valeur = tr.find("td").text
        tr_content[product_info] = valeur

    #RATING
    rating = ""
    if soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class": "star-rating One"}):
        rating = "1/5"
    elif soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class": "star-rating Two"}):
        rating = "2/5"
    elif soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class": "star-rating Three"}):
        rating = "3/5"
    elif soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class": "star-rating Four"}):
        rating = "4/5"
    elif soup.find("div", {"class":"col-sm-6 product_main"}).find("p", {"class": "star-rating Five"}):
        rating = "5/5"

    #STORE BOOK INFO
    store_book_info = {"product_page_url": url_book,
                "universal_product_code": tr_content["UPC"],
                "title":title,
                "price_including_tax": tr_content["Price (incl. tax)"].replace("Â£", "") + " £",
                "price_excluding_tax": tr_content["Price (excl. tax)"].replace("Â£", "") + " £",
                "number_available": "".join(filter(str.isdigit, tr_content["Availability"])),
                "product_description": description,
                "category": category,
                "review_rating": rating,
                "image_url": book_image_url
                }

    #DOWNLOAD IMAGE
    image_name = re.sub(r'[\\/*?:"<>|#]',"",title) + ".jpg"
    image_path = os.path.join("output_image", image_name)
    image_request = requests.get(book_image_url)
    with open (image_path, "wb") as file :
        file.write(image_request.content)
    
    return store_book_info

def get_category_dict(url_index):

    index_soup = get_soup(url_index)
    url_category = {}
    category_list = index_soup.find("ul", {"class":"nav nav-list"}).find("li").find("ul").find_all("li")
    for category in category_list :
        category_name = category.find("a").text.strip()
        url_category[category_name] = urljoin(url_index,category.find("a")["href"])
    return url_category

category_dict = get_category_dict(url_index)

for category in category_dict:
    category_name_output = os.path.join("output", category + ".csv")
    category_url = category_dict[category]
    result = []
    for book_url in get_book_list_url_all_pages(category_url):
            result.append(get_book_info(book_url))
    with open (category_name_output, "w", newline="", encoding="utf-8") as out_csv :
        if result:
            writer = csv.DictWriter(out_csv, fieldnames=result[0].keys())
            writer.writeheader()
            writer.writerows(result)