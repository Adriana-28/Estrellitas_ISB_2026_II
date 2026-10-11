# Transformada wavelet

## Definición de wavelet
Es una onda corta que tiene un fin, a diferencia del seno que no tiene un límite. Su energía se concentra en un intervalo pequeño de tiempo.
Tiene tres caracteristicas principales: duración finita, localización temporal y es multiescala. 

Todas las wavelets de una familia salen de una sola: la wavelet madre ψ(t). Esta se puede escalar y trasladar. 
 ψ_a,b(t) = (1/√|a|) · ψ((t - b) / a)

El parámetro "b" mueve la wavelet en el tiempo y el parámetro "a" la comprime o estira. 
| Escala | Wavelet | Detecta |
|---|---|---|
| Pequeña | Comprimida | Altas frecuencias, eventos rápidos |
| Grande | Expandida | Bajas frecuencias, tendencias lentas |

## Diferencia con Fourier
Fourier descompone la señal en senos infinitos. Te dice las frecuencias que hay, pero no en que momento aparecen. La wavelet conserva la información de tiempo.

## Transformada wavelet continua (CWT)
La fórmula es 
W(a,b) = (1/√|a|) ∫ x(t) ψ*((t−b)/a) dt
Es una correlación entre la señal y la wavelet. 
La wavelet se desliza por la señal y en cada instante mide cuánto se le parece. El resultado es un escalograma: tiempo en X, escala o frecuencia en Y, energía en color.
Sirve para Ver y explorar señales no estacionarias y  Ubicar eventos transitorios.
El problema con la CWT es que es lenta y un poco redundante. 

## Transformada wavelet discreta (DWT)
La DWT usa escalas en potencias de 2 y se calcula con un banco de filtros:
1. La señal pasa por un pasa-bajas h0 y un pasa-altas h1.
2. Cada salida se decima por 2.
3. Salen cA (aproximación) y cD (detalle), cada una con unas N/2 muestras.
4. El proceso se repite solo sobre cA.

## Familias de wavelets
### Discretas
| Familia | Código | Característica |
|---|---|---|
| Haar | `haar` | Escalón +1/−1, la más simple, discontinua |
| Daubechies | `db2`...`dbN` | Soporte compacto, N momentos nulos. db4 se parece al QRS |
| Symlets | `symN` | Daubechies casi simétricas, menos distorsión de fase |
| Coiflets | `coifN` | Momentos nulos también en la función de escala |
| Biortogonales | `biorX.Y`, `rbioX.Y` | Simétricas, con filtros distintos para descomponer y reconstruir |
| Meyer discreta | `dmey` | Aproximación FIR de la wavelet de Meyer |

### Continuas
| Familia | Código | Característica |
|---|---|---|
| Morlet | `morl` | Seno modulado por una gaussiana |
| Sombrero mexicano | `mexh` | Segunda derivada de una gaussiana, detecta picos |
| Gaussianas | `gausN` | Derivadas de una gaussiana, detectan bordes |
| Morlet compleja | `cmorB-C` | La más usada para escalogramas |
| Gaussianas complejas | `cgauN` | Versión compleja de gaus |
| Shannon | `shanB-C` | Muy buena resolución en frecuencia |
| B-spline de frecuencia | `fbspM-B-C` | Generaliza a Shannon |

## Aplicaciones 
- ECG: detección de QRS, variabilidad cardiaca (HRV), eliminación de línea base y ruido.
- EEG: bandas cerebrales (delta, theta, alfa, beta), epilepsia, artefactos.
- EMG: fatiga y activación muscular.

## Filtros adaptativos (LMS)
Un filtro de coeficientes fijos pierde eficacia cuando el ruido cambia con el tiempo. 
Este funciona como un ciclo de prueba y error:
1. Filtra y obtiene una salida y(n).
2. La compara con lo que debería salir, d(n). La diferencia es el error: e(n) = d(n) − y(n).
3. Corrige sus coeficientes un poquito para equivocarse menos la próxima vez.
4. Repite miles de veces por segundo.



