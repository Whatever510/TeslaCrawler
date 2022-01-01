import threading
from datetime import date

import os
from PyQt5 import uic
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel

import sys
from definitions import get_country_codes_na, get_country_code_eu, links_eu, links_na

from extractor import start

class Ui(QMainWindow):

    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi("Ui/MainWindow.ui", self)

        self.all_contry_codes = get_country_codes_na() + get_country_code_eu()
        self.selected_countries = dict.fromkeys(self.all_contry_codes, False)

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
        self.checkbox_all_na = self.findChild(QCheckBox, 'checkBox_all_north_america')
        self.checkbox_all_na.stateChanged.connect(self.allSetNAChanged)

        # All Checked EU
        self.checkbox_all_eu = self.findChild(QCheckBox, 'checkBox_all_europe')
        self.checkbox_all_eu.stateChanged.connect(self.allSetEUChanged)

        # Country Checkboxes
        self.checkbox_us = self.findChild(QCheckBox, 'checkBox_usa')
        self.checkbox_ca = self.findChild(QCheckBox, 'checkBox_canada')
        self.checkbox_mx = self.findChild(QCheckBox, 'checkBox_mexico')
        self.checkbox_pr = self.findChild(QCheckBox, 'checkBox_puerto')
        self.checkbox_at = self.findChild(QCheckBox, 'checkBox_austria')
        self.checkbox_be = self.findChild(QCheckBox, 'checkBox_belgium')
        self.checkbox_hr = self.findChild(QCheckBox, 'checkBox_croatia')
        self.checkbox_cz = self.findChild(QCheckBox, 'checkBox_czech')
        self.checkbox_dk = self.findChild(QCheckBox, 'checkBox_denmark')
        self.checkbox_fi = self.findChild(QCheckBox, 'checkBox_finnland')
        self.checkbox_de = self.findChild(QCheckBox, 'checkBox_germany')
        self.checkbox_gr = self.findChild(QCheckBox, 'checkBox_greece')
        self.checkbox_hu = self.findChild(QCheckBox, 'checkBox_hungary')
        self.checkbox_is = self.findChild(QCheckBox, 'checkBox_iceland')
        self.checkbox_ie = self.findChild(QCheckBox, 'checkBox_ireland')
        self.checkbox_it = self.findChild(QCheckBox, 'checkBox_italy')
        self.checkbox_lu = self.findChild(QCheckBox, 'checkBox_luxembourg')
        self.checkbox_nl = self.findChild(QCheckBox, 'checkBox_netherlands')
        self.checkbox_no = self.findChild(QCheckBox, 'checkBox_norway')
        self.checkbox_pl = self.findChild(QCheckBox, 'checkBox_poland')
        self.checkbox_pt = self.findChild(QCheckBox, 'checkBox_portugal')
        self.checkbox_ro = self.findChild(QCheckBox, 'checkBox_romania')
        self.checkbox_sl = self.findChild(QCheckBox, 'checkBox_slovenija')
        self.checkbox_es = self.findChild(QCheckBox, 'checkBox_spain')
        self.checkbox_se = self.findChild(QCheckBox, 'checkBox_sweden')
        self.checkbox_ch = self.findChild(QCheckBox, 'checkBox_switzerland')
        self.checkbox_gb = self.findChild(QCheckBox, 'checkBox_united_kingdom')
        self.checkbox_fr = self.findChild(QCheckBox, 'checkBox_france')
        self.label_output = self.findChild(QLabel, "label_output")





    def startButtonPressed(self):

        counter = 0


        self.update_checkbox_list()
        self.genereate_links()

        if (self.links_to_crawl):

            self.label_output.setText("Processing, expect the UI to freeze ...")
            self.label_output.repaint()

            #Preparation for multithreading to keep the gui from freezing. Not yet working
            x = threading.Thread(target=start, args=(self.links_to_crawl,))

            x.start()
            x.join()

            self.check_if_changed()

        else:
            print("Please select at least one country")
            self.label_output.setText("Please select at least one country")

    def allSetChanged(self):
        if self.checkbox_all.isChecked():
            self.checkbox_all_na.setChecked(True)
            self.checkbox_all_eu.setChecked(True)
        else:
            self.checkbox_all_na.setChecked(False)
            self.checkbox_all_eu.setChecked(False)

    def allSetNAChanged(self):

        if self.checkbox_all_na.isChecked():

            self.checkbox_us.setChecked(True)
            self.checkbox_mx.setChecked(True)
            self.checkbox_ca.setChecked(True)
            self.checkbox_pr.setChecked(True)

        else:
            self.checkbox_us.setChecked(False)
            self.checkbox_us.setChecked(False)
            self.checkbox_mx.setChecked(False)
            self.checkbox_ca.setChecked(False)
            self.checkbox_pr.setChecked(False)


    def allSetEUChanged(self):

        if self.checkbox_all_eu.isChecked():
            self.checkbox_at.setChecked(True)
            self.checkbox_be.setChecked(True)
            self.checkbox_hr.setChecked(True)
            self.checkbox_cz.setChecked(True)
            self.checkbox_dk.setChecked(True)
            self.checkbox_fi.setChecked(True)
            self.checkbox_de.setChecked(True)
            self.checkbox_gr.setChecked(True)
            self.checkbox_hu.setChecked(True)
            self.checkbox_is.setChecked(True)
            self.checkbox_ie.setChecked(True)
            self.checkbox_it.setChecked(True)
            self.checkbox_lu.setChecked(True)
            self.checkbox_nl.setChecked(True)
            self.checkbox_no.setChecked(True)
            self.checkbox_pl.setChecked(True)
            self.checkbox_pt.setChecked(True)
            self.checkbox_ro.setChecked(True)
            self.checkbox_sl.setChecked(True)
            self.checkbox_es.setChecked(True)
            self.checkbox_se.setChecked(True)
            self.checkbox_ch.setChecked(True)
            self.checkbox_gb.setChecked(True)
            self.checkbox_fr.setChecked(True)
        else:
            self.checkbox_at.setChecked(False)
            self.checkbox_be.setChecked(False)
            self.checkbox_hr.setChecked(False)
            self.checkbox_cz.setChecked(False)
            self.checkbox_dk.setChecked(False)
            self.checkbox_fi.setChecked(False)
            self.checkbox_de.setChecked(False)
            self.checkbox_gr.setChecked(False)
            self.checkbox_hu.setChecked(False)
            self.checkbox_is.setChecked(False)
            self.checkbox_ie.setChecked(False)
            self.checkbox_it.setChecked(False)
            self.checkbox_lu.setChecked(False)
            self.checkbox_nl.setChecked(False)
            self.checkbox_no.setChecked(False)
            self.checkbox_pl.setChecked(False)
            self.checkbox_pt.setChecked(False)
            self.checkbox_ro.setChecked(False)
            self.checkbox_sl.setChecked(False)
            self.checkbox_es.setChecked(False)
            self.checkbox_se.setChecked(False)
            self.checkbox_ch.setChecked(False)
            self.checkbox_gb.setChecked(False)
            self.checkbox_fr.setChecked(False)

    def update_checkbox_list(self):
        self.selected_countries["US"] = self.checkbox_us.isChecked()
        self.selected_countries["CA"] = self.checkbox_ca.isChecked()
        self.selected_countries["MX"] = self.checkbox_mx.isChecked()
        self.selected_countries["PR"] = self.checkbox_pr.isChecked()
        self.selected_countries["BE"] = self.checkbox_be.isChecked()
        self.selected_countries["CZ"] = self.checkbox_cz.isChecked()
        self.selected_countries["DK"] = self.checkbox_dk.isChecked()
        self.selected_countries["GR"] = self.checkbox_gr.isChecked()
        self.selected_countries["ES"] = self.checkbox_es.isChecked()
        self.selected_countries["FR"] = self.checkbox_fr.isChecked()
        self.selected_countries["HR"] = self.checkbox_hr.isChecked()
        self.selected_countries["IE"] = self.checkbox_ie.isChecked()
        self.selected_countries["IS"] = self.checkbox_is.isChecked()
        self.selected_countries["IT"] = self.checkbox_it.isChecked()
        self.selected_countries["LU"] = self.checkbox_lu.isChecked()
        self.selected_countries["HU"] = self.checkbox_hu.isChecked()
        self.selected_countries["NL"] = self.checkbox_nl.isChecked()
        self.selected_countries["NO"] = self.checkbox_no.isChecked()
        self.selected_countries["AT"] = self.checkbox_at.isChecked()
        self.selected_countries["PL"] = self.checkbox_pl.isChecked()
        self.selected_countries["PT"] = self.checkbox_pt.isChecked()
        self.selected_countries["RO"] = self.checkbox_ro.isChecked()
        self.selected_countries["SL"] = self.checkbox_sl.isChecked()
        self.selected_countries["CH"] = self.checkbox_ch.isChecked()
        self.selected_countries["SE"] = self.checkbox_se.isChecked()
        self.selected_countries["FI"] = self.checkbox_fi.isChecked()
        self.selected_countries["GB"] = self.checkbox_gb.isChecked()
        self.selected_countries["DE"] = self.checkbox_de.isChecked()

    def genereate_links(self):

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
                filesize = os.path.getsize(filename)

                if filesize > 1250:
                    output_text += "Possible change in " + key + " " + model + "\n"

                self.label_output.setText(output_text)



app = QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
