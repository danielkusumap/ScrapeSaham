from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
import time
import pandas as pd
from Sektor import Sektor

class ListSaham(QDialog):
    message_signal = pyqtSignal(str)
    def get_list_saham(self, sektornya = Sektor.ALL, csv_file = "list_saham.csv"):
        
        CSV_FILE = csv_file
        options = Options()
        options.add_argument('--log-level=3')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        options.add_argument("--headless")

        driver = webdriver.Chrome(options = options)

        self.message_signal.emit(f"{sektornya.value} sektor\n")
        self.message_signal.emit("web loading\n")
        # print(f"{sektornya.value} sektor")
        # print("web loading")
        driver.get("https://www.idx.co.id/data-pasar/data-saham/daftar-saham/")

        while True:
            time.sleep(1)
            try:
                entry = Select(driver.find_element(By.XPATH, '//*[@id="stockTable_length"]/label/select'))
                entry.select_by_visible_text("100")
                break
            except:
                pass
        
        self.message_signal.emit("web loaded\n")
        # print("web loaded")
        time.sleep(0.5)

        sectors = ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
                    "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

        papan = ["Akselerasi", "Utama", "Pengembangan"]

        if sektornya != Sektor.ALL:
            sectors = [sektornya.value]

        self.message_signal.emit("collecting data\n")
        # print("Collecting data")
        list_kode = []
        list_nama_perusahaan = []
        list_sektor = []
        for se in sectors:
            self.message_signal.emit(f"Sektor: {se}\n")
            # print(f"Sektor: {se}")
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
                        list_sektor.append(se)
                        count += 1
                    except:
                        break

        df = pd.DataFrame({
            "kode": list_kode,
            "nama perusahaan": list_nama_perusahaan,
            "sektor": list_sektor
        })
        df.to_csv(CSV_FILE, index = False)

        self.message_signal.emit("data collected\n")
        self.message_signal.emit("Finished\n")
        # print(f"data collected and saved as {CSV_FILE}")
        # print("Finished")
        driver.quit()

def get_list_saham(sektor = Sektor.ALL, csv_file = "list_saham.csv"):
    CSV_FILE = csv_file
    options = Options()
    options.add_argument('--log-level=3')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    options.add_argument("--headless")

    driver = webdriver.Chrome(options = options)

    print(f"{sektor.value} sektor")
    print("web loading")
    driver.get("https://www.idx.co.id/data-pasar/data-saham/daftar-saham/")

    while True:
        time.sleep(1)
        print("CCCCCCCc")
        try:
            print("A")
            driver.find_element(By.XPATH, '//*[@id="stockTable_length"]/label/select')
            print("B")
            entry = Select(driver.find_element(By.XPATH, '//*[@id="stockTable_length"]/label/select'))
            entry.select_by_visible_text("100")
            break
        except:
            print("Except")
            pass

    print("web loaded")
    time.sleep(0.5)

    sectors = ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
                "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

    papan = ["Akselerasi", "Utama", "Pengembangan"]

    if sektor != Sektor.ALL:
        sectors = [sektor.value]

    print("Collecting data")
    list_kode = []
    list_nama_perusahaan = []
    list_sektor = []
    for se in sectors:
        print(f"Sektor: {se}")
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
                    list_sektor.append(se)
                    count += 1
                except:
                    break

    df = pd.DataFrame({
        "kode": list_kode,
        "nama perusahaan": list_nama_perusahaan,
        "sektor": list_sektor
    })
    df.to_csv(CSV_FILE, index = False)

    print(f"data collected and saved as {CSV_FILE}")
    print("Finished")
    driver.quit()

def test(s = Sektor.ALL):
    print([x.value for x in Sektor])

if __name__ == "__main__":
    get_list_saham()
    # test()