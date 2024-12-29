from colorama import Fore
from bin.core import restart
from datetime import datetime
import time

def commands():
    return {
        'datetime': get_datetime
    }

def get_datetime():
    print(Fore.GREEN + datetime.now().strftime("%Y.%m.%d %H:%M:%S") + Fore.RESET)
    time.sleep(1)
    return restart()