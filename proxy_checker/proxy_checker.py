import requests
from requests.exceptions import ProxyError, ConnectTimeout
from pprint import pprint


TIMEOUT = 3 


with open("to_check.txt") as f:
    proxies = [line.strip() for line in f.readlines()]

good = []

for i, proxy in enumerate(proxies, 1):
    print(f"{i}/{len(proxies)}")

    try:
        proxy_url = f"http://{proxy}"
        requests.get("https://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=TIMEOUT)
        good.append(proxy)
    except (ProxyError, ConnectTimeout):
        pass

with open("proxies.txt", "w") as f:
    f.writelines([f"{proxy}\n" for proxy in good])

print("Profit!")
