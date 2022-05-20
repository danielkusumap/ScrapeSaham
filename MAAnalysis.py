from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QDialog
import sys
from os import listdir
import pandas as pd

class MAAnalysis(QDialog):
    def __init__(self):
        super(MAAnalysis, self).__init__()
        uic.loadUi('MAAnalysis.ui', self)

        self.emiten = ""
        self.ma = ""
        self.max_loss= -3
        self.list_transaksi = []
        self.list_transaksi_return = []

        self.ma_combobox_urutkan.activated[str].connect(self.urutkan)
        self.ma_checkbox.stateChanged.connect(self.checkbox_state)

        self.setWindowTitle("Detail")

    def checkbox_state(self):
        isChecked = self.ma_checkbox.isChecked()
        if isChecked:
            self.ma_input.setDisabled(False)
        else:
            self.ma_input.setDisabled(True)
            try:
                self.ma = int(self.ma_input.toPlainText())
                self.list_transaksi = []
                self.getwinLoss()
            except:
                self.ma_label.setText("Pastikan MA int!")

    def getwinLoss(self):
        # self.ma_emiten.setText(f"Emiten: {self.emiten}")
        self.ma_value.setText(f"Menggunakan MA")
        df = pd.read_csv(f"data_saham/{self.emiten}.JK.csv")
        df = df[::-1]
        start, end = 0, self.ma
        transaksi_terakhir = "jual"
        total_transaksi = 0
        list_data = []
        for date, close in zip(df["Date"], df["Adj Close"]):
            if len(df["Adj Close"][start:end]) == self.ma:
                manya = sum(df["Adj Close"][start:end])/self.ma
                start += 1
                end += 1
                temp = [date, close,manya]
                list_data.append(temp)
        
        list_data = list_data[::-1]
        win_loss = []
        harga_beli = ""
        harga_jual = ""
        tanggal_beli = ""
        tanggal_jual = ""
        # list_transaksi = []
        for data in list_data:
            try:
                returnnya = round(((data[1] - harga_beli)/harga_beli)*100,2)
            except:
                returnnya = 0
            if data[1] > data[2] and transaksi_terakhir == "jual":
                transaksi_terakhir = "beli"
                harga_beli = data[1]
                tanggal_beli = data[0]
            elif (data[1] < data[2] and transaksi_terakhir == "beli"):
                transaksi_terakhir = "jual"
                total_transaksi += 1
                harga_jual = data[1]
                tanggal_jual = data[0]
                if harga_beli >= harga_jual:
                    # self.list_transaksi.append([tanggal_beli, tanggal_jual, harga_beli, harga_jual])
                    win_loss.append(0)
                else:
                    # self.list_transaksi.append([tanggal_beli, tanggal_jual, harga_beli, harga_jual])
                    # print(harga_beli, harga_jual, tanggal_beli, tanggal_jual)
                    win_loss.append(1)
                self.list_transaksi.append([tanggal_beli, tanggal_jual, harga_beli, harga_jual])
            # elif (returnnya <= self.max_loss) and transaksi_terakhir == "beli":
            #     print(returnnya)
            #     transaksi_terakhir = "jual"
            #     total_transaksi += 1
            #     harga_jual = data[1]
            #     tanggal_jual = data[0]
            #     if harga_beli >= harga_jual:
            #         win_loss.append(0)
            #     else:
            #         win_loss.append(1)
            #     self.list_transaksi.append([tanggal_beli, tanggal_jual, harga_beli, harga_jual])

        self.ma_total_transactions.setText(f"Total Transactioins: {len(win_loss)}")
        self.ma_win.setText(f"Win: {win_loss.count(1)}")
        self.ma_loss.setText(f"Loss: {win_loss.count(0)}")
        win_rate = round((win_loss.count(1)/len(win_loss))*100,2)
        self.ma_winrate.setText(f"Win Rate: {win_rate}%")

        self.inputToTable()
        # self.ma_table_detail.setRowCount(0)
        # total = len(self.list_transaksi)
        # self.ma_table_detail.setRowCount(total)
        # for i in range(total):
        #     self.ma_table_detail.setItem(i, 0, QTableWidgetItem(str(self.list_transaksi[i][0])))
        #     self.ma_table_detail.setItem(i, 1, QTableWidgetItem(str(self.list_transaksi[i][1])))
        #     self.ma_table_detail.setItem(i, 2, QTableWidgetItem(str(self.list_transaksi[i][2])))
        #     self.ma_table_detail.setItem(i, 3, QTableWidgetItem(str(self.list_transaksi[i][3])))
        #     returnnya = round(((self.list_transaksi[i][3] - self.list_transaksi[i][2])/self.list_transaksi[i][2])*100,2)
        #     self.ma_table_detail.setItem(i, 4, QTableWidgetItem(str(f"{returnnya}%")))

    def inputToTable(self, urutkan = "Terlama"):
        if urutkan == "Terbaru":
            list_transaksi = self.list_transaksi[::-1]
        elif urutkan == "Terlama":
            list_transaksi = self.list_transaksi
        elif urutkan == "%Tertinggi":
            list_transaksi = [i[1] for i in sorted(self.list_transaksi_return)[::-1]]
        elif urutkan == "%Terendah":
            list_transaksi = [i[1] for i in sorted(self.list_transaksi_return)]
        self.list_transaksi_return.clear()
        self.ma_table_detail.setRowCount(0)
        total = len(list_transaksi)
        self.ma_table_detail.setRowCount(total)
        return_sum = 0
        for i in range(total):
            self.ma_table_detail.setItem(i, 0, QTableWidgetItem(str(list_transaksi[i][0])))
            self.ma_table_detail.setItem(i, 1, QTableWidgetItem(str(list_transaksi[i][1])))
            self.ma_table_detail.setItem(i, 2, QTableWidgetItem(str(list_transaksi[i][2])))
            self.ma_table_detail.setItem(i, 3, QTableWidgetItem(str(list_transaksi[i][3])))
            returnnya = round(((list_transaksi[i][3] - list_transaksi[i][2])/list_transaksi[i][2])*100,2)
            self.list_transaksi_return.append([returnnya, list_transaksi[i]])
            return_sum += returnnya
            self.ma_table_detail.setItem(i, 4, QTableWidgetItem(str(f"{returnnya}%")))

        # print(self.list_transaksi_return[:5])
        # print(sorted(self.list_transaksi_return)[:5])
        # print(self.list_transaksi_return[:5])
        # self.ma_average_return.setText(f"Avg Return: {round(return_sum/len(list_transaksi),2)}%")
        self.ma_average_return.setText(f"Total Return: {round(return_sum,2)}%")

    def urutkan(self):
        urut = self.ma_combobox_urutkan.currentText()
        try:
            self.inputToTable(urutkan=urut)
        except:
            pass