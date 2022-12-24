import socket
import json
from threading import Thread, Lock
from backend.interfaz import Interfaz
from backend.encriptacion import encriptar, desencriptar


class Cliente:
    lock_cliente = Lock()
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
        bytes_mensaje = b''
        chunks_mensaje = int.from_bytes(self.socket_cliente.recv(4), 'little')

        for _ in range(chunks_mensaje):
            bloque = int.from_bytes(self.socket_cliente.recv(4), 'big')
            completo = int.from_bytes(self.socket_cliente.recv(1), 'little')
            cantidad_bytes = int.from_bytes(self.socket_cliente.recv(1),'little')
            bytes_mensaje += self.socket_cliente.recv(cantidad_bytes)

        mensaje = self.decodificar_mensaje(bytes_mensaje)
        try:
            mensaje = desencriptar(mensaje)
        except KeyError:
            pass
        return mensaje
        

    def enviar(self, mensaje):
        try:
            mensaje = encriptar(mensaje)
        except TypeError:
            pass
        bytes_mensaje = self.codificar_mensaje(mensaje)
        mensaje_final = b''
        tamano_chunk = 20
        numero_chunks = len(bytes_mensaje) // tamano_chunk + 1
        bytes_numero_chunks = numero_chunks.to_bytes(4, 'little')
        mensaje_final += bytes_numero_chunks

        for i in range(0, len(bytes_mensaje), tamano_chunk):

            byte_bloque = (i // tamano_chunk).to_bytes(4, 'big')

            largo = min(len(bytes_mensaje) - i, tamano_chunk)
            byte_largo = (largo).to_bytes(1, 'little')

            if largo < tamano_chunk:
                byte_completo = b'\x00'
            else:
                byte_completo = b'\x01'

            mensaje_final += byte_bloque + byte_completo + byte_largo + bytes_mensaje[i:i+largo]
        
        with self.lock_cliente:
            self.socket_cliente.sendall(mensaje_final)

    def codificar_mensaje(self, mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json.JSONDecodeError:
            print('ERROR: No se pudo codificar el mensaje')
            return b''

    def decodificar_mensaje(self, mensaje_bytes):
        try:
            mensaje = json.loads(mensaje_bytes)
            return mensaje
        except json.JSONDecodeError:
            print('ERROR: No se pudo decodificar el mensaje')
            return {}
