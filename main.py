import subprocess, sys, os, time, configparser
from bin import config

def clear(): os.system('cls' if os.name == 'nt' else 'clear')
    
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

if config.CHECK_PIP_LIBS is True:
    install_dependencies()

from colorama import Fore, init
from git import Repo
init()
print(Fore.GREEN + 'Иницилизация ядра...' + Fore.RESET)
time.sleep(1)
clear()

cnf = configparser.ConfigParser()
cnf.read('config.ini')
check_update = cnf["into"]["check_update"].lower() == 'true'
use_git = cnf["into"]["use_git"].lower() == 'true'
is_started = cnf["into"]["is_started"].lower() == 'true'

if check_update is True:
    if is_started is False:
        cnf.set('into', 'is_started', 'true')
        cnf.set('into', 'check_update', 'false')
        with open('config.ini', 'w') as configfile:
            cnf.write(configfile)
    if use_git is True:
        try:
            repo_path = os.path.dirname(os.path.abspath(__file__))
            if not os.path.isdir(os.path.join(repo_path, '.git')):
                print(Fore.RED + f"Ошибка: директория {repo_path} не является репозиторием!" + Fore.RESET)
                exit(401)

            repo = Repo(repo_path)
            origin = repo.remote(name='origin')
            origin.fetch()

            current_branch = repo.active_branch.name
            remote_ref = f'origin/{current_branch}'

            local_commit = repo.commit(current_branch)
            remote_commit = repo.commit(remote_ref)

            #if repo.is_dirty(untracked_files=True):
            #    print(Fore.RED + "Есть несохранённые изменения. Пожалуйста, закоммитьте их или удалите." + Fore.RESET)
            #    exit()

            if local_commit != remote_commit:
                print("Выполняется обновление...")
                origin.pull()
                print("Обновление завершено. Скрипт перезапускается...")
                time.sleep(0.1)
                python_exec = sys.executable
                os.execl(python_exec, python_exec, *sys.argv)
            else:
                print(Fore.GREEN + "Новых обновлений не обнаружено" + Fore.RESET)
                time.sleep(1)
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")
    else:
        print(Fore.RED + 'Поддержка git отключена. Для обновления включите поддержку git либо отключите проверку обновлений. Для этого измените настройки в файле config.ini' + Fore.RESET)
        exit(401)
else:
    print(Fore.RED + 'Проверка обновлений отключена' + Fore.RESET)

from bin import core
core.start()
exit()