import json
import socket
from threading import Thread, Lock
from logica import Logica
from encriptacion import encriptar, desencriptar


class Servidor:
    lock_servidor = Lock()
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.conectado = False
        self.logica = Logica(self)
        self.id_cliente = 0
        self.log(''.center(80, '-'))
        self.log('Inicializando servidor...')
        self.iniciar_servidor()


    def iniciar_servidor(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.conectado = True
        self.log(f'Escuchando desde Host: {self.host} / Puerto: {self.port}')
        self.comenzar_a_aceptar()
        
        
    def comenzar_a_aceptar(self):
        thread_aceptar_cliente = Thread(target = self.aceptar_clientes, daemon = True)
        thread_aceptar_cliente.start()
        

    def aceptar_clientes(self):

        while self.conectado:
            try:
                socket_cliente, _ = self.socket_servidor.accept()
                thread_escuchar_cliente = Thread(target = self.escuchar_cliente, args = (self.id_cliente, socket_cliente))
                thread_escuchar_cliente.start()
                self.id_cliente += 1
            except ConnectionError as error:
                print('La conexión ha fallado')
                print(f'Error: {error}')


    def escuchar_cliente(self, id_cliente, socket_cliente): 
        self.log(f'Comenzando a escuchar al cliente {id_cliente}...')
        try:
            while True:
                mensaje = self.recibir_mensaje(socket_cliente)
                if mensaje != '':
                    respuesta = self.logica.procesar_mensaje(mensaje, socket_cliente)
                    if respuesta:
                        self.enviar_mensaje(respuesta, socket_cliente)
                    else:
                        raise ConnectionError
                else:
                    raise ConnectionError
        except ConnectionError as error:
            print('Error de conexión')
            self.eliminar_cliente(id_cliente, socket_cliente)


    def recibir_mensaje(self, socket_cliente):
        bytes_mensaje = b''
        chunks_mensaje = int.from_bytes(socket_cliente.recv(4), byteorder = 'little')
        
        for _ in range(chunks_mensaje):
            bloque = int.from_bytes(socket_cliente.recv(4), byteorder = 'big')
            completo = int.from_bytes(socket_cliente.recv(1), byteorder = 'little')
            cantidad_bytes = int.from_bytes(socket_cliente.recv(1), byteorder = 'little')
            bytes_mensaje += socket_cliente.recv(cantidad_bytes)
            
        mensaje = self.decodificar_mensaje(bytes_mensaje)
        try:
            mensaje = desencriptar(mensaje)
        except KeyError:
            pass
        return mensaje
        
    def enviar_mensaje(self, mensaje, socket_cliente):
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
            
        socket_cliente.send(mensaje_final) 

    def eliminar_cliente(self, id_cliente, socket_cliente):
        try:
            self.log(f'Borrando socket del cliente {id_cliente}.')
            socket_cliente.close()
            self.logica.procesar_mensaje({'comando': 'desconectar'}, socket_cliente)
        except KeyError as e:
            self.log(f'ERROR: {e}')

    def codificar_mensaje(self, mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json-json.JSONDecodeError:
            print('No se pudo codificar el mensaje')
            return b''


    def decodificar_mensaje(self, mensaje_bytes):
        try:
            mensaje = json.loads(mensaje_bytes)
            return mensaje
        except json.JSONDecodeError:
            print('No se pudo decodificar el mensaje')
            return ''

    def log(self, mensaje: str):
        print('|' + mensaje.center(80, ' ') + '|')
