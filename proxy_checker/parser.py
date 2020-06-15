import requests

from bs4 import BeautifulSoup as bs


PROXIES_URL = "http://spys.one/"


def get_soup(url):
    return bs(requests.get(url).text, "html.parser")

def parse_proxies():
    soup = get_soup(PROXIES_URL)
    rows = soup.find_all("tr", class_="spy1xx")
    rows.extend(soup.find_all("tr", class_="spy1x"))

    proxies = []
    
    for row in rows:
        proxies.append(row.find("td").text.strip())

    return proxies


if __name__ == "__main__":
    proxies = parse_proxies()
    print(proxies)
