# Resumen del Laboratorio 7 — Filtrado de señales II: filtros adaptativos y Transformada Wavelet en ECG

Laboratorio del curso **Introducción a las Señales Biomédicas** (Universidad Peruana Cayetano Heredia). La idea del lab es simple: tomar un ECG real, ensuciarlo a propósito con ruido conocido, probar varias técnicas de filtrado y ver cuál recupera mejor la señal original. Todo está hecho en Python dentro de un notebook de Google Colab.

## Objetivo

Evaluar y comparar distintas técnicas de filtrado digital (pasa-banda, notch, filtro adaptativo LMS y Transformada Wavelet) para la recuperación de una señal ECG contaminada de forma controlada, utilizando criterios visuales y métricas cuantitativas (RMSE, SNR y correlación).

## Metodología

El procedimiento siguió la secuencia **observación → contaminación → análisis → filtrado → evaluación**.

1. **Adquisición y lectura de datos.** La señal fue registrada con un BITalino (r)evolution mediante OpenSignals y exportada en formato de texto (`basal1.txt`). Los metadatos de la cabecera indicaron una frecuencia de muestreo de 1000 Hz y una resolución de 10 bits para el canal analógico `A2`, correspondiente al sensor ECG. La columna `nSeq` es un contador de paquetes (0–15) utilizado para detectar pérdidas de muestras, por lo que no se emplea como eje temporal; este se construye como `t = n / Fs`. En el registro no se detectaron muestras perdidas.
2. **Conversión a unidades físicas.** Los valores del ADC se convirtieron a milivoltios con la función de transferencia del sensor (VCC = 3.3 V, ganancia 1100) y se restó la media. Se obtuvo una señal de 34.65 s con amplitudes entre ≈ −0.35 mV y 0.39 mV, que se tomó como ECG de referencia.
3. **Contaminación artificial controlada.** A la señal de referencia se le sumaron:
   - interferencia de red a 60 Hz,
   - su segundo armónico a 120 Hz,
   - ruido gaussiano.

   De esta forma se dispone de una "respuesta correcta" contra la cual medir el desempeño de cada filtro.
4. **Análisis espectral (FFT).** El espectro de la señal contaminada muestra dos picos nítidos en 60 y 120 Hz, además de un aumento del piso de ruido en todas las frecuencias. La energía del ECG se concentra por debajo de aproximadamente 40 Hz.
5. **Filtrado y evaluación.** Se aplicaron los métodos descritos a continuación y se compararon mediante gráficas en el tiempo, espectros y métricas respecto al ECG original.

## Métodos de filtrado probados

| Método | Idea | Lo bueno | Lo malo |
|---|---|---|---|
| **Pasa-banda Butterworth 0.5–40 Hz** (orden 4, `sosfiltfilt`) | Deja pasar solo la banda típica del ECG | Quita las dos interferencias y casi todo el ruido de alta frecuencia | También recorta contenido real (deriva de base y parte del QRS) |
| **Notch 60 Hz / 60+120 Hz** (`iirnotch`, Q = 30) | Corta una frecuencia puntual | Casi no altera la morfología del ECG | Hay que conocer la frecuencia exacta; no toca el ruido de banda ancha |
| **LMS adaptativo** (μ = 0.005) | Un filtro que ajusta sus pesos muestra a muestra usando senos/cosenos de 60 y 120 Hz como referencia | Converge en unos cientos de ms y puede seguir interferencias que cambian en el tiempo | Necesita una señal de referencia; tampoco quita el ruido gaussiano |
| **Wavelet (db4, 8 niveles, umbral universal soft)** | Descompone la señal por escalas y anula coeficientes pequeños | Reduce bien el ruido gaussiano y conserva los QRS | Las interferencias sinusoidales intensas generan coeficientes grandes y sobreviven al umbral |
| **Híbrido: notch → Wavelet** | El notch quita las interferencias y la Wavelet el ruido de banda ancha | Combina lo mejor de ambos | Más pasos y más parámetros que elegir |

Todos los filtros convencionales se aplicaron con fase cero (`filtfilt` / `sosfiltfilt`) para que los complejos QRS no se desplacen en el tiempo.

### Cómo se ve la Wavelet por niveles

Con `db4` y 8 niveles, la descomposición queda más o menos así:

- **D1–D2** (125–500 Hz): casi vacíos en el original; en el contaminado dominan por el ruido gaussiano.
- **D3–D4** (31–125 Hz): ahí caen las interferencias de 120 y 60 Hz.
- **D5–D7**: contienen la energía de los complejos QRS, localizados en el tiempo (justo lo que la FFT global no muestra).
- **A8** (0–2 Hz): tendencia lenta y deriva de línea de base.

## Resultados

Métricas calculadas contra el ECG original, excluyendo 2 s al inicio y al final para evitar efectos de borde:

| Método | RMSE (mV) | SNR (dB) | Correlación r |
|---|---|---|---|
| Contaminado (sin filtrar) | 0.0699 | 1.09 | 0.7509 |
| **A — Pasa-banda** | **0.0092** | **18.72** | **0.9933** |
| Híbrido notch + Wavelet | 0.0194 | 12.21 | 0.9779 |
| B2 — Notch 60+120 Hz | 0.0239 | 10.40 | 0.9572 |
| LMS adaptativo | 0.0244 | 10.23 | 0.9564 |
| Wavelet (denoising) | 0.0332 | 7.56 | 0.9083 |
| B1 — Notch 60 Hz | 0.0414 | 5.64 | 0.8859 |

## Conclusiones

- **El pasa-banda obtuvo el mejor SNR, pero el resultado debe interpretarse con cuidado.** Es el único método que elimina además el ruido gaussiano fuera de 0.5–40 Hz, lo que explica su ventaja en la tabla. Sin embargo, al aplicarlo al ECG original sin ruido se obtiene un SNR de ~21.7 dB, lo que indica que el propio filtro introduce distorsión (pérdida de deriva de base y de componentes rápidas del QRS). El notch aplicado al original da ~29.3 dB, es decir, lo altera mucho menos.
- **Interferencia ≠ ruido.** La interferencia (60/120 Hz) es un pico en el espectro y es fácil de quitar con un notch. El ruido gaussiano es un fondo plano que comparte frecuencias con el ECG, así que ningún filtro lineal lo separa del todo.
- **El LMS rinde casi igual que el notch doble** en este caso porque las interferencias son estables. Su ventaja real aparecería si la amplitud o la fase cambiaran en el tiempo.
- **La Wavelet sola no es buena para interferencias de banda estrecha**, pero combinada con un notch da el mejor resultado después del pasa-banda y con mejor correlación que las demás opciones por separado.
- **Ningún método es mejor en todo.** Depende del tipo de contaminación, de qué parte de la señal fisiológica se quiere conservar y de la aplicación (monitoreo, diagnóstico, detección de QRS, tiempo real).
- Cabe resaltar que la contaminación es **artificial y con fines didácticos**. En un ECG real también hay deriva de línea de base, artefactos de movimiento, EMG, mal contacto de electrodos, etc.

## Parámetros modificables

En el notebook, algunas celdas tienen un bloque marcado como `PARÁMETROS MODIFICABLES`. Cambiar esos valores y volver a ejecutar permite ver cómo afecta cada uno al resultado del filtrado (el laboratorio plantea varias de estas pruebas como preguntas):

```python
f1, f2 = 60, 120          # frecuencias de interferencia (50 y 100 Hz para Europa)
fc_baja, fc_alta = 0.5, 40.0   # banda del pasa-banda
Q = 30                    # ancho de la muesca del notch (probar 5 y 100)
MU = 0.005                # paso del LMS (probar 0.0005 y 0.05)
WAVELET = "db4"           # probar "sym8"
modo = "soft"             # probar "hard"
```

## Librerías usadas

`numpy`, `pandas`, `matplotlib`, `scipy.signal` (`butter`, `iirnotch`, `filtfilt`, `sosfiltfilt`, `freqz`) y `PyWavelets` (`pywt`).

## Cómo correrlo

1. Abrir el notebook en Google Colab (o Jupyter local).
2. Subir el archivo `basal1.txt` (export de OpenSignals) a la misma carpeta.
3. Si hace falta, instalar PyWavelets: `pip install PyWavelets`.
4. Ejecutar las celdas en orden.
