import os
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup as bs4

from beautifier import beautify_js
from compare import generate_diff_custom
from prettifier import prettify_string

"""
# Setting up the workspace by creating the necessary folders
"""


def setup():
    current_files = os.listdir()
    if not "previous_saves" in current_files:
        os.mkdir("previous_saves")
        print("Created dir \"previous_saves/\"")

    if not "differences" in current_files:
        os.mkdir("differences")
        print("Created dir \"differences/\"")

    print("[INFO] Directory is setup. Everything is good to go")


"""
# Get the source code from the specified website.
@param url: url The url to be crawled
@return soup: returns the soup object of the crawled website
"""


def get_website(url):
    session = requests.Session()
    session.headers[
        "User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    html = session.get(url).content

    soup = bs4(html, "html.parser")

    return soup


"""
# Extract the javascript content of the given website/ soup object
@param soup: The previously extracted soup object
@return longest_text: The longest_text represents the relevant js_section
"""


def get_js_file(soup):
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


"""
# Beautify the relevant text and save it to as js file
@param relevant_text: The text to be beautified
@return car_model: Specifies the current model being processed. It´s one of the following:
    {Model S, Model 3, Model X, Model Y}
"""


def save_file(relevant_text, car_model):
    today = date.today().strftime("%d_%m_%y")

    output_file_name = "previous_saves/" + today + "_" + car_model + ".js"

    if output_file_name.strip("previous_saves/") in os.listdir("previous_saves"):
        print("[INFO]" + car_model + " already saved today")
        return
    else:
        beautify_js(relevant_text, output_file_name)


"""
# Create the diff file for the saved JS of today and yesterday
@param key: the model to be processed
"""


def create_diff_file(key, past_days=1):
    today = date.today().strftime("%d_%m_%y")
    yesterday = (date.today() - timedelta(past_days)).strftime("%d_%m_%y")

    today_date_filename = today + "_" + key + ".js"
    yesterday_date_filename = yesterday + "_" + key + ".js"

    file_list = os.listdir("previous_saves/")

    if not (today_date_filename in file_list):
        print("[ERROR] File for today " + today_date_filename + " does not exist")
        return

    if not (yesterday_date_filename in file_list):
        print("[ERROR] File for yesterday " + yesterday_date_filename + " does not exist")
        print("[INFO] Please try again tomorrow")
        return

    today_date_filename = "previous_saves/" + today_date_filename
    yesterday_date_filename = "previous_saves/" + yesterday_date_filename

    generate_diff_custom(today_date_filename, yesterday_date_filename)


def prettify_dir(car_model):
    today = date.today().strftime("%d_%m_%y")

    output_file_name = "previous_saves/" + today + "_" + car_model + ".js"
    line_list = []
    with open(output_file_name, "r") as file:

        lines = file.readlines()
        for line in lines:

            if "\"DSServices\"" in line:
                line_list.append(prettify_string(line))
                continue

            line_list.append(line)

    with open(output_file_name, "w") as file:
        file.writelines("".join(line_list))


def main():
    # Specify the websites to be crawled. Currently on Tesla Models are supported
    file_dict = {
        "model3": "https://www.tesla.com/de_de/model3/design#overview",
        "models": "https://www.tesla.com/de_de/models/design#overview",
        "modely": "https://www.tesla.com/de_de/modely/design#overview",
        "modelx": "https://www.tesla.com/de_de/modelx/design#overview"
    }

    # Run the setup. Folders are only created once
    setup()

    # Iterate over the different Tesla Models
    for key in file_dict:
        print("[INFO] Processing " + key)
        value = file_dict[key]

        url = value
        soup = get_website(url)

        # Extract the relevant javascript section
        relevant_text = get_js_file(soup)

        # In case the relevant section could not be extracted, abort
        if not relevant_text:
            print("[ERROR] Extracting the relevant text failed, aborting")
            return -1

        save_file(relevant_text, key)
        if (len(os.listdir("previous_saves/")) <= 4):
            print("[INFO] Extracting was successful, not enough files to create diff yet. \n Please come back tomorrow")
            return -1

        prettify_dir(key)
        print("[INFO] Relevant text for " + key + " extracted and saved, creating diff-file")

        create_diff_file(key, 1)

        print("[SUCCESS] Diff file for " + key + " successfully created. View it in the \"differences/\" folder")

    return 0


if __name__ == '__main__':
    main()
