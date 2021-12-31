import pandas as pd
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

"""
Setup the workspace by creating the necessary folder
"""
def setup():
    content = os.listdir()

    if not ("xmlPages" in content):
        os.mkdir("xmlPages/")
    print("[INFO] Setup done - Directory successfully created")

"""
Extract the URLs from the soup element.
@param soup: The soup element.
@param url_list: The list which will contain the extracted -> used as return value.
@param update_list: The list of last updates - extracted but not used -> used as return value.
"""
def extract_urls(soup, url_list, update_list):
    scripts = list(soup.find_all("loc"))
    updates = list(soup.find_all("lastmod"))
    counter = 0
    for i in range(len(scripts)):
        url_string = str(scripts[i]).replace("<loc>","").replace("</loc>","")

        url_list.append(url_string)

    for i in range(len(updates)):
        update_string = str(updates[i]).replace("<lastmod>","").replace("</lastmod>","")
        if update_string == "":
            counter += 1
        update_list.append(update_string)

"""
#Not used. Not all urls provide a last updated field.
"""
def create_history_file(url_list, update_list):

    assert(len(url_list) == len(update_list))

    for i in range(len(url_list)):
        url = url_list[i]
        timestamp = update_list[i]
        print(url + "--" + timestamp)

"""
Pull the xml file of the Tesla website.
@param url: the url to the xml site.
@return soup: The extracted soup element.
"""
def pull_xml(url):

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    response = session.get(url).content

    soup = BeautifulSoup(response,
                "lxml-xml",
                )

    return soup

"""
Save a local copy of the urls
@param url_list: A list containing all of the extraced urls.
"""
def save_webpages(url_list):
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    total = len(url_list)
    skipped = 0
    not_skipped = 0

    for url in tqdm(url_list):

        splitted_url = url.lower().split("/")
        if ("ko_kr" in splitted_url or "es_mx" in splitted_url or "en_pr" in splitted_url or
        "es_pr" in splitted_url or "he_il" in splitted_url or "ar_ae" in splitted_url or
        "en_ae" in splitted_url or "en_jo" in splitted_url or "zh_hk" in splitted_url or
        "en_hk" in splitted_url or "zh_mo" in splitted_url or "en_mo" in splitted_url or
        "zh_tw" in splitted_url or "ja_jp" in splitted_url or "en_sg" in splitted_url or
        "ko_kr" in splitted_url or url.__contains__("supercharger") or "cn" in splitted_url or
        "services" in splitted_url or "stores" in splitted_url or "findus" in splitted_url or
        "superchargers" in splitted_url or "blog" in splitted_url or url.__contains__("dc") or
        url.__contains__("press")):
            skipped += 1
            continue

        not_skipped += 1


        response = session.get(url).content

        soup = BeautifulSoup(response, "html.parser")

        filename = url.replace("/","_").replace("www.", "").replace(".com","").replace("%","")[8:]
        filename = "xmlPages/"+filename+".html"
        with open(filename, "w", encoding="utf-8") as html_page:
            html_page.write(str(soup))

    print("Total: {}, Skipped: {}, Not skipped: {}".format(total, skipped, not_skipped))



def main():
    setup()
    sitemaps = ["https://www.tesla.com/sitemap.xml?page=1", "https://www.tesla.com/sitemap.xml?page=2"]
    url_list = []
    update_list = []
    for sitemap in sitemaps:

        soup = pull_xml(sitemap)
        extract_urls(soup, url_list, update_list)


    save_webpages(url_list)


if __name__ == '__main__':
    main()
