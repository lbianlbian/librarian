import requests 
import urllib.parse
import json
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
from time import sleep

ARTICLE_CLASS = 'toc-article-link   '
WORLD_ANVIL = "https://www.worldanvil.com"
OUTPUT_FOLDER = "articles"

class MyHTMLParser(HTMLParser):
    def add_collector(self):
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            is_article_link = False
            for attr_name, attr_val in attrs:
                if attr_name == "class" and attr_val == ARTICLE_CLASS:
                    is_article_link = True
                    break
            if not is_article_link:
                return
            
            for attr_name, attr_val in attrs:
                if attr_name == "href":
                    self.links.append(attr_val)

parser = MyHTMLParser()    
parser.add_collector()  
with open("article_links.json", "r") as linkfile:
    link_html = json.loads(linkfile.read())["contents"]
    parser.feed(link_html)

for link in parser.links:
    print(link)
    targetUrl = urllib.parse.quote(f"{WORLD_ANVIL}{link}")
    url = f"http://api.scrape.do/?url={targetUrl}&token=xxxxxxxxx"
    response = requests.request("get", url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find("div", class_="article-content-left")
    # .decode_contents() is the exact equivalent of JavaScript's .innerHTML
    inner_html = element.decode_contents()

    article_name = link.split("/")[-1]
    save_path = os.path.join(OUTPUT_FOLDER, f"{article_name}.txt")
    with open(save_path, "w") as outfile:
        outfile.write(inner_html)
    
    sleep(2)
