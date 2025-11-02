from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(_name_)

# --- Base de datos ---
def crear_tabla_usuarios():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def crear_usuario_inicial():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO usuarios (nombre, usuario, contrasena) VALUES (?, ?, ?)",
                  ('Administrador', 'admin', 'admin'))
    conn.commit()
    conn.close()

# --- Rutas ---
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def validar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('panel'))
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/panel')
def panel():
    return "<h1>Bienvenido al expediente clínico HGLP</h1>"

# --- Inicialización ---
if _name_ == "_main_":
    crear_tabla_usuarios()
    crear_usuario_inicial()
    app.run(host="0.0.0.0", port=10000)
