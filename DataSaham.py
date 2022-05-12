from email import header
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests, time, os
import pandas as pd

def get_data(csv_file):
    df = pd.read_csv(csv_file)

    total_data = len(df)

    options = Options()
    options.add_argument("--headless")
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options = options)

    print("program started")

    count = 1
    berhasil, gagal = 0,0
    for kode in df["kode"][140:]:
        os.system("cls")
        print(f"collecting data ({kode}) {count}/{total_data}")
        url = f"https://finance.yahoo.com/quote/{kode}.JK/history?p={kode}.JK"
        driver.get(url)

        x = 0
        while True:
            time.sleep(0.5)
            if x > 30:
                gagal += 1
                break
            try:
                find_link = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
                berhasil += 1
                break
            except:
                pass
            x += 1

        try:
            period = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div')
            period.click()

            max_period = driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button')
            max_period.click()

            find_link = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
            link_download = find_link.get_attribute("href")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
            }
            r = requests.get(link_download, headers=headers)
            open(f"data_saham/{kode}.JK.csv", "wb").write(r.content)
            count += 1
        except:
            pass
    driver.quit()
    print(f"gagal: {gagal}, berhasil: {berhasil}, total: {gagal+berhasil}")

if __name__ == "__main__":
    get_data("list_saham.csv")