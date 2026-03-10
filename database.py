import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
purchases INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER,
data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(
invoice_id TEXT,
user_id INTEGER,
product_id INTEGER
)
""")

conn.commit()


def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users(id) VALUES(?)",(user_id,))
    conn.commit()


def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def add_product(name,price):
    cursor.execute(
    "INSERT INTO products(name,price) VALUES(?,?)",
    (name,price))
    conn.commit()


def add_item(product_id,data):
    cursor.execute(
    "INSERT INTO items(product_id,data) VALUES(?,?)",
    (product_id,data))
    conn.commit()


def get_item(product_id):

    cursor.execute(
    "SELECT * FROM items WHERE product_id=? LIMIT 1",
    (product_id,)
    )

    item = cursor.fetchone()

    if item:
        cursor.execute("DELETE FROM items WHERE id=?",(item[0],))
        conn.commit()

    return item