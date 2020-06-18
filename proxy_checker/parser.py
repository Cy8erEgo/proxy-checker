import re
import base64

import requests
from bs4 import BeautifulSoup as bs
from user_agent import generate_user_agent


PROXIES_URL = "http://free-proxy.cz/ru/proxylist/country/all/https/ping/%s"
PAGES_COUNT = 10
HTTP_HEADERS = {"User-Agent": generate_user_agent()}
TIMEOUT = 10


def get_soup(url):
    return bs(requests.get(url, headers=HTTP_HEADERS, timeout=TIMEOUT).text, "html.parser")


def parse_proxies():
    pattern = re.compile("(?:\d{1,3}\.){3}\d{1,3}:\d+")
    proxies = []

    for page_num in range(1, PAGES_COUNT + 1):
        soup = get_soup(PROXIES_URL % page_num)
        rows = soup.find("table", id="proxy_list").findall("tr")
        
        for row in rows:
            script = row.find("script").text
            cipher = re.findall(r'Base64.decode\("(.+)"\)', script)[0]
            ip = base64.b64decode(cipher)
            proxy = ip

            if proxy and re.find(pattern, proxy):
                proxies.append(proxy)

    return proxies


if __name__ == "__main__":
    proxies = parse_proxies()
    print(proxies)
