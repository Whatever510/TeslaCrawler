import requests
from bs4 import BeautifulSoup as bs4
from datetime import date, timedelta
import os
from prettifier import prettify_string

from beautifier import beautify_js
from compare import generate_diff_custom

differences_dir = "differences"
previous_dir = "previous_saves"

"""
# Setting up the workspace by creating the necessary folders
"""
def setup(country_code):
    current_files = os.listdir()
    if not previous_dir in current_files:
        os.mkdir(previous_dir)


    if not differences_dir in current_files:
        os.mkdir(differences_dir)

    if not country_code in os.listdir(differences_dir):
        os.mkdir(os.path.join(differences_dir, country_code))

    if not country_code in os.listdir(previous_dir):
        os.mkdir(os.path.join(previous_dir, country_code))


"""
# Get the source code from the specified website.
@param url: url The url to be crawled
@return soup: returns the soup object of the crawled website
"""
def get_website(url):

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

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
        if(length > longest):
            longest_text = str(text)
            longest = length

    return longest_text

"""
# Beautify the relevant text and save it to as js file
@param relevant_text: The text to be beautified
@return car_model: Specifies the current model being processed. It´s one of the following:
    {Model S, Model 3, Model X, Model Y}
"""
def save_file(relevant_text, car_model, country_code):
    today = date.today().strftime("%d_%m_%y")

    output_file_name = previous_dir + "/" + country_code + "/" + today + "_" + car_model+".js"

    beautify_js(relevant_text, output_file_name)


"""
# Create the diff file for the saved JS of today and yesterday
@param key: the model to be processed
"""
def create_diff_file(key, country_code, past_days = 1):

    today= date.today().strftime("%d_%m_%y")
    yesterday = (date.today() - timedelta(past_days)).strftime("%d_%m_%y")


    today_date_filename = today + "_" + key + ".js"
    yesterday_date_filename =  yesterday + "_" + key + ".js"
    prefix = os.path.join(previous_dir, country_code)
    file_list = os.listdir(prefix)

    if not (today_date_filename in file_list):
        print("[ERROR] File for today "+today_date_filename+" does not exist")
        return

    if not (yesterday_date_filename in file_list):
        print("[ERROR] File for yesterday "+yesterday_date_filename+" does not exist")
        print("[INFO] Please try again tomorrow")
        return

    today_date_filename = prefix + "/" +today_date_filename
    yesterday_date_filename = prefix + "/"+yesterday_date_filename

    generate_diff_custom(today_date_filename, yesterday_date_filename, country_code)



def prettify_dir(car_model, country_code):
    today = date.today().strftime("%d_%m_%y")

    output_file_name = previous_dir +"/" + country_code +"/" +today + "_" + car_model+".js"
    line_list = []
    with open(output_file_name, "r") as file:

        lines = file.readlines()
        for line in lines:
            #print(type(line))
            if "\"DSServices\"" in line:
                line_list.append(prettify_string(line))
                continue

                #print(line)
            line_list.append(line)


    with open(output_file_name, "w") as file:
        file.writelines("".join(line_list))


def start(input_file):
    #Specify the websites to be crawled. Currently on Tesla Models are supported

    for country in input_file:
        setup(country)
        for url in input_file[country]:
            print("Processing:", url)
            model = url.split('/')[-2]
            print("Processing:", model)
            soup = get_website(url)

            #Extract the relevant javascript section
            relevant_text = get_js_file(soup)

            #In case the relevant section could not be extracted, abort
            if not relevant_text:
                print("[ERROR] Extracting the relevant text failed, aborting")
                return -1

            save_file(relevant_text, model, country)

            prettify_dir(model, country)
            if (len(os.listdir(os.path.join(previous_dir, country))) <= 4):
                #print("[INFO] Extracting was successful, not enough files to create diff yet. \n Please come back tomorrow")
                continue
            else:


                create_diff_file(model, country, 1)




    return 0

