from utils import data_json
from random import choice

class Logica:
    def __init__(self, parent):
        self.parent = parent
        self.admin = {}
        self.usuarios = {}

    def validar_login(self, nombre, socket_cliente):
        if len(self.usuarios.keys()) >= data_json("MAX_JUGADORES"):
            return {'comando': 'respuesta_validacion_login',    
                    'estado': 'rechazado','error': 'max_jugadores'}   
        elif 1 <= len(nombre) <= 10  and nombre.isalnum() and nombre not in self.usuarios.keys():
            if len(self.usuarios) == 0:
                self.admin[nombre] = socket_cliente
            self.usuarios[nombre] = socket_cliente
            return {'comando': 'respuesta_validacion_login','estado': 'aceptado',
                'nombre_usuario': nombre,'admin': ''.join(self.admin.keys()),
                'usuarios': ','.join(self.usuarios.keys())}
        return {'comando': 'respuesta_validacion_login','estado': 'rechazado',
            'nombre_usuario': nombre,'error': 'datos invalidos'}

    def procesar_mensaje(self, mensaje, socket_cliente):
        try:
            comando = mensaje['comando']
        except KeyError:
            return {}
        if comando == 'validar_login':
            respuesta = self.validar_login(mensaje['nombre usuario'], socket_cliente)
            self.parent.log(respuesta['nombre_usuario'] + ' intenta ingresar')
            if respuesta['estado'] == 'aceptado':
                self.parent.log(respuesta['nombre_usuario'] + ' logro ingresar')
                listo = True if len(self.usuarios.keys()) >= data_json("MIN_JUGADORES") else False
                for usuario in self.usuarios.keys():   
                    self.parent.enviar_mensaje({'comando': 'actualizar_ventana_espera',
                                                'admin': ''.join(self.admin.keys()),
                                                'nombre_usuario': usuario,
                                                'usuarios': ','.join(self.usuarios.keys()),
                                                'listo': listo}, self.usuarios[usuario])
            else:
                self.parent.log(respuesta['nombre_usuario'] + ' no logro ingresar')

        elif comando == 'desconectar':
            for cliente in self.usuarios.keys():
                if self.usuarios[cliente] == socket_cliente:
                    del self.usuarios[cliente]
                    break
            return None
        elif comando == 'iniciar_partida':
            self.parent.log('Inicia la partida')
            colores = ['AZUL', 'AMARILLA', 'VERDE', 'ROJA']
            colores_ocupados = []
            for usuario in self.usuarios.keys():
                self.parent.log('Jugador ' + usuario)
                color = choice(colores)
                colores_ocupados.append(color)
                colores.remove(color)
            i = 0
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje({'comando': 'iniciar_partida',
                                            'admin': ''.join(self.admin.keys()),
                                            'usuarios': ','.join(self.usuarios.keys()),
                                            'colores': ','.join(colores_ocupados),
                                            'color': colores_ocupados[i]}, self.usuarios[usuario])
                i += 1
            self.iniciar_partida()
            respuesta = {'comando':'nada'}
        elif comando == 'siguiente_turno':
            usuarios = [i for i in self.usuarios.keys()]
            c = usuarios.index(mensaje['turno'])
            if c + 1 == len(usuarios):
                c = 0
            else:
                c += 1
            turno = usuarios[c]
            self.parent.log('Juega ' + turno)
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje({'comando': 'jugar', 'turno': turno},
                                             self.usuarios[usuario])
            respuesta = {'comando':'nada'}
        elif comando == 'actualizar_interfaz':
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje(mensaje, self.usuarios[usuario])
            respuesta = {'comando':'nada'}
        elif comando == 'actualizar_tablero':
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje(mensaje, self.usuarios[usuario])
            respuesta = {'comando':'nada'}
        
        elif comando == 'fin_juego':
            self.parent.log('Finaliza el juego')
            self.parent.log('Ganador: ' + mensaje['ganador'])
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje({'comando': 'fin_juego', 'ganador': mensaje['ganador'],
                                            'usuarios': ','.join(self.usuarios.keys())}, 
                                            self.usuarios[usuario])
            self.usuarios = {}
            self.admin = {}
            respuesta = {'comando':'nada'}

        elif comando == 'cheat':
            self.parent.log('Jugador ' + mensaje['usuario'] + ' utiliza cheat')
            for usuario in self.usuarios.keys():
                self.parent.enviar_mensaje(mensaje, self.usuarios[usuario])
            respuesta = {'comando':'nada'}
        return respuesta

    def iniciar_partida(self):
        usuarios = [i for i in self.usuarios.keys()]
        turno = usuarios[0]
        self.jugar(turno)

    def jugar(self, turno):
        for usuario in self.usuarios.keys():
            self.parent.enviar_mensaje({'comando': 'jugar', 'turno': turno}, 
                                        self.usuarios[usuario])


