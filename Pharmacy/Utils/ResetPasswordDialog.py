from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Pharmacy.Utils.SMSService import SMSService


class ResetPasswordDialog(QDialog):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setWindowTitle("Restablecer Contraseña")
        self.setGeometry(400, 200, 350, 200)

        # Aplicar el estilo general
        self.setStyleSheet(self.estilo_general())

        layout = QVBoxLayout()

        # Etiqueta para el número de teléfono
        self.label = QLabel("Introduce tu número de teléfono:", self)
        self.label.setFont(QFont('Montserrat', 12))  # Cambiamos la fuente a Montserrat
        layout.addWidget(self.label)

        # Campo de texto para el número de teléfono
        self.input_telefono = QLineEdit(self)
        self.input_telefono.setPlaceholderText("Número de teléfono")
        self.input_telefono.setFont(QFont('Roboto', 10))  # Fuente Roboto
        layout.addWidget(self.input_telefono)

        # Botón para enviar el OTP
        self.boton_enviar = QPushButton("Enviar OTP", self)
        self.boton_enviar.setFont(QFont('Montserrat', 10, QFont.Bold))  # Fuente Montserrat en negrita
        self.boton_enviar.clicked.connect(self.enviar_otp)
        layout.addWidget(self.boton_enviar)

        self.setLayout(layout)

    def estilo_general(self):
        """
        Aplica un estilo general a la ventana con degradado en el fondo y botones estilo Mac.
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
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.8);  /* Fondo semitransparente */
                border: 2px solid rgba(255, 255, 255, 0.3);  /* Borde semitransparente */
                border-radius: 15px;  /* Redondear bordes */
                padding: 10px;
                font-size: 14px;
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
                background-color: #2C6F99;  /* Color aún más oscuro al presionar */
            }
        """

    def enviar_otp(self):
        """
        Función para manejar el envío del OTP y la verificación del número de teléfono ingresado.
        """
        try:
            telefono = self.input_telefono.text().strip()  # Obtener y limpiar el número de teléfono

            # Validar que el número de teléfono no esté vacío
            if not telefono:
                QMessageBox.warning(self, "Error", "El número de teléfono no puede estar vacío.")
                return

            # Llamar al AuthService para enviar el OTP
            self.auth_service.enviar_otp_por_sms(telefono)

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Éxito", f"Se ha enviado un código OTP a tu número de teléfono: {telefono}")

            # Pedir el código OTP al usuario
            otp, ok = QInputDialog.getText(self, "Verificar OTP", "Introduce el código OTP:")
            if ok and otp:
                if self.auth_service.verificar_otp(telefono, otp):
                    # Si el OTP es correcto, pedir la nueva contraseña
                    nueva_contrasena, ok_contrasena = QInputDialog.getText(self, "Nueva contraseña", "Introduce tu nueva contraseña:")
                    if ok_contrasena and nueva_contrasena:
                        # Actualizar la contraseña en la base de datos
                        self.auth_service.actualizar_contrasena(telefono, nueva_contrasena)
                        QMessageBox.information(self, "Éxito", "Contraseña restablecida con éxito.")
                        self.close()
                    else:
                        QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía.")
                else:
                    QMessageBox.warning(self, "Error", "El código OTP es incorrecto o ha expirado.")
            else:
                QMessageBox.warning(self, "Error", "Debes ingresar el código OTP.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al procesar la solicitud: {e}")
            print(f"Error: {e}")
