from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ¡AQUÍ ESTÁ LA VULNERABILIDAD! (Inyección SQL)
        # Estamos concatenando el texto directamente en la consulta.
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                return f"<h1>Bienvenido al Sistema de Incidentes</h1><p>Usuario: {user['username']}</p><p>Rol asignado: <strong>{user['role']}</strong></p>"
            else:
                error = "Credenciales incorrectas."
        except sqlite3.Error as e:
            # Mostramos el error SQL en pantalla (mala práctica de seguridad, excelente para hacking)
            error = f"Error de sintaxis SQL: {e}"
            
        conn.close()
            
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)