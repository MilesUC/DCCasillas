from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
                                                        'RUTA_VENTANA_JUEGO')))


class VentanaJuego(window_name, base_class):

    senal_enviar_login = pyqtSignal(dict)
    senal_mostrar_ventana_principal = pyqtSignal(str)
    senal_lanzar_dado = pyqtSignal()
    senal_cheat = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_dado.clicked.connect(self.lanzar_dado)
        self.boton_dado.setDisabled(True)

        self.ficha_azul_1.setParent(self)
        self.ficha_azul_2.setParent(self)
        self.ficha_amarilla_1.setParent(self)
        self.ficha_amarilla_2.setParent(self)
        self.ficha_verde_1.setParent(self)
        self.ficha_verde_2.setParent(self)
        self.ficha_roja_1.setParent(self)
        self.ficha_roja_2.setParent(self)

        self.teclas = ['x', 'x']

    def keyPressEvent(self, event):
        self.teclas.pop(0)
        self.teclas.append(event.text())
        if self.teclas[0] == 'w' and self.teclas[1] == 'p':
            self.senal_cheat.emit()

    def preparar_ventana(self, usuarios, colores):
        for i in range(len(usuarios)):
            if i == 0:
                self.label_j1.setText(usuarios[0])
                self.label_ficha_j1.setPixmap(QPixmap(join(*data_json(f'RUTA_{colores[0]}'))))
                self.label_ficha_j1.setScaledContents(True)
            elif i == 1:
                self.label_j2.setText(usuarios[1])
                self.label_ficha_j2.setPixmap(QPixmap(join(*data_json(f'RUTA_{colores[1]}'))))
            elif i == 2:
                self.label_j3.setText(usuarios[2])
                self.label_ficha_j3.setPixmap(QPixmap(join(*data_json(f'RUTA_{colores[2]}'))))
            elif i == 3:
                self.label_j4.setText(usuarios[3])
                self.label_ficha_j4.setPixmap(QPixmap(join(*data_json(f'RUTA_{colores[3]}'))))

        if len(usuarios) >= 3:
            self.label_tapa_1.close()
            if len(usuarios) == 4:
                self.label_tapa_2.close()

    def actualizar_turno(self, nombre, dado):
        self.jugador_turno.setText(nombre)
        self.jugador_turno.repaint()

        if dado:
            self.boton_dado.setDisabled(False)
        else:
            self.boton_dado.setDisabled(True)

    def lanzar_dado(self):
        self.senal_lanzar_dado.emit()

    def actualizar_tablero(self, color, posicion, ficha):

        if ficha == 1:
            if color == 'AZUL':
                self.ficha_azul_1.setGeometry(60 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            elif color == 'AMARILLA':
                self.ficha_amarilla_1.setGeometry(60 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            elif color == 'VERDE':
                self.ficha_verde_1.setGeometry(60 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            else:
                self.ficha_roja_1.setGeometry(60 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)

        elif ficha == 2:
            if color == 'AZUL':
                self.ficha_azul_2.setGeometry(100 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            elif color == 'AMARILLA':
                self.ficha_amarilla_2.setGeometry(100 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            elif color == 'VERDE':
                self.ficha_verde_2.setGeometry(100 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)
            else:
                self.ficha_roja_2.setGeometry(100 + posicion[1] * 90, 220 + posicion[0] * 90, 31, 51)


    def actualizar_interfaz(self, color, colores, info):
        fichas_base = info[0]
        fichas_color = info[1]
        fichas_victoria = info[2]

        for i in range(len(colores)):
            if i == 0 and colores[i] == color:
                self.fichas_base_j1.setText(str(fichas_base))
                self.fichas_color_j1.setText(str(fichas_color))
                self.fichas_victoria_j1.setText(str(fichas_victoria))
                self.fichas_base_j1.repaint()
                self.fichas_color_j1.repaint()
                self.fichas_victoria_j1.repaint()

            elif i == 1 and colores[i] == color:
                self.fichas_base_j2.setText(str(fichas_base))
                self.fichas_color_j2.setText(str(fichas_color))
                self.fichas_victoria_j2.setText(str(fichas_victoria))
                self.fichas_base_j2.repaint()
                self.fichas_color_j2.repaint()
                self.fichas_victoria_j2.repaint()

            elif i == 2 and colores[i] == color:
                self.fichas_base_j3.setText(str(fichas_base))
                self.fichas_color_j3.setText(str(fichas_color))
                self.fichas_victoria_j3.setText(str(fichas_victoria))
                self.fichas_base_j3.repaint()
                self.fichas_color_j3.repaint()
                self.fichas_victoria_j3.repaint()

            elif i == 3 and colores[i] == color:
                self.fichas_base_j4.setText(str(fichas_base))
                self.fichas_color_j4.setText(str(fichas_color))
                self.fichas_victoria_j4.setText(str(fichas_victoria))
                self.fichas_base_j4.repaint()
                self.fichas_color_j4.repaint()
                self.fichas_victoria_j4.repaint()

    def cambiar_numero(self, numero):
        self.numero_obtenido.setText(str(numero))
        self.numero_obtenido.repaint()

    def ocultar(self):
        self.ficha_azul_1.setGeometry(60, 220, 31, 51)
        self.ficha_amarilla_1.setGeometry(510, 220, 31, 51)
        self.ficha_verde_1.setGeometry(510, 670, 31, 51)
        self.ficha_roja_1.setGeometry(60, 670, 31, 51)
        self.ficha_azul_2.setGeometry(100, 220, 31, 51)
        self.ficha_amarilla_2.setGeometry(550, 220, 31, 51)
        self.ficha_verde_2.setGeometry(550, 670, 31, 51)
        self.ficha_roja_2.setGeometry(100, 670, 31, 51)
        self.fichas_base_j1.setText("2")
        self.fichas_color_j1.setText("0")
        self.fichas_victoria_j1.setText("0")
        self.fichas_base_j1.repaint()
        self.fichas_color_j1.repaint()
        self.fichas_victoria_j1.repaint()
        self.fichas_base_j2.setText("2")
        self.fichas_color_j2.setText("0")
        self.fichas_victoria_j2.setText("0")
        self.fichas_base_j2.repaint()
        self.fichas_color_j2.repaint()
        self.fichas_victoria_j2.repaint()
        self.fichas_base_j3.setText("2")
        self.fichas_color_j3.setText("0")
        self.fichas_victoria_j3.setText("0")
        self.fichas_base_j3.repaint()
        self.fichas_color_j3.repaint()
        self.fichas_victoria_j3.repaint()
        self.fichas_base_j4.setText("2")
        self.fichas_color_j4.setText("0")
        self.fichas_victoria_j4.setText("0")
        self.fichas_base_j4.repaint()
        self.fichas_color_j4.repaint()
        self.fichas_victoria_j4.repaint()

        self.hide()

        




