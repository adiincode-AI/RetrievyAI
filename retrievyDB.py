import sqlite3


def connect_db():
    return sqlite3.connect("retrievy.db")


def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    item_type TEXT,
                    category TEXT,
                    location TEXT NOT NULL,
                    date TEXT,
                    contact_info TEXT,
                    description TEXT,
                    image_path TEXT
                   )
                """)
    connection.commit()
    connection.close()


def add_item(item_name, item_type, location, date, category, contact_info, description, image_path):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items(item_name,item_type,location,date,category,contact_info,description,image_path) VALUES (?,?,?,?,?,?,?,?)",
                   (item_name, item_type, location, date, category, contact_info, description, image_path))
    connection.commit()
    connection.close()


def get_all_items():
    connection = connect_db()
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    cursor.execute("SELECT *FROM items")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_items_by_type(item_type):
    connection = connect_db()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE item_type= ?", (item_type,))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows] 

def get_items_by_category(category):
    connection = connect_db()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE category= ?", (category,))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows] 




