import threading
from datetime import date

import os
from PyQt5 import uic
from PyQt5.QtCore import QThreadPool, QRegularExpression, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel
import time
import sys
from definitions import get_country_codes_na, get_country_code_eu, links_eu, links_na
import logging

from extractor import Extractor

class Ui(QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi("Ui/MainWindow.ui", self)

        self.all_contry_codes = get_country_codes_na() + get_country_code_eu()
        self.selected_countries = dict.fromkeys(self.all_contry_codes, False)
        self.start = 0
        self.end = 0
        self.extractor = Extractor()
        self.extractor.finished.connect(self.check_if_changed)

        self.all_links = {}
        self.all_links.update(links_na)
        self.all_links.update(links_eu)

        self.threadpool = QThreadPool()

        self.links_to_crawl = {}

        # Start button
        self.button_start = self.findChild(QPushButton, 'pushButton_start')
        self.button_start.clicked.connect(self.startButtonPressed)

        # All Checked:
        self.checkbox_all = self.findChild(QCheckBox, 'checkBox_all')
        self.checkbox_all.stateChanged.connect(self.allSetChanged)

        # All Check NA
        self.checkbox_all_na = self.findChild(QCheckBox, 'checkBox_na')
        self.checkbox_all_na.stateChanged.connect(self.allSetNAChanged)

        # All Checked EU
        self.checkbox_all_eu = self.findChild(QCheckBox, 'checkBox_eu')
        self.checkbox_all_eu.stateChanged.connect(self.allSetEUChanged)

        self.label_output = self.findChild(QLabel, "label_output")


    def startButtonPressed(self):
        self.start = time.time()
        self.update_checkbox_list()
        self.generate_links()

        if self.links_to_crawl:
            self.label_output.setText("Processing ...")
            threading.Thread(target=self.extractor.start, args=(self.links_to_crawl,)).start()
        else:
            print("Please select at least one country")
            self.label_output.setText("Please select at least one country")
       
        

    def allSetChanged(self, state):
        self.allSetNAChanged(state)
        self.allSetEUChanged(state)

    def allSetNAChanged(self, state):
        na_checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_na_.*'))
        na_checkboxes.append(self.checkbox_all_na)
        for checkbox in na_checkboxes:
            checkbox.setChecked(state == Qt.Checked)


    def allSetEUChanged(self, state):
        eu_checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_eu_.*'))
        eu_checkboxes.append(self.checkbox_all_eu)
        for checkbox in eu_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def update_checkbox_list(self):
        checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_.*_.*'))
        for checkbox in checkboxes:
            self.selected_countries[checkbox.objectName().split('_')[2]] = checkbox.isChecked()

    def generate_links(self):
        self.links_to_crawl = {}
        for code in self.all_contry_codes:
            links_to_crawl_temp = []
            if self.selected_countries[code]:
                links_to_crawl_temp.append(self.all_links[code])
                links_to_crawl_temp.append(self.all_links[code].replace("models","modelx"))
                links_to_crawl_temp.append(self.all_links[code].replace("models","model3"))
                links_to_crawl_temp.append(self.all_links[code].replace("models","modely"))
                self.links_to_crawl[code] = links_to_crawl_temp


    def check_if_changed(self):
        today = date.today().strftime("%d_%m_%y")
        models = ["models", "modelx", "model3", "modely"]

        output_text = ""
        for key in self.links_to_crawl:
            prefix = "differences/"+key +"/"
            for model in models:
                filename = prefix + "diff_" + model + "_" + today + ".diff"
                if not os.path.exists(filename):
                    continue

                filesize = os.path.getsize(filename)

                if filesize > 1250:
                    output_text += "Possible change in " + key + " " + model + "\n"

        if len(output_text) == 0:
            output_text = 'No changes found.'

        self.label_output.setText(output_text)
        self.end = time.time()
        logging.info("Processing done in %d seconds", self.end - self.start)


app = QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
