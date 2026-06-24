import sqlite3

def get_db():
    conn = sqlite3.connect('instance/shop.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 顧客表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tax_id TEXT UNIQUE,
            name TEXT NOT NULL,
            address TEXT,
            phone1 TEXT,
            phone2 TEXT,
            contact_person TEXT
        )
    ''')
    
    # 產品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # 訂單主檔
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            delivery_date TEXT,
            delivery_place TEXT,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # 訂單明細
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("資料庫建立完成！")

if __name__ == '__main__':
    init_db()