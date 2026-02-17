import requests
from bs4 import BeautifulSoup


URL = "https://www.scrapethissite.com/pages/forms/"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) EducationalScraper/1.0'}

MAX_DISPLAY = 15

def scrape_nh1_teams():
    print("NHL Team Scraper")
    print(f"Fetching: {URL}\n")

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

        print(f"Success Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        print(f"Page Title: {soup.title.string.strip()}")

        team_rows = soup.select("tr.team")

        if not team_rows:
            print(f"No rows with class='team' Found\n")
            return []


        print(f"Found {len(team_rows)} Team Rows\n")

        teams = []

        for row in team_rows:
            name_cell = row.select_one("td.name")
            year_cell = row.select_one("td.year")
            win_cell = row.select_one("td.wins")
            loss_cell = row.select_one("td.losses")
            tl_cell = row.select_one("td.ot-losses")
            pct_cell = row.select_one("td.pct")
            gf_cell = row.select_one("td.gf")
            ga_cell = row.select_one("td.diff text-success")
            diff_cell = row.select_one("td.diff")


            if not name_cell or not year_cell:
                continue

            team = {
                "Team": name_cell.get_text(strip=True),
                "Year": year_cell.get_text(strip=True),
                "W": win_cell.get_text(strip=True) if win_cell else "-",
                "L": loss_cell.get_text(strip=True) if loss_cell else "-",
                "OTL": tl_cell.get_text(strip=True) if tl_cell and tl_cell.get_text(strip=True) else "-",
                "Win%": pct_cell.get_text(strip=True) if pct_cell else "-",
                "GF": gf_cell.get_text(strip=True) if gf_cell else "-",
                "GA": ga_cell.get_text(strip=True) if ga_cell else "-",
                "+/-": diff_cell.get_text(strip=True) if diff_cell else "-"
            }

            teams.append(team)

        return teams

    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return []
    except Exception as e:
        print(f"Unknown Error: {e}")

def display_teams(teams):
    if not teams:
        print("No teams extracted.")
        return

    print(f"{'#':<3} {'Team':<25} {'Year':<6} {'W':<4} {'L':<4} {'OTL':<5} {'Win%':<6} {'GF':<5} {'GA':<5} {'+/-':<5}")
    print("─" * 90)

    for i, t in enumerate(teams[:MAX_DISPLAY], 1):
        print(f"{i:<3} {t['Team']:<25} {t['Year']:<6} {t['W']:<4} {t['L']:<4} "
                f"{t['OTL']:<5} {t['Win%']:<6} {t['GF']:<5} {t['GA']:<5} {t['+/-']:<5}")

    if len(teams) > MAX_DISPLAY:
         print(f"\n... showing first {MAX_DISPLAY} of {len(teams)} teams")



 

if __name__ == "__main__":
    scrape_nh1_teams()
    teams_list = scrape_nh1_teams()
    display_teams(teams_list)