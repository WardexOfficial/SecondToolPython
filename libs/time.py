from colorama import Fore
from bin.core import start
import time, datetime

def commands():
    return {
        'year': get_year
    }

def get_year():
    print(Fore.GREEN + '2024' + Fore.RESET)
    time.sleep(1)
    return start()