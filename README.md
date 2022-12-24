# Tarea X: DCCasillas :school_satchel:


## Consideraciones generales :octocat:

EL juego funciona correctamente en general, se ingresan los clientes al servidor, inicia el juego, avanza el juego por turnos y cuando un 
jugador tiene 2 fichas en la meta se declara ganador.

Importante: El programa únicamente contiene un problema con la codificación solicitada en el enunciado ya que se bugea luego de unos turnos lo que sospecho
que es porque el programa demora en codificar y decodificar una gran cantidad de mensajes enviados entre cliente y servidor, por ello para
temas de revisión de juego recomiendo corregir el archivo original. Sin embargo, para temas de revisión de la codificación se deben hacer dos cambios, 
en main.py de Servidor se debe comentar la línea 9 y descomentar la 10, y en main.py de Cliente se debe comentar la línea 13 y descomentar la 14 para 
comprobar que el envío de bytes está correcto (estas líneas están indicadas en el archivo). Y por esta razón es que existen dos archivos servidor y 
dos archivos cliente.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 23 pts (18%)
##### ✅ Protocolo <Se implementa correctamente todo el protocolo TCP de networking\>
##### ✅ Correcto uso de sockets <Se utilizan correctamente los sockets de servidor y cliente\>
##### ✅ Conexión <La conexión es robusta y a prueba de errores\>
##### ✅ Manejo de clientes <El servidor ingresa correctamente clientes y se comunica con ellos\>
#### Arquitectura Cliente - Servidor: 31 pts (25%)
##### ✅ Roles <Bien definido el rol de cliente y servidor\>
##### ✅ Consistencia <Relación robusta entre cliente y servidor\>
##### ✅ Logs <Se implementan logs que informan mediante el cmd los sucesos de la partida\>
#### Manejo de Bytes: 26 pts (21%)
##### ✅ Codificación <Se realiza correctamente la codificación\>
##### ✅ Decodificación <Se realiza correctamente la decodificación\>
##### 🟠 Encriptación <Se realiza correctamente la encriptación pero con str y no bytes\>
##### 🟠 Desencriptación <Se realiza correctamente la desencriptación pero con str y no bytes\>
##### ✅ Integración <Se integra la codificación, decodificación entre mensajes\>
#### Interfaz: 23 pts (18%)
##### ✅ Ventana inicio <Se crea correctamente la ventana de inicio para cada cliente\>
##### ✅ Sala de Espera <Se crea y actualiza correctamente la ventana de inicio para cada cliente\>
##### ✅ Sala de juego <Se crea y actualiza correctamente la ventana de juego para cada cliente\>
##### ✅ Ventana final <Se muestra correctamente la ventana de postjuego para cada cliente\>
#### Reglas de DCCasillas: 18 pts (14%)
##### ✅ Inicio del juego <Se implementa correctamente el inicio y juego por turnos\>
##### ✅ Ronda <Se implementa correctamente el cambio de turnos\>
##### ✅ Termino del juego <Ocurre correctamente el término de juego cuando un cliente \>
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON) <Se implementan correctamente los archivos json\>
#### Bonus: 5 décimas máximo
##### ✅ Cheatcode <Se implementa correctamente el cheatcode, se debe tipear la palabra en orden\>
##### ❌ Turnos con tiempo <No se implementa\>
##### ✅ Rebote <Se implementa correctamente el rebote\>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` para el servidor
El módulo principal de la tarea a ejecutar es  ```main.py``` para los clientes

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```
2. ```json```: ```dumps```, ```loads```
3. ```PyQt5.QtCore```: ```pyqtSignal```, ```QObject```, ```QTimer```, ```QRect```, ```QUrl```
4. ```PyQt5.QtWidgets```: ```QApplication```, ```QWidget```, ```QLabel```, ```QVBoxLayout```, ```QHBoxLayout```, ```QPushButton```
5. ```PyQt5.QtGui```: ```QPixmap```, ```QFont```, ```QIcon```
6. ```PyQt5```: ```uic```
7. ```random```: ```randint()```, ```choice()```
8. ```os``` : ```path```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ``` parametros```: Contiene los parámetros utilizados en el programa
2. ``` utils```: ```data_json```
3. ``` servidor.servidor ```: ```Servidor```
4. ``` servidor.logica ```: ```Logica```
5. ``` servidor.encriptacion```: ``` encriptar```, ``` desencriptar```
6. ``` cliente.backend.cliente```: ``` Cliente```
7. ``` cliente.backend.interfaz ```: ```Interfaz```
8. ``` cliente.frontend.ventana_login```: ``` VentanaLogin```
9. ``` cliente.frontend.ventana_espera```: ``` VentanaEspera```
10. ``` cliente.frontend.ventana_juego```: ``` VentanaJuego```
11. ``` cliente.frontend.ventana_postjuego```: ``` VentanaPostJuego```
12. ``` cliente.encriptacion```: ``` encriptar```, ``` desencriptar```


