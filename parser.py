import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
CSV = "cards.csv"
HOST = "https://minfin.com.ua/"
URL = "https://minfin.com.ua/ua/cards/"
BANK = "https://minfin.com.ua/company/"
HEADERS = {
    "user-agent": user,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

def get_html(url, params=""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all("div", class_="sc-182gfyr-0")
    cards = []
    for item in items:
        cards.append(
            {
                "title": item.find("div", class_="kwXsZB").find_all("a")[-1].get_text(),
                "link-product": HOST +  item.find("div", class_="cxzlon").find("a").get("href")[21:],
                "brand": item.find("span", class_="dksWIi").get_text(strip=True),
                "card-img": item.find("div", class_="fJFiLL").find("a", class_="knHhYO").find("img").get("srcset"),
            }
        )
    return cards

def save_content(items, path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Назва послуги", "Силка на послугу", "Банк", "Силка на зображення"])
        for item in items:
            writer.writerow([item["title"], item["link-product"], item["brand"], item["card-img"]])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        cards.extend(get_content(html))
        save_content(cards, CSV)
    else:
        print("Something went wrong :(")

parser()