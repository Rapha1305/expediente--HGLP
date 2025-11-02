from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "HGLP_SECRET_KEY"

# ---------------------- DB ---------------------- #
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Usuarios
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                 )""")
    # Pacientes
    c.execute("""CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    fecha_nacimiento TEXT,
                    expediente TEXT,
                    sexo TEXT
                 )""")
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------- Decorador login ---------------------- #
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ---------------------- Rutas ---------------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/nuevo_paciente", methods=["GET", "POST"])
@login_required
def nuevo_paciente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        expediente = request.form["expediente"]
        sexo = request.form["sexo"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO paci
