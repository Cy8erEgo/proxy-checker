import requests
from requests.exceptions import ProxyError, ConnectTimeout
from pprint import pprint
from multiprocessing import Process, Manager
import os


TIMEOUT = 3 


def check_proxy(proxy: str, list_) -> None:
    print(f"[{os.getpid()}] {proxy}")
    proxy_url = f"http://{proxy}"
    try:
        requests.get("https://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=TIMEOUT)
        list_.append(proxy)
    except (ProxyError, ConnectTimeout):
        pass


print("=" * 10, "CHECKING", "=" * 10)

# read proxies
with open("to_check.txt") as f:
    proxies = [line.strip() for line in f.readlines()]

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

# write the proxies
with open("proxies.txt", "w") as f:
    f.writelines([f"{proxy}\n" for proxy in good])

# output the proxies
print("=" * 10, "PROFIT!", "=" * 10)
print("\n".join(good))
