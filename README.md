# Parcial 2 - Informática 2

Se presenta el desarrollo del trabajo solicitado comon proyecto para el segundo parcial.se desarollo el sistema exploratorio en Python para procesar, analizar y graficar señales biomédicas. El programa permite trabajar con archivos CSV (relacionados a eventos - ERP en pacientes con esquizofrenia) y archivos MAT (registros de EEG bajo estímulos sensoriales).

# Hecho por:
- Carlos Daniel Duitama Sora.
- Luna Daniela Tapia Guerrero.

# Requisitos e Instalación
Para que el programa funcione correctamente, necesitas instalar las librerías requeridas (numpy, pandas, scipy y matplotlib). Puedes instalarlas todas de una vez ejecutando el siguiente comando en tu terminal:
    pip install -r requirements.txt
  # Este archivo se encuentra guardado en la carpeta.

# Cómo usar el programa
1. Se necesita tener instalados los archivos CSV y en todo caso los archivos .Mat .
2. Una vez subidos los archivos ejecutar el codigo principal desde la consola:
    python menu.py

3. Sigue las instrucciones del menú interactivo. El sistema te pedirá ingresar la ruta del archivo que quieres cargar y luego podrás elegir opciones para ver información estadística, operar canales o generar gráficas.
4. **Nota:** Todas las figuras y gráficas que generes se guardarán automáticamente en la carpeta (graficos/) que el programa crea por defecto.

# Estructura del proyecto
- menu.py: Es el script principal que contiene la interfaz de usuario en consola.
- clases.py: Contiene toda la lógica detras del funcionamiento (clases, setters y getters). Aquí definimos las clases Archivo, ArchivoCSV, ArchivoMAT y Sistema, además de las funciones encargadas de hacer los cálculos y exportar los gráficos.
- .gitignore: Se añadio para ignorar archivos temporales, entornos virtuales y los archivos pesados .mat, para que no suceda justamente lo que el profesor repitio tanto en el grupo.

## Esperamos sea de su agrado :) ##