from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_segura_hglp'  # Necesario para manejar sesiones y mensajes flash


# === Funciones de Base de Datos ===
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

def crear_tabla_pacientes():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expediente TEXT NOT NULL,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT,
            sexo TEXT,
            diagnostico TEXT
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


# === Rutas ===
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
        session['usuario'] = usuario
        return redirect(url_for('menu'))
    else:
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for('login'))


@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')


@app.route('/nuevo_paciente', methods=['GET', 'POST'])
def nuevo_paciente():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        expediente = request.form['expediente']
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        sexo = request.form['sexo']
        diagnostico = request.form['diagnostico']

        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        c.execute("INSERT INTO pacientes (expediente, nombre, fecha_nacimiento, sexo, diagnostico) VALUES (?, ?, ?, ?, ?)",
                  (expediente, nombre, fecha_nacimiento, sexo, diagnostico))
        conn.commit()
        conn.close()

        flash("Paciente agregado correctamente")
        return redirect(url_for('menu'))

    return render_template('nuevo_paciente.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


# === Inicialización ===
if __name__ == "__main__":
    crear_tabla_usuarios()
    crear_tabla_pacientes()
    crear_usuario_inicial()
    app.run(host="0.0.0.0", port=10000)
