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

**Evaluación de la calidad.** Se verifica la respuesta en frecuencia de la cascada pasa-banda más notch. Se compara el espectro antes y después de filtrar. Se mide la altura del pico de 60 Hz respecto de sus vecinas. Por último, se estima la relación señal-ruido usando el baseline filtrado como piso de ruido.

```math
SNR \approx 20 \log_{10} \frac{RMS_{prueba}}{RMS_{ruido}}
```



