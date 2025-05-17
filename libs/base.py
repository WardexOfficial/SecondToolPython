from colorama import Fore
from bin.core import restart
import time, shutil, os, configparser, subprocess, sys

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
        'core --version': core_version,
        'clearcache': clearcache
    }

def core_version():
    cnf = configparser.ConfigParser()
    cnf.read('config.ini')
    version = cnf["core"]["version"]
    package = cnf["core"]["package"]
    print(Fore.CYAN + f'Core version: {version} ({package})' + Fore.RESET)
    input(Fore.YELLOW + 'OK>>> ' + Fore.RESET)
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
    input(Fore.YELLOW + 'OK>>> ' + Fore.RESET)
    return restart()