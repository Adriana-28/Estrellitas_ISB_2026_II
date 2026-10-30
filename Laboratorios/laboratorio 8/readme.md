## 1. Fundamentos fisiológicos
El músculo no se contrae en bloque, sino que se organiza en unidades motoras (UM), cada una formada por una motoneurona de la médula espinal y todas las fibras musculares que inerva. Cuando la motoneurona dispara, sus fibras se despolarizan casi a la vez y generan un potencial de acción de unidad motora (MUAP), una onda bifásica o trifásica de pocos milisegundos.

El sistema nervioso regula la fuerza con dos mecanismos.

| Mecanismo | Qué ocurre | Efecto en la sEMG |
| --- | --- | --- |
| Reclutamiento | Se activan más unidades motoras, primero las pequeñas (principio de Henneman) | Aumenta la amplitud |
| Codificación por frecuencia | Cada UM dispara más rápido (aprox. 8 a 30 disparos por segundo) | Aumentan la amplitud y la densidad de la señal |

Los electrodos no registran una UM aislada, registran la suma espacial y temporal de los MUAP de muchas unidades. El resultado es un patrón de interferencia que parece ruido aleatorio, pero cuya amplitud y contenido espectral codifican la activación muscular. La grasa y la piel actúan como un filtro pasabajos, por eso el ancho de banda que llega a la superficie es menor que el de los pulsos a nivel muscular.

| Propiedad | Valor típico |
| --- | --- |
| Amplitud | De microvoltios (reposo) a pocos milivoltios (hasta unos 10 mV pico a pico) |
| Banda útil | Aprox. 20 a 450/500 Hz |
| Energía dominante | Aprox. 50 a 150 Hz |

## 2. Qué se puede medir con sEMG

La señal permite cuantificar de forma objetiva tres cosas. La intensidad de activación muscular (más señal implica más esfuerzo), el momento de activación entre músculos y el estado fisiológico del músculo (normal, anormal o fatigado). Cada efecto fisiológico se asocia a una característica de la señal y a un cálculo concreto.

Tambien hay disfunciones que pueden medirse, los más frecuentes son:

1. Exceso de tono basal (hipertonía), es decir, activación en reposo cuando el músculo debería estar relajado.
2. Asimetría muscular en movimientos bilaterales.
3. Déficit de actividad muscular, cuando un músculo trabaja menos de lo que debería.
4. Exceso de coactivación.
5. Sinergia alterada y timing de activación.

## 3. Preprocesamiento de la señal
Antes de filtrar se estima la densidad espectral de potencia (PSD) con el método de Welch. El método divide la señal en segmentos solapados, aplica una ventana a cada uno para reducir la fuga espectral, calcula el periodograma de cada segmento con la FFT y promedia los resultados. En sEMG sirve para ver dónde se concentra la potencia y para calcular la frecuencia media y la mediana, que se usan en el estudio de la fatiga.

**Filtros empleados.**

| Filtro | Diseño | Función |
| --- | --- | --- |
| Pasa-banda | Butterworth de orden 4, 20 a 450 Hz, en secciones de segundo orden (SOS) por estabilidad numérica | Quita deriva, movimiento y ruido de alta frecuencia con respuesta plana en la banda de paso |
| Notch | IIR en 60 Hz con Q = 30 (banda de aprox. 2 Hz) | Suprime la red eléctrica sin afectar frecuencias vecinas |
| Fase cero | Filtrado hacia adelante y hacia atrás (`sosfiltfilt` y `filtfilt`) | Evita el desfase. Es válido para análisis offline, un sistema en tiempo real usaría filtros causales |

La condición obligatoria del diseño es `0 < f_baja < f_alta < Fs/2`. Antes de filtrar se resta la media de la señal.

Un pasa-bajos de 50 Hz no es adecuado para limpiar la sEMG porque eliminaría gran parte de la energía muscular, que se extiende hasta unos 150 Hz o más, y dejaría pasar los artefactos de movimiento.

## 4. Segmentación, ventaneo y etiquetado

**Envolvente y detección de inicio de actividad.** La envolvente RMS móvil (ventana de 200 ms) resume la amplitud instantánea. La actividad se detecta comparando la envolvente con un umbral derivado del reposo.

**Ventaneo.** La sEMG es no estacionaria, por lo que las características se calculan sobre ventanas cortas.

**Etiquetado automático.** Cada ventana recibe una etiqueta según la fracción de sus muestras que cae dentro de una contracción detectada.

| Etiqueta | Criterio | Uso |
| --- | --- | --- |
| Contracción | 80 % o más dentro de una contracción | Entrenamiento |
| Reposo | 5 % o menos | Entrenamiento |
| Transición | El resto | Se excluye por etiqueta ambigua |

## 5. Extracción de características

**Amplitud y energía.** Indican cuánta actividad hay. Crecen con el reclutamiento y la frecuencia de disparo.

| Característica | Definición | Intuición |
| --- | --- | --- |
| MAV | Media del valor absoluto | Amplitud media rectificada |
| RMS | Raíz de la media de los cuadrados | Relacionada con la potencia |
| iEMG | Suma del valor absoluto | Área bajo la señal rectificada |
| VAR | Varianza muestral (N−1) | Potencia, pues la señal filtrada tiene media cercana a 0 |


**Complejidad y forma de onda.** Forman el conjunto clásico de Hudgins et al. (1993) para control de prótesis. ZC, SSC y WAMP usan un umbral de ruido ε para no contar fluctuaciones del piso de ruido. Se fijó en ε = 3σ del baseline filtrado.

| Característica | Definición | Intuición |
| --- | --- | --- |
| WL (longitud de onda) | Suma de \|x(i+1) − x(i)\| | Longitud del trazo, combina amplitud y frecuencia |
| ZC (cruces por cero) | Cambios de signo de x con diferencia mayor o igual a ε | Estimador temporal de frecuencia |
| SSC (cambios de signo de pendiente) | Cambios de signo de la pendiente que superan ε | Densidad de picos |
| WAMP (amplitud de Willison) | Veces que \|x(i+1) − x(i)\| supera ε | Relacionada con el disparo de UM |

Como cuentan solo eventos mayores que ε, estas tres características mezclan amplitud y frecuencia.

**Estadísticas de la distribución.** Preguntan si las amplitudes se parecen a una campana de Gauss.

| Característica | Interpretación |
| --- | --- |
| Asimetría (skewness) | 0 indica distribución simétrica |
| Curtosis de Fisher | 0 indica gaussiana. Mayor que 0 indica colas pesadas o picos aislados. Menor que 0 indica distribución aplanada |

Con muchas UM la sEMG tiende a ser cuasi gaussiana. La saturación recorta las colas y empuja la curtosis hacia valores negativos.

**Espectrales.** Se calculan sobre la PSD de Welch de cada ventana (`nperseg = 128`), restringida a 20 a 450 Hz.

| Característica | Definición | Interpretación |
| --- | --- | --- |
| MNF (frecuencia media) | Suma de f·P dividida por la suma de P | Centro de masa del espectro |
| MDF (frecuencia mediana) | Frecuencia que divide la potencia en dos mitades | Más robusta al ruido |
| Potencia por bandas | Fracción de potencia en 20 a 80, 80 a 150 y 150 a 450 Hz | Distribución espectral gruesa |

## 6. Deep learning

### Características diseñadas vs. aprendidas
Hasta ahora las características (RMS, ZC, MDF…) las elegimos nosotros con base en conocimiento fisiológico. En deep learning, la red **aprende sus propios filtros** a partir de los datos.

| | Clásico (características + LDA/SVM) | Deep learning (CNN) |
|---|---|---|
| Entrada | Vector de ~15 números | Señal cruda (1D-CNN) o imagen tiempo-frecuencia |
| Conocimiento experto | Alto | Bajo (la red lo descubre) |
| Datos necesarios | Pocos | Muchos (miles de ventanas, varios sujetos) |
| Interpretabilidad | Alta | Baja |
| Costo computacional | Mínimo | Alto (entrenamiento) |

### De la señal a una imagen: la STFT
- La FFT dice **qué** frecuencias hay, pero no **cuándo**. La STFT aplica la FFT sobre ventanas deslizantes.
- El **espectrograma** |X(m,k)|² es una matriz tiempo × frecuencia, es decir, **una imagen**, y las CNN extraen muy bien patrones de imágenes.
- **Incertidumbre tiempo-frecuencia:** ventana larga = buena resolución en frecuencia y mala en tiempo, y viceversa. Con `nperseg = 64` a 1000 Hz la resolución es de 15.6 Hz y 64 ms.
- Otras representaciones usadas en la literatura: wavelet continua (escalogramas), Hilbert-Huang y matrices multicanal HD-sEMG.

### Preparación de los datos
- Ventanas de **500 ms** (50 % de solapamiento), con transiciones descartadas.
- Cada ventana se convierte en un espectrograma de **27 frecuencias × 29 instantes** (banda 20–450 Hz, escala log10).
- Total: **185 imágenes** (106 reposo, 79 contracción).
- En los espectrogramas, la contracción llega a ≈ −3 (log10) frente a ≈ −5 del reposo, es decir, unas **100 veces más potencia**.
- El espectrograma del registro completo muestra ~20 franjas verticales brillantes (una por contracción), más intensas en las frecuencias bajas.

### Modelo y entrenamiento
- CNN muy pequeña: **1 330 parámetros entrenables**, elegida a propósito porque hay pocos datos (las CNN de imágenes suelen tener millones).
- Entrenamiento con Adam y entropía cruzada, evaluado con **GroupKFold (5 pliegues)**: cada ciclo reposo + contracción va completo al entrenamiento o a la prueba, sin fuga de datos.

### Resultados
| Pliegue | 1 | 2 | 3 | 4 | 5 | Promedio |
|---|---|---|---|---|---|---|
| Exactitud balanceada | 0.955 | 1.000 | 1.000 | 0.967 | 0.969 | **0.978 ± 0.019** |

- **Matriz de confusión agregada:** 104/106 reposos y 77/79 contracciones bien clasificados, solo **4 errores en 185 imágenes**.
- **Curva de pérdida:** baja rápido en las primeras épocas, pero luego tiene saltos bruscos y sube al final, lo que indica un entrenamiento inestable. Una tasa de aprendizaje menor o detener el entrenamiento en el mínimo de la pérdida probablemente lo estabilizaría.

### ¿Qué aprendió la red?
- Se visualizaron las activaciones de los **8 filtros de la primera capa**: no responden todos igual. Por ejemplo, el filtro 7 se activa en frecuencias bajas, mientras que los filtros 1 y 5 lo hacen en frecuencias altas.
- Son **características aprendidas**: no tienen nombre ni fórmula fisiológica clara, y esa es la pérdida de **interpretabilidad** del deep learning.

### Comparación con el enfoque clásico
| Método | Exactitud balanceada |
|---|---|
| CNN (espectrograma) | 0.978 ± 0.019 |
| SVM (15 características) | 0.972 ± 0.016 |
| LDA (15 características) | 0.966 ± 0.023 |
| **Un solo umbral en RMS** | **0.991 ± 0.011** |

### Conclusiones
- La CNN supera numéricamente al LDA y a la SVM, pero la diferencia es **menor que la variación entre pliegues**, así que no es concluyente.
- Para reposo vs. contracción, **un solo umbral en RMS rinde incluso mejor** que la CNN: tarea fácil, no hace falta un modelo complejo.
- Para esta tarea, las características clásicas ofrecen similar rendimiento con menor costo e interpretabilidad mucho mayor.
- Las CNN cobran sentido en tareas más difíciles (p. ej. distinguir varios gestos) y con muchos más datos.
- Limitación: ~200 imágenes de **un solo sujeto**, por lo que no se puede asegurar que el modelo generalice a otra persona.


