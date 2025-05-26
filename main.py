import subprocess, sys

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

import bin.bios as bios
print('SecondTool present`s')
print('core objective')
bios.start()