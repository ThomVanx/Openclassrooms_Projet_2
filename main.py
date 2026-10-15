import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

title = soup.find("h1").text

descritption = soup.find("meta", {"name": "description"}).get("content")

#EXTRACT BOOK INFO FROM PRODUCT INFO
tr_balises = soup.find_all("tr")
tr_content = {}

for tr in tr_balises :
    categorie = tr.find("th").text
    valeur = tr.find("td").text
    tr_content[categorie] = valeur

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
book_info = {"product_page_url": url,
             "universal_product_code": tr_content["UPC"],
             "title":title,
             "price_including_tax": tr_content["Price (incl. tax)"].replace("Â£", "") + " £",
             "price_excluding_tax": tr_content["Price (excl. tax)"].replace("Â£", "") + " £",
             "number_available": "".join(filter(str.isdigit, tr_content["Availability"])),
             "product_description": descritption,
             "category": 4,
             "review_rating": rating,
             "image_url": 6
             }

print (book_info)