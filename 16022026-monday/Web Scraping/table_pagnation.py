import requests
from bs4 import BeautifulSoup
import pandas as pd


def basic_fetch():
    response = requests.get("https://www.scrapethissite.com/pages/forms/")
    sop = BeautifulSoup(response.text, "html.parser")
    print(response.status_code)

    return sop


def extract_table_header(soup):
    table = soup.find("table", class_="table")
    headers = []
    for th in table.find_all("th"):
        headers.append(th.get_text(strip=True))
    # print(headers)
    return headers


def extract_table_row(soup):
    table = soup.find("table", class_="table")
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        for td in cols:
            cols = td.get_text(strip=True)
            data.append(cols)
    print(data)

    # data = []
    # rows = soup.find("tbody").find_all("tr")
    # for row in rows:
    #     cols = row.find_all("td")
    #     for col in cols:
    #         data.append(col.get_text(strip=True))


def structure_format(soup, headers):
    stuc_data = []

    table = soup.find("table", class_="table")
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        team_data = {
            headers[i]: cols[i].get_text(strip=True) for i in range(len(cols))
        }
        stuc_data.append(team_data)
    print(stuc_data[:4])



def pagination():
    all_data = []
    for page in range(1, 3):
        url = f"https://www.scrapethissite.com/pages/forms/?page_num={page}"
        print(f"Pagination for page {page}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="table")
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            for td in cols:
                cols = td.get_text(strip=True)
                all_data.append(cols)

    print(len(all_data))


def table_format():
    response = requests.get("https://www.scrapethissite.com/pages/forms/")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table")

    headers = []
    for head in table.find_all("th"):
        headers.append(head.get_text(strip=True))

    rows = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")

        # Skip rows that don't have td elements (like the header row)
        if len(cols) == 0:
            continue

        # 3. Create a NEW list for this specific row's data
        current_row_data = []
        for td in cols:
            current_row_data.append(td.get_text(strip=True))
        rows.append(current_row_data)

    df = pd.DataFrame(rows, columns=headers)
    print(df)



def table_pagination():
    # all_rows = []
    # headers = []
    # for page in range(1, 3):
    #     url = f"https://www.scrapethissite.com/pages/forms/?page_num={page}"
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #
    #     table = soup.find("table", class_="table")
    #
    #     if not headers:
    #         headers = [head.get_text(strip=True) for head in table.find_all("th")]
    #
    #     rows = table.find_all("tr")
    #     for row in rows:
    #         cols = row.find_all("td")
    #         for td in cols:
    #             cols = [td.get_text(strip=True)]
    #             all_rows.append(cols)
    # print(f"Total rows collected : {len(all_rows)}")
    #
    #
    # df = pd.DataFrame(all_rows, columns=headers)
    # print(df.head())

    all_rows = []
    headers = []

    for page in range(1, 24):
        url = f"https://www.scrapethissite.com/pages/forms/?page_num={page}"
        print(f"Pagination for page {page}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="table")

        # Get headers only once
        if not headers:
            headers = [head.get_text(strip=True) for head in table.find_all("th")]

        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if not tds:
                continue

            # Group all cells for THIS row into one list
            row_data = [td.get_text(strip=True) for td in tds]
            all_rows.append(row_data)

    print(f"Total rows collected: {len(all_rows)}")

    # Now all_rows is a list of lists, which matches the 9 headers
    df = pd.DataFrame(all_rows, columns=headers)
    print(df)
    df.to_csv("table_pagination.csv")




if __name__ == "__main__":
    sup = basic_fetch()
    head =  extract_table_header(sup)
    # extract_table_row(sup)
    # structure_format(sup, head)
    # pagination()
    # table_format()
    table_pagination()
    # print(sup.prettify())
