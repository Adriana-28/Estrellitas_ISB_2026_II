# Procesamiento de señales de EEG

## El pipeline completo

Un proyecto de EEG convierte ondas microscópicas y ruidosas del cuero cabelludo en un diagnóstico o en un comando para una computadora. Los pasos son cinco:

1. Adquisición con electrodos ubicados según el sistema 10-20.
2. Filtrado para quitar ruido de red, deriva lenta y artefactos musculares u oculares.
3. Preprocesamiento: re-referenciado espacial (CAR, Laplaciano) y normalización (z-score, GFP).
4. Extracción de características en tiempo, frecuencia, tiempo-frecuencia, espacio y entropía.
5. Modelado con SVM, geometría Riemanniana, EEGNet o Transformers.

## EEG 
El EEG registra la actividad sincronizada de potenciales post-sinápticos en poblaciones de neuronas corticales. Se usa en epilepsia, sueño, carga cognitiva e interfaces cerebro-computadora (BCI). Sin embargo, la señal llega débil porque atraviesa meninges, líquido cefalorraquídeo, cráneo y piel. Esto implica que un parpadeo, un apretón de mandíbula o un cable cercano pueden ser entre 10 y 50 veces más grandes que la señal cerebral. 
Además es no estacionaria y no lineal. Por eso se corta en ventanas cortas (épocas) donde se pueda asumir que es casi estacionaria.

## 2. Ritmos cerebrales

| Banda | Frecuencia | Para qué se mide |
|---|---|---|
| Delta | 0.5 a 4 Hz | Sueño profundo (N3). En un adulto despierto puede indicar lesión focal o encefalopatía. |
| Theta | 4 a 8 Hz | Somnolencia, meditación profunda, memoria de trabajo. |
| Alpha | 8 a 13 Hz | Relajación con ojos cerrados, zona occipital. Desaparece al abrir los ojos. |
| Mu | similar a alpha | Nace en la corteza motora (C3, Cz, C4). Cae al mover o imaginar movimiento (ERD), base del control de prótesis. |
| Beta | 13 a 30 Hz | Atención, cálculo, control motor. El exceso frontal se asocia con estrés. |
| Gamma | sobre 30 Hz | Integración multisensorial, percepción consciente, emociones. |

## 3. Electrodos y paradigmas de adquisición

El sistema 10-20 ubica los electrodos en fracciones proporcionales de la distancia entre nasion e inion, así que funciona igual en cráneos de distinto tamaño. Las letras indican el lóbulo (Fp, F, C, T, P, O). Los números impares van a la izquierda, los pares a la derecha y la z marca la línea media.

Hay tres paradigmas y de ellos depende el algoritmo:

- Actividad espontánea o inducida, como la imaginación motora o el sueño. Se analizan cambios de potencia con Welch, wavelets y CSP.
- ERP, como la onda P300. Se mira la forma de la onda promediada en el tiempo, no las bandas.
- SSVEP. El usuario mira un botón que parpadea a una frecuencia fija y la corteza occipital responde a esa misma frecuencia.

## 4. Artefactos y filtrado

| Artefacto | Origen | Efecto |
|---|---|---|
| Ocular (EOG) | El ojo es un dipolo eléctrico | Contamina Fp1 y Fp2 e imita delta. |
| Muscular (EMG) | Cara, mandíbula, cuello | Destruye beta y gamma en canales temporales y frontales. |
| Cardíaco (ECG) | Complejo QRS | Picos rítmicos en el fondo. |
| Red eléctrica | Cables y enchufes | Sinusoide constante, 60 Hz en Perú y 50 Hz en Europa. |

Para la limpieza temporal se usan un pasa-altas (quita la deriva de línea base), un pasa-bajas (recorta ruido muscular y térmico) y un notch en la frecuencia de red. En EEG se filtra siempre con fase cero para no desplazar los picos en el tiempo.

## 5. Preprocesamiento espacial y limpieza

El CAR (Common Average Reference) resta a cada electrodo el promedio de todos los electrodos. Cancela interferencias que llegan a todos por igual y funciona mejor con cobertura amplia y simétrica.

El filtro Laplaciano resta solo el promedio de los vecinos inmediatos. Actúa como un filtro pasa-altas espacial: lo que viene de lejos se parece en C3 y en sus vecinos y desaparece, mientras que lo que nace justo bajo C3 se queda.

La normalización z-score deja cada canal con media 0 y varianza 1, para que ni los canales ni los pacientes con más voltaje dominen el modelo. El GFP es la desviación estándar entre todos los electrodos en cada instante. Los mapas en los picos del GFP, agrupados con clustering, dan los microestados del EEG.

Un filtro de frecuencias no puede quitar los parpadeos porque ocupan la misma banda que delta y theta. Ahí entra ICA, que separa los canales en fuentes independientes, identifica la del ojo o la del corazón, la pone en cero y reconstruye el EEG. 

## 6. Densidad espectral de potencia y método de Welch
No se usa una FFT directa porque da un espectro lleno de picos falsos, la varianza del estimador no baja aunque haya más datos. Welch utiliza 5 pasos: cortar en segmentos superpuestos, aplicar una ventana (Hamming o Hann), calcular la FFT de cada uno, obtener el periodograma modificado y promediar todos. 

La PSD se grafica en dB/Hz. El cerebro sigue una ley 1/f, así que delta tiene muchísima más potencia bruta que beta o gamma. En escala lineal solo se vería el pico de delta.

## 7. Extracción de características

| Dominio | Ejemplos | Uso típico |
|---|---|---|
| Tiempo | Media, varianza, parámetros de Hjorth | Epilepsia, sueño, P300 |
| Frecuencia | Potencia absoluta y relativa (Welch), ratios entre bandas | Carga cognitiva, TDAH, fatiga al conducir |
| Tiempo-frecuencia | Wavelets (DWT, CWT), STFT, EMD | Espigas epilépticas, husos del sueño, ERD/ERS |
| Espacial y de red | CSP, coherencia, PLV, PLI | Imaginación motora, Alzheimer |
| No lineal | Entropía diferencial, Sample Entropy, dimensión fractal de Higuchi | Emociones, conciencia |

Los parámetros de Hjorth (actividad, movilidad y complejidad) salen solo de varianzas de la señal y sus derivadas, así que cuestan casi nada. La potencia relativa reduce la variabilidad entre personas porque expresa cada ritmo como porcentaje del total. Las wavelets sirven cuando Welch promedia demasiado y se pierde el instante exacto de un evento breve.

Para conectividad, la coherencia es como una correlación por frecuencia, el PLV mide sincronía de fase con la transformada de Hilbert y el PLI descarta diferencias de fase de 0 o pi para esquivar la conducción de volumen. La entropía diferencial es la característica con mejor precisión en reconocimiento de emociones sobre los datasets SEED y DEAP.

## 8. Clasificación clásica y geometría Riemanniana

CSP aprende una combinación lineal de electrodos que crea canales virtuales con varianza máxima para una clase (mano izquierda) y mínima para la otra. La característica final es el logaritmo de la varianza de los primeros y últimos filtros. Sin embargo, exige filtrar antes en una banda fija.

La geometría Riemanniana parte de que la matriz de covarianza espacial de cada época es simétrica definida positiva. Esas matrices viven en una superficie curva, no en un espacio plano.

## 9. Deep learning

EEGNet es una CNN compacta pensada para pocos datos. Su convolución temporal aprende los filtros pasa-banda, la espacial depthwise aprende algo equivalente a un CSP por banda y la separable resume en el tiempo con pocos parámetros. Otras arquitecturas que aparecen en la literatura:

- ShallowConvNet y DeepConvNet, donde la primera reproduce el pipeline de FBCSP.
- EEG-TCNet, con convoluciones dilatadas causales sobre EEGNet.
- DGCNN, que trata cada electrodo como un nodo de un grafo.
- EEG-Conformer, que une convoluciones con self-attention.



