import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Borramos la tabla vieja si existe para limpiar la estructura
    cursor.execute('DROP TABLE IF EXISTS users')
    
    # Creamos la tabla con los campos exactos que pediste (+ password)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos recreada con la nueva estructura (id, username, email, password, fecha).")

if __name__ == '__main__':
    init_db()