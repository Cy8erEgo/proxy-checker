import requests
from requests.exceptions import RequestException
from multiprocessing import Process, Manager
import os
import re
import argparse
from typing import Optional


TIMEOUT = 3


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download proxies instead of taking them from a file",
    )
    parser.add_argument(
        "-c", "--country", default="all", help="Which country should proxies belong to"
    )
    c_args = parser.parse_args()
    return c_args


def check_proxy(proxy: str, list_) -> None:
    print(f"[{os.getpid()}] {proxy}")
    proxy_url = f"http://{proxy}"
    try:
        r = requests.get(
            "http://ip-api.com/json/",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=TIMEOUT,
        )
        list_.append({"proxy": proxy, "country_code": r.json()["countryCode"]})
    except (RequestException, Exception):
        pass


# parse command line arguments
args = parse_args()

print("=" * 10, "CHECKING", "=" * 10)

if args.download:
    print("Download proxies...")
    from parser import parse_proxies

    proxies = parse_proxies(country=args.country)
else:
    # read proxies
    with open("to_check.txt") as f:
        text = f.read()
    proxies = set(re.findall(r"(?:\d{1,3}\.){3}\d{1,3}(?:\:|\s+)\d+", text))
    proxies = [re.sub("\s+", ":", p, count=1) for p in proxies]

print(f"Got {len(proxies)} proxies")

# check the proxies
with Manager() as manager:
    good = manager.list()
    processes = []

    for proxy in proxies:
        p = Process(target=check_proxy, args=(proxy, good))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    good = list(good)

# filter by country
filtered_proxies = []

if args.country == "all":
    filtered_proxies = good
else:
    for proxy in good:
        if proxy["country_code"].lower() in args.country.lower().split(","):
            filtered_proxies.append(proxy)

# write the proxies
with open("proxies.txt", "w") as f:
    f.writelines([f"{proxy['proxy']} [{proxy['country_code']}]\n" for proxy in filtered_proxies])

# output the proxies
print("=" * 10, "PROFIT!", "=" * 10)
for i in filtered_proxies:
    print(i["proxy"], i["country_code"], sep="\t") 
