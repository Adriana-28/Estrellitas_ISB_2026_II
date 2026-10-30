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

## 6. Clasificación y validación
**LDA** (análisis discriminante lineal) es rápido, robusto, con pocos parámetros y muy usado en control mioeléctrico. Supone clases gaussianas con la misma covarianza. **SVM con kernel RBF** permite una frontera de decisión no lineal. En ambos casos la normalización z-score se ajusta solo con los datos de entrenamiento, por lo que se encapsula en un `Pipeline`.

**Diseño de la comparación.** Cada clasificador se evalúa con tres conjuntos de características para medir cuánto aporta la amplitud: las 15 características, solo RMS y todas menos las de amplitud (curtosis, asimetría, MNF, MDF y bandas). Como referencia simple se añade un árbol de decisión de profundidad 1, que aprende exactamente un umbral sobre el RMS. También se prueba el LDA con log(RMS), porque el logaritmo comprime valores grandes y acerca los datos al supuesto gaussiano del LDA.

**Fuga de datos (data leakage).** Con solapamiento del 50 %, dos ventanas consecutivas comparten la mitad de sus muestras. Si una cae en entrenamiento y su vecina en prueba, el modelo ya vio parte de la prueba y el desempeño se sobreestima. La solución es dividir por grupos con `GroupKFold` de 5 pliegues, usando el ciclo como grupo, de modo que cada ciclo completo vaya a entrenamiento o a prueba. Para mostrar el efecto se compara con un `KFold` aleatorio. En estudios con varios sujetos, el equivalente es dividir por sujeto.

**Métrica.** Exactitud balanceada, que promedia el acierto de cada clase (0.5 equivale al azar y 1.0 a acertar todo). Se complementa con la matriz de confusión.



