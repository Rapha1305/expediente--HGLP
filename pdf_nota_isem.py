from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def generar_nota_isem(data, output_path):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER

    def encabezado():
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, height - 40, "GOBIERNO DEL ESTADO DE MÉXICO")
        c.drawCentredString(width / 2, height - 55, "SALUD - ISEM")
        c.setFont("Helvetica", 9)

    # -------- ANVERSO --------
    encabezado()

    c.drawString(40, height - 90, f"Unidad Médica: {data['unidad']}")
    c.drawString(40, height - 110, f"Nombre del Paciente: {data['paciente']}")
    c.drawString(350, height - 110, f"Edad: {data['edad']}  Sexo: {data['sexo']}")
    c.drawString(350, height - 90, f"No. Expediente: {data['expediente']}")

    # Signos vitales
    y_sv = height - 140
    c.drawString(40, y_sv, f"TA: {data['sv']['ta']}")
    c.drawString(120, y_sv, f"Temp: {data['sv']['temp']}")
    c.drawString(200, y_sv, f"FC: {data['sv']['fc']}")
    c.drawString(260, y_sv, f"FR: {data['sv']['fr']}")
    c.drawString(320, y_sv, f"Peso: {data['sv']['peso']}")
    c.drawString(390, y_sv, f"Talla: {data['sv']['talla']}")

    # Nota
    y_texto = height - 170
    c.setFont("Helvetica", 9)

    for linea in data["nota"].split("\n"):
        if y_texto < 80:
            c.showPage()
            encabezado()
            y_texto = height - 90
        c.drawString(40, y_texto, linea)
        y_texto -= 12

    # Diagnóstico
    y_texto -= 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y_texto, "Diagnóstico:")
    c.setFont("Helvetica", 9)

    for d in data["diagnosticos"]:
        y_texto -= 12
        c.drawString(60, y_texto, f"- {d['desc']} ({d['cie11']})")

    # Firma
    y_texto -= 40
    c.drawString(40, y_texto, f"Médico: {data['medico']}")
    c.drawString(40, y_texto - 15, f"Cédula: {data['cedula']}")

    c.save()
