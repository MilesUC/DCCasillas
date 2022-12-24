import sys
from servidor import Servidor
from servidor_c import Servidor_c
from utils import data_json

if __name__ == '__main__':
    HOST = data_json('HOST')
    PORT = data_json('PORT')
    servidor = Servidor_c(HOST, PORT)     #Comentar para revisar codificacion
    #servidor = Servidor(HOST, PORT)      #Descomentar para revisar codificacion

    try:
        while True:
            input('[Presione Ctrl+C para cerrar]'.center(82, '+') + '\n')
    except KeyboardInterrupt:
        print('\n\n')
        print('Cerrando servidor...'.center(80, ' '))
        print(''.center(82, '-'))
        print(''.center(82, '-') + '\n')
        servidor.socket_servidor.close()
        sys.exit()