#Run this script only once - on first installation

import sqlite3

path_to_db = '/home/pipa/Desktop/backend/database.db'

conn = sqlite3.connect(path_to_db)

conn.execute('''CREATE TABLE IF NOT EXISTS users(
                userID TEXT PRIMARY KEY,
                name TEXT,
                surname TEXT,
                class TEXT);''')

conn.execute('''CREATE TABLE IF NOT EXISTS orders(
                orderid TEXT,
                order_name TEXT,
                order_surname TEXT,
                order_class TEXT,
                date TEXT,
                time TEXT);''')

conn.commit()
conn.close()
