import sqlite3

LOGO = '''
███████╗███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗
██╔════╝██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗
███████╗█████╗  ██║     ██║   ██║██╔██╗ ██║██║  ██║ 
╚════██║██╔══╝  ██║     ██║   ██║██║╚██╗██║██║  ██║
███████║███████╗╚██████╗╚██████╔╝██║ ╚████║██████╔╝
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝'''
CHECK_PIP_LIBS = True
DB_FILE = 'data.db'
LIBS_FOLDER = 'libs'

def init_database():
    sql = sqlite3.connect(DB_FILE)
    cursor = sql.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS libs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    version TEXT
    )""")
    sql.commit()

    return sql, cursor