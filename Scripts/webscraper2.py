
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import random
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

start_time = time.time()
pages = []
for p in range(1, 284):
    pages.append(
        f"https://www.nasdaq.com/market-activity/stocks/screener?page={p}&rows_per_page=25"
    )

stock_list = []

for page in pages:
    driver.get(page)

    time.sleep(random.uniform(3, 5))

    soup = bs(driver.page_source, "html.parser")

    rows = soup.select(
        "tbody.jupiter22-c-symbol-screener-table__body tr"
    )

    print("Rows found:", len(rows))  

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 6:
            continue

        ticker = tds[0].find("a").text.strip()
        name = tds[1].find("a").text.strip()
        last_price = tds[2].text.strip()
        net_change = tds[3].text.strip()
        pct_change = tds[4].text.strip()
        market_cap = tds[5].text.strip()

        stock_list.append([
            ticker,
            name,
            last_price,
            net_change,
            pct_change,
            market_cap
        ])



stocks_df = pd.DataFrame(stock_list,columns=["Ticker","Name","Last Sale","Net Change","% Change","Market Cap"])
print(stocks_df.head())
stocks_df.to_csv("../Data/stocks.csv")
end_time= time.time()