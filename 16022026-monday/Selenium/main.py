from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    print("driver created")
    return driver


def open_page(driver, local_url):
    driver.get(local_url)
    print("File opened")


def extract_table_rows(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols_text = [col.text.strip() for col in cols]
        data.append(cols_text)

    # print(data)
    return data


def paginate(driver, pages=5):
    base_url = "https://www.scrapethissite.com/pages/forms/"
    all_data = []
    for page in range(1, pages + 1):
        driver.get(f"{base_url}?page_num={page}")
        table_data = extract_table_rows(driver)
        all_data.extend(table_data)
    print(all_data)


if __name__ == "__main__":
    drvr = create_driver()
    url = "https://www.scrapethissite.com/pages/forms/"
    open_page(drvr, url)
    # extract_table_rows(drvr)
    paginate(drvr)