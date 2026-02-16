import requests
from bs4 import BeautifulSoup


def basic_fetch():
    response = requests.get("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    sop = BeautifulSoup(response.text, "html.parser")

    return sop


def extract_h1_h2_h3(soup):
    headings = soup.find_all(["h1", "h2", "h3"])
    for heading in headings:
        print(heading.text)


def extract_link(soup):
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        text = link.text
        print(f"{text} -> {href}")


def find_section(soup):
    section = soup.find("section", id="kinds-of-objects")
    print(section.text)


def extract_code_block(soup):
    codes = soup.select("div.highlight pre")

    for code in codes:
        print("------Code-------")
        print(code.text)


def scrape_all(soup):
    links = soup.find_all("a")
    internal_doc = []

    for link in links:
        href = link.get("href")

        if href and href.startswith("#"):
            internal_doc.append(href)

    print(internal_doc)


def save_to_txt(soup):
    with open("internal.txt", "w", encoding="utf-8") as file:
        heading = soup.find_all(["h1", "h2", "h3"])
        for head in heading:
            file.write(head.text+ "\n\n")

        for code in soup.select("div.highlight pre"):
            file.write("----Code-------\n")
            file.write(code.text+"\n\n")




if __name__ == "__main__":
    sup = basic_fetch()
    # extract_h1_h2_h3(sup)
    # extract_link(sup)
    # find_section(sup)
    # extract_code_block(sup)
    scrape_all(sup)
    save_to_txt(sup)
    print("success")
