import re

import requests
from bs4 import BeautifulSoup as bs


PROXIES_URL = "http://spys.one/"


def get_soup(url):
    return bs(requests.get(url).text, "html.parser")

def parse_proxies():
    soup = get_soup(PROXIES_URL)
    rows = soup.find_all("tr", class_="spy1xx")
    rows.extend(soup.find_all("tr", class_="spy1x"))

    pattern = re.compile("(?:\d{1,3}\.){3}\d{1,3}:\d+")
    proxies = []
    
    for row in rows:
        proxy = re.findall(pattern, row.find("td").text)
        if proxy:
            proxies.extend(proxy)

    return proxies


if __name__ == "__main__":
    proxies = parse_proxies()
    print(proxies)
