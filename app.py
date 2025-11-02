from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'expediente_clinico_seguro_2025'  # 🔒 Necesario para usar sesiones y mensajes flash

# -------------------------
# CREAR BASE DE DATOS SI NO EXISTE
# -------------------------
def init_db():
    if not os.path.exists('pacientes.db'):
        conn = sqlite3.connect('pacientes.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expediente TEXT UNIQUE,
                nombre TEXT,
                fecha_nacimiento TEXT,
                sexo TEXT,
                diagnostico TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Base de datos creada correctamente")
    else:
        print("📁 Base de datos ya existente")

# -------------------------
# RUTA DE LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Usuario y contraseña de prueba
        if usuario == 'admin' and contraseña == '1234':
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# -------------------------
# RUTA DE MENÚ PRINCIPAL
# -------------------------
@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

# -------------------------
# RUTA NUEVO PACIENTE
# -------------------------
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

        conn = sqlite3.connect('pacientes.db')
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO pacientes (expediente, nombre, fecha_nacimiento, sexo, diagnostico)
                VALUES (?, ?, ?, ?, ?)
            ''', (expediente, nombre, fecha_nacimiento, sexo, diagnostico))
            conn.commit()
            flash('Paciente agregado exitosamente.', 'success')
        except sqlite3.IntegrityError:
            flash('⚠️ El número de expediente ya existe.', 'danger')
        finally:
            conn.close()

        return redirect(url_for('nuevo_paciente'))

    return render_template('nuevo_paciente.html')

# -------------------------
# RUTA BUSCAR PACIENTE
# -------------------------
@app.route('/buscar_paciente', methods=['GET', 'POST'])
def buscar_paciente():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    resultados = []
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        conn = sqlite3.connect('pacientes.db')
        c = conn.cursor()
        c.execute("""
            SELECT expediente, nombre, fecha_nacimiento, sexo, diagnostico
            FROM pacientes
            WHERE nombre LIKE ? OR expediente LIKE ?
        """, (f'%{busqueda}%', f'%{busqueda}%'))
        resultados = c.fetchall()
        conn.close()

    return render_template('buscar_paciente.html', resultados=resultados)

# -------------------------
# CERRAR SESIÓN
# -------------------------
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))

# -------------------------
# EJECUTAR APP
# -------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
