# Save as app/crawler_dynamic.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv, time, os

def run_dynamic():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.shl.com/solutions/products/product-catalog/")
    time.sleep(6)  # wait for JS to load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    rows = []
    for a in soup.select("a[href*='/product/']"):
        name = a.get_text(" ", strip=True)
        href = a.get("href")
        if name and "/product/" in href and "solutions" not in href:
            rows.append({"Assessment Name": name, "URL": href})

    driver.quit()

    os.makedirs("data", exist_ok=True)
    with open("data/shl_catalog.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Assessment Name", "URL"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to data/shl_catalog.csv")

if __name__ == "__main__":
    run_dynamic()
