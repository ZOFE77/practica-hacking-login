from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_la_practica'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        try:
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                session['username'] = user['username']
                # AQUÍ ESTÁ LA MAGIA: te mandamos al HTML con Bootstrap
                return redirect(url_for('home')) 
            else:
                error = "Credenciales incorrectas."
        except sqlite3.Error as e:
            error = f"Error en la base de datos: {e}"
        finally:
            conn.close()
            
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']      # Capturamos el correo del formulario
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insertamos username, email y password. 
            # El ID y la registration_date se generan solos en SQLite.
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            error = f"Error al registrar: {e}"
        finally:
            conn.close()
            
    return render_template('register.html', error=error)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)