from email import header
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyQt5.QtCore import pyqtSignal,QObject
from PyQt5.QtWidgets import QDialog
import requests, time, os
import pandas as pd

class DataSaham(QObject):
    message_signal = pyqtSignal(str)
    finished = pyqtSignal()
    emiten = ""
    def get_data(self, csv_file = "list_saham.csv"):
        self.message_signal.emit("started")
        data = self.emiten
        if data == "semua":
            df = pd.read_csv(csv_file)
            total_data = len(df)
            list_kode = list(df["kode"])
        else:
            list_kode = [data]
            total_data = len(list_kode)

        options = Options()
        options.add_argument("--headless")
        options.add_argument('--log-level=3')

        driver = webdriver.Chrome(options = options)

        self.message_signal.emit(f"checking for new available data\n")

        cek = list_kode[0]
        url_tgl = f"https://finance.yahoo.com/quote/{cek}.JK/history?p={cek}.JK"
        driver.get(url_tgl)

        tanggal = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[1]/td[1]/span')
        bulan = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Okt": "10",
            "Nov": "11",
            "Dec": "12"
        }
        tanggal = tanggal.text.replace(",", "")
        tanggal = tanggal.split()
        tanggal = f"{tanggal[2]}-{bulan[tanggal[0]]}-{tanggal[1]}"
        # self.message_signal.emit(f"{tanggal}")
        # print("program started")

        count = 1
        berhasil, gagal = 0,0
        for kode in list_kode:
            self.message_signal.emit("started")
            # os.system("cls")
            # print(f"collecting data ({kode}) {count}/{total_data}")
            
            try:
                df_emiten = pd.read_csv(f"data_saham/{kode}.JK.csv")
                self.message_signal.emit(f"{kode} found in local\n")
                self.message_signal.emit(f"collecting data ({kode}) {count}/{total_data}\n")
                # df_emiten = df_emiten[::-1]
                tanggal_terakhir = df_emiten["Date"].iloc[-1]
                if tanggal == tanggal_terakhir:
                    self.message_signal.emit(f"{kode} updated\n")
                    berhasil += 1
                    count += 1
                    update_data = False
                else:
                    self.message_signal.emit(f"updating {kode} ...\n")
                    update_data = True
            except:
                self.message_signal.emit(f"{kode} not found in local\n")
                self.message_signal.emit(f"collecting data ({kode}) {count}/{total_data}\n")
                update_data = True
            finally:
                if update_data:
                    # self.message_signal.emit(f"collecting data ({kode}) {count}/{total_data}\n")
                    url = f"https://finance.yahoo.com/quote/{kode}.JK/history?p={kode}.JK"
                    # self.message_signal.emit(url)
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
                    # self.message_signal.emit(str(berhasil)+"\n")
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
                        self.message_signal.emit(f"{kode} collected\n")
                        count += 1
                    except:
                        # self.message_signal.emit("except\n")
                        pass
        self.message_signal.emit(f"gagal: {gagal}, berhasil: {berhasil}\n")
        self.message_signal.emit(f"total: {gagal + berhasil}\n")
        self.message_signal.emit("finished")
        self.finished.emit()
        driver.quit()
        # print(f"gagal: {gagal}, berhasil: {berhasil}, total: {gagal+berhasil}")

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
    for kode in df["kode"]:
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