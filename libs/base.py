from colorama import Fore
from bin.core import start
import time

def commands():
    return { 
        'clearcache': clearcache
    }

def clearcache():
    print(Fore.GREEN + 'Cache cleared!' + Fore.RESET)
    time.sleep(1)
    return start()