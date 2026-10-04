# Clases.py - Parcial 2, Informatica 2.
# En este archivo se encuentran las clases que se implementaran en menu.
# Commit 3: Cambios en los imports.
import io
import os
import unicodedata

import numpy as np
import pandas as pd

#  guardar todas los graficos.

CARPETA_GRAFICOS = "graficos"  

# Primeras funciones para hacer la parte de validacion numerica

# Pedir un entero, repetir hasta que sea valida la entrada. (pedir un minimo y un maximo)
def leer_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Entrada no valida: escriba un numero entero.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"El valor debe ser menor o igual a {maximo}.")
        else:
            return valor

# Para mostrar una lista ennumerada y devolver el elemento elegido.
def elegir_de_lista(opciones, mensaje = "Seleccione una opcion: "):
    opciones = list(opciones)
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion}")
    return opciones[leer_entero(mensaje, 1, len(opciones)) - 1]

# funcion para guardar las graficas como archivos PNG y devolver la ruta.
def guardar_figura(fig, nombre_archivo):
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    ruta = os.path.join(CARPETA_GRAFICOS, nombre_archivo)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    return ruta

# Funcion para que no hallan errores de texto, para que todo este en minusculas y sin tildes.
def _normalizar(texto):
    sin_tildes = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower().strip()

# Para devolver la columna con que coincide con algun candidato (con la normalizacion del texto).
    # Primero busca coincidencia exacta y, si no hay, que el nombre contenga al candidato.
def _buscar_columna(columnas, candidatos):
    normalizadas = {col: _normalizar(col) for col in columnas}
    for candidato in candidatos:
        for col, norm in normalizadas.items():
            if norm == candidato:
                return col
    for candidato in candidatos:
        for col, norm in normalizadas.items():
            if candidato in norm:
                return col
    return None

# Primera clase (base): guarda cualquier archivo cargado (ruta y nombre).
class Archivo:
    def __init__(self, ruta):
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"No existe el archivo: {ruta}")
        self.__ruta = os.path.abspath(ruta)
        self.__nombre = os.path.basename(ruta)
    def verRuta(self):
        return self.__ruta
    def verNombre(self):
        return self.__nombre

# Clase para manejar un archivo CSV de ERP. Hace tabla de pandas con el tiempo, como indice.
class ArchivoCSV(Archivo):
    def __init__(self, ruta):
        Archivo.__init__(self, ruta)
        tabla = pd.read_csv(ruta)
        # la columna de tiempo pasa a ser el índice de las filas
        self.__tabla = tabla.set_index("time_ms")
# Para ver la tabla, canales, condiciones. 
    def verTabla(self):
        return self.__tabla

    def verCondiciones(self):
        return sorted(self.__tabla["condition"].unique())

    def verCanales(self):
        canales = []
        for columna in self.__tabla.columns:
            if columna != "subject" and columna != "condition":
                canales.append(columna)
        return canales

    def __str__(self):
        buffer = io.StringIO()
        self.__tabla.info(buf=buffer)
        return buffer.getvalue() + "\n" + str(self.__tabla.describe())