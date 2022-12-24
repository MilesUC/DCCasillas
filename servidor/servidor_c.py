import json
import socket
import threading
from logica import Logica


class Servidor_c:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.conectado = False
        self.logica = Logica(self)
        self.id_cliente = 0
        self.log("".center(80, "-"))
        self.log("Inicializando servidor...")
        self.iniciar_servidor()


    def iniciar_servidor(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.conectado = True
        self.log(f'Escuchando desde Host: {self.host} / Puerto: {self.port}')
        self.comenzar_a_aceptar()
        
        
    def comenzar_a_aceptar(self):
        thread_aceptar_cliente = threading.Thread(target = self.aceptar_clientes, daemon = True)
        thread_aceptar_cliente.start()
        

    def aceptar_clientes(self):

        while self.conectado:
            try:
                socket_cliente, _ = self.socket_servidor.accept()
                thread_escuchar_cliente = threading.Thread(target = self.escuchar_cliente, args = (self.id_cliente, socket_cliente))
                thread_escuchar_cliente.start()
                self.id_cliente += 1
            except ConnectionError as error:
                print('La conexión ha fallado')
                print(f'Error: {error}')


    def escuchar_cliente(self, id_cliente, socket_cliente): 
        self.log(f"Comenzando a escuchar al cliente {id_cliente}...")
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
        largo_mensaje = int.from_bytes(socket_cliente.recv(4), byteorder = 'little')
        bytes_mensaje = bytearray()
        while len(bytes_mensaje) < largo_mensaje:
            bytes_mensaje.extend(socket_cliente.recv(min(64, largo_mensaje - len(bytes_mensaje))))
        return self.decodificar_mensaje(bytes_mensaje)
        


    def enviar_mensaje(self, mensaje, socket_cliente):
        recibido = self.codificar_mensaje(mensaje)
        largo_mensaje = len(recibido).to_bytes(4, byteorder = 'little')
        socket_cliente.send(largo_mensaje + recibido)


    def eliminar_cliente(self, id_cliente, socket_cliente):
        try:
            self.log(f"Borrando socket del cliente {id_cliente}.")
            socket_cliente.close()
            self.logica.procesar_mensaje({"comando": "desconectar"}, socket_cliente)
        except KeyError as e:
            self.log(f"ERROR: {e}")

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
        print("|" + mensaje.center(80, " ") + "|")
