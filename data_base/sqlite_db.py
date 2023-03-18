import sqlite3 as sq

from create_bot import bot


# Create sqlite data base and menu table
def sql_start():
    global base, cur
    base = sq.connect("menu_db.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
    base.commit()
