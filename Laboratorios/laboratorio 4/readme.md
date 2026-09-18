# Resumen del Laboratorio 4

## **1. Introducción**

El electrocardiograma, o ECG, es el registro de la actividad eléctrica del corazón a lo largo del tiempo, obtenido mediante electrodos de superficie colocados en la piel. Esta actividad eléctrica se origina en el sistema de conducción cardiaco y se traduce en una series de ondas características (P, complejo QRS y T) que representan, respectivamente, la despolarización auricular, la despolarización ventricular y la repolarización ventricular. Como señal biomédica, el ECG es una señal bioeléctrica, de baja amplitud (en el orden de los milivoltios) y de bajo ancho de banda (aproximadamente 0.05 - 150 Hz).
Desde el un punto de vista clínico, el ECG es una herramienta fundamental ya que permite evaluar el ritmo cardíaco, detectar infartos, arritmias e isquemias, entre otras alteraciones estructurales o funcionales del corazón, de forma no invasiva y de bajo costo. Su estudio es especialmente valioso porque combina fisiología, instrumentación y procesamiento digital de señales.

<p align="center">
  <img src="../../img/ecg_ondas.jpg" alt="Ondas caracteríasticas del ECG" width="350">
</p>

## **2. Objetivos**

- Aprender a configurar correctamente el BITalino (r)evolution para la adquisición de señales cardíacas
- Registrar y observar una señal ECG usando el software OpenSignals
- Reconocer las ondas principales (P, QRS, T) en un registro electrocardiográfico
- Analizar los cambios en la señal EMG bajo diferentes condiciones fisiológicas (Reposo, hiperventilación, hipoventilación, actividad física)

## **3. Materiales y equipo**

| Materiales | Cantidad | Imagen |
|:-----------|:--------:|:------:|
| Software OpenSignals | 1 | <img src="../../img/opensignals.jpg" alt="Software OpenSignals" width="250"> |
| Electrodos descartables | 6 | <img src="../../img/elctrodos.jpg" alt="Electrodos descartables" width="250"> |
| BITalino (r)evolution | 1 | <img src="../../img/bitalino_revolution.jpg" alt="BITalino (r)evolution" width="250"> |
| Cable de 3 electrodos | 1 | <img src="../../img/cable_3_electrodos.jpg" alt="Cable de 3 electrodos" width="250"> |
| Laptop | 1 | <img src="../../img/laptop_ejemplo.jpg" alt="Laptop" width="250"> |

## **4. El electrocardiograma**

El ECG clínico estándar es registrado con 12 derivaciones, lo que hace posible observar la actividad eléctrica cardíaca desde distintos planos. Estas derivaciones son obtenidas usando electrodos colocados en las extremidades y en la región torácica del paciente. De estas 12 derivaciones, 6 corresponden a un plano frontal (DI, DII, DII, aVR, aVL y aVF) y las otras 6 corresponden a un plano horizontal (precordiales V1 a V6). Esta disposición es capaz de brindar una visión completa del proceso de despolarización y repolarización del corazón.

<p align="center">
  <img src="../../img/derivaciones.jpg" alt="12 derivaciones del ECG" width="350">
</p>

## **5. Procedimiento**

1. Primero, se colocaron los electrodos en 3 zonas del cuerpo de la persona a la que se le realizaron las mediciones, en las clavículas derecha e izquierda y en la cresta iliaca izquierda.
2. Posteriormente, se realizó la medición basal de las las derivadas DI, DII, y DIII, intercambiando la colocación de los electrodos para la medición de cada una de las derivadas.
3. Luego, se realizó una simulación de hiperventilación, en el cual la persona inhala la mayor cantidad de aire posible y exhala rápidamente, durante 30 segundos, con descansos de aproximadamente 1 minuto entre medición, para posteriormente realizar la medición de ECG de las 3 derivadas.
4. Después, se realizó una simulación de hipoventilación, la persona inhala la mayor cantidad de aire posible y aguanta la respiración hasta su límite máximo, cuando termina de exhalar se realiza la medición de las 3 derivadas, hubo descansos de aproximadamente 1 minuto entre medición para que la persona se recupere.
5. Finalmente, se realizaron entre 5-10 minutos de actividad aeróbica hasta que la persona llegara a su límite. Tan pronto como terminó la actividad física se tomaron las mediciones de DI, DII y DIII, intercambiando la posición de los electrodos rápidamente entre derivadas para evitar que el ritmo cardíaco se estabilice.

A continuación, se muestran los videos grabados durante la adquisición de las señales ECG en el laboratorio:

- Estado Basal:
  
  | Basal DI | Basal DII | Basal DIII |
  |:-----------:|:--------:|:------:|
  | https://github.com/user-attachments/assets/08c10fd2-b14d-4df7-9ab7-0c01d74b590f | https://github.com/user-attachments/assets/cce29694-c699-446d-b7e8-08ea2e9777f7 | |
  
- Hiperventilación:

  | Hiperventilación |
  |:-----------:|
  | https://github.com/user-attachments/assets/81fd1436-12cd-4a28-8a53-4444337e6627 |
  
- Hipoventilación:

  | Hipoventilación |
  |:-----------:|
  | https://github.com/user-attachments/assets/93acc030-8811-4839-9871-0527c0f1c176 |
  
- Actividad Física Aeróbica:

  | Ejercicio Aeróbico | Medición |
  |:-----------:|:-----------:|
  | https://github.com/user-attachments/assets/fe256214-56a9-44f2-be78-703842bffebb | https://github.com/user-attachments/assets/1aaa9691-7f8b-4eb0-9efb-d8d6023b232c |

## **6. Procesamiento de datos**

Para el procesamiento y análisis de los datos se desarrolló un código en Python utilizando las librerías NumPy, Matplotlib y SciPy. El código permite cargar la señal ECG adquirida, visualizar la señal cruda, aplicar filtros para reducir el ruido y analizar su contenido frecuencial mediante la Transformada Rápida de Fourier (FFT).

El procesamiento se realizó sobre el archivo basal1.txt, correspondiente a la adquisición de la señal ECG en condición basal. A partir de este archivo se obtuvo la señal de interés, se realizó su filtrado y posteriormente se compararon sus características tanto en el dominio temporal como en el dominio frecuencial.

### a) Librerías usadas

Se importaron las librerías necesarias para la manipulación de los datos, visualización de las señales y aplicación de los filtros digitales.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch
from pathlib import Path
```

La librería NumPy se utilizó para el manejo de los datos y para realizar el cálculo de la FFT. Matplotlib permitió generar las gráficas de las señales en el dominio temporal y frecuencial. Por su parte, SciPy proporcionó las funciones necesarias para implementar los filtros pasa-banda y notch. Finalmente, Path se utilizó para organizar la ubicación de los archivos y almacenar las gráficas generadas en una carpeta de resultados.

### b) Cargar y organizar los datos

Se cargaron los datos de la adquisición que obtuvimos durante el laboratorio.

```python
with open("basal1.txt", "r") as f:
    lineas = f.readlines()

datos_limpios = [line.strip().split() for line in lineas if not line.startswith("#")]
datos = np.array(datos_limpios, dtype=float)
```
### c) Aplicación de filtros
La señal ECG puede contener diferentes componentes de ruido e interferencias eléctricas que dificultan su análisis. Por este motivo, se aplicaron dos filtros: un filtro pasa-banda y un filtro notch.

Filtro Pasa Banda

Se implementó un filtro pasa-banda Butterworth de cuarto orden con frecuencias de corte de 0.5 Hz y 40 Hz. Este filtro permite conservar las componentes de frecuencia comprendidas dentro de dicho intervalo y atenuar aquellas que se encuentran fuera de él.

```python
def filtro_pasabanda(senal, fs, frec_baja=0.5, frec_alta=40.0, orden=4):
    nyquist = 0.5 * fs
    bajo = frec_baja / nyquist
    alto = frec_alta / nyquist
    b, a = butter(orden, [bajo, alto], btype="band")
    return filtfilt(b, a, senal)
```
Para el diseño del filtro se utilizó la frecuencia de Nyquist, definida como:
F_nyquist = F_muestreo / 2
Y como la F_muestreo = 1000Hz, entonces la F_nyquist = 500Hz
Las frecuencias de corte del filtro se normalizaron respecto a la frecuencia de Nyquist antes de diseñar el filtro Butterworth.

El filtro se aplicó mediante la función filtfilt(), que realiza el filtrado en ambas direcciones de la señal. De esta manera, se evita introducir un desplazamiento de fase significativo en la señal resultante.

Filtro Notch

Después del filtro pasa-banda se aplicó un filtro notch centrado en 60 Hz, utilizando un factor de calidad (Q=30).

```python
def filtro_notch(senal, fs, frec_notch=60.0, Q=30.0):
    nyquist = 0.5 * fs
    w0 = frec_notch / nyquist
    b, a = iirnotch(w0, Q)
    return filtfilt(b, a, senal)
```
El filtro notch fue utilizado para reducir la interferencia localizada alrededor de los 60 Hz, asociada principalmente con la red eléctrica.

El parámetro (Q = 30), denominado factor de calidad, determina el ancho de la banda de rechazo alrededor de la frecuencia central.

Aplicación de los filtros:
```python
ecg_filtrado = filtro_pasabanda(ecg, fs, 0.5, 40)
ecg_filtrado = filtro_notch(ecg_filtrado, fs, 60)
```
De esta manera, primero se atenúan las componentes de muy baja y alta frecuencia mediante el filtro pasa-banda y posteriormente se reduce específicamente la interferencia alrededor de los 60 Hz mediante el filtro notch

### d) Ploteo de señales

### Estado basal

| Tipo                 |  Señal original - 1ra derivada  |  Señal filtrada - 1ra derivada  |
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |  <img src="../../img/ECG_cruda.png" width="867" alt="ECG_cruda">  |  <img src="../../img/ECG_cruda_filtrada.png" width="867" alt="ECG_cruda_filtrada">  |
| FFT                |  <img src="../../img/ECG_FFT_CRUDA.png" width="867" alt="ECG">  |  <img src="../../img/ECG_cruda_FFT_filtrada.png" width="867" alt="ECG">  |
| FFT (dB)              |  <img src="../../img/ECG_FFT_CRUDA_EN_dB.png" width="867" alt="ECG">  |  <img src="../../img/ECG_FFT_CRUDA_EN_dB_filtrada.png" width="867" alt="ECG">  |


| Tipo                 | Señal original - 2da derivada| Señal filtrada - 2da derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |  <img src="../../img/ECG_cruda (1).png" width="867" alt="ECG">  |  <img src="../../img/ECG_cruda_filtrada (1).png" width="867" alt="ECG">  |
| FFT                |  <img src="../../img/ECG_FFT_CRUDA (1).png" width="867" alt="ECG">  |  <img src="../../img/ECG_cruda_FFT_filtrada (1).png" width="867" alt="ECG">  |
| FFT (dB)              |  <img src="../../img/ECG_FFT_CRUDA_EN_dB (1).png" width="867" alt="ECG">  |  <img src="../../img/ECG_FFT_CRUDA_EN_dB_filtrada (1).png" width="867" alt="ECG">  |

| Tipo                 | Señal original - 3ra derivada| Señal filtrada - 3ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |  <img src="../../img/ECG_cruda (2).png" width="867" alt="ECG">  |  <img src="../../img/ECG_cruda_filtrada (2).png" width="867" alt="ECG">  |
| FFT                |  <img src="../../img/ECG_FFT_CRUDA (2).png" width="867" alt="ECG">  |  <img src="../../img/ECG_cruda_FFT_filtrada (2).png" width="867" alt="ECG">  |
| FFT (dB)              |  <img src="../../img/ECG_FFT_CRUDA_EN_dB (2).png" width="867" alt="ECG">  |  <img src="../../img/ECG_FFT_CRUDA_EN_dB_filtrada (2).png" width="867" alt="ECG">  |

### Estado hiperventilación
| Tipo                 | Señal original - 1ra derivada| Señal filtrada - 1ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |  <img src="../../img/ECG_hiperventilación_cruda.png" width="867" alt="ECG">  |  <img src="../../img/ECG_hiperventilación_filtrada.png" width="867" alt="ECG">  |
| FFT                |  <img src="../../img/ECG_hiperventilación_FFT_CRUDA.png" width="867" alt="ECG">  |  <img src="../../img/ECG_hiperventilación_FFT_filtrada.png" width="867" alt="ECG">  |
| FFT (dB)              |  <img src="../../img/ECG_hiperventilación_CRUDA_EN_dB.png" width="867" alt="ECG">  |  <img src="../../img/ECG_hiperventilación_CRUDA_EN_dB_filtrada.png" width="867" alt="ECG">  |

| Tipo                 | Señal original - 2da derivada| Señal filtrada - 2da derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

| Tipo                 | Señal original - 3ra derivada| Señal filtrada - 3ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

### Estado hipoventilación
| Tipo                 | Señal original - 1ra derivada| Señal filtrada - 1ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

| Tipo                 | Señal original - 2da derivada| Señal filtrada - 2da derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

| Tipo                 | Señal original - 3ra derivada| Señal filtrada - 3ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

### Actividad aerobica
| Tipo                 | Señal original - 1ra derivada| Señal filtrada - 1ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

| Tipo                 | Señal original - 2da derivada| Señal filtrada - 2da derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |

| Tipo                 | Señal original - 3ra derivada| Señal filtrada - 3ra derivada|
| ------------------------------- | -------------------------- | -------------------------- |
| Señal                |    |    |
| FFT                |    |    |
| FFT (dB)              |    |    |
