from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(_name_)
app.secret_key = "expediente_hglp_key"

# --------------------------
# Base de datos
# --------------------------
DB_NAME = "expediente_hglp.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                    )''')
        c.execute('''CREATE TABLE pacientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        edad INTEGER,
                        sexo TEXT,
                        diagnostico TEXT,
                        cie11 TEXT,
                        notas TEXT
                    )''')
        # Usuario administrador inicial
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ("admin", generate_password_hash("admin123"), "admin"))
        conn.commit()
        conn.close()

init_db()

# --------------------------
# Rutas principales
# --------------------------
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        session["user"] = user[1]
        session["role"] = user[3]
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="Usuario o contraseña incorrectos")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM pacientes")
    pacientes = c.fetchall()
    conn.close()
    return render_template("dashboard.html", pacientes=pacientes, user=session["user"])

@app.route("/nuevo_paciente", methods=["POST"])
def nuevo_paciente():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    sexo = request.form["sexo"]
    diagnostico = request.form["diagnostico"]
    cie11 = request.form["cie11"]
    notas = request.form["notas"]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO pacientes (nombre, edad, sexo, diagnostico, cie11, notas) VALUES (?, ?, ?, ?, ?, ?)",
              (nombre, edad, sexo, diagnostico, cie11, notas))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

if _name_ == "_main_":
    app.run(debug=True)
