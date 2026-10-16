import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

url_book = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
request = requests.get(url_book)
soup = BeautifulSoup(request.text, "html.parser")

title = soup.find("h1").text
category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
descritption = soup.find("meta", {"name": "description"}).get("content")
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
if soup.find("p", {"class": "star-rating One"}):
    rating = "1/5"
elif soup.find("p", {"class": "star-rating Two"}):
    rating = "2/5"
elif soup.find("p", {"class": "star-rating Three"}):
    rating = "3/5"
elif soup.find("p", {"class": "star-rating Four"}):
    rating = "4/5"
elif soup.find("p", {"class": "star-rating Five"}):
    rating = "5/5"
else:
    print("error : no rating")

#STORE BOOK INFO
book_info = {"product_page_url": url_book,
             "universal_product_code": tr_content["UPC"],
             "title":title,
             "price_including_tax": tr_content["Price (incl. tax)"].replace("Â£", "") + " £",
             "price_excluding_tax": tr_content["Price (excl. tax)"].replace("Â£", "") + " £",
             "number_available": "".join(filter(str.isdigit, tr_content["Availability"])),
             "product_description": descritption,
             "category": category,
             "review_rating": rating,
             "image_url": book_image_url
             }

with open ("book_info.csv", "w", newline="", encoding="utf-8") as out_csv :
    writer = csv.DictWriter(out_csv, fieldnames=book_info.keys())
    writer.writeheader()
    writer.writerow(book_info)

print (book_info)