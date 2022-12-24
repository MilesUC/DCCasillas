from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
                                    "RUTA_VENTANA_POSTJUEGO")))


class VentanaPostJuego(window_name, base_class):

    senal_abrir_ventana_login = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_volver.clicked.connect(self.volver)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.volver()

    def volver(self):
        self.senal_abrir_ventana_login.emit()

    def preparar_ventana(self, color, colores, info):
        fichas_base = info[0]
        fichas_color = info[1]
        fichas_victoria = info[2]
        if len(colores) >= 3:
            self.label_tapa_1.close()
            if len(colores) == 4:
                self.label_tapa_2.close()
        
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

    def mostrar(self, ganador, usuarios):
        self.ganador.setText(ganador)
        self.ganador.repaint()

        for i in range(len(usuarios)):
            if i == 0:
                self.label_nombre1.setText(usuarios[0])
            elif i == 1:
                self.label_nombre2.setText(usuarios[1])
            elif i == 2:
                self.label_nombre3.setText(usuarios[2])
            elif i == 3:
                self.label_nombre4.setText(usuarios[3])

        self.show()
    



