import mysql.connector
import json

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='kaizen_test'
    )

def save_to_database(json_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (data) VALUES (%s)
    ''', (json.dumps(json_data),))
    conn.commit()
    conn.close()

def get_report_from_database(report_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT data FROM reports WHERE id = %s
    ''', (report_id,))
    data = cursor.fetchone()
    conn.close()
    return json.loads(data['data']) if data else None
