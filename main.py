""" Main GUI """

import logging
import os
import sys
import threading
import time
from datetime import date

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool, QRegularExpression, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow,\
    QPushButton, QCheckBox, QLabel

from definitions import get_country_codes_na, get_country_code_eu, get_country_codes_apac,\
    links_eu, links_na, links_apac
from extractor import Extractor


class Ui(QMainWindow):
    """
    Main Window Class
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()
        uic.loadUi("Ui/MainWindow.ui", self)

        self.all_country_codes = get_country_codes_na() + get_country_code_eu()\
                                 + get_country_codes_apac()
        self.selected_countries = dict.fromkeys(self.all_country_codes, False)
        self.start = 0
        self.end = 0
        self.extractor = Extractor()
        self.extractor.finished.connect(self.check_if_changed)

        self.all_links = {}
        self.all_links.update(links_na)
        self.all_links.update(links_eu)
        self.all_links.update(links_apac)

        self.threadpool = QThreadPool()

        self.links_to_crawl = {}

        # Start button
        self.button_start = self.findChild(QPushButton, 'pushButton_start')
        self.button_start.clicked.connect(self.start_button_pressed)

        # All Checked:
        self.checkbox_all = self.findChild(QCheckBox, 'checkBox_all')
        self.checkbox_all.stateChanged.connect(self.all_set_changed)

        # All Check NA
        self.checkbox_all_na = self.findChild(QCheckBox, 'checkBox_na')
        self.checkbox_all_na.stateChanged.connect(self.all_set_na_changed)

        # All Checked EU
        self.checkbox_all_eu = self.findChild(QCheckBox, 'checkBox_eu')
        self.checkbox_all_eu.stateChanged.connect(self.all_set_eu_changed)

        # All Checked APAC
        self.checkbox_all_apac = self.findChild(QCheckBox, 'checkBox_apac')
        self.checkbox_all_apac.stateChanged.connect(self.all_set_apac_changed)

        self.label_output = self.findChild(QLabel, "label_output")

    def start_button_pressed(self):
        """
        Process Start Button Event.
        :return:
        """
        self.start = time.time()
        self.update_checkbox_list()
        self.generate_links()

        if self.links_to_crawl:
            self.label_output.setText("Processing ...")
            threading.Thread(target=self.extractor.start, args=(self.links_to_crawl,)).start()
        else:
            print("Please select at least one country")
            self.label_output.setText("Please select at least one country")

    def all_set_changed(self, state):
        """
        Change the state of all selected countries
        :param state: the state to change to
        :return:
        """
        self.all_set_na_changed(state)
        self.all_set_eu_changed(state)
        self.all_set_apac_changed(state)

    def all_set_na_changed(self, state):
        """
        CHange the state of all NA countries.
        :param state: the state to change to.
        :return:
        """
        na_checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_na_.*'))
        na_checkboxes.append(self.checkbox_all_na)
        for checkbox in na_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def all_set_eu_changed(self, state):
        """
        Change the state of all EU countries
        :param state: the state to change to
        :return:
        """
        eu_checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_eu_.*'))
        eu_checkboxes.append(self.checkbox_all_eu)
        for checkbox in eu_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def all_set_apac_changed(self, state):
        """
        Change the state of all APAC countries
        :param state: the state to change to
        :return:
        """
        apac_checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_apac_.*'))
        apac_checkboxes.append(self.checkbox_all_apac)
        for checkbox in apac_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def update_checkbox_list(self):
        """
        Update the checkbox list
        :return:
        """
        checkboxes = self.findChildren(QCheckBox, QRegularExpression('checkBox_.*_.*'))
        for checkbox in checkboxes:
            self.selected_countries[checkbox.objectName().split('_')[2]] = checkbox.isChecked()

    def generate_links(self):
        """
        Generate the links for the selected countries
        :return:
        """
        self.links_to_crawl = {}
        for code in self.all_country_codes:
            links_to_crawl_temp = []
            if self.selected_countries[code]:
                links_to_crawl_temp.append(self.all_links[code])
                links_to_crawl_temp.append(self.all_links[code].replace("models", "modelx"))
                links_to_crawl_temp.append(self.all_links[code].replace("models", "model3"))
                links_to_crawl_temp.append(self.all_links[code].replace("models", "modely"))
                self.links_to_crawl[code] = links_to_crawl_temp

    def check_if_changed(self):
        """
        Check if changes have happened to the previous day.
        :return:
        """
        today = date.today().strftime("%d_%m_%y")
        models = ["models", "modelx", "model3", "modely"]

        output_text = ""
        for key in self.links_to_crawl:
            prefix = "differences/" + key + "/"
            for model in models:
                filename = prefix + "diff_" + model + "_" + today + ".diff"
                if not os.path.exists(filename):
                    continue

                filesize = os.path.getsize(filename)

                if filesize > 1750:
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
