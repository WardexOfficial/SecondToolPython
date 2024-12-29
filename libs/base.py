from colorama import Fore
from bin.core import restart
import time, shutil, os

def commands():
    return { 
        'clearcache': clearcache,
        'ddos': ddos
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
    return restart()