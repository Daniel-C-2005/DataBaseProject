from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QStackedWidget, QFrame
from PyQt5.QtGui import QIcon, QFont, QPalette, QLinearGradient, QColor, QFontDatabase
from PyQt5.QtCore import QTimer, QTime, Qt, QSize

from Pharmacy.DataBase.PruebaConexion import usuario


class PuntoDeVenta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farmacia Luz y Esperanza")
        self.setGeometry(100, 100, 1000, 700)

        # Usuario activo
        self.usuario_activo_nombre = usuario

        # Cargar la fuente personalizada desde el archivo TTF
        font_id = QFontDatabase.addApplicationFont("../Fonts/emmasophia.ttf")
        if font_id == -1:
            print("Error al cargar la fuente")
        else:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                print("Fuente cargada:", font_families[0])
                self.fuente_personalizada = font_families[0]
            else:
                self.fuente_personalizada = 'Arial'

        # Configurar estilo Fusion con degradado azul
        self.aplicar_estilos()

        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Añadir un espacio antes del menú superior
        layout_principal.addSpacing(15)

        # Texto principal
        texto_principal = QLabel("Farmacia Luz y Esperanza", self)
        texto_principal.setAlignment(Qt.AlignCenter)
        texto_principal.setFont(QFont('Montserrat', 24, QFont.Bold))
        texto_principal.setStyleSheet("color: white;")
        layout_principal.addWidget(texto_principal)

        # Añadir un espacio antes del menú superior
        layout_principal.addSpacing(15)

        # Añadir la línea blanca debajo del texto principal
        linea_divisora = QFrame()
        linea_divisora.setFrameShape(QFrame.HLine)
        linea_divisora.setFrameShadow(QFrame.Sunken)
        linea_divisora.setStyleSheet("color: white; border: 3px solid white;")
        layout_principal.addWidget(linea_divisora)

        # Añadir un espacio antes del menú superior
        layout_principal.addSpacing(15)

        # Crear el menú superior con botones para las diferentes secciones
        self.crear_menu_superior(layout_principal)

        # Sección principal donde se mostrará el contenido de cada sección
        self.contenido_principal = QStackedWidget()
        layout_principal.addWidget(self.contenido_principal)

        # Crear la pantalla de inicio
        self.crear_inicio()

        # Crear las diferentes secciones (Items y Gestión Inventario)
        self.crear_secciones()

        # Layout para usuario activo y reloj
        self.crear_pie_de_pagina(layout_principal)

        # Configurar el widget central
        central_widget.setLayout(layout_principal)

    def aplicar_estilos(self):
        """
        Aplica el estilo Mac y un degradado en tonos de azul más fuertes como fondo.
        """
        QApplication.setStyle('Fusion')
        palette = QPalette()

        # Degradado de azul oscuro a tonos más suaves
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setColorAt(0.0, QColor(0, 39, 77))  # Azul oscuro (#00274D)
        gradient.setColorAt(0.3, QColor(0, 64, 128))  # Azul intermedio oscuro (#004080)
        gradient.setColorAt(0.7, QColor(0, 89, 179))  # Azul intermedio (#0059B3)
        gradient.setColorAt(1.0, QColor(0, 39, 77))  # Azul claro (#0073E6)

        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def crear_menu_superior(self, layout):
        """
        Crea el menú superior con botones para las diferentes secciones.
        """
        layout_menu = QHBoxLayout()

        # Tamaño de los íconos
        icon_size = QSize(32, 32)

        # Botón Inicio
        boton_inicio = QPushButton("Inicio")
        boton_inicio.setFont(QFont('Arial', 55, QFont.Bold))
        boton_inicio.setIcon(QIcon('../Images/Home.png'))
        boton_inicio.setIconSize(icon_size)
        boton_inicio.clicked.connect(self.mostrar_inicio)
        boton_inicio.setStyleSheet(self.estilo_boton())
        layout_menu.addWidget(boton_inicio)

        # Botón Items
        boton_items = QPushButton("Items")
        boton_items.setFont(QFont('Arial', 32, QFont.Bold))
        boton_items.setIcon(QIcon('../Images/inventario.png'))
        boton_items.setIconSize(icon_size)
        boton_items.clicked.connect(self.mostrar_items)
        boton_items.setStyleSheet(self.estilo_boton())
        layout_menu.addWidget(boton_items)

        # Botón Gestión de Inventario
        boton_gestion_inventario = QPushButton("Gestión Inventario")
        boton_gestion_inventario.setFont(QFont('Arial', 32, QFont.Bold))
        boton_gestion_inventario.setIcon(QIcon('../Images/Gestionar_Formulario.png'))
        boton_gestion_inventario.setIconSize(icon_size)
        boton_gestion_inventario.clicked.connect(self.mostrar_gestion_inventario)
        boton_gestion_inventario.setStyleSheet(self.estilo_boton())
        layout_menu.addWidget(boton_gestion_inventario)

        # Añadir el layout del menú superior al layout principal
        layout.addLayout(layout_menu)

    def estilo_boton(self):
        """
        Estilo para los botones: transparentes, con bordes redondeados y hover.
        """
        return """
            QPushButton {
                background-color: transparent;  /* Botón transparente */
                border: 3px solid white;  /* Borde blanco */
                border-radius: 15px;  /* Bordes redondeados */
                padding: 10px;
                color: white;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);  /* Fondo semitransparente en hover */
            }
            QPushButton:pressed {
                background-color:  blue  /* Fondo un poco más fuerte al presionar */
            }
        """

    def crear_inicio(self):
        """
        Crear la pantalla de inicio.
        """
        pantalla_inicio = QLabel("TU SALUD, NUESTRO COMPROMISO", self)
        pantalla_inicio.setAlignment(Qt.AlignCenter)
        pantalla_inicio.setFont(QFont(self.fuente_personalizada, 18, QFont.StyleItalic))
        pantalla_inicio.setStyleSheet("color: gold;")
        self.contenido_principal.addWidget(pantalla_inicio)

    def crear_secciones(self):
        """
        Crea las secciones de Items y Gestión de Inventario.
        """
        # Sección Items
        widget_items = QWidget()
        layout_items = QVBoxLayout()
        label_items = QLabel("Aquí puedes gestionar los items", self)
        label_items.setFont(QFont('Arial', 18))
        layout_items.addWidget(label_items)
        widget_items.setLayout(layout_items)
        self.contenido_principal.addWidget(widget_items)

        #Agregar cosas a la seccion de items
        #Bottones de la seccion de items
        boton_agregar = QPushButton("Agregar Item")
        boton_agregar.setFont(QFont('Arial', 18))
        layout_items.addWidget(boton_agregar)



        # Sección Gestión de Inventario
        widget_gestion_inventario = QWidget()
        layout_gestion_inventario = QVBoxLayout()
        label_gestion_inventario = QLabel("Aquí puedes gestionar el inventario", self)
        label_gestion_inventario.setFont(QFont('Arial', 18))
        layout_gestion_inventario.addWidget(label_gestion_inventario)
        widget_gestion_inventario.setLayout(layout_gestion_inventario)
        self.contenido_principal.addWidget(widget_gestion_inventario)

    def crear_pie_de_pagina(self, layout):
        """
        Crea el pie de página con el usuario activo y el reloj.
        """
        layout_pie = QHBoxLayout()

        # Reloj en la esquina inferior izquierda
        self.reloj = QLabel(self)
        self.reloj.setAlignment(Qt.AlignLeft)
        layout_pie.addWidget(self.reloj)

        # Mostrar el usuario activo
        self.usuario_activo = QLabel(f"Usuario activo: {self.usuario_activo_nombre}", self)
        self.usuario_activo.setAlignment(Qt.AlignRight)
        layout_pie.addWidget(self.usuario_activo)

        # Actualizar la hora cada segundo
        timer = QTimer(self)
        timer.timeout.connect(self.mostrar_hora)
        timer.start(1000)

        layout.addLayout(layout_pie)

    def mostrar_hora(self):
        """
        Función para mostrar la hora actual en la esquina inferior izquierda.
        """
        hora = QTime.currentTime().toString('hh:mm:ss')
        self.reloj.setText(f"Hora: {hora}")

    def mostrar_inicio(self):
        """
        Método para mostrar la pantalla de inicio.
        """
        self.contenido_principal.setCurrentIndex(0)

    def mostrar_items(self):
        """
        Método para mostrar la sección de Items.
        """
        self.contenido_principal.setCurrentIndex(1)

    def mostrar_gestion_inventario(self):
        """
        Método para mostrar la sección de Gestión de Inventario.
        """
        self.contenido_principal.setCurrentIndex(2)


# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication([])
    window = PuntoDeVenta()
    window.show()
    app.exec_()

