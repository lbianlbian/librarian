import requests 
import urllib.parse
import json
from bs4 import BeautifulSoup

URL = "https://www.worldanvil.com/w/world-of-fun-swifttail/t/history-of-the-world-of-fun-timeline"
OUTFILE = "timeline.json"
output = []  # each is a dict of title and text

targetUrl = urllib.parse.quote(URL)
url = f"http://api.scrape.do/?url={targetUrl}&token=xxxxxx"

response = requests.request("get", url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

timeline_entries = soup.find_all("li", class_="timeline-entry")
for timeline_entry in timeline_entries:
    title = timeline_entry.find("h5").get_text()
    text = timeline_entry.find("p").get_text()
    no_link_text = " ".join([word for word in text.strip().split(" ") if "https://" not in word])
    output.append(
        {
            "title": title.strip(),
            "text": no_link_text
        }
    )

with open(OUTFILE, "w") as output_file:
    output_file.write(json.dumps(output))
