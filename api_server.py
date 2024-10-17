from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

def get_db_connection():
    return mysql.connector.connect(
        host="mysql-9b7d77c-iisgalvanimi-49c1.h.aivencloud.com",
        user="onlyReader",
        password="AVNS_-OFu2d9See3eDRGFs_s",
        database="W3Schools",
        port=16723
    )

@app.route('/api/data', methods=['GET'])
def get_data():
    table_name = request.args.get('table')
    if not table_name:
        return jsonify({"error": "Missing table parameter"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Restituisce righe come dizionari

    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(rows), 200, {'Content-Type': 'application/json'}

@app.route('/api/tables', methods=['GET'])
def get_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    
    return jsonify(tables)

@app.route('/api/execute', methods=['POST'])
def execute_query():
    query = request.json.get('query', '')  # Prendi la query dal corpo della richiesta
    if not query:  # Se la query è vuota
        return jsonify({"error": "La query SQL non può essere vuota"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute(query)
        if cursor.description:  # Se è una SELECT o query che restituisce dati
            results = cursor.fetchall()
        else:  # Per operazioni che non restituiscono dati (INSERT, UPDATE, DELETE)
            connection.commit()
            results = {'status': 'Query eseguita con successo'}
    except mysql.connector.Error as err:
        results = {'error': str(err)}
    finally:
        cursor.close()
        connection.close()
    
    return jsonify(results)  # Assicurati che venga sempre restituito un oggetto JSON

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Products WHERE ProductID = %s"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()  # Preleva una singola riga corrispondente all'ID
    cursor.close()
    conn.close()

    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Prodotto non trovato"}), 404

@app.route('/api/customer/<int:customer_id>/purchases', methods=['GET'])
def get_user_purchases(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Supponiamo che le tabelle Orders e OrderDetails siano strutturate con relazioni a Users e Products
    query = """
        SELECT Products.ProductID, Products.ProductName, Products.Price
        FROM Orders
        JOIN Order_details ON Orders.OrderID = Order_details.OrderID
        JOIN Products ON Order_details.ProductID = Products.ProductID
        WHERE Orders.CustomerID = %s
    """
    cursor.execute(query, (customer_id,))
    purchases = cursor.fetchall()
    cursor.close()
    conn.close()

    if purchases:
        return jsonify(purchases), 200
    else:
        return jsonify({"error": "Nessun acquisto trovato per l'utente"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
