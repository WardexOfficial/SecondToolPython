from colorama import Fore
import sys, os, time, configparser
from libs import base
from bin import config
import time, os

cnf = configparser.ConfigParser()
cnf.read('config.ini')

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def main():
    if config.CHECK_PIP_LIBS is True:
        base.install_dependencies()

    from colorama import Fore, init
    from git import Repo
    init()
    print(Fore.GREEN + 'Иницилизация ядра...' + Fore.RESET)
    time.sleep(1)
    clear()

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
        time.sleep(1)

    from bin import core
    core.start()
    exit()

def start():
    clear()
    print('...')
    time.sleep(0.1)
    clear()
    time.sleep(0.1)
    print('BIOS start...')
    time.sleep(0.5)
    clear()
    print('Консоль стартера BIOS')
    print(Fore.CYAN + 'enter help for help')
    print(Fore.YELLOW + 'Для запуска утилиты нажмите ENTER')

    skip_bios = cnf["into"]["skip_bios"].lower() == 'true'
    if skip_bios == True:
        return main()

    while True:
        command = input(Fore.CYAN + 'command>>> ' + Fore.YELLOW)

        if command == '':
            return main()

        if command == 'help':
            print(Fore.BLUE + '''
    checkupdate --enable : включить проверку обновлений
    checkupdate --disable : выключить проверку обновлений
    core --version : узнать версию / билд ядра
    exit : выйти из консоли, завершить работу BIOS
    clear : очистить консоль
            ''' + Fore.RESET)
        elif command == 'core --version':
            version = cnf["core"]["version"]
            package = cnf["core"]["package"]
            print(Fore.CYAN + f'Core version: {version} ({package})' + Fore.RESET)
        elif command == 'checkupdate --enable':
            cnf.set('into', 'check_update', 'true')
            with open('config.ini', 'w') as configfile:
                cnf.write(configfile)
            print(Fore.GREEN + 'Проверка обновлений включена!' + Fore.RESET)
        elif command == 'checkupdate --disable':
            cnf.set('into', 'check_update', 'false')
            with open('config.ini', 'w') as configfile:
                cnf.write(configfile)
            print(Fore.GREEN + 'Проверка обновлений отключена!' + Fore.RESET)
        elif command == 'exit':
            print(Fore.RESET + 'BIOS close...')
            break
        elif command == 'clear':
            clear()
        else:
            print(Fore.RED + 'command nof found\n' + Fore.RESET)
    exit(1)