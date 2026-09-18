#Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch
from pathlib import Path

# Carpeta donde se encuentra BASAL1.py
carpeta = Path(__file__).resolve().parent

# Crear la carpeta resultados si todavía no existe
carpeta_resultados = carpeta / "resultados"
carpeta_resultados.mkdir(exist_ok=True)
#Definimos filtros con scipy.signal
def filtro_pasabanda(senal, fs, frec_baja=0.5, frec_alta=40.0, orden=4):
    nyquist = 0.5 * fs
    bajo = frec_baja / nyquist
    alto = frec_alta / nyquist
    b, a = butter(orden, [bajo, alto], btype="band")
    return filtfilt(b, a, senal)

def filtro_notch(senal, fs, frec_notch=60.0, Q=30.0):
    nyquist = 0.5 * fs
    w0 = frec_notch / nyquist
    b, a = iirnotch(w0, Q)
    return filtfilt(b, a, senal)
#Abrimos el archivo sin incluir las filas que inician con"#"
with open("EJERCICIOD3_2026-09-11_12-42-00.txt", "r") as f:
    lineas = f.readlines()

datos_limpios = [line.strip().split() for line in lineas if not line.startswith("#")]
datos = np.array(datos_limpios, dtype=float)

#Señal ECG y tiempo de muestreo
ecg = datos[:, -1] * -1   # señal ECG (última columna)
fs = 1000# frecuencia de muestreo
tiempo = np.arange(len(ecg)) / fs # vector de tiempo

#Aplicacion de filtros
ecg_filtrado = filtro_pasabanda(ecg, fs, 0.5, 40)
ecg_filtrado = filtro_notch(ecg_filtrado, fs, 60)

#FFT
fft_vals_cruda = np.fft.rfft(ecg) # Cruda
fft_freqs_cruda = np.fft.rfftfreq(len(ecg), 1/fs) # Cruda

fft_vals_filtrada = np.fft.rfft(ecg_filtrado) # Filtrada
fft_freqs_filtrada = np.fft.rfftfreq(len(ecg_filtrado), 1/fs) # Filtrada

# FFT en dB
fft_db_cruda = 20 * np.log10(np.abs(fft_vals_cruda) / np.max(np.abs(fft_vals_cruda)))
fft_db_filtrada = 20 * np.log10(np.abs(fft_vals_filtrada) / np.max(np.abs(fft_vals_filtrada)))

# Ploteo de señales
# Señal cruda
plt.figure(figsize=(14, 4))
plt.plot(tiempo, ecg, color="darkblue", linewidth=0.6)
plt.title("Señal ECG derivada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.xlim(0, 5)
plt.grid()
# Guardar la imagen antes de mostrarla
plt.savefig(
    carpeta_resultados / "ECG_ejercicio_cruda(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
# FFT de señal cruda
plt.figure(figsize=(10, 4))
plt.plot(fft_freqs_cruda, np.abs(fft_vals_cruda), color="darkorange", linewidth=0.6)
plt.title("Espectro de frecuencias (FFT) - ECG")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.xlim(0, 200)
plt.ylim(0, 150000)
plt.grid()
plt.savefig(
    carpeta_resultados / "ECG_FFT_ejercicio(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# FFT de señal cruda en dB
plt.figure(figsize=(10, 4))
plt.plot(fft_freqs_cruda, fft_db_cruda, color="darkgreen", linewidth=0.6)
plt.title("Espectro de frecuencias en dB - ECG")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud [dB]")
plt.xlim(0, 200)
plt.ylim(-200, 5)
plt.grid()
plt.savefig(
    carpeta_resultados / "ECG_FFT_ejercicio_EN_dB(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Señal filtrada-zoom
plt.figure(figsize=(14, 4))
plt.plot(tiempo, ecg_filtrado, color="darkblue", linewidth=0.8)
plt.title("Señal ECG filtrada: Pasabanda + notch" )
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud ")
plt.xlim(0, 35)
plt.grid()
plt.savefig(
    carpeta_resultados / "ECG_ejercicio_filtrada(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# FFT de señal filtrada
plt.figure(figsize=(10, 4))
plt.plot(fft_freqs_filtrada, np.abs(fft_vals_filtrada), color="darkorange", linewidth=0.6)
plt.title("Espectro de frecuencias (FFT) - ECG filtrado")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.xlim(0, 200)
plt.ylim(0, 150000)
plt.grid()
plt.savefig(
    carpeta_resultados / "ECG_ejercicio_FFT_filtrada(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# FFT de señal filtrada en dB
plt.figure(figsize=(10, 4))
plt.plot(fft_freqs_filtrada, fft_db_filtrada, color="darkgreen", linewidth=0.6)
plt.title("Espectro de frecuencias en dB - ECG filtrado")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud [dB]")
plt.xlim(0, 75)
plt.ylim(-200, 5)
plt.grid()
plt.savefig(
    carpeta_resultados / "ECG_FFT_ejercicio_EN_dB_filtrada(2).png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
