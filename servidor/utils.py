import json
from os.path import join


def data_json(llave):
    ruta = join("parametros.json")
    with open(ruta, "r", encoding="UTF-8") as archivo:
        diccionario_data = json.load(archivo)
    valor = diccionario_data[llave]
    return valor


