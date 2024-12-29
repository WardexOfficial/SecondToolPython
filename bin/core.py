from colorama import Fore
from bin import config
import time, os, configparser, sys, sqlite3, importlib.util

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def start():
    clear()
    print(Fore.YELLOW + config.LOGO)
    print('SecondTool presents' + Fore.RESET)
    try: 
        a = int(input(Fore.CYAN + f'''
1.DDOS
2.SEARCH
3.MODULE`s
4.HELP
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
        if config.LIBS_FOLDER not in sys.path:
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
                print(f"Модуль {module}: {', '.join(commands)}")
            command = input(Fore.CYAN + 'Enter command>>> ' + Fore.YELLOW).strip()
            if command == "exit":
                print(Fore.GREEN + "Выход из программы.")
                break
            if command in commands_registry:
                try:
                    commands_registry[command]()
                except Exception as e:
                    print(Fore.RED + f"Ошибка при выполнении команды {command}: {e}")
            else:
                print(Fore.RED + f"Команда '{command}' не найдена.")
    elif a == 4:
        print(Fore.CYAN + '''
Help? You need help? Are you crazy?
        ''' + Fore.RESET)
    
    exit(1)