from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

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
    
    # Prevenire l'SQL Injection controllando il nome della tabella
    valid_tables = ['Customers', 'Products', 'Orders', 'Categories']  # Aggiungi qui le tue tabelle valide
    if table_name not in valid_tables:
        return jsonify({"error": "Invalid table name"}), 400

    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(rows), 200, {'Content-Type': 'application/json'}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
