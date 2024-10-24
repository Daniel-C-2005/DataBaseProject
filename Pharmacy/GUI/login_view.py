import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from Pharmacy.Services.auth_service import AuthService  # Verifica que la ruta sea correcta
from Pharmacy.Utils.ResetPasswordDialog import ResetPasswordDialog


class LoginView(QDialog):
    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()  # Instancia del servicio de autenticación
        self.mostrar_contrasena = False  # Estado para mostrar/ocultar la contraseña

        self.initUI()

    def initUI(self):
        self.setWindowTitle(" ")  # Título de la ventana
        self.setGeometry(300, 200, 400, 500)  # Ajustamos el tamaño de la ventana
        self.setStyleSheet(self.estilo_ventana())  # Aplicar estilo con degradado

        layout = QVBoxLayout()

        # Obtener la ruta base de este archivo (login_view.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Añadir un ícono de usuario en la parte superior
        self.avatar = QLabel(self)
        avatar_path = os.path.join(base_dir, "../Images/avatar.png")  # Ruta absoluta a la imagen de avatar
        pixmap = QPixmap(avatar_path)  # Cargar la imagen de avatar
        if not pixmap.isNull():  # Verificar si la imagen se cargó correctamente
            self.avatar.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajustar el tamaño
        else:
            print(f"Error: No se pudo cargar la imagen de avatar desde {avatar_path}")
        self.avatar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.avatar)

        # Añadir un texto debajo del avatar que diga "LOGIN"
        self.label_login = QLabel("LOGIN")
        self.label_login.setFont(QFont('Arial', 18, QFont.Bold))
        self.label_login.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_login)

        # Campo de entrada para el nombre de usuario con ícono de hacker(1).png
        # El texto sera algo transparente
        self.entrada_usuario = self.crear_campo_con_icono("Nombre de usuario", os.path.join(base_dir, "../Images/hacker (1).png"))
        layout.addLayout(self.entrada_usuario[0])

        # Campo de entrada para la contraseña con ícono y botón de mostrar/ocultar contraseña
        self.entrada_contrasena = self.crear_campo_con_icono("Contraseña", os.path.join(base_dir, "../Images/verificado (1).png"), is_password=True)
        layout.addLayout(self.entrada_contrasena[0])

        # Botón de login
        self.boton_login = QPushButton("LOGIN", self)
        self.boton_login.setFont(QFont('Arial', 12, QFont.Bold))
        self.boton_login.setStyleSheet(self.estilo_boton())
        self.boton_login.clicked.connect(self.verificar_login)
        layout.addWidget(self.boton_login)

        # Añadir un enlace de "Forgot Your Password?"
        # Añadir un enlace funcional de "Forgot Your Password?"
        self.forgot_password = QLabel("<a href='#'>¿Olvidaste tu contraseña?</a>")
        self.forgot_password.setFont(QFont('Arial', 10))
        self.forgot_password.setStyleSheet("color: #4A90E2;")
        self.forgot_password.setAlignment(Qt.AlignCenter)
        self.forgot_password.linkActivated.connect(
            self.abrir_dialogo_reset_contrasena)  # Conectar a la función que abre el diálogo
        layout.addWidget(self.forgot_password)

        self.setLayout(layout)

    def crear_campo_con_icono(self, placeholder_text, icon_path, is_password=False):
        layout = QHBoxLayout()

        # Etiqueta para el ícono
        icon_label = QLabel(self)
        icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajustar el tamaño del ícono
        layout.addWidget(icon_label)

        # Campo de entrada
        entrada = QLineEdit(self)
        entrada.setPlaceholderText(placeholder_text)
        entrada.setStyleSheet(self.estilo_campo())
        if is_password:
            entrada.setEchoMode(QLineEdit.Password)
            # Botón para mostrar/ocultar la contraseña
            boton_contrasena = QPushButton(self)
            boton_contrasena.setIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Images/EyeClose.png")))  # Ruta absoluta
            boton_contrasena.setFixedSize(32, 32)
            boton_contrasena.setStyleSheet("border: none;")
            boton_contrasena.clicked.connect(lambda: self.cambiar_estado_contrasena(entrada, boton_contrasena))
            layout.addWidget(entrada)
            layout.addWidget(boton_contrasena)
        else:
            layout.addWidget(entrada)

        return layout, entrada

    def cambiar_estado_contrasena(self, entrada, boton_contrasena):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtener la ruta del archivo actual
        if entrada.echoMode() == QLineEdit.Password:
            entrada.setEchoMode(QLineEdit.Normal)
            boton_contrasena.setIcon(QIcon(os.path.join(base_dir, "../Images/EyeOpen.png")))  # Cambiar a imagen de ojo abierto
        else:
            entrada.setEchoMode(QLineEdit.Password)
            boton_contrasena.setIcon(QIcon(os.path.join(base_dir, "../Images/EyeClose.png")))  # Cambiar a imagen de ojo cerrado

    def estilo_ventana(self):
        return """
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #B0BEC5,  /* Gris claro */
                    stop: 0.5 #E0F7FA,  /* Azul pastel claro */
                    stop: 1 #FFFFFF    /* Blanco */
                );
                color: #333333;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
        """

    def estilo_campo(self):
        return """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.2);  /* Fondo transparente */
                border: 2px solid rgba(255, 255, 255, 0.3);  /* Borde semitransparente */
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
            }
        """

    def estilo_boton(self):
        return """
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2C6F99;
            }
        """

    # Función para verificar las credenciales con auth_service.py
    def verificar_login(self):
        nombre_usuario = self.entrada_usuario[1].text()
        contrasena = self.entrada_contrasena[1].text()

        if self.auth_service.verificar_credenciales(nombre_usuario, contrasena):
            self.mostrar_mensaje_exito("Login exitoso")  # Mostrar mensaje de éxito
        else:
            QMessageBox.critical(self, "Error", "Nombre de usuario o contraseña incorrectos")

    def abrir_dialogo_reset_contrasena(self):
        # Crear y mostrar el diálogo de restablecimiento de contraseña por SMS
        dialogo_reset = ResetPasswordDialog(self.auth_service)
        dialogo_reset.exec_()  # Mostrar el diálogo de forma modal

    def mostrar_mensaje_exito(self, mensaje):
        # Crear un QLabel para mostrar el mensaje de "Login exitoso"
        self.label_exito = QLabel(mensaje, self)
        self.label_exito.setFont(QFont('Arial', 14))
        self.label_exito.setStyleSheet("color: green;")
        self.label_exito.setAlignment(Qt.AlignCenter)

        # Reemplazar el layout actual por solo el mensaje
        layout = QVBoxLayout()
        layout.addWidget(self.label_exito)
        self.setLayout(layout)

        # Esperar 1.5 segundos y luego abrir la ventana principal y cerrar la ventana de login
        QTimer.singleShot(700, self.abrir_ventana_principal)

    def abrir_ventana_principal(self):
        from Pharmacy.GUI.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    login_view = LoginView()
    login_view.show()

    sys.exit(app.exec_())