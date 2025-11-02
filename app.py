from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "expediente_hglp_key"

# --- Base de datos ---
def init_db():
    with sqlite3.connect("expedienteHGLP.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                    )""")
        con.commit()

init_db()

# --- Rutas ---
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    with sqlite3.connect("expedienteHGLP.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

    if user and check_password_hash(user[2], password):
        session["user"] = username
        return redirect(url_for("dashboard"))
    else:
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# --- Usuario inicial ---
def crear_usuario_inicial():
    with sqlite3.connect("expedienteHGLP.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username='admin'")
        if not cur.fetchone():
            hashed = generate_password_hash("admin123")
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ("admin", hashed, "Administrador"))
            con.commit()

crear_usuario_inicial()

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
