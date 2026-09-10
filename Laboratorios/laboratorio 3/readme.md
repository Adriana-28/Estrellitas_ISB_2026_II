# Resumen del Laboratorio 3

## **1. Introducción**

La electromiografía (EMG) es un método de registro biomédico que hace posible la medición de la actividad eléctrica producida por los músculos esqueléticos mientras estos se contraen. Esta actividad eléctrica se produce en los potenciales de acción que se propagan por las fibras musculares cuando reciben activación de las neuronas motoras del sistema nervioso. Para la obtención de dichas señales fisiológicas se hace uso del BITalino, el cual es un dispositivo que permite recolectar datos biomédicos (EMG, EEG, ECG, etc). Además, se hace uso del software OpenSignals (r)evolution para poder visualizar en tiempo real las señales obtenidas, guardarlas y exportarlas.
[Imágen aquí]

## **2. Objetivos**

- Aprender lo básico acerca de recolección de señales fisiológicas usando el BITalino
- Visualizar en tiempo real, almacenar y exportar señales biomédicas usando OpenSignals (r)evolution
- Aplicar filtros para procesar y mejorar la calidad de las señales recolectadas
- Analizar e interpretar las señales obtenidas

## **3. Materiales y equipos**

| Materiales | Cantidad | Imagen |
|:-----------|:--------:|:------:|
| Software OpenSignals | 1 | <img src="../../img/opensignals.jpg" alt="Software OpenSignals" width="250"> |
| Electrodos descartables | 6 | <img src="../../img/elctrodos.jpg" alt="Electrodos descartables" width="250"> |
| BITalino (r)evolution | 1 | <img src="../../img/bitalino_revolution.jpg" alt="BITalino (r)evolution" width="250"> |
| Cable de 3 electrodos | 1 | <img src="../../img/cable_3_electrodos.jpg" alt="Cable de 3 electrodos" width="250"> |
| Laptop | 1 | <img src="../../img/laptop_ejemplo.jpg" alt="Laptop" width="250"> |

## **4. Procedimiento**



## **5. Resultados**

En esta sección se presentan los resultados obtenidos a partir de las señales de electromiografía superficial (EMG) registradas durante las diferentes condiciones de actividad muscular. El procesamiento permitió visualizar las señales tanto en el dominio temporal como en el dominio frecuencial, con el propósito de facilitar la comparación de la actividad eléctrica muscular entre las distintas condiciones evaluadas.

Las señales fueron procesadas mediante una serie de etapas que incluyeron la eliminación de la componente continua, filtrado pasabanda, rectificación de la señal y análisis frecuencial.

El procedimiento se aplicó a los registros obtenidos para el **flexor radial del carpo** y las **fibras descendentes del trapecio**, considerando las condiciones de reposo, movimiento leve sin oposición y movimiento fuerte con oposición.

### **5.1. Procesamiento y visualización de las señales EMG**

Para el procesamiento de las señales se emplearon herramientas de Python para el manejo de los datos, filtrado digital, análisis espectral y generación de las gráficas. A partir de los registros obtenidos durante la adquisición, se realizó el procesamiento de cada señal siguiendo una secuencia común para todas las condiciones experimentales.

### a) Importación de librerías

En primer lugar, se cargaron las librerías necesarias para realizar las operaciones matemáticas, el procesamiento de señales y la generación de las representaciones gráficas.

```python
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch, iirnotch
```

### b) Selección y ubicación del registro

Para cada análisis se seleccionó el archivo correspondiente a la señal EMG que se deseaba procesar.

```python
from pathlib import Path

carpeta = Path(__file__).resolve().parent

ruta = carpeta / "basalflexocarpiradiales1.txt"

carpeta_resultados = carpeta / "resultados"
carpeta_resultados.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo:\n{ruta}\n"
        "Verifica que el nombre esté escrito correctamente."
    )
```


### c) Definición de los filtros

Para reducir las componentes no deseadas presentes en las señales se implementaron dos tipos de filtros. El primero corresponde a un filtro pasabanda entre **20 y 450 Hz**, utilizado para conservar el intervalo de frecuencias de interés de la señal EMG. Posteriormente, se aplicó un filtro Notch centrado en **60 Hz**, destinado a reducir la interferencia proveniente de la red eléctrica.

```python
def filtro_pasabanda(
    señal,
    frecuencia_muestreo,
    frecuencia_baja=20.0,
    frecuencia_alta=450.0,
    orden=4
):
    nyquist = frecuencia_muestreo / 2

    frecuencia_baja_normalizada = frecuencia_baja / nyquist
    frecuencia_alta_normalizada = frecuencia_alta / nyquist

    b, a = butter(
        orden,
        [frecuencia_baja_normalizada, frecuencia_alta_normalizada],
        btype="bandpass"
    )

    return filtfilt(b, a, señal)


def filtro_notch(
    señal,
    frecuencia_muestreo,
    frecuencia_notch=60.0,
    Q=30.0
):
    nyquist = frecuencia_muestreo / 2
    frecuencia_normalizada = frecuencia_notch / nyquist

    b, a = iirnotch(frecuencia_normalizada, Q)

    return filtfilt(b, a, señal)
```

### d) Carga y caracterización inicial de la señal

Los datos almacenados en el archivo fueron cargados mediante `numpy`. Debido a que la señal EMG se encuentra en la última columna del archivo generado durante la adquisición, esta columna fue seleccionada para realizar el procesamiento.

La frecuencia de muestreo utilizada fue de **1000 Hz**, a partir de la cual se construyó el vector temporal correspondiente al registro.

```python
datos = np.loadtxt(ruta, comments="#")

print("Dimensiones del archivo:", datos.shape)
print("Número de columnas:", datos.shape[1])

emg = datos[:, -1].astype(float)

fs = 1000

tiempo = np.arange(len(emg)) / fs

print("Número de muestras:", len(emg))
print("Duración:", round(len(emg) / fs, 2), "segundos")
print("Valor mínimo:", np.min(emg))
print("Valor máximo:", np.max(emg))
```

Además de obtener la señal, se verificaron características básicas del registro, como el número de muestras, duración, valor mínimo y valor máximo.

### e) Eliminación de la componente continua y filtrado

Antes de aplicar los filtros, se eliminó la componente continua de la señal mediante la resta de su valor medio. Posteriormente, se aplicó el filtro pasabanda de 20 a 450 Hz y, finalmente, el filtro Notch de 60 Hz.

```python
emg_sin_media = emg - np.mean(emg)

emg_filtrada = filtro_pasabanda(emg_sin_media, fs)

emg_filtrada = filtro_notch(
    emg_filtrada,
    fs,
    frecuencia_notch=60.0,
    Q=30.0
)
```

Con este procesamiento se obtuvo una señal con menor presencia de componentes continuas e interferencias fuera del rango de interés.

### f) Rectificación de la señal

Después del filtrado se realizó la rectificación de la señal EMG mediante el valor absoluto de cada muestra. Esta transformación permite expresar todas las variaciones de la señal en valores positivos, facilitando la visualización de la magnitud de la actividad muscular.

```python
emg_rectificada = np.abs(emg_filtrada)
```

### g) Representación de la señal original

La primera representación corresponde a la señal EMG directamente obtenida durante la adquisición, sin aplicar el procesamiento descrito anteriormente.

```python
plt.figure(figsize=(12, 4))
plt.plot(tiempo, emg, color="#00008B", linewidth=0.5)
plt.title("Señal EMG original – Flexor radial del carpo en reposo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Valor digital (ADC)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    carpeta_resultados / "antebrazo_reposo_original.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

### h) Representación de la señal filtrada

A continuación, se generó la representación temporal de la señal después de eliminar la componente continua y aplicar los filtros pasabanda y Notch.

```python
plt.figure(figsize=(12, 4))
plt.plot(tiempo, emg_filtrada, color="#006400", linewidth=0.5)
plt.title("Señal EMG filtrada – Flexor radial del carpo en reposo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud filtrada (ADC)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    carpeta_resultados / "antebrazo_reposo_filtrada.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

### i) Representación de la señal rectificada

La señal filtrada también fue rectificada mediante el cálculo de su valor absoluto. La gráfica resultante permite visualizar la magnitud de la actividad eléctrica sin considerar la polaridad de la señal.

```python
plt.figure(figsize=(12, 4))
plt.plot(tiempo, emg_rectificada, color="#D97706", linewidth=0.5)
plt.title("Señal EMG rectificada – Flexor radial del carpo en reposo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud absoluta (ADC)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    carpeta_resultados / "antebrazo_reposo_rectificada.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

### j) Densidad espectral de potencia mediante Welch

Para evaluar la distribución de la potencia de la señal en función de la frecuencia se utilizó el método de Welch. El tamaño del segmento se estableció como el menor valor entre 1024 muestras y la cantidad total de muestras disponibles.

```python
segmento = min(1024, len(emg_filtrada))

frecuencias, psd = welch(
    emg_filtrada,
    fs=fs,
    nperseg=segmento
)

plt.figure(figsize=(12, 4))
plt.semilogy(frecuencias, psd, color="purple")
plt.title(
    "Densidad espectral de potencia – "
    "Flexor radial del carpo en reposo"
)
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("PSD (ADC²/Hz)")
plt.xlim(0, 500)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    carpeta_resultados / "antebrazo_reposo_welch.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

### k) Espectro de frecuencias mediante FFT

Finalmente, se obtuvo el espectro de frecuencias utilizando la Transformada Rápida de Fourier (FFT). En este caso, la amplitud fue normalizada de acuerdo con el número total de muestras para facilitar la interpretación de los componentes frecuenciales.

```python
numero_muestras = len(emg_filtrada)

fft_valores = np.fft.rfft(emg_filtrada)
fft_frecuencias = np.fft.rfftfreq(
    numero_muestras,
    d=1/fs
)

amplitud_fft = (
    2 / numero_muestras
) * np.abs(fft_valores)

plt.figure(figsize=(12, 4))
plt.plot(
    fft_frecuencias,
    amplitud_fft,
    color="darkred",
    linewidth=0.7
)

plt.title(
    "Espectro de frecuencias – "
    "Flexor radial del carpo en reposo"
)

plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.xlim(0, 500)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    carpeta_resultados / "antebrazo_reposo_fft.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```
---

### **5.2. EMG - Flexor radial del carpo**
En esta sección se presentan las gráficas correspondientes al registro del **flexor radial del carpo** para las tres condiciones evaluadas.

| Condición                       | Señal original             | Señal filtrada             | Señal rectificada          |
| ------------------------------- | -------------------------- | -------------------------- | -------------------------- |
| Reposo                          | <img src="../../resultados_lab3/antebrazo_reposo_original.png" width="867" alt="antebrazo_reposo_original"> | <img src="../../resultados_lab3/antebrazo_reposo_filtrada.png" width="867" alt="antebrazo_reposo_filtrada"> | <img src="../../resultados_lab3/antebrazo_reposo_rectificada.png" width="867" alt="antebrazo_reposo_rectificada"> | 
| Movimiento leve sin oposición   | <img src="../../resultados_lab3/movimiento_leve_original.png" width="867" alt="movimiento_leve_original"> | <img src="../../resultados_lab3/movimiento_leve_filtrada.png" width="867" alt="movimiento_leve_filtrada"> | <img src="../../resultados_lab3/movimiento_leve_rectificada.png" width="867" alt="movimiento_leve_rectificada"> |
| Movimiento fuerte con oposición | <img src="../../resultados_lab3/antebrazo_fuerza_original.png" width="867" alt="antebrazo_fuerza_original"> | <img src="../../resultados_lab3/antebrazo_fuerza_filtrada.png" width="867" alt="antebrazo_fuerza_filtrada"> | <img src="../../resultados_lab3/antebrazo_fuerza_rectificada.png" width="867" alt="antebrazo_fuerza_rectificada"> |

| Condición                       | Densidad Espectral de Potencia (Welch) | Espectro de Frecuencias (FFT) |
| ------------------------------- | -------------------------------------- | ----------------------------- |
| Reposo                          | <img src="../../resultados_lab3/antebrazo_reposo_welch.png" width="867" alt="antebrazo_reposo_welch"> | <img src="../../resultados_lab3/antebrazo_reposo_fft.png" width="867" alt="antebrazo_reposo_fft"> |
| Movimiento leve sin oposición   | <img src="../../resultados_lab3/movimiento_leve_welch.png" width="867" alt="movimiento_leve_welch">             | <img src="../../resultados_lab3/movimiento_leve_fft.png" width="867" alt="movimiento_leve_fft">    |
| Movimiento fuerte con oposición | <img src="../../resultados_lab3/antebrazo_fuerza_welch.png" width="867" alt="antebrazo_fuerza_welch">             | <img src="../../resultados_lab3/antebrazo_fuerza_fft.png" width="867" alt="antebrazo_fuerza_fft">    |


### **5.3. EMG - Fibras descendentes del trapecio**

En esta sección se presentan los resultados correspondientes a las **fibras descendentes del trapecio**. Se siguió el mismo procedimiento de procesamiento utilizado para el flexor radial del carpo.

| Condición                       | Señal original             | Señal filtrada             | Señal rectificada          |
| ------------------------------- | -------------------------- | -------------------------- | -------------------------- |
| Reposo                          | <img src="../../resultados_lab3/cuello_reposo_original.png" width="867" alt="cuello_reposo_original"> | <img src="../../resultados_lab3/cuello_reposo_filtrada.png" width="867" alt="cuello_reposo_filtrada"> | <img src="../../resultados_lab3/cuello_reposo_rectificada.png" width="867" alt="cuello_reposo_rectificada"> |
| Movimiento leve sin oposición   | <img src="../../resultados_lab3/rolando_original.png" width="867" alt="rolando_original"> | <img src="../../resultados_lab3/rolando_filtrada.png" width="867" alt="rolando_filtrada"> | <img src="../../resultados_lab3/rolando_rectificada.png" width="867" alt="rolando_rectificada"> |
| Movimiento fuerte con oposición | <img src="../../resultados_lab3/Cuello_fuerza_original.png" width="867" alt="Cuello_fuerza_original"> | <img src="../../resultados_lab3/Cuello_fuerza_filtrada.png" width="867" alt="Cuello_fuerza_filtrada"> | <img src="../../resultados_lab3/Cuello_fuerza_rectificada.png" width="867" alt="Cuello_fuerza_rectificada"> |

| Condición                       | Densidad Espectral de Potencia (Welch) | Espectro de Frecuencias (FFT) |
| ------------------------------- | -------------------------------------- | ----------------------------- |
| Reposo                          | <img src="../../resultados_lab3/cuello_reposo_welch.png" width="867" alt="cuello_reposo_welch"> | <img src="../../resultados_lab3/cuello_reposo_fft.png" width="867" alt="cuello_reposo_fft"> |
| Movimiento leve sin oposición   | <img src="../../resultados_lab3/rolando_welch.png" width="867" alt="rolando_welch">             | <img src="../../resultados_lab3/rolando_fft.png" width="867" alt="rolando_fft">    |
| Movimiento fuerte con oposición | <img src="../../resultados_lab3/Cuello_fuerza_welch.png" width="867" alt="Cuello_fuerza_welch">             | <img src="../../resultados_lab3/Cuello_fuerza_fft.png" width="867" alt="Cuello_fuerza_fft">    |


## **6. Análisis y discusión**
El procesamiento de las señales mediante filtros pasabanda y notch (60 Hz) demostró ser efectivo para atenuar el ruido de red eléctrica y eliminar componentes fuera del rango de interés, permitiendo visualizar las respuestas musculares.

### **6.1. EMG - Flexor radial del carpo**
En los registros de este músculo, la amplitud y el espectro varían según la actividad realizada.

- **Reposo**: La señal presenta una amplitud baja y oscilaciones distribuidas durante el registro. Después del filtrado y rectificado se observa una actividad muscular baja, y en los análisis de Welch y FFT se muestran un contenido frecuencial de menor magnitud.
- **Movimiento leve sin oposición**: Se observan aproximadamente tres periodos de activación claramente diferenciados, característicos de las 3 repeticiones que se realizó. La señal rectificada permite identificar mejor estos eventos y con el Welch y FFT se muestran un incremento de la potencia y amplitud respecto al reposo y distribuídas en las frecuencias bajas y medias.
- **Movimiento fuerte con aceleración**: Se observa un mismo patrón como en las anteriores actividades pero con mayor magnitud, evidenciando con ello una mayor actividad muscular.

### **6.2. EMG - Fibras descendentes del trapecio**
Al igual que en el caso anterior, sigue un comportamiento similar pero con valores distintos.

- **Reposo**: La señal permanece cercana al nivel basal durante gran parte del registro, aunque se observan algunos picos hacia el final, esto último puede deberse a algún movimiento que hizo el participante durante la medición.
- **Movimiento leve sin oposición**: Se visualizan tres cambios claros y moderados. La rectificación facilita su visualización y los análisis de Welch y FFT muestran un aumento de la actividad espectral.
- **Movimineto fuerte con oposición**: Presenta los mayores picos de amplitud temporal de toda la prueba. El análisis en el dominio de la frecuencia (Welch y FFT) muestra un incremento en la potencia de la señal. Con ello se puede decir que en esta prueba, se realizó una mayor actividad muscular para poder vencer la resistencia producida por la oposicón.

## **7. Limitaciones**
- Las señales EMG pueden verse afectadas por factores externos como el desplazamiento de los electrodos, el movimiento de los cables y la interferencia eléctrica, incluso después del filtrado aplicado.
- Los resultados sólo permiten comparar la actividad muscular entre las 3 condiciones evaluadas
- Diafonía (Cross-talk): Especialmente en el antebrazo (flexor radial del carpo), al haber múltiples músculos cercanos, es posible que la señal adquirida capte la actividad eléctrica (cross-talk) de músculos adyacentes durante los movimientos, afectando la pureza del registro.
- La impedancia en la interfaz piel-electrodo.

## **8. Conclusiones**
- El procesamiento aplicado permitió obtener señales EMG más adecuadas para su análisis mediante el filtrado, la rectificación y el análisis en los dominios temporal y frecuencial.
- Tanto el flexor radial del carpo como las fibras descendentes del trapecio presentaron una mayor actividad durante el movimiento fuerte con oposición en comparación con el reposo y el movimiento leve sin oposición.
- Los resultados muestran que el aumento de la exigencia del movimiento se relaciona con un incremento de la amplitud y de la potencia de las señales EMG analizadas, comprobando de esa manera la relación fisiológica directa entre la intensidad del esfuerzo y la amplitud de la señal EMG.

## **9. Cuestionario**

**P1. ¿Cuáles son las frecuencias significativas para las adquisiciones de EMG? ¿Son las mismas en todas las zonas del cuerpo, como el área facial?**

Las señales EMG presentan principalmente componentes de frecuencia en un rango aproximado de 20 a 450 Hz, por lo que en el procesamiento realizado se utilizó un filtro pasabanda de este rango. Sin embargo, las frecuencias predominantes pueden variar dependiendo del músculo, la ubicación de los electrodos y las características de la actividad muscular. Por ello, no necesariamente son iguales en todas las zonas del cuerpo, como el área facial.

**P2. ¿Qué tipo de filtro es esencial cuando se trabaja con señales EMG? ¿Por qué necesitamos aplicar dicho filtro?**


Un filtro pasabanda es fundamental para eliminar componentes de frecuencia que no corresponden principalmente a la actividad electromiográfica de interés. En este caso se utilizó un filtro de 20 a 450 Hz. Además, se aplicó un filtro notch de 60 Hz para reducir la interferencia proveniente de la red eléctrica. Estos filtros permiten obtener una señal más limpia y facilitar su análisis tanto en el dominio temporal como frecuencial.

**P3. ¿Cómo difiere la amplitud en cada contracción muscular? ¿Existe alguna diferencia según la ubicación del músculo en el cuerpo?**

En las señales obtenidas se observó que la amplitud aumentó conforme aumentó la exigencia del movimiento. Durante el reposo se registraron amplitudes bajas, mientras que en el movimiento leve sin oposición aparecieron periodos de activación más definidos. Finalmente, durante el movimiento fuerte con oposición se observaron las mayores amplitudes en ambos músculos. La amplitud también puede variar entre músculos debido a sus características anatómicas, su función y la ubicación de los electrodos.

**P4. Muestra una captura de pantalla de una parte relevante de los datos de Electromiografía (EMG) obtenidos durante el experimento propuesto en la Sección D, correspondiente a un músculo de interés.**

¿Esta señal corresponde con lo que esperabas? ¿Por qué? ¿Qué emoción y acción realizaste para activar el músculo? ¿Qué músculo activaste?

Se puede observar las imágenes obtenidas en la sección de resultados, donde la señal obtenida corresponde con lo esperado, ya que se observó una actividad muscular baja durante el reposo y un incremento de la amplitud durante las condiciones de movimiento. Para el flexor radial del carpo, se realizó un movimiento del antebrazo, observándose una mayor activación durante el movimiento fuerte con oposición. Para las fibras descendentes del trapecio, se realizó un movimiento que involucró la elevación o estabilización del hombro, observándose también una mayor actividad durante el movimiento fuerte con oposición.

**P5. Según tu conocimiento, ¿la amplitud de la señal EMG es igual a la cantidad de fuerza que has generado con tu músculo?**

No necesariamente. La amplitud de la señal EMG está relacionada con el nivel de activación muscular, pero no es igual directamente a la fuerza generada. Una mayor amplitud puede indicar un mayor reclutamiento de unidades motoras, pero la relación entre la señal EMG y la fuerza depende de diferentes factores, como el músculo analizado, la posición, la ubicación de los electrodos y las condiciones de la contracción. Por ello, en este experimento la amplitud permite comparar el nivel de actividad entre las condiciones evaluadas, pero no determinar directamente la fuerza producida.
