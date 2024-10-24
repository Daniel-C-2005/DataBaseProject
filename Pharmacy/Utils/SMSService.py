import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SMSService(QDialog):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.api_key = 'Clave de TeltBext'  # Cambia a tu clave de TextBelt si tienes una premium

        # Establecer el estilo general de la ventana
        self.setWindowTitle("Envío de OTP por SMS")
        self.setGeometry(400, 200, 350, 150)
        self.setStyleSheet(self.estilo_general())

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Etiqueta para mostrar el estado
        self.label_estado = QLabel("Enviar código OTP por SMS")
        self.label_estado.setFont(QFont('Montserrat', 12))  # Cambiar la fuente a Montserrat
        layout.addWidget(self.label_estado)

        # Botón para realizar el envío del SMS
        self.boton_enviar = QPushButton("Enviar OTP", self)
        self.boton_enviar.setFont(QFont('Montserrat', 10, QFont.Bold))  # Fuente Montserrat en negrita
        self.boton_enviar.clicked.connect(self.enviar_sms)
        layout.addWidget(self.boton_enviar)

        # Establecer el layout en la ventana
        self.setLayout(layout)

    def estilo_general(self):
        """
        Establece un estilo visual con degradado y fuentes modernas.
        """
        return """
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #B0BEC5,    /* Gris claro */
                    stop: 0.5 #E0F7FA,  /* Azul pastel claro */
                    stop: 1 #FFFFFF     /* Blanco */
                );
                color: #333333;  /* Color del texto general */
            }
            QLabel {
                font-family: 'Montserrat';  /* Fuente moderna */
                font-size: 14px;
                color: #333333;  /* Color del texto */
            }
            QPushButton {
                background-color: #4A90E2;  /* Color azul Mac-like */
                color: white;
                border-radius: 20px;  /* Bordes redondeados estilo Mac */
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ABD;  /* Color más oscuro al pasar el ratón */
            }
            QPushButton:pressed {
                background-color: #2C6F99;  /* Color más oscuro al presionar */
            }
        """

    def enviar_sms(self, telefono='+502XXXXXXXX', mensaje="Tu código OTP es: 123456"):
        """
        Envía un SMS utilizando la API de TextBelt y muestra el resultado en una ventana emergente.
        """
        # Enviar el SMS usando la API de TextBelt
        response = requests.post("https://textbelt.com/text", {
            'phone': telefono,
            'message': mensaje,
            'key': self.api_key,
        })

        # Procesar la respuesta
        result = response.json()
        if result['success']:
            # Mostrar un mensaje de éxito
            QMessageBox.information(self, "Éxito", f"SMS enviado con éxito al número {telefono}")
        else:
            # Mostrar un mensaje de error
            QMessageBox.warning(self, "Error", f"Error al enviar SMS: {result['error']}")

        return result['success']


