import requests
from bs4 import BeautifulSoup
import time


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
            file.write("-----Code-------\n")
            file.write(code.text+"\n\n")

def advance_scrape_section(soup):
    sections = soup.find_all("div", class_="section")

    for section in sections:
        section_id = section.get("id")
        title = section.find(["h1", "h2", "h3"])

        if title:
            print("SECTION:", title.get_text(strip=True))

        print("-" * 50)




def structure_data_extraction(soup):
    data = []

    sections = soup.find_all("div", class_="section")

    for section in sections:
        title_tag = section.find(["h1", "h2", "h3"])

        if title_tag:
            title = title_tag.get_text(strip=True)

            content = section.get_text(strip=True)

            data.append({
                "title": title,
                "content": content
            })

    print(data[:2])




def sleep_program():
    time.sleep(2)



def advance_selector(soup):
    # Select section by id
    soup.select_one("#kinds-of-objects")

    # Select all code blocks
    soup.select("div.highlight > pre")

    # Select nested heading
    soup.select("div.section h2")


if __name__ == "__main__":
    sup = basic_fetch()
    # extract_h1_h2_h3(sup)
    # extract_link(sup)
    # find_section(sup)
    # extract_code_block(sup)
    scrape_all(sup)
    save_to_txt(sup)
    sleep_program()
    advance_scrape_section(sup)
    structure_data_extraction(sup)
    sleep_program()
    advance_selector(sup)
    print("success")
