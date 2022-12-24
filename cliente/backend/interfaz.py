from PyQt5.QtCore import pyqtSignal, QObject
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_login import VentanaLogin
from frontend.ventana_espera import VentanaEspera
from frontend.ventana_postjuego import VentanaPostJuego
from random import randint
from utils import data_json


class Interfaz(QObject):
    senal_actualizar_ventana_espera = pyqtSignal(list, bool)
    senal_abrir_ventana_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()
    senal_login_rechazado = pyqtSignal()
    senal_actualizar_turno = pyqtSignal(str, bool)
    senal_preparar_ventana_juego = pyqtSignal(list, list)
    senal_actualizar_tablero = pyqtSignal(str, list, int)
    senal_actualizar_interfaz = pyqtSignal(str, list, list)
    senal_abrir_ventana_postjuego = pyqtSignal(str, list)
    senal_actualizar_numero = pyqtSignal(int)
    senal_cerrar_ventana_juego = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.nombre = None
        self.color = None
        self.pos = None
        self.ficha = None
        self.fichas_base = 2
        self.fichas_color = 0
        self.fichas_victoria = 0
        self.ventana_login = VentanaLogin()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()
        self.ventana_postjuego = VentanaPostJuego()
        self.ventana_login.senal_enviar_login.connect(parent.enviar)
        self.ventana_espera.senal_iniciar_partida.connect(self.iniciar_partida)
        self.senal_actualizar_ventana_espera.connect(self.ventana_espera.actualizar)
        self.senal_abrir_ventana_espera.connect(self.ventana_login.hide)
        self.senal_abrir_ventana_espera.connect(self.ventana_espera.show)
        self.senal_actualizar_numero.connect(self.ventana_juego.cambiar_numero)
        self.ventana_juego.senal_lanzar_dado.connect(self.lanzar_dado)
        self.senal_preparar_ventana_juego.connect(self.ventana_juego.preparar_ventana)
        self.senal_abrir_ventana_juego.connect(self.ventana_espera.ocultar)
        self.senal_abrir_ventana_juego.connect(self.ventana_juego.show)
        self.ventana_postjuego.senal_abrir_ventana_login.connect(self.ventana_postjuego.hide)
        self.ventana_postjuego.senal_abrir_ventana_login.connect(self.ventana_login.show)
        self.senal_cerrar_ventana_juego.connect(self.ventana_juego.ocultar)
        self.senal_abrir_ventana_postjuego.connect(self.ventana_postjuego.mostrar)
        self.senal_actualizar_turno.connect(self.ventana_juego.actualizar_turno)
        self.senal_actualizar_interfaz.connect(self.ventana_postjuego.preparar_ventana)
        self.senal_actualizar_interfaz.connect(self.ventana_juego.actualizar_interfaz)
        self.senal_actualizar_tablero.connect(self.ventana_juego.actualizar_tablero)

        self.senal_login_rechazado.connect(self.ventana_login.mostrar_error)

        self.ventana_juego.senal_cheat.connect(self.cheat)

    def manejar_mensaje(self, mensaje: dict):
        try:
            comando = mensaje['comando']
        except KeyError:
            return {}

        if comando == 'respuesta_validacion_login':
            if mensaje['estado'] == 'aceptado':
                self.nombre = mensaje['nombre_usuario']
                self.senal_abrir_ventana_espera.emit()
            else:
                self.senal_login_rechazado.emit()
        
        elif comando == 'actualizar_ventana_espera':
            usuarios = mensaje['usuarios'].split(',')
            self.listo = mensaje['listo'] if mensaje['admin'] == mensaje['nombre_usuario'] else False
            self.iniciar_partida() if len(usuarios) >= data_json("MAX_JUGADORES") else self.listo
            self.senal_actualizar_ventana_espera.emit(usuarios, self.listo)

        elif comando == 'iniciar_partida':
            self.usuarios = mensaje['usuarios'].split(',')
            self.colores = mensaje['colores'].split(',')
            self.color = mensaje['color']
            self.ficha = 1
            if self.color == 'AZUL':
                self.pos = [0, 0]
            elif self.color == 'AMARILLA':
                self.pos = [0, 5]
            elif self.color == 'ROJA':
                self.pos = [5, 0]
            else:
                self.pos = [5, 5]
            self.senal_preparar_ventana_juego.emit(self.usuarios, self.colores)
            self.senal_abrir_ventana_juego.emit()

        elif comando == 'jugar':
            dado = True if mensaje['turno'] == self.nombre else False
            self.senal_actualizar_turno.emit(mensaje['turno'], dado)

        elif comando == 'actualizar_interfaz':
            self.senal_actualizar_interfaz.emit(mensaje['color'], mensaje['colores'].split(','),
                                                mensaje['info'].split(','))
        elif comando == 'actualizar_tablero':
            self.revisar_colision(mensaje['color'], mensaje['pos'])
            self.senal_actualizar_tablero.emit(mensaje['color'], mensaje['pos'], mensaje['ficha'])

        elif comando == 'fin_juego':
            self.senal_cerrar_ventana_juego.emit()
            self.senal_abrir_ventana_postjuego.emit(mensaje['ganador'], self.usuarios)

        elif comando == 'cheat':
            if mensaje['usuario'] != self.nombre:
                if self.color == 'AZUL':
                    self.pos = [0, 0]
                elif self.color == 'AMARILLA':
                    self.pos = [0, 5]
                elif self.color == 'ROJA':
                    self.pos = [5, 0]
                else:
                    self.pos = [5, 5]
                self.parent.enviar({'comando':'actualizar_tablero','color': self.color,
                                     'pos': self.pos, 'ficha': self.ficha})

    def iniciar_partida(self):
        self.parent.enviar({'comando':'iniciar_partida'})

    def lanzar_dado(self):
        n = randint(1, 3)
        self.senal_actualizar_numero.emit(n)
        self.mover(n)

    def mover(self, n):
        if self.ficha == 1:
            self.fichas_base = 1
        elif self.ficha == 2:
            self.fichas_base = 0
        while n > 0:
            if self.pos[0] == 0 and 0 <= self.pos[1] <= 3:
                self.pos[1] += 1
            elif self.pos[0] == 0 and self.pos[1] == 4:
                if self.color == 'AMARILLA':
                    self.pos[0] = 1
                    self.pos[1] = 4
                    self.fichas_color += 1
                else:
                    self.pos[0] = 1
                    self.pos[1] = 5

            elif self.pos[1] == 5 and 0 <= self.pos[0] <= 3:
                self.pos[0] += 1
            elif self.pos[1] == 5 and self.pos[0] == 4:
                if self.color == 'VERDE':
                    self.pos[0] = 4
                    self.pos[1] = 4
                    self.fichas_color += 1
                else:
                    self.pos[0] = 5
                    self.pos[1] = 4
            
            elif self.pos[0] == 5 and 2 <= self.pos[1] <= 5:
                self.pos[1] -= 1
            elif self.pos[0] == 5 and self.pos[1] == 1:
                if self.color == 'ROJA':
                    self.pos[0] = 4
                    self.pos[1] = 1
                    self.fichas_color += 1
                else:
                    self.pos[0] = 4
                    self.pos[1] = 0
            
            elif self.pos[1] == 0 and 2 <= self.pos[0] <= 5:
                self.pos[0] -= 1
            elif self.pos[1] == 0 and self.pos[0] == 1:
                if self.color == 'AZUL':
                    self.pos[0] = 1
                    self.pos[1] = 1
                    self.fichas_color += 1
                else:
                    self.pos[0] = 0
                    self.pos[1] = 1

            elif 1 <= self.pos[0] <= 2 and self.pos[1] == 4:
                if self.pos[0] == 2 and n > 1:
                    self.pos[0] -= n - 2
                    n = 0
                elif self.pos[0] == 1 and n > 2:
                    self.pos[0] += n - 2
                    n = 0
                else:
                    self.pos[0] += 1

            elif self.pos[0] == 4 and 3 <= self.pos[1] <= 4:
                if self.pos[1] == 3 and n > 1:
                    self.pos[1] += n - 2
                    n = 0
                elif self.pos[1] == 4 and n > 2:
                    self.pos[1] -= n - 2
                    n = 0
                else:
                    self.pos[1] -= 1

            elif 3 <= self.pos[0] <= 4 and self.pos[1] == 1:
                if self.pos[0] == 3 and n > 1:
                    self.pos[0] += n - 2
                    n = 0
                elif self.pos[0] == 4 and n > 2:
                    self.pos[0] -= n - 2
                    n = 0
                else:
                    self.pos[0] -= 1

            elif self.pos[0] == 1 and 1 <= self.pos[1] <= 2:
                if self.pos[1] == 2 and n > 1:
                    self.pos[1] -= n - 2
                    n = 0
                elif self.pos[1] == 1 and n > 2:
                    self.pos[1] += n - 2
                    n = 0
                else:
                    self.pos[1] += 1

            n -= 1

        self.parent.enviar({'comando':'actualizar_tablero','color': self.color, 'pos': self.pos,
                             'ficha': self.ficha})
        info = [str(self.fichas_base), str(self.fichas_color), str(self.fichas_victoria)]
        self.parent.enviar({'comando':'actualizar_interfaz', 'colores': ','.join(self.colores),
                            'color': self.color,'info': ','.join(info)})
        termino = False

        if self.pos[0] == 3 and self.pos[1] == 4:
            self.fichas_color -= 1
            self.fichas_victoria += 1
            if self.ficha == 2:
                self.victoria()
                termino = True
            else:
                self.ficha = 2
                self.pos[0] = 0
                self.pos[1] = 5

        elif self.pos[0] == 4 and self.pos[1] == 2:
            self.fichas_color -= 1
            self.fichas_victoria += 1
            if self.ficha == 2:
                self.victoria()
                termino = True
            else:
                self.ficha = 2
                self.pos[0] = 5
                self.pos[1] = 5

        elif self.pos[0] == 2 and self.pos[1] == 1:
            self.fichas_color -= 1
            self.fichas_victoria += 1
            if self.ficha == 2:
                self.victoria()
                termino = True
            else:
                self.ficha = 2
                self.pos[0] = 5
                self.pos[1] = 0

        elif self.pos[0] == 1 and self.pos[1] == 3:
            self.fichas_color -= 1
            self.fichas_victoria += 1
            if self.ficha == 2:
                self.victoria()
                termino = True
            else:
                self.ficha = 2
                self.pos[0] = 0
                self.pos[1] = 0

        if not termino:
            self.parent.enviar({'comando':'actualizar_tablero','color': self.color,
                             'pos': self.pos, 'ficha': self.ficha})
            info = [str(self.fichas_base), str(self.fichas_color), str(self.fichas_victoria)]
            self.parent.enviar({'comando':'actualizar_interfaz', 'colores': ','.join(self.colores),
                                'color': self.color,'info': ','.join(info)})

            self.parent.enviar({'comando': 'siguiente_turno', 'turno': self.nombre})

    def victoria(self):
        self.parent.enviar({'comando': 'fin_juego', 'ganador': self.nombre})

    def cheat(self):
        self.parent.enviar({'comando': 'cheat', 'usuario': self.nombre})

    def revisar_colision(self, color, pos):
        if self.pos == pos and self.color != color:
            if self.color == 'AZUL':
                self.pos = [0, 0]
            elif self.color == 'AMARILLA':
                self.pos = [0, 5]
            elif self.color == 'ROJA':
                self.pos = [5, 0]
            else:
                self.pos = [5, 5]

            self.parent.enviar({'comando':'actualizar_tablero','color': self.color,
                                 'pos': self.pos, 'ficha': self.ficha})