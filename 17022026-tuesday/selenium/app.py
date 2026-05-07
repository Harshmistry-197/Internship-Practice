"""
Selenium Demo - NHL Teams Scraper (Reliable URL Pagination)
===========================================================

Target: https://www.scrapethissite.com/pages/forms/

This version uses direct URL pagination (?page_num=) instead of clicking "Next".
This avoids common click failures on this site and is much more stable.

Features:
- Automatic ChromeDriver via webdriver-manager
- Headless by default
- Scrapes all pages (~24–25)
- Saves to CSV
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────

BASE_URL = "https://www.scrapethissite.com/pages/forms/"
CSV_FILENAME = "nhl_teams_selenium_all.csv"

HEADLESS = True
PAGE_DELAY = 1.8  # polite delay between pages


# ────────────────────────────────────────────────
# SELENIUM SETUP
# ────────────────────────────────────────────────

def init_driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) EducationalSelenium/1.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# ────────────────────────────────────────────────
# SCRAPING FUNCTIONS
# ────────────────────────────────────────────────

def scrape_page(driver, wait: WebDriverWait, page_num: int) -> list[dict]:
    url = f"{BASE_URL}?page_num={page_num}"
    print(f"Loading: {url}")
    driver.get(url)

    teams = []

    try:
        # Wait for table rows
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.team")))

        team_rows = driver.find_elements(By.CSS_SELECTOR, "tr.team")
        print(f"  Page {page_num}: Found {len(team_rows)} teams")

        for row in team_rows:
            try:
                team = {
                    "Team": row.find_element(By.CSS_SELECTOR, "td.name").text.strip(),
                    "Year": row.find_element(By.CSS_SELECTOR, "td.year").text.strip(),
                    "Wins": row.find_element(By.CSS_SELECTOR, "td.wins").text.strip(),
                    "Losses": row.find_element(By.CSS_SELECTOR, "td.losses").text.strip(),
                    "OTL": row.find_element(By.CSS_SELECTOR, "td.ot-losses").text.strip() or "",
                    "Win%": row.find_element(By.CSS_SELECTOR, "td.pct").text.strip(),
                    "GF": row.find_element(By.CSS_SELECTOR, "td.gf").text.strip(),
                    "GA": row.find_element(By.CSS_SELECTOR, "td.ga").text.strip(),
                    "+/-": row.find_element(By.CSS_SELECTOR, "td.diff").text.strip()
                }
                teams.append(team)
            except:
                continue  # skip broken rows

    except Exception as e:
        print(f"  Page {page_num} extraction failed: {e}")

    return teams


def scrape_all_pages():
    driver = init_driver()
    all_teams = []
    page_num = 1

    wait = WebDriverWait(driver, 12)

    try:
        while True:
            page_teams = scrape_page(driver, wait, page_num)

            if not page_teams:
                print(f"  Page {page_num}: No teams → stopping")
                break

            all_teams.extend(page_teams)
            page_num += 1
            time.sleep(PAGE_DELAY)

    finally:
        driver.quit()
        print("Browser closed.")

    return all_teams


def save_to_csv(teams: list[dict]):
    if not teams:
        print("No data scraped.")
        return

    fieldnames = teams[0].keys()

    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teams)

    print(f"Saved {len(teams)} teams to {CSV_FILENAME}")


# ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Selenium Demo - NHL Teams (URL Pagination) ===")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = time.time()

    teams_data = scrape_all_pages()

    print(f"\nTotal teams: {len(teams_data)}")
    save_to_csv(teams_data)

    elapsed = time.time() - start_time
    print(f"\nFinished in {elapsed:.2f} seconds (~{elapsed / 60:.1f} min)")

    print("\nTeaching points:")
    print("  • Prefer URL-based pagination when available → simpler & more reliable")
    print("  • Avoid clicking if possible — reduces flakiness")
    print("  • Use driver.get() to jump directly to any page")
    print("  • This site doesn't need Selenium, but shows how to handle dynamic cases")