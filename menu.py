from clases import *

MENU = """
    >>>>>>>>>> MENÚ PRINCIPAL <<<<<<<<<<
    //////////// Archivos ///////////////
    1. Cargar archivo CSV 
    2. Cargar archivo MAT 
    3. Listar archivos cargados
    //////////// CSV ///////////////////
    4. Información del CSV 
    5. Gráficos de una condición 
    6. Diferencia interhemisférica 
    //////////// MAT ///////////////////
    7. Información del MAT
    8. Operar 4 canales 
    9. Promedio y desviación sobre dos ejes
    //////////// Sistema ///////////////
    10. Buscar archivo por nombre
    11. Salir
    """

def main():
    sis = Sistema()
    while True:
        print(MENU)
        menu = leer_entero("Elija por favor la opción que desea usar: ", 1, 11)

        if menu == 1:
            ruta = input("Ruta del archivo CSV: ").strip().strip('"')
            try:
                sis.ingresarArchivo(ArchivoCSV(ruta))
                print("Archivo cargado")
            except Exception as error:
                print("No se pudo cargar el archivo:", error)

        elif menu == 2:
            ruta = input("Ruta del archivo MAT: ").strip().strip('"')
            try:
                sis.ingresarArchivo(ArchivoMAT(ruta))
                print("Archivo cargado")
            except Exception as error:
                print("No se pudo cargar el archivo:", error)

        elif menu == 3:
            archivos = sis.listar()
            if len(archivos) == 0:
                print("No hay archivos cargados")
            for a in archivos:
                print("-", a.verNombre(), "(" + type(a).__name__ + ")")

        elif menu == 4:
            archivo = sis.verArchivo(input("Nombre del archivo CSV (ej. ERP_01.csv): "))
            if isinstance(archivo, ArchivoCSV):
                print(archivo)
            else:
                print("Ese archivo CSV no está cargado")

        elif menu == 5:
            archivo = sis.verArchivo(input("Nombre del archivo CSV (ej. ERP_01.csv): "))
            if isinstance(archivo, ArchivoCSV):
                canales = archivo.verCanales()
                print("Condición:")
                condicion = elegir_de_lista(archivo.verCondiciones())
                print("Canal para el stem y el histograma:")
                canal = elegir_de_lista(canales)
                print("Canal del eje x del scatter:")
                canal_x = elegir_de_lista(canales)
                print("Canal del eje y del scatter:")
                canal_y = elegir_de_lista(canales)
                ruta = archivo.graficar_condicion(condicion, canal, canal_x, canal_y)
                print("Figura guardada en:", ruta)
            else:
                print("Ese archivo CSV no está cargado")

        elif menu == 6:
            archivo = sis.verArchivo(input("Nombre del archivo CSV (ej. ERP_01.csv): "))
            if isinstance(archivo, ArchivoCSV):
                print("Diferencia = canal del hemisferio izquierdo - canal del derecho")
                print("Pares homólogos: FC3-FC4, C3-C4, CP3-CP4 (Fz, FCz y Cz no tienen homólogo)")
                canales = archivo.verCanales()
                print("Canal izquierdo:")
                izquierdo = elegir_de_lista(canales)
                print("Canal derecho:")
                derecho = elegir_de_lista(canales)
                if izquierdo == derecho:
                    print("Debe escoger dos canales distintos")
                else:
                    print(archivo.diferencia_interhemisferica(izquierdo, derecho).head(10))
            else:
                print("Ese archivo CSV no está cargado")

        elif menu == 7:
            archivo = sis.verArchivo(input("Nombre del archivo MAT (ej. Sound_Cue.mat): "))
            if isinstance(archivo, ArchivoMAT):
                print(archivo)
            else:
                print("Ese archivo MAT no está cargado")

        elif menu == 8:
            archivo = sis.verArchivo(input("Nombre del archivo MAT (ej. Sound_Cue.mat): "))
            if isinstance(archivo, ArchivoMAT):
                print("Operación:\n 1- Suma\n 2- Resta (canal 1 - canal 2 - canal 3 - canal 4)\n 3- Multiplicación")
                opcion = leer_entero("Elija por favor la opción que desea usar: ", 1, 3)
                
                if opcion == 1:
                    funcion = suma
                elif opcion == 2:
                    funcion = resta
                else:
                    funcion = multiplicacion
                n = archivo.verCanales()
                canales = []
                for i in range(1, 5):
                    canales.append(leer_entero(f"Canal {i} (1 a {n}): ", 1, n))
                total = archivo.verTotalPuntos()
                print(f"Puntos disponibles: 0 a {total - 1} "
                      f"({archivo.verEnsayos()} ensayos x {archivo.verPuntos()} muestras, {archivo.verFs()} Hz)")
                pmin = leer_entero("Punto mínimo: ", 0, total - 2)
                pmax = leer_entero("Punto máximo: ", pmin + 1, total - 1)
                ruta = archivo.operar_cuatro_canales(funcion, canales, pmin, pmax)
                print("Figura guardada en:", ruta)
            else:
                print("Ese archivo MAT no está cargado")

        elif menu == 9:
            archivo = sis.verArchivo(input("Nombre del archivo MAT (ej. Sound_Cue.mat): "))
            if isinstance(archivo, ArchivoMAT):
                print("Ejes de la matriz 3D: 0 = canales, 1 = muestras, 2 = ensayos")
                eje1 = leer_entero("Primer eje: ", 0, 2)
                eje2 = leer_entero("Segundo eje: ", 0, 2)
                while eje2 == eje1:
                    print("Los dos ejes deben ser diferentes")
                    eje2 = leer_entero("Segundo eje: ", 0, 2)
                ruta = archivo.estadisticas_dos_ejes(eje1, eje2)
                print("Figura guardada en:", ruta)
            else:
                print("Ese archivo MAT no está cargado")

        elif menu == 10:
            texto = input("Nombre (o parte del nombre) del archivo: ")
            encontrados = sis.buscar(texto)
            if len(encontrados) == 0:
                print("No se encontró ningún archivo con ese nombre")
            for a in encontrados:
                print("-", a.verNombre(), "->", a.verRuta())

        elif menu == 11:
            print("Programa finalizado")
            break

if __name__ == "__main__":
    main()