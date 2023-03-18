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


#  Upload the menu item created by the admin to the database
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


# Fetch and show all menu items from database
async def client_menu_read(message):
    for ret in cur.execute("SELECT * FROM menu").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice {ret[-1]}")


async def admin_menu_read():
    return cur.execute("SELECT * FROM menu").fetchall()


async def sql_delete_command(data):
    cur.execute("DELETE FROM menu WHERE name == ?", (data,))
    base.commit()
