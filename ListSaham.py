from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def get_list_saham(csv_file):
    CSV_FILE = csv_file
    options = Options()
    options.add_argument('--log-level=3')
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options = options)

    print("web loading")
    driver.get("https://www.idx.co.id/data-pasar/data-saham/daftar-saham/")

    while True:
        time.sleep(1)
        try:
            entry = Select(driver.find_element(By.XPATH, '//*[@id="stockTable_length"]/label/select'))
            entry.select_by_visible_text("100")
            break
        except:
            pass

    print("web loaded")
    time.sleep(0.5)

    sectors = ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
                "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

    papan = ["Akselerasi", "Utama", "Pengembangan"]


    print("Collecting data")
    list_kode = []
    list_nama_perusahaan = []
    for se in sectors:
        sec = driver.find_element(By.XPATH, '//*[@id="select2-sectorList-container"]')
        sec.click()
        sec_input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
        sec_input.send_keys(se)
        sec_input.send_keys(Keys.ENTER)
        
        for pa in papan:
            # print(se, pa)
            pap = driver.find_element(By.XPATH, '//*[@id="select2-boardList-container"]')
            pap.click()
            pap_input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
            pap_input.send_keys(pa)
            pap_input.send_keys(Keys.ENTER)
            
            
            cari = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div[4]/button')
            cari.click()
            time.sleep(2)
            count = 1
            while True:
                try:
                    kode = driver.find_element(By.XPATH, f'//*[@id="stockTable"]/tbody/tr[{count}]/td[2]')
                    nama_perusahaan = driver.find_element(By.XPATH, f'//*[@id="stockTable"]/tbody/tr[{count}]/td[3]')
                    list_kode.append(kode.text)
                    list_nama_perusahaan.append(nama_perusahaan.text)
                    count += 1
                except:
                    break

    df = pd.DataFrame({
        "kode": list_kode,
        "nama perusahaan": list_nama_perusahaan
    })
    df.to_csv(CSV_FILE, index = False)

    print(f"data collected and saved as {CSV_FILE}")
    print("Finished")
    driver.quit()

if __name__ == "__main__":
    get_list_saham("list_saham.csv")