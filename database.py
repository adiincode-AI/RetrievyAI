import sqlite3
import uuid
import bcrypt


def connect_db():
    return sqlite3.connect("retrievy.db")


def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password BLOB NOT NULL
                   )
                """)
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
                    image_path TEXT,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                   )
                """)

    connection.commit()
    connection.close()


def add_item(item_name, item_type, location, date, category, contact_info, description, image_path,user_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items(item_name,item_type,location,date,category,contact_info,description,image_path,user_id) VALUES (?,?,?,?,?,?,?,?,?)",
                   (item_name, item_type, location, date, category, contact_info, description, image_path,user_id))
    connection.commit()
    connection.close()


def get_all_items():
    connection = connect_db()
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    cursor.execute("SELECT *FROM items")
    rows = cursor.fetchall()
    connection.close() 
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
 
def register_user(username, password):
    connection = connect_db()
    cursor = connection.cursor()

    hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?,?)",(username, hashed)
        )
        connection.commit()
        return True
    except:
        return False
    finally:
        connection.close()

def login_user(username, password):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = ?",(username,))
    user = cursor.fetchone()
    connection.close()

    if user:
        user_id, stored_hash = user

        if bcrypt.checkpw(password.encode(),stored_hash):
            return {"id": user_id, 
                    "username": username
            }
    
    return None

def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    






