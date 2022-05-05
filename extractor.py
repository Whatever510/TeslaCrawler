""" Main Extractor class """

import concurrent.futures
import logging
import os
from datetime import date, timedelta

import requests
from PyQt5.QtCore import QObject, pyqtSignal
from bs4 import BeautifulSoup as bs4

from beautifier import beautify_js
from compare import generate_diff_custom
from prettifier import prettify_string

DIFFERENCES_DIR = "differences"
PREVIOUS_SAVES_DIR = "previous_saves"

DEBUG = False


class Extractor(QObject):
    """ This class extracts the configurator content"""
    finished = pyqtSignal()


    def __init__(self):
        super().__init__()
        if DEBUG:
            logging.basicConfig(level=logging.INFO)
            logging.root.setLevel(logging.NOTSET)

    @staticmethod
    def setup(country_code):
        """
        Setup the necessary folders
        :param country_code: The country code, will be the name of the folder.
        """
        current_files = os.listdir()
        if PREVIOUS_SAVES_DIR not in current_files:
            os.mkdir(PREVIOUS_SAVES_DIR)

        if DIFFERENCES_DIR not in current_files:
            os.mkdir(DIFFERENCES_DIR)

        if country_code not in os.listdir(DIFFERENCES_DIR):
            os.mkdir(os.path.join(DIFFERENCES_DIR, country_code))

        if country_code not in os.listdir(PREVIOUS_SAVES_DIR):
            os.mkdir(os.path.join(PREVIOUS_SAVES_DIR, country_code))

    @staticmethod
    def get_website(url):
        """
        Get the source code from the specified website.
        :param url: url The url to be crawled
        :return: the soup object of the crawled website
        """
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
                                        " (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

        html = session.get(url).content
        soup = bs4(html, "html.parser")
        return soup

    @staticmethod
    def get_js_file(soup):
        """
        Extract the javascript content of the given website/ soup object
        :param soup: The previously extracted soup object
        :return: The longest_text represents the relevant js_section
        """
        scripts = soup.find_all("script")

        longest = 0
        longest_text = ""

        for script in scripts:
            text = script.extract()
            length = len(str(text))

            if length > longest:
                longest_text = str(text)
                longest = length

        return longest_text

    @staticmethod
    def save_file(relevant_text, car_model, country_code):
        """
        Beautify the relevant text and save it to as js file
        :param relevant_text: The text to be beautified
        :return: Specifies the current model being processed. It´s one of the following:
        {Model S, Model 3, Model X, Model Y}
        """
        today = date.today().strftime("%d_%m_%y")
        output_file_name = PREVIOUS_SAVES_DIR + "/" + country_code + "/" + \
                           today + "_" + car_model + ".js"
        beautify_js(relevant_text, output_file_name)

    @staticmethod
    def create_diff_file(key, country_code, past_days=1):
        """
        Create the diff file for the saved JS of today and yesterday
        :param key: the model to be processed
        :param country_code: the country code
        :param past_days: the day difference
        """
        today = date.today().strftime("%d_%m_%y")
        yesterday = (date.today() - timedelta(past_days)).strftime("%d_%m_%y")

        today_date_filename = today + "_" + key + ".js"
        yesterday_date_filename = yesterday + "_" + key + ".js"
        prefix = os.path.join(PREVIOUS_SAVES_DIR, country_code)
        file_list = os.listdir(prefix)

        if today_date_filename not in file_list:
            print("[ERROR] File for today " + today_date_filename + " does not exist")
            return

        if yesterday_date_filename not in file_list:
            print("[ERROR] File for yesterday " + yesterday_date_filename + " does not exist")
            print("[INFO] Please try again tomorrow")
            return

        today_date_filename = prefix + "/" + today_date_filename
        yesterday_date_filename = prefix + "/" + yesterday_date_filename

        generate_diff_custom(today_date_filename, yesterday_date_filename, country_code)

    @staticmethod
    def prettify_dir(car_model, country_code):
        """
        Prettify the directory
        :param car_model: the car model
        :param country_code: the country code
        """
        today = date.today().strftime("%d_%m_%y")

        output_file_name = PREVIOUS_SAVES_DIR + "/" + country_code + "/" +\
                           today + "_" + car_model + ".js"
        line_list = []
        with open(output_file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if "\"DSServices\"" in line:
                    line_list.append(prettify_string(line))
                    continue
                line_list.append(line)

        with open(output_file_name, "w", encoding="utf-8") as file:
            file.writelines("".join(line_list))

    def process_urls(self, country, url):
        """
        Process the given url = extract the information
        :param country: Country to be processed
        :param url: Model to be processed
        """
        model = url.split('/')[-2]
        logging.info("Processing: %s", model)
        soup = self.get_website(url)

        # Extract the relevant javascript section
        relevant_text = self.get_js_file(soup)

        # In case the relevant section could not be extracted, abort
        if not relevant_text:
            print("[ERROR] Extracting the relevant text for " + model + " in " + country + " failed, skipping")
            return -1

        self.save_file(relevant_text, model, country)

        self.prettify_dir(model, country)
        if not len(os.listdir(os.path.join(PREVIOUS_SAVES_DIR, country))) <= 4:
            self.create_diff_file(model, country, 1)
            return 0
        return -1

    def process_countries(self, input_file, country):
        """
        Process all countries
        :param input_file: the input_file dir
        :param country: the country to be processed
        """
        self.setup(country)
        logging.info("Processing: %s", country)
        args = ((country, url) for url in input_file[country])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as thread_pool:
            thread_pool.map(lambda p: self.process_urls(*p), args)

    def start(self, input_file):
        """
        "Main" Method. This Method gets called by the GUI
        :param input_file: a dir containing all countries to be processed
        """
        args_main = ((input_file, country_code) for country_code in input_file)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(input_file)) as main_executor:
            main_executor.map(lambda t: self.process_countries(*t), args_main)

        self.finished.emit()
