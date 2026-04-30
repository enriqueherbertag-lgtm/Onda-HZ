import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import find_peaks

def extract_intention(audio_path):
    # Cargar audio
    rate, data = wav.read(audio_path)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # stereo a mono
    data = data / np.max(np.abs(data))  # normalizar
    
    # 1. Energía media (amplitud general)
    energy = np.mean(data**2)
    
    # 2. Variación de amplitud (dinámica)
    amplitude_variation = np.std(np.abs(data))
    
    # 3. Detección de pausas (señales de baja energía)
    window_size = int(rate * 0.02)  # 20 ms
    energy_envelope = np.convolve(data**2, np.ones(window_size)/window_size, mode='same')
    pause_threshold = 0.01 * np.max(energy_envelope)
    pauses = energy_envelope < pause_threshold
    pause_duration = np.sum(pauses) / rate
    pause_ratio = pause_duration / (len(data)/rate)
    
    # 4. Ritmo estimado (detección de picos en la envolvente)
    peaks, _ = find_peaks(energy_envelope, height=0.05*np.max(energy_envelope), distance=rate*0.1)
    if len(peaks) > 1:
        rhythm = rate / np.mean(np.diff(peaks))  # picos por segundo
    else:
        rhythm = 0
    
    # 5. Inclinación espectral (brillo, agudo vs grave)
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1/rate)
    # Evitar frecuencias muy bajas o ruido extremo
    valid = (freqs[1:50] > 0) & (np.abs(fft[1:50]) > 1e-6)
    if np.sum(valid) > 1:
        spectral_slope = np.polyfit(freqs[1:50][valid], np.abs(fft[1:50])[valid], 1)[0]
    else:
        spectral_slope = -600  # valor por defecto si no se puede calcular
    
    # Diccionario con parámetros crudos
    intention = {
        "energy": float(energy),
        "amplitude_variation": float(amplitude_variation),
        "pause_ratio": float(pause_ratio),
        "rhythm": float(rhythm),
        "spectral_slope": float(spectral_slope)
    }
    
    # Clasificación mejorada (4 estados)
    intention["label"] = classify_intention(
        intention["energy"],
        intention["rhythm"],
        intention["pause_ratio"],
        intention["spectral_slope"]
    )
    
    return intention

def classify_intention(energy, rhythm, pause_ratio, spectral_slope):
    """
    Clasifica la intención según parámetros acústicos.
    Retorna: 'high_energy_urgent', 'low_mood_slow', 'hesitant_doubtful', 'neutral'
    """
    # Urgente: energía alta, ritmo rápido, pocas pausas
    if energy > 0.12 and rhythm > 3.0 and pause_ratio < 0.5:
        return "high_energy_urgent"
    
    # Triste/Lento: energía baja, ritmo lento, muchas pausas, tono grave
    if energy < 0.10 and rhythm < 2.5 and pause_ratio > 0.6 and spectral_slope < -500:
        return "low_mood_slow"
    
    # Dudoso: ritmo muy lento, muchas pausas (independientemente de energía)
    if rhythm < 2.0 and pause_ratio > 0.5:
        return "hesitant_doubtful"
    
    # Neutro: cualquier otro caso
    return "neutral"

# Ejemplo de uso directo
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_intention(sys.argv[1])
        print("=== Parámetros extraídos ===")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("Uso: python3 extract_intention.py archivo.wav")
