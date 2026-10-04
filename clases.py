# Clases.py - Parcial 2, Informatica 2.
# En este archivo se encuentran las clases que se implementaran en menu.
import io
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import scipy.io as sio

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
# Graficar cada condicion.
    def graficar_condicion(self, condicion, canal, canal_x, canal_y):
        datos = self.__tabla[self.__tabla["condition"] == condicion]
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 2, 3)
        ax3 = fig.add_subplot(2, 2, 4)
        fig.suptitle(f"{self.verNombre()} - condición {condicion}")

# Stem con una línea roja en t = 0 ms (sin marcadores y con líneas finas,
# son muchas muestras y si no se vuelve una mancha)
        marcas, lineas, base = ax1.stem(datos.index, datos[canal], markerfmt=" ", basefmt="k-")
        lineas.set_linewidth(0.4)
        ax1.axvline(0, color="red", linestyle="--")
        ax1.set_title(f"Señal del canal {canal}")
        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Voltaje (µV)")

# Histograma del mismo canal
        ax2.hist(datos[canal], bins=30, edgecolor="black")
        ax2.set_title(f"Histograma del canal {canal}")
        ax2.set_xlabel("Voltaje (µV)")
        ax2.set_ylabel("Frecuencia")
        
# Scatter entre dos canales
        ax3.scatter(datos[canal_x], datos[canal_y], s=10, alpha=0.5)
        ax3.set_title(f"{canal_x} vs {canal_y}")
        ax3.set_xlabel(f"{canal_x} (µV)")
        ax3.set_ylabel(f"{canal_y} (µV)")

        fig.tight_layout()
        ruta = guardar_figura(fig, f"{os.path.splitext(self.verNombre())[0]}_cond{condicion}_{canal}")
        plt.show()
        plt.close(fig)
        return ruta
    
    def diferencia_interhemisferica(self, canal_izq, canal_der):
# Canal del hemisferio izquierdo menos derecho.
        nueva = "Dif_" + canal_izq + "-" + canal_der
        self.__tabla[nueva] = self.__tabla[canal_izq] - self.__tabla[canal_der]
        return self.__tabla[["condition", canal_izq, canal_der, nueva]]

# Sistema final para guardar y buscar archivos.
class Sistema:
    def __init__(self):
        self.__archivos = {}

    def ingresarArchivo(self, a):
        self.__archivos[a.verNombre()] = a

    def verArchivo(self, nombre):
        return self.__archivos.get(nombre, False)

    def listar(self):
        return list(self.__archivos.values())

    def buscar(self, texto):
        encontrados = []
        for nombre in self.__archivos:
            if texto.lower() in nombre.lower():
                encontrados.append(self.__archivos[nombre])
        return encontrados
# Clase para cargar y manipular un archivo Mat
class ArchivoMAT(Archivo):
    def __init__(self, ruta):
        Archivo.__init__(self, ruta)
        self.__fs = 250
# whosmat da variable, dimensiones y tipo sin cargar los datos
        self.__info = sio.whosmat(ruta)
        self.__variable = ""
        for nombre, forma, tipo in self.__info:
            if len(forma) == 3:
                self.__variable = nombre
        if self.__variable == "":
            raise ValueError("El .mat no tiene ninguna variable de 3 dimensiones")
        self.__matriz = sio.loadmat(ruta)[self.__variable]

    def verFs(self):
        return self.__fs

    def verMatriz3D(self):
        return self.__matriz

    def verCanales(self):
        return self.__matriz.shape[0]

    def verPuntos(self):
        return self.__matriz.shape[1]

    def verEnsayos(self):
        return self.__matriz.shape[2]

    def verTotalPuntos(self):
        return self.__matriz.shape[1] * self.__matriz.shape[2]

    def convertirA2D(self):
        # (canales, puntos, ensayos) -> (canales, puntos * ensayos), un ensayo tras otro
        canales, puntos, ensayos = self.__matriz.shape
        return np.reshape(self.__matriz, (canales, puntos * ensayos), order="F")

    def __str__(self):
        tabla = pd.DataFrame(self.__info, columns=["Variable", "Dimensiones", "Tipo"])
        return tabla.to_string(index=False) + "\nVariable usada: " + self.__variable

# Funcion para configurar de manera correcta las graficas que se hacen.

    def estadisticas_dos_ejes(self, eje1, eje2):
        promedio = np.mean(self.__matriz, axis=(eje1, eje2), dtype=np.float64)
        desviacion = np.std(self.__matriz, axis=(eje1, eje2), dtype=np.float64)
        print("Forma del promedio:", promedio.shape)
        print("Forma de la desviación estándar:", desviacion.shape)

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.boxplot([promedio, desviacion])
        ax.set_xticks([1, 2], ["Promedio", "Desviación estándar"])
        ax.set_title(f"{self.verNombre()} - ejes {eje1} y {eje2}")
        ax.set_xlabel("Estadístico")
        ax.set_ylabel("Voltaje (µV)")

        ruta = guardar_figura(fig, f"{os.path.splitext(self.verNombre())[0]}_boxplots_ejes_{eje1}_{eje2}")
        plt.show()
        plt.close(fig)
        return ruta
# Funcion para operar los canales.

    def operar_cuatro_canales(self, funcion, canales, pmin, pmax):
        # canales: 4 números de canal como los ve el usuario.
        # pmin y pmax: puntos de la matriz convertida a 2D (ambos incluidos).
        matriz2d = self.convertirA2D()
        senales = matriz2d[[c - 1 for c in canales], pmin:pmax + 1].astype(np.float64)
        resultado = funcion(senales[0], senales[1], senales[2], senales[3])
        tiempo = np.arange(pmin, pmax + 1) / self.__fs

        fig = plt.figure(figsize=(11, 8))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        fig.suptitle(f"{self.verNombre()} - puntos {pmin} a {pmax}")

        for i in range(4):
            ax1.plot(tiempo, senales[i], label=f"Canal {canales[i]}")
        ax1.set_title("Canales seleccionados")
        ax1.set_xlabel("Tiempo (s)")
        ax1.set_ylabel("Voltaje (µV)")
        ax1.legend()

        ax2.plot(tiempo, resultado, color="black")
        ax2.set_title(f"Resultado: {funcion.__name__} de los canales {canales}")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Amplitud")

        fig.tight_layout()
        ruta = guardar_figura(fig, f"{os.path.splitext(self.verNombre())[0]}_{funcion.__name__}_{pmin}-{pmax}")
        plt.show()
        plt.close(fig)
        return ruta