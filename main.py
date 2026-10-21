import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import re


def get_soup(url):
    """Get soup from URL"""
    try :
        request = requests.get(url, timeout=10)
        soup = BeautifulSoup(request.text, "html.parser")
        return soup
    except requests.RequestException as e:
        print (f"Error on {url} : {e}")
        return None


def get_book_list_url(url):
    """Get a list of book's URLs from an URL"""
    soup = get_soup(url)
    book_list_url = []
    
    for urls in soup.find_all("h3"):
        book_url = urljoin(url,urls.find("a").get("href"))
        book_list_url.append(book_url)

    return book_list_url

def get_book_list_url_all_pages(url):
    """Get the list of all pages from a category and execute get_book_list_url to get the list
    of book's URLs from all pages in the category"""
    soup = get_soup(url)
    book_list_url_all = get_book_list_url(url)
    while soup.find("li", {"class":"next"}):
        url = urljoin(url,soup.find("li", {"class":"next"}).find("a")["href"])
        book_list_url_all = book_list_url_all + get_book_list_url(url)
        soup = get_soup(url)
    return book_list_url_all

def download_image(image_url, book_title, category):
    """Download the image from the image URL"""
    try:
        image_name = re.sub(r'[\\/*?:"<>|#]',"",book_title) + ".jpg"
        image_path = os.path.join("output_image", category, image_name)
        image_request = requests.get(image_url, timeout=10)
        with open (image_path, "wb") as file :
            file.write(image_request.content)
    except requests.RequestException as e:
        print (f"Error downloading image {book_title} : {e}")

def get_book_info(url_book):
    """Get all the infos from a book's URL and store into a dictionary. also execute the function
    download_image"""
    soup = get_soup(url_book)
    title = soup.find("h1").text.strip()
    category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
    description = soup.find("meta", {"name": "description"}).get("content")
    book_image_url = urljoin(url_book,soup.find("img")["src"])

    #EXTRACT BOOK INFO FROM PRODUCT INFO
    tr_tags = soup.find_all("tr")
    tr_content = {}

    for tr in tr_tags :
        product_info = tr.find("th").text
        value = tr.find("td").text
        tr_content[product_info] = value

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

    download_image(book_image_url, title, category)
    
    return store_book_info

def get_category_dict(url_index):
    """Get category's URLs list from Index's URL"""
    index_soup = get_soup(url_index)
    url_category = {}
    category_list = index_soup.find("ul", {"class":"nav nav-list"}).find("li").find("ul").find_all("li")
    for category in category_list :
        category_name = category.find("a").text.strip()
        url_category[category_name] = urljoin(url_index,category.find("a")["href"])
    return url_category

if __name__ == "__main__":

    os.makedirs("output", exist_ok=True)
    os.makedirs("output_image", exist_ok=True)
    url_index = "https://books.toscrape.com/index.html"
    category_dict = get_category_dict(url_index)

    print("Begin Extraction")

    for category in category_dict:
        print (category + " - Extracting")
        os.makedirs(os.path.join("output_image", category), exist_ok=True)
        category_name_output = os.path.join("output", category + ".csv")
        result = []
        for book_url in get_book_list_url_all_pages(category_dict[category]):
                result.append(get_book_info(book_url))
        with open (category_name_output, "w", newline="", encoding="utf-8") as out_csv :
            if result:
                writer = csv.DictWriter(out_csv, fieldnames=result[0].keys())
                writer.writeheader()
                writer.writerows(result)
        print (category + " - Extraction finished")

    print ("All extractions finished")