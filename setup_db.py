import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Insertar usuarios de prueba (Admin y Analyst)
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'SuperSecretPassword2026', 'Admin')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('analyst_1', 'analyst123', 'Analyst')")
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada con éxito.")

if __name__ == '__main__':
    init_db()