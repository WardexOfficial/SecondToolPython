from colorama import Fore
from bin.core import restart
import time, shutil, os, configparser, subprocess

cnf = configparser.ConfigParser()
cnf.read('config.ini')

def install_dependencies():
    try:
        with open("requirements.txt") as f:
            dependencies = [line.strip() for line in f if line.strip()]
        installed = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode('utf-8')
        for dependency in dependencies:
            if dependency.split("==")[0].strip().lower() not in installed.lower():
                subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
                print(f"Зависимость '{dependency}' установлена.")
            else:
                print(f"Зависимость '{dependency}' уже установлена.")
    except FileNotFoundError:
        print("Файл requirements.txt не найден.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

def commands():
    return { 
        'enable --checkupdate': enable_check_update,
        'disable --checkupdate': disable_check_update,
        'clearcache': clearcache
    }

def enable_check_update():
    cnf.set('into', 'check_update', 'true')
    with open('config.ini', 'w') as configfile:
        cnf.write(configfile)
    print(Fore.GREEN + 'Проверка обновлений включена!' + Fore.RESET)
    time.sleep(2)
    return restart()

def disable_check_update():
    cnf.set('into', 'check_update', 'false')
    with open('config.ini', 'w') as configfile:
        cnf.write(configfile)
    print(Fore.GREEN + 'Проверка обновлений отключена!' + Fore.RESET)
    time.sleep(2)
    return restart()

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