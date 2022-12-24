from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
                                    "RUTA_VENTANA_ESPERA")))


class VentanaEspera(window_name, base_class):

    senal_iniciar_partida= pyqtSignal()
    senal_mostrar_ventana_juego = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_iniciar.clicked.connect(self.iniciar_partida)
        self.boton_iniciar.setDisabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.iniciar_partida()

    def iniciar_partida(self):
        self.senal_iniciar_partida.emit()
    
    def actualizar(self, usuarios, listo):
        if listo:
            self.boton_iniciar.setDisabled(False)
        for i in range(len(usuarios)):
            if i == 0:
                self.label_nombre1.setText(usuarios[0])
                self.label_nombre1.repaint()
            elif i == 1:
                self.label_nombre2.setText(usuarios[1])
                self.label_nombre2.repaint()
            elif i == 2:
                self.label_nombre3.setText(usuarios[2])
                self.label_nombre3.repaint()
            elif i == 3:
                self.label_nombre4.setText(usuarios[3])
                self.label_nombre4.repaint()

    def ocultar(self):
        self.boton_iniciar.setDisabled(True)
        self.label_nombre1.setText('')
        self.label_nombre1.repaint()
        self.label_nombre2.setText('')
        self.label_nombre2.repaint()
        self.label_nombre3.setText('')
        self.label_nombre3.repaint()
        self.label_nombre4.setText('')
        self.label_nombre4.repaint()

        self.hide()



