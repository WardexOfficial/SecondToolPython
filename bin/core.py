from colorama import Fore
from bin import config
import time, os, configparser, sys

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def start():
    clear()
    print(Fore.YELLOW + config.LOGO)
    print('SecondTool presents' + Fore.RESET)
    try: 
        a = int(input(Fore.CYAN + f'''
1.DDOS
2.SEARCH
3.HELP
9.RESTART {Fore.YELLOW}[DEV]{Fore.CYAN}
0.QUIT
>>> ''' + Fore.YELLOW))
    except ValueError:
        print(Fore.RED + 'FATAL ERROR' + Fore.RESET)
        time.sleep(3)
        clear()
        start()
    
    if a == 0:
        exit(1)
    elif a == 9:
        python_exec = sys.executable
        os.execl(python_exec, python_exec, *sys.argv)
    
    if a == 1:
        ...
    elif a == 2:
        ...
    elif a == 3:
        print(Fore.CYAN + '''
Help? You need help? Are you crazy?
        ''' + Fore.RESET)
    
    exit(1)