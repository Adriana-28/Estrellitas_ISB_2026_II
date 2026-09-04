# Resumen de los 3 laboratorios
# Laboratorio 1: Introducción al análisis de señales biomédicas con PhysioNet

## Resumen

En este laboratorio se aprendió a acceder, visualizar y analizar señales biomédicas reales disponibles en **PhysioNet**, una plataforma que contiene bases de datos de señales fisiológicas como electrocardiogramas (ECG), electroencefalogramas (EEG), electromiogramas (EMG), señales respiratorias y presión arterial.

Para el desarrollo del laboratorio se utilizó la **MIT-BIH Arrhythmia Database**, identificada en PhysioNet como `mitdb`. Esta base contiene registros electrocardiográficos empleados para el estudio de alteraciones del ritmo cardiaco. Se comprendió que la identificación de una señal requiere especificar tanto la base de datos (`DATABASE`) como el registro (`RECORD`), debido a que un mismo número puede aparecer en diferentes bases de datos.

## Herramientas utilizadas

El procesamiento se realizó en Python mediante Google Colab/Jupyter Notebook. Se utilizaron las siguientes librerías:

- `wfdb`: descarga y lectura de registros de PhysioNet.
- `NumPy`: procesamiento numérico y cálculo de estadísticas.
- `Pandas`: organización de datos.
- `Matplotlib`: representación gráfica de las señales.
- `SciPy`: conversión y exportación del ECG a formato WAV.

## Análisis del registro 100

Inicialmente se analizó el registro `100` de la base de datos `mitdb`. Este registro presenta las siguientes características:

| Característica | Resultado |
|---|---:|
| Frecuencia de muestreo | 360 Hz |
| Número de muestras | 650 000 |
| Número de canales | 2 |
| Canales disponibles | MLII y V5 |
| Unidad | mV |
| Duración total | 1805.56 segundos |
| Canal seleccionado | Canal 0 – MLII |

La frecuencia de muestreo de 360 Hz indica que se adquieren 360 muestras por segundo. Por lo tanto, un segmento de 10 segundos contiene 3600 muestras y el periodo de muestreo es:

$$
T_s=\frac{1}{f_s}=\frac{1}{360}=0.00278\text{ s}
$$

Esto significa que se registra una muestra aproximadamente cada 2.78 milisegundos.

Para construir el eje temporal se empleó la relación:

$$
t[n]=\frac{n}{f_s}
$$

donde `n` representa el índice de la muestra y `fs` la frecuencia de muestreo.

## Representaciones realizadas

La señal ECG fue estudiada mediante cuatro representaciones:

### 1. ECG completo

Permitió observar el comportamiento global del registro y detectar cambios bruscos o posibles artefactos.

<p align="center">
  <img src="../../img/cuadro1.png" alt="Señal ECG completa" width="850">
</p>

<p align="center"><em>Figura 1. Representación completa de la señal ECG.</em></p>

### 2. Segmento ECG de 10 segundos

Facilitó la observación detallada de la morfología cardiaca y de estructuras como los complejos QRS.

<p align="center">
  <img src="../../img/cuadro2.png" alt="Segmento ECG de 10 segundos" width="850">
</p>

<p align="center"><em>Figura 2. Segmento correspondiente a los primeros 10 segundos del ECG.</em></p>

### 3. Histograma de amplitudes

Mostró la distribución de los valores de amplitud de la señal. Sin embargo, esta representación no conserva información sobre el instante en el que aparece cada valor.

<p align="center">
  <img src="../../img/cuadro3.png" alt="Histograma de amplitudes del ECG" width="700">
</p>

<p align="center"><em>Figura 3. Distribución de las amplitudes del segmento ECG analizado.</em></p>

### 4. Representación discreta

Permitió observar individualmente las muestras que forman la señal digital y comprobar que estas fueron adquiridas en instantes separados.

<p align="center">
  <img src="../../img/cuadro4.png" alt="Representación discreta del ECG" width="850">
</p>

<p align="center"><em>Figura 4. Representación discreta de las primeras muestras del ECG.</em></p>

En el segmento de 10 segundos del registro 100 se obtuvieron los siguientes resultados:

| Parámetro | Valor |
|---|---:|
| Media | −0.3199 mV |
| Desviación estándar | 0.1702 mV |
| Mínimo | −0.6450 mV |
| Máximo | 0.9600 mV |
| Rango | 1.6050 mV |


## Comparación con otro registro

Como ejercicio adicional se analizó el registro `115`, canal 0 (`MLII`). Este registro también posee una frecuencia de muestreo de 360 Hz y dos canales: MLII y V1.

Al compararlo con el registro 100, se observaron diferencias en la amplitud, la distribución de los datos y la cantidad de complejos QRS presentes durante los primeros 10 segundos. Las estadísticas del segmento fueron:

| Parámetro | Valor |
|---|---:|
| Media | −0.4823 mV |
| Desviación estándar | 0.2973 mV |
| Mínimo | −1.4200 mV |
| Máximo | 1.8000 mV |
| Rango | 3.2200 mV |

El mayor rango y desviación estándar indican que el registro 115 presenta una variación de amplitud superior a la observada en el registro 100.

## Reto final: registro 101

Para el reto final se seleccionó el registro `101` de la MIT-BIH Arrhythmia Database y se analizó el canal 1, denominado `V1`.

| Característica | Resultado |
|---|---:|
| Base de datos | MIT-BIH Arrhythmia Database (`mitdb`) |
| Registro | 101 |
| Frecuencia de muestreo | 360 Hz |
| Número de muestras | 650 000 |
| Número de canales | 2 |
| Canales disponibles | MLII y V1 |
| Canal analizado | Canal 1 – V1 |
| Duración total | 1805.56 segundos |
| Duración analizada | 10 segundos |
| Muestras analizadas | 3600 |

Las estadísticas obtenidas para los primeros 10 segundos del canal V1 fueron:

| Parámetro | Valor |
|---|---:|
| Media | −0.1499 mV |
| Desviación estándar | 0.0428 mV |
| Mínimo | −0.4100 mV |
| Máximo | −0.0500 mV |
| Rango | 0.3600 mV |

La media negativa indica que el segmento se encuentra desplazado respecto a cero. La baja desviación estándar y el rango de 0.36 mV muestran que las amplitudes del canal V1 presentan menor dispersión que las observadas en los registros 100 y 115. Estas diferencias pueden relacionarse con la orientación de la derivación, la ubicación de los electrodos y las características particulares del registro.

## Exportación del ECG a WAV

El segmento del registro 101 fue convertido al formato WAV mediante el siguiente procedimiento:

1. Eliminación de la componente media o componente DC.
2. Normalización de la amplitud.
3. Conversión de los datos de `float64` a `int16`.
4. Conservación de la frecuencia de muestreo de 360 Hz.
5. Generación del archivo `ecg_record_101_channel_1.wav`.

Aunque el ECG puede almacenarse como WAV porque ambos formatos contienen muestras ordenadas temporalmente, el archivo generado no representa un sonido cardiaco real. El ECG registra la actividad eléctrica del corazón, mientras que un sonido cardiaco corresponde a una señal acústica. La visualización gráfica continúa siendo más adecuada para identificar las ondas P, los complejos QRS, las ondas T y sus amplitudes.

## Conclusiones

Durante el laboratorio se logró cargar y analizar correctamente señales electrocardiográficas reales obtenidas de PhysioNet. Se identificaron los metadatos de los registros, sus canales, unidades, frecuencia de muestreo y duración. También se construyó el eje temporal y se representaron las señales mediante gráficas temporales, histogramas y muestras discretas.

El análisis estadístico permitió comparar cuantitativamente diferentes segmentos y registros. Además, se comprobó que la morfología y la amplitud del ECG pueden cambiar dependiendo del paciente, el registro y la derivación seleccionada.

Finalmente, se exportó un segmento ECG a formato WAV conservando su organización temporal. Este laboratorio permitió establecer las bases para posteriores procedimientos de procesamiento digital de señales, como la aplicación de filtros FIR e IIR, el análisis en frecuencia y la Transformada Z. Los resultados obtenidos son descriptivos y no deben interpretarse como un diagnóstico clínico.

# Resumen del Laboratorio 2: Análisis Multidominio de Señales Biomédicas

Este Laboratorio 2 se centró en la exploración y análisis de señales biomédicas, específicamente registros de electrocardiograma (ECG) de la base de datos NSRDB (Normal Sinus Rhythm Database) de PhysioNet. El objetivo primordial fue comprender cómo una señal puede ser analizada desde tres perspectivas complementarias: el dominio temporal, el dominio frecuencial (utilizando la Transformada Rápida de Fourier - FFT) y el dominio tiempo-frecuencia (mediante la Transformada de Fourier de Tiempo Corto - STFT).

### Objetivos Específicos del Laboratorio

- **Importación y Caracterización de Registros**: Aprender a importar registros fisiológicos desde PhysioNet usando la librería `wfdb` e identificar sus características básicas como frecuencia de muestreo (fs), número de muestras, cantidad y nombres de canales, y unidades de medida.
- **Representación Temporal**: Visualizar las señales en el dominio del tiempo para observar su morfología, amplitud, periodicidad, y la presencia de eventos o artefactos.
- **Análisis Frecuencial (FFT)**: Calcular y analizar el contenido frecuencial de las señales mediante la FFT, comparando los espectros antes y después de eliminar la componente de corriente directa (DC), que representa el valor medio de la señal.
- **Análisis Tiempo-Frecuencia (STFT)**: Estudiar cómo evoluciona el contenido frecuencial de las señales a lo largo del tiempo, mediante la generación de espectrogramas, y comprender el compromiso entre resolución temporal y frecuencial al ajustar el tamaño de la ventana (`nperseg`).
- **Comparación y Conclusión**: Comparar los hallazgos de tres registros ECG específicos (16265, 16272, 16420) en los diferentes dominios y extraer conclusiones sobre su comportamiento.

### Pasos Clave y Herramientas Utilizadas

- **Configuración del Entorno**: Se utilizaron librerías fundamentales como `wfdb` para el acceso a datos de PhysioNet, NumPy para operaciones numéricas y la implementación de la FFT, SciPy para el cálculo de la STFT, y Matplotlib para la visualización de las señales y sus transformadas.

- **Carga de Registros**: Se cargaron los registros 16265, 16272 y 16420 desde la base de datos `nsrdb` de PhysioNet, extrayendo un segmento inicial de 3600 muestras (aproximadamente 28.12 segundos a una fs de 128 Hz) para cada uno. Se verificó que todos compartían una frecuencia de muestreo de 128 Hz y dos canales (ECG1, ECG2).

- **Análisis en el Dominio Temporal**: Se graficaron las señales en función del tiempo. Se observó que los registros 16265 y 16420 presentaban morfologías ECG periódicas y relativamente estables, mientras que el registro 16272 mostró una mayor variabilidad en amplitud y una morfología menos definida, sugiriendo posiblemente ruido o una condición fisiológica diferente.

  A continuación, se muestra un ejemplo de la representación temporal para el registro 16420:

  <p align="center">
  <img src="../../img/reto_lab2_timedomain.png" alt="Señal ECG completa" width="850">
  </p>

- **Análisis en el Dominio Frecuencial (FFT)**:
  - Se implementó una función para calcular la FFT con y sin la componente DC. La eliminación de la DC (`x - np.mean(x)`) resultó crucial para una visualización clara del contenido frecuencial no estacionario.
  - Para los registros 16265 y 16420, se identificaron picos dominantes de frecuencia alrededor de 1.60 Hz y 1.636 Hz, respectivamente, lo cual es consistente con las frecuencias cardíacas esperadas.
  - El registro 16272 mostró un comportamiento atípico, con un pico dominante muy bajo de 0.142 Hz, lo que podría indicar una oscilación lenta subyacente o la presencia de artefactos significativos en el rango de muy baja frecuencia.

  Un ejemplo de la FFT sin componente DC para el registro 16420:

  <p align="center">
  <img src="../../img/reto_lab2_fftsdc.png" alt="Señal ECG completa" width="850">
  </p>

- **Análisis en el Dominio Tiempo-Frecuencia (STFT)**:
  - Se calculó la STFT para los registros, utilizando una ventana `nperseg=256` para todos (lo que representa 2 segundos de señal). Esto permitió generar espectrogramas que muestran la evolución del contenido frecuencial a lo largo del tiempo.
  - Los espectrogramas de 16265 y 16420 exhibieron concentraciones de energía estables en bajas frecuencias a lo largo del tiempo, reflejando la periodicidad de sus ECG.
  - El espectrograma de 16272, aunque también mostró energía concentrada en bajas frecuencias, su contexto de mayor variabilidad temporal sugiere que una ventana `nperseg` más pequeña (como 32, sugerido en el ejercicio original) podría haber ofrecido una mejor resolución temporal para eventos transitorios.

  Observa el espectrograma STFT del registro 16420:

  <p align="center">
  <img src="../../img/reto_lab2_stft.png" alt="Señal ECG completa" width="850">
  </p>

### Conclusiones Generales

El laboratorio reafirmó la importancia del análisis multidominio para una comprensión integral de las señales biomédicas. Mientras que el dominio temporal es indispensable para la observación directa de la morfología y eventos visibles, el dominio frecuencial (FFT) revela el contenido de frecuencia global y la STFT ofrece una ventana a la dinámica de esas frecuencias a lo largo del tiempo. La comparación de los registros destacó que, aunque superficialmente todos eran ECG, el registro 16272 presentó características distintivas en todos los dominios que sugieren una fisiología alterada o una mayor influencia de ruido, diferenciándolo claramente de los patrones más regulares de 16265 y 16420. La elección adecuada de parámetros en las transformadas (como la eliminación de DC en FFT y el tamaño de ventana en STFT) es crucial para extraer la información más relevante de las señales.
