from colorama import Fore
from bin import config
import time, os, configparser, sys, sqlite3, importlib.util

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def start():
    clear()

    if config.LIBS_FOLDER not in sys.path:
        sys.path.append(config.LIBS_FOLDER)
    
    sql, cursor = config.init_database()
    cursor.execute("SELECT * FROM libs")
    libs = cursor.fetchall()
    commands_result = {}

    for lib in libs:
        lib_name = lib[1]
        lib_path = os.path.join(config.LIBS_FOLDER, f"{lib_name}.py")
        try:
            if not os.path.exists(lib_path):
                print(f"Файл {lib_path} для модуля {lib_name} не найден.")
                continue
            
            spec = importlib.util.spec_from_file_location(lib_name, lib_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "commands") and callable(module.commands):
                commands_result[lib_name] = module.commands()
            else:
                print(f"Модуль {lib_name} не содержит функцию 'commands'.")
        except Exception as e:
            print(f"Ошибка при обработке модуля {lib_name}: {e}")
    
    for lib_name, commands in commands_result.items():
        print(f"Команды из {lib_name}: {commands}")

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