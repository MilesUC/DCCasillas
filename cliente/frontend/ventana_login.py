from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
                                                        'RUTA_VENTANA_LOGIN')))


class VentanaLogin(window_name, base_class):

    senal_enviar_login = pyqtSignal(dict)
    senal_mostrar_ventana_principal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_jugar.clicked.connect(self.enviar_login)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.enviar_login()

    def enviar_login(self):
        nombre_usuario = self.label_nombre.text().replace('','')
        diccionario = {
            'comando': 'validar_login',
            'nombre usuario': nombre_usuario,
        }
        self.senal_enviar_login.emit(diccionario)

    def mostrar_error(self):
        self.label_nombre.setText('Datos invalidos')


