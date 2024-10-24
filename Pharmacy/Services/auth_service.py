import sqlite3
import os
from datetime import datetime, timedelta
from random import randint

from Pharmacy.Utils.SMSService import SMSService


class AuthService:
    def __init__(self):
        # Obtener la ruta absoluta al archivo de la base de datos
        db_path = os.path.join(os.path.dirname(__file__), '../DataBase/usuarios.db')
        db_path = os.path.abspath(db_path)  # Convertirlo a una ruta absoluta

        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Instanciar el servicio de SMS
        self.sms_service = SMSService(self)

    def verificar_credenciales(self, nombre_usuario, contrasena):
        self.cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?",
                            (nombre_usuario, contrasena))
        resultado = self.cursor.fetchone()

        return resultado is not None

    def generar_otp(self, telefono):
        otp = str(randint(100000, 999999))  # Generar un OTP de 6 dígitos
        expiration = datetime.now() + timedelta(minutes=10)  # OTP válido por 10 minutos

        # Almacenar el OTP y la fecha de expiración en la base de datos
        self.cursor.execute("""
            UPDATE usuarios 
            SET otp_reset = ?, otp_expiration = ? 
            WHERE numero_telefono = ?
        """, (otp, expiration, telefono))
        self.conn.commit()

        return otp

    def enviar_otp_por_sms(self, telefono):
        otp = self.generar_otp(telefono)
        mensaje = f"Tu código de verificación para restablecer tu contraseña es: {otp}"

        # Usar el servicio de SMS para enviar el OTP
        self.sms_service.enviar_sms(telefono, mensaje)

    def verificar_otp(self, telefono, otp):
        self.cursor.execute("""
            SELECT * FROM usuarios 
            WHERE numero_telefono = ? AND otp_reset = ? AND otp_expiration > ?
        """, (telefono, otp, datetime.now()))
        usuario = self.cursor.fetchone()

        return usuario is not None

    def actualizar_contrasena(self, telefono, nueva_contrasena):
        self.cursor.execute("""
            UPDATE usuarios 
            SET contrasena = ?, otp_reset = NULL, otp_expiration = NULL 
            WHERE numero_telefono = ?
        """, (nueva_contrasena, telefono))
        self.conn.commit()

        print(f"Contraseña restablecida para el número {telefono}")

    def cerrar_conexion(self):
        self.conn.close()

