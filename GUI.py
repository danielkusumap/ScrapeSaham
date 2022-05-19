from ListSaham import ListSaham
from MAAnalysis import MAAnalysis
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QDialog
import sys
from Sektor import Sektor
from DataSaham import DataSaham
import pandas as pd
from threading import *
from os import listdir
import datetime

# class Worker(QObject):
#     finished = pyqtSignal()
#     progress = pyqtSignal(list)

#     def run(self, x):
#         list_data = []
#         try:
#             self.table_data.setRowCount(0)
#             self.label_emiten.setText(f"{self.emitennya} : ")
#             df = pd.read_csv(f"data_saham/{self.emitennya}.JK.csv")
#             self.put_message("Data collected\n")
#             date_list = list(df["Date"])
#             open_list = list(df["Open"])
#             adj_close_list = list(df["Adj Close"])
#             list_data.append(date_list)
#             list_data.append(open_list)
#             list_data.append(adj_close_list)
#             # print("try2")
#             # total = len(date_list)
#             # self.table_data.setRowCount(total)
#             # print("A")
#             # for i in range(total):
#             #     # print("1")
#             #     self.table_data.setItem(i, 0, QTableWidgetItem(str(date_list[i])))
#             #     # print("2")
#             #     self.table_data.setItem(i, 1, QTableWidgetItem(str(open_list[i])))
#             #     # print("3")
#             #     self.table_data.setItem(i, 2, QTableWidgetItem(str(adj_close_list[i])))
#             #     # print("4")
#             #     # break
#             # print("X")
#         except:
#             print("AAAAAA")
#             pass
#         self.progress.emit(list_data)
#         self.finished.emit()

class Ui(QtWidgets.QMainWindow):
    CSV_FILE = "list_saham.csv"
    done = pyqtSignal()
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Main.ui', self)

        self.sektornya = ""
        self.emitennya = ""
        self.message = ""
        self.list_data = ""
        
        self.setWindowTitle("Saham")

        self.listSaham = ListSaham()
        # self.dataSaham = DataSaham()

        self.listSaham.message_signal.connect(self.put_message)
        # self.dataSaham.message_signal.connect(self.put_message)
        sektor = [x.value for x in Sektor]
        self.sektor_key = [x for x in Sektor]
        emiten = self.readList()

        self.combo_box_sektor.clear()
        self.combo_box_sektor.addItems(sektor)
        self.combo_box_sektor.setMaxVisibleItems(5)
        self.combo_box_sektor.activated[str].connect(self.get_sektor)
        
        self.combo_box_emiten.clear()
        self.combo_box_emiten.addItems(emiten)
        self.combo_box_emiten.setMaxVisibleItems(7)
        self.combo_box_emiten.activated[str].connect(self.get_emiten)

        self.emiten_checkbox.stateChanged.connect(self.checkbox_state)
        
        self.get_data_emiten.clicked.connect(self.get_data_emiten_x)
        self.get_list_button.clicked.connect(self.thread_get_list_saham)
        self.get_all_data_button.clicked.connect(self.all_data)
        self.ma_analysis_button.clicked.connect(self.ma_analysis)

        # geek_list = ["Geek", "Geeky Geek", "Legend Geek", "Ultra Legend Geek"]
    #     self.comboBox.addItems(geek_list)
  
    #     # creating a editable combo box
    #     self.comboBox.activated[str].connect(self.test)
    #     self.comboBox.activated.connect(self.test2)
    #     # self.comboBox.setEditable(False)
    #     self.comboBox.setMaxVisibleItems(4)

    def all_data(self):
        if len(self.readList()) == 1:
            self.put_message("Get list dulu\n")
        else:
            self.data_emiten(True)
    
    def readList(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            emiten = [kode for kode in df["kode"]]
        except:
            emiten = ["No data found"]
        return emiten

    def checkbox_state(self):
        isChecked = self.emiten_checkbox.isChecked()
        if isChecked:
            self.combo_box_emiten.setEditable(True)
        else:
            self.combo_box_emiten.setEditable(False)

    def get_data_emiten_x(self):
        if self.emitennya == "":
            # self.message_label.setText("")
            # self.message = ""  
            self.put_message("silahkan pilih emiten dulu")
        else:
            self.data_emiten(False)

    def data_emiten(self, all):
        # self.message_label.setText("")
        # self.message = ""
        self.disabledElement(False, True)
        if all:
            self.thread = QThread()
            self.dataSaham = DataSaham()
            self.dataSaham.emiten = "semua"
            self.dataSaham.moveToThread(self.thread)
            self.thread.started.connect(self.dataSaham.get_data)
            self.dataSaham.finished.connect(self.thread.quit)
            self.dataSaham.finished.connect(self.dataSaham.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.dataSaham.message_signal.connect(self.put_message)
            self.thread.start()
            self.thread.finished.connect(self.tampilin_data)
            # self.disabledElement(True, False)
        
        else:
            self.list_data = ""
            # self.disabledElement(False, True)
            if f"{self.emitennya}.JK.csv" in listdir("data_saham"):
                self.put_message(f"{self.emitennya} found in local\n")
                self.put_message("Collecting data may take a while\n")
                self.put_message("Collecting data ...\n")
                self.tampilin_data()
                # self.list_data = self.tampilin_data()
                # self.list_data = self.tampilin_data()
            else:
                self.put_message(f"{self.emitennya} not found in local\n")
                self.put_message("Collecting data may take a while\n")
                # self.dataSaham.get_data(self.emitennya, self.CSV_FILE)
                self.thread = QThread()
                self.dataSaham = DataSaham()
                self.dataSaham.emiten = self.emitennya
                self.dataSaham.moveToThread(self.thread)
                self.thread.started.connect(self.dataSaham.get_data)
                self.dataSaham.finished.connect(self.thread.quit)
                self.dataSaham.finished.connect(self.dataSaham.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.dataSaham.message_signal.connect(self.put_message)

                self.thread.start()
                self.thread.finished.connect(self.tampilin_data)
                # self.list_data = self.tampilin_data()
            # self.disabledElement(True, False)
        self.disabledElement(True, False)
        

    def tampilin_data(self):
        list_data = []
        try:
            self.table_data.setRowCount(0)
            self.label_emiten.setText(f"{self.emitennya} : ")
            df = pd.read_csv(f"data_saham/{self.emitennya}.JK.csv")
            df = df.iloc[::-1]
            self.put_message("Data collected\n")
            date_list = list(df["Date"])
            open_list = list(df["Open"])
            adj_close_list = list(df["Adj Close"])
            list_data.append(date_list)
            list_data.append(open_list)
            list_data.append(adj_close_list)
            # print("try2")
            total = len(date_list)
            self.table_data.setRowCount(total)
            for i in range(total):
                # print("1")
                self.table_data.setItem(i, 0, QTableWidgetItem(str(date_list[i])))
                # print("2")
                self.table_data.setItem(i, 1, QTableWidgetItem(str(open_list[i])))
                # print("3")
                self.table_data.setItem(i, 2, QTableWidgetItem(str(adj_close_list[i])))
                # print("4")
            # print("X")
        except:
            pass
        self.list_data = list_data

    def thread_get_list_saham(self):
        t1 = Thread(target=self.get_list_saham)
        t1.start()

    def get_list_saham(self):
        if self.sektornya == "":
            # self.message_label.setText("")
            # self.message = ""  
            self.put_message("silahkan pilih sektor dulu")
        else:
            # self.message_label.setText("")
            # self.message = ""
            self.disabledElement(False, True)
            self.listSaham.get_list_saham(sektornya = self.sektornya, csv_file = self.CSV_FILE)
            self.disabledElement(True, False)
            emiten = self.readList()
            self.combo_box_emiten.clear()
            self.combo_box_emiten.addItems(emiten)

    def disabledElement(self, combo_box, button):
        self.combo_box_sektor.setEnabled(combo_box)
        self.combo_box_emiten.setEnabled(combo_box)
        self.get_list_button.setDisabled(button)
        self.get_data_emiten.setDisabled(button)
        self.get_all_data_button.setDisabled(button)
        self.ma_analysis_button.setDisabled(button)

    def put_message(self, text):
        currentime = datetime.datetime.now()
        mixed = currentime.strftime('%H:%M:%S')
        text = f"[{mixed}] {text}"
        self.message += text
        self.message_label.setText(self.message)

    def get_sektor(self):
        self.sektornya = self.combo_box_sektor.currentText()
        for x in self.sektor_key:
            if x.value == self.sektornya:
                self.sektornya = x

    def get_emiten(self):
        self.emitennya = self.combo_box_emiten.currentText()
        self.combo_box_emiten.setEditable(False)
        self.emiten_checkbox.setChecked(False)
    
    def ma_analysis(self):
        maAnalysis = MAAnalysis()
        maAnalysis.emiten = self.emitennya
        maAnalysis.list_transaksi.clear()
        maAnalysis.ma_emiten.setText(f"Emiten: {self.emitennya}")
        # maAnalysis.getwinLoss()
        maAnalysis.exec_()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()