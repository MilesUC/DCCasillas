import sys
from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from backend.cliente_c import Cliente_c
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    
    try:
        app = QApplication(sys.argv)
        cliente = Cliente_c(HOST, PORT)         #Comentar para revisar codificacion
        #cliente = Cliente(HOST, PORT)          #Descomentar para revisar codificacion

        sys.exit(app.exec_())

    except ConnectionError as e:
        print("Ocurrió un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.salir()
        sys.exit()