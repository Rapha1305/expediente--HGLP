from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DB_PATH = "database/expediente.db"

# ===============================
# CREAR BASE DE DATOS SI NO EXISTE
# ===============================

def init_db():
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla pacientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad TEXT,
        sexo TEXT,
        fecha_registro TEXT
    )
    """)

    # Nota de ingreso
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas_ingreso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        motivo TEXT,
        padecimiento TEXT,
        diagnostico TEXT,
        plan TEXT,
        fecha TEXT
    )
    """)

    # Evoluciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evoluciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        subjetivo TEXT,
        objetivo TEXT,
        analisis TEXT,
        plan TEXT,
        fecha TEXT
    )
    """)

    # Indicaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indicaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        dieta TEXT,
        soluciones TEXT,
        medicamentos TEXT,
        cuidados TEXT,
        fecha TEXT
    )
    """)

    # Laboratorios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laboratorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        estudios TEXT,
        diagnostico TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ===============================
# RUTAS PRINCIPALES
# ===============================

@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", pacientes=pacientes)

# ===============================
# NUEVO PACIENTE
# ===============================

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nombre, edad, sexo, fecha_registro)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["nombre"],
            request.form["edad"],
            request.form["sexo"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    return render_template("nuevo_paciente.html")

# ===============================
# DETALLE PACIENTE
# ===============================

@app.route("/paciente/<int:paciente_id>")
def paciente_detalle(paciente_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,))
    paciente = cursor.fetchone()

    cursor.execute("SELECT * FROM notas_ingreso WHERE paciente_id=?", (paciente_id,))
    ingresos = cursor.fetchall()

    cursor.execute("SELECT * FROM evoluciones WHERE paciente_id=?", (paciente_id,))
    evoluciones = cursor.fetchall()

    cursor.execute("SELECT * FROM indicaciones WHERE paciente_id=?", (paciente_id,))
    indicaciones = cursor.fetchall()

    cursor.execute("SELECT * FROM laboratorios WHERE paciente_id=?", (paciente_id,))
    labs = cursor.fetchall()

    conn.close()

    return render_template(
        "paciente_detalle.html",
        paciente=paciente,
        ingresos=ingresos,
        evoluciones=evoluciones,
        indicaciones=indicaciones,
        labs=labs
    )

# ===============================
# NOTA DE INGRESO
# ===============================

@app.route("/nota_ingreso/<int:paciente_id>", methods=["GET", "POST"])
def nota_ingreso(paciente_id):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notas_ingreso
            (paciente_id, motivo, padecimiento, diagnostico, plan, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            request.form["motivo"],
            request.form["padecimiento"],
            request.form["diagnostico"],
            request.form["plan"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("paciente_detalle", paciente_id=paciente_id))

    return render_template("nota_ingreso.html", paciente_id=paciente_id)

# ===============================
# NOTA DE EVOLUCION
# ===============================

@app.route("/nota_evolucion/<int:paciente_id>", methods=["GET", "POST"])
def nota_evolucion(paciente_id):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO evoluciones
            (paciente_id, subjetivo, objetivo, analisis, plan, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            request.form["subjetivo"],
            request.form["objetivo"],
            request.form["analisis"],
            request.form["plan"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("paciente_detalle", paciente_id=paciente_id))

    return render_template("nota_evolucion.html", paciente_id=paciente_id)

# ===============================
# INDICACIONES MEDICAS
# ===============================

@app.route("/indicaciones/<int:paciente_id>", methods=["GET", "POST"])
def indicaciones(paciente_id):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO indicaciones
            (paciente_id, dieta, soluciones, medicamentos, cuidados, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            request.form["dieta"],
            request.form["soluciones"],
            request.form["medicamentos"],
            request.form["cuidados"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("paciente_detalle", paciente_id=paciente_id))

    return render_template("indicaciones_medicas.html", paciente_id=paciente_id)

# ===============================
# LABORATORIOS
# ===============================

@app.route("/laboratorios/<int:paciente_id>", methods=["GET", "POST"])
def laboratorios(paciente_id):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO laboratorios
            (paciente_id, estudios, diagnostico, fecha)
            VALUES (?, ?, ?, ?)
        """, (
            paciente_id,
            request.form["estudios"],
            request.form["diagnostico"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("paciente_detalle", paciente_id=paciente_id))

    return render_template("laboratorios.html", paciente_id=paciente_id)

# ===============================

if __name__ == "__main__":
    app.run(debug=True)
