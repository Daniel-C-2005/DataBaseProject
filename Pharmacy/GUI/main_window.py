from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox


# Ventana Principal después de hacer login
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 600, 400)

        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de bienvenida
        etiqueta = QLabel("Bienvenido a la Ventana Principal", self)
        etiqueta.setGeometry(50, 50, 300, 50)
        layout.addWidget(etiqueta)

        # Botón de acción
        boton_accion = QPushButton("Acción", self)
        boton_accion.clicked.connect(self.realizar_accion)
        layout.addWidget(boton_accion)

        # Aplicar layout al widget central
        central_widget.setLayout(layout)

    def realizar_accion(self):
        # Acción que se ejecutará al presionar el botón
        QMessageBox.information(self, "Acción", "Botón presionado")

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


