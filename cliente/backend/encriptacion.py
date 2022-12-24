#FUNCIONES PARA ENCRIPTAR Y DESENCRIPTAR


def encriptar(mensaje):

    bytes_mensaje = bytes(mensaje, 'utf-8')
    
    A = ''      #Parte A en hexadecimal
    A_s = bytearray()   #Parte A en bytearray
    B = ''      #Parte B en hexadecimal
    B_s = bytearray()   #Parte B en bytearray

    #Ciclo para formar A, A_s, B, B_s

    for i in range(len(bytes_mensaje)):     
        if i % 2 == 0:
            A += hex(bytes_mensaje[i])
            A_s.extend(bytes_mensaje[i].to_bytes(1, 'little'))
        else:
            B += hex(bytes_mensaje[i])
            B_s.extend(bytes_mensaje[i].to_bytes(1, 'little'))

    #Si el largo es par los centrales son los dos bytes centrales
    #Si el largo es impar los centrales son el byte central con el promedio

    if len(A_s) % 2 == 0:  
        centrales_A = A[len(A) // 2 - 4 : len(A) // 2 + 4]
    else:                 
        centrales_A = A[(len(A) - 4) // 2 - 4 : (len(A) - 4) // 2 + 8]

    if len(B_s) % 2 == 0:  
        centrales_B = B[len(B) // 2 - 4 : len(B) // 2 + 4]
    else:                 
        centrales_B = B[(len(B) - 4) // 2 - 4 : (len(B) - 4) // 2 + 8]

    if len(A_s) % 2 == 0:   
        suma_centrales_A = int(centrales_A[:4], 16) + int(centrales_A[4:], 16)
    else:
        suma_centrales_A = int(centrales_A[4:8], 16) + (int(centrales_A[:4], 16) + int(centrales_A[8:], 16)) / 2
        
    if len(B_s) % 2 == 0:
        suma_centrales_B = int(centrales_B[:4], 16) + int(centrales_B[4:], 16)
    else:
        suma_centrales_B = int(centrales_B[4:8], 16) + (int(centrales_B[:4], 16) + int(centrales_B[8:], 16)) / 2

    #Comparacion de bytes centrales

    mensaje_encriptado = bytearray()

    if suma_centrales_A <= suma_centrales_B:
        mensaje_encriptado.extend(b'\x01' + A_s + B_s)
    else:
        mensaje_encriptado.extend(b'\x00' + A_s + B_s)
    
    mensaje_encriptado = str(bytes(mensaje_encriptado))[2:-1]

    return mensaje_encriptado


def desencriptar(mensaje):
    orden = mensaje[3]
    mensaje = mensaje[4:]
    mensaje_desencriptado = ''

    #Formar las partes A y B

    if orden == '1':
        if len(mensaje) % 2 == 0:
            A = mensaje[: len(mensaje) // 2]
            B = mensaje[len(mensaje) // 2 :]
        else:
            A = mensaje[: len(mensaje) // 2 + 1]
            B = mensaje[len(mensaje) // 2 + 1:]

    else:
        if len(mensaje) % 2 == 0:
            A = mensaje[: len(mensaje) // 2]
            B = mensaje[len(mensaje) // 2 :]
        else:
            A = mensaje[: len(mensaje) // 2 + 1]
            B = mensaje[len(mensaje) // 2 + 1:]

    #Formar el mensaje original

    i = 0
    while i < len(A) or i < len(B):
        if i < len(A):
            mensaje_desencriptado += A[i]
        if i < len(B):
            mensaje_desencriptado += B[i]
        i += 1

    return mensaje_desencriptado



