from colorama import Fore
from bin.core import restart
from datetime import datetime
import time

def commands():
    return {
        'datetime': get_datetime,
        'timestamp': timestamp
    }

def get_datetime():
    print(Fore.GREEN + datetime.now().strftime("%Y.%m.%d %H:%M:%S") + Fore.RESET)
    input(Fore.YELLOW + 'OK>>> ' + Fore.RESET)
    return restart()

def timestamp():
    print(f'{Fore.GREEN} {time.time()} {Fore.RESET}')
    input(Fore.YELLOW + 'OK>>> ' + Fore.RESET)
    return restart()