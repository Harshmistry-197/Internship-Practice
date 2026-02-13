import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"

def fetch_basic():
    response = requests.get(url)
    print(response.status_code)
    print(response.text[:500]) # print first 500 character


def parse_html():
    respose = requests.get(url)
    soup = BeautifulSoup(respose.text, "html.parser")

    print(soup.title)
    print(soup.title.string)


def find_elements():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    print(f"Finding single Element {soup.find("h3")}\n")
    print(f"Finding all elements {soup.find_all("h3")}\n")


def extract_attributes():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    anchor = soup.find_all("a")
    for href in anchor:
        print(href.get("href"))


def merge_section_and_ptag():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all("section")

    for section in sections:
        h1 = section.find("h1")
        p = section.find_all("p")
        if h1:
            print(h1.text)
            for p1 in p:
                print(f" -> {p1.text}")
            print()


def store_to_list():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    list1 = []
    title = soup.find_all("title")
    p = soup.find_all("p")
    for title, p in zip(title, p):
        list1.append({
            "Main Heading" : title.text,
            "Sub Heading" : p.text
        })
    print(list1)


def store_to_csv():

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")


    # 1. Find all div tags with the class "highlight"
    codes = soup.select_one("div.highlight-default pre")

    # 2. Transform the Tag objects into a list of dictionaries containing just the text
    # We use .get_text() to extract only the code snippets
    data_to_save = [{"code snippets": tag.get_text().strip()} for tag in codes]

    # 3. Open file with newline="" to avoid blank rows
    with open("codes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["code snippets"])
        writer.writeheader()

        # 4. Now writerows receives a list of dicts, which it expects
        writer.writerows(data_to_save)




if __name__ == "__main__":
    # fetch_basic()
    # parse_html()
    # find_elements()
    # extract_attributes()
    # merge_section_and_ptag()
    # store_to_list()
    store_to_csv()