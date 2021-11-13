import pandas as pd
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

def extract_urls(soup, url_list):
    scripts = list(soup.find_all("loc"))


    for i in range(len(scripts)):
        url_string = str(scripts[i]).replace("<loc>","").replace("</loc>","")

        url_list.append(url_string)


def pull_xml(url):

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    response = session.get(url).content

    soup = BeautifulSoup(response,
                "lxml-xml",
                )

    #soup = soup.prettify()
    #print(soup)
    return soup



def main():
    sitemaps = ["https://www.tesla.com/sitemap.xml?page=1", "https://www.tesla.com/sitemap.xml?page=2"]
    url_list = []
    for sitemap in sitemaps:

        soup = pull_xml(sitemap)
        extract_urls(soup, url_list)
        print(len(url_list))


if __name__ == '__main__':
    main()
