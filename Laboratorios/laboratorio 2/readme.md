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

1. **ECG completo:** permitió observar el comportamiento global del registro y detectar cambios bruscos o posibles artefactos.
2. **Segmento de 10 segundos:** facilitó la observación de la morfología cardiaca y de estructuras como los complejos QRS.
3. **Histograma de amplitudes:** mostró la distribución de los valores de amplitud, aunque no conserva información sobre el momento en que aparece cada valor.
4. **Representación discreta:** permitió observar las muestras individuales que forman la señal digital.

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