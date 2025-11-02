import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox, QFrame
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# --------------------------- Login Window --------------------------- #
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - PHEDS")
        self.setFixedSize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("PHEDS - Login")
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        login_btn = QPushButton("Ingresar")
        login_btn.setStyleSheet("background-color: #2E8B57; color: white; font-weight: bold; height: 35px;")
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def check_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        # Usuario y contraseña de ejemplo
        if username == "admin" and password == "admin123":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

# --------------------------- Main Window --------------------------- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PHEDS - Expediente Clínico")
        self.setFixedSize(1000, 600)
        self.initUI()

    def initUI(self):
        # --- Layout principal ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- Menú lateral ---
        menu_frame = QFrame()
        menu_frame.setFixedWidth(200)
        menu_frame.setStyleSheet("background-color: #f0f0f0;")
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10, 10, 10, 10)
        menu_layout.setSpacing(15)
        menu_frame.setLayout(menu_layout)

        # Logos pequeños arriba
        logo_label = QLabel("LOGO")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 14, QFont.Bold))
        menu_layout.addWidget(logo_label)

        # Botones del menú
        buttons_info = [
            ("Hoja Frontal", 0),
            ("Nota de Evolución", 1),
            ("Indicaciones Médicas", 2),
            ("Solicitud de Laboratorio e Imagen", 3),
            ("Signos Vitales", 4),
            ("Resumen", 5)
        ]
        self.menu_buttons = []

        for text, index in buttons_info:
            btn = QPushButton(text)
            btn.setStyleSheet("background-color: #2E8B57; color: white; font-weight: bold; height: 40px;")
            btn.clicked.connect(lambda checked, idx=index: self.display_page(idx))
            menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        menu_layout.addStretch()

        # --- Área de contenido ---
        self.stack = QStackedWidget()
        self.pages = []

        # Creación de páginas
        page_titles = [
            "Hoja Frontal",
            "Nota de Evolución",
            "Indicaciones Médicas",
            "Solicitud de Laboratorio e Imagen",
            "Signos Vitales",
            "Resumen"
        ]

        for title in page_titles:
            page = QWidget()
            layout = QVBoxLayout()
            label = QLabel(title)
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            page.setLayout(layout)
            self.stack.addWidget(page)
            self.pages.append(page)

        # --- Layout final ---
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(self.stack)

    def display_page(self, index):
        self.stack.setCurrentIndex(index)

# --------------------------- Aplicación --------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
