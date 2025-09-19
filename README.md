# Análisis del Movimiento de un Tiro Parabólico con OpenCV

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flatfor-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=flatfor-the-badge&logo=Matplotlib&logoColor=black)


Este proyecto corresponde a la primera tarea de la materia **Procesamiento Digital de Imágenes 2025-2** de la **Universidad de Antioquia**.  

El objetivo es realizar un análisis del movimiento parabólico de un objeto captado en video, utilizando técnicas de procesamiento de imágenes y visión por computadora. Para este propósito se emplea la biblioteca **OpenCV**, junto con **NumPy**, **Pandas** y **Matplotlib**, que permiten procesar el video, extraer información y analizar los resultados físicos.

---

## 📌 Modo de uso

El proyecto está compuesto por **tres scripts principales** que deben ejecutarse en orden, ya que cada uno genera los archivos necesarios para el siguiente.

### 01_calcularCentroydes.py
Este script carga el video, lo transforma al espacio de color **HSV** y crea una máscara para segmentar el objeto en movimiento.  
Luego, con la función **`cv2.findContours()`**, detecta el contorno y calcula el **centroide del objeto** en cada frame.  

El resultado se guarda en un archivo llamado **`centroides.txt`**, que contiene la posición `(x, y)` del centroide y su respectiva marca de tiempo.

![example 01_calcularCentroydes.py](https://imgur.com/4eODWHF)

> **Nota**: Para ajustar los valores de la máscara se recomienda usar el script auxiliar [aux_hallarRangosColores.py](#aux_hallarRangosColorespy).

---

### 02_calcularParametrosMovimiento.py
Este script lee el archivo **`centroides.txt`**, realiza la conversión de píxeles a **metros** (basada en el diámetro real del objeto) y calcula la velocidad y aceleración en cada instante.  

El resultado se guarda en el archivo **`parametros_movimiento.txt`**, que contiene las posiciones, velocidades y aceleraciones expresadas en unidades físicas.

![example 02_calcularParametrosMoviento.py](https://imgur.com/kCTDC1u)

> **Nota**: Para estimar el diámetro en píxeles de su objeto en el video, se puede usar el script auxiliar [aux_calcularPosicionPX.py](#aux_calcularPosiciónpy).

---

### 03_dataInterpreter.py
Este script lee los archivos generados (**`centroides.txt`** y **`parametros_movimiento.txt`**) y produce gráficas para interpretar el comportamiento del lanzamiento:  
- Trayectoria en píxeles y en metros.  
- Ajuste parabólico de la trayectoria.  
- Gráficas de velocidad y aceleración en función del tiempo.  
- Ángulo de la velocidad en cada instante.  

Las gráficas se muestran en pantalla y también se guardan en la carpeta **`plots/`**.  
Además, genera un archivo **`resumen_movimiento.csv`** con los datos procesados.

![example 03_dataInterpreter.py](https://imgur.com/PniF7AJ)

---

## ⚙️ Scripts Auxiliares

### aux_hallarRangosColores.py
Herramienta para determinar los rangos de color en el espacio **HSV** que permiten segmentar correctamente el objeto del video.  Muestra en tiempo real la máscara generada y ayuda a ajustar los valores de **Hue**, **Saturation** y **Value**.

### aux_calcularPosición.py
Permite medir en píxeles el tamaño aproximado del objeto en el video. Esto es fundamental para realizar la conversión de píxeles a metros en el análisis físico posterior.

---

## 🛠️ Tecnologías Usadas

- **Python 3.13.7**
  - **opencv-python 4.12.0**  
  - **numpy 2.3.3**  
  - **pandas 2.32**  
  - **matplotlib 3.10.6**

---
