# TeslaCrawler
Crawl the Tesla configurator website to spot changes in the source code.

##Pull the configurator code

Pull the source code for the 4 Tesla models from the configurator.  

Starting with the second pull the algorithm will create a diff-file to the source code of the previous day.
### Setup
Install the necessary requirements
```
pip install jsbeautifier
pip install diff-match-patch
pip install beautifulsoup4
pip install urllib3
```

### Using the code
1. Clone the Repo
2. Run:

```
python websitecrawl.py
```
Note: You need the pulls of at least two different days to generate a diff file.

## Pull the website of the sitemap

Tesla has a xml sitemap. The sitemap can be found at [Tesla Sitemap Overview](https://www.tesla.com/sitemap.xml).
To pull the websites listed in the sitemap run:

```
python xmlpull.py
```

Note: Certain Websites are skipped, like supercharger location and Websites from certain regions.
    Pulling takes approximately 60 minutes. The websites are saved in the "xmlPages" Folder. 
