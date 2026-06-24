from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# ========== 顧客管理 ==========
@app.route('/customers')
def list_customers():
    db = get_db()
    customers = db.execute('SELECT * FROM customers').fetchall()
    db.close()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.form
    db = get_db()
    db.execute(
        'INSERT INTO customers (tax_id, name, address, phone1, phone2, contact_person) VALUES (?, ?, ?, ?, ?, ?)',
        (data['tax_id'], data['name'], data['address'], data['phone1'], data['phone2'], data['contact_person'])
    )
    db.commit()
    db.close()
    return redirect(url_for('list_customers'))

# ========== 產品管理 ==========
@app.route('/products')
def list_products():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    db.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.form
    db = get_db()
    db.execute(
        'INSERT INTO products (name, price) VALUES (?, ?)',
        (data['name'], float(data['price']))
    )
    db.commit()
    db.close()
    return redirect(url_for('list_products'))

# ========== 訂單管理（簡化版） ==========
@app.route('/orders')
def list_orders():
    db = get_db()
    orders = db.execute('''
        SELECT orders.*, customers.name as customer_name 
        FROM orders 
        JOIN customers ON orders.customer_id = customers.id
    ''').fetchall()
    db.close()
    return render_template('orders.html', orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.form
    db = get_db()
    
    # 新增訂單主檔
    cursor = db.execute(
        'INSERT INTO orders (customer_id, order_date, delivery_date, delivery_place, total_amount) VALUES (?, ?, ?, ?, ?)',
        (data['customer_id'], data['order_date'], data['delivery_date'], data['delivery_place'], float(data['total_amount']))
    )
    order_id = cursor.lastrowid
    
    # 新增訂單明細（這裡只示範一筆，可擴充）
    db.execute(
        'INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
        (order_id, data['product_id'], int(data['quantity']), float(data['price']))
    )
    
    db.commit()
    db.close()
    return redirect(url_for('list_orders'))

if __name__ == '__main__':
    init_db() # 第一次執行會建立資料庫
    app.run(debug=True)