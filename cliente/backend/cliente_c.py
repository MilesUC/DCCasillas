import socket
import json
from threading import Thread, Lock
from backend.interfaz import Interfaz


class Cliente_c:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.interfaz = Interfaz(self)
        self.iniciar_cliente()

    def iniciar_cliente(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.comenzar_a_escuchar()
            self.interfaz.ventana_login.show()
        except ConnectionError as error:
            print('No se pudo conectar')
            print(f'Error: {error}')

    def comenzar_a_escuchar(self):
        thread_comenzar_a_escuchar = Thread(target = self.escuchar_servidor, daemon = True)
        thread_comenzar_a_escuchar.start()

    def escuchar_servidor(self):
        while self.conectado:
            try:
                mensaje = self.recibir()
                self.interfaz.manejar_mensaje(mensaje)
            except ConnectionError as error:
                print('Error en escuchar')
                print(f'Error: {error}')

    def recibir(self):
        largo_mensaje = int.from_bytes(self.socket_cliente.recv(4), byteorder = 'little')
        bytes_mensaje = bytearray()
        while len(bytes_mensaje) < largo_mensaje:
            bytes_mensaje.extend(self.socket_cliente.recv(min(64, largo_mensaje - len(bytes_mensaje))))
        mensaje = self.decodificar_mensaje(bytes_mensaje)
        return mensaje

    def enviar(self, mensaje):
        recibido = self.codificar_mensaje(mensaje)
        largo_mensaje = len(recibido).to_bytes(4, byteorder = 'little')
        self.socket_cliente.sendall(largo_mensaje + recibido)

    def codificar_mensaje(self, mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json.JSONDecodeError:
            print("ERROR: No se pudo codificar el mensaje")
            return b""

    def decodificar_mensaje(self, mensaje_bytes):
        try:
            mensaje = json.loads(mensaje_bytes)
            return mensaje
        except json.JSONDecodeError:
            print("ERROR: No se pudo decodificar el mensaje")
            return {}
