import pyaudio
import wave
import numpy as np
import threading
import time
from extract_intention import extract_intention

def record_audio(filename, duration=5, rate=16000):
    """Graba audio desde el micrófono y lo guarda en un archivo WAV"""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=1024)
    frames = []
    for _ in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def build_enriched_prompt(intention, user_text):
    """Construye un prompt enriquecido con la intención detectada"""
    label = intention.get("label", "neutral")
    rhythm = intention.get("rhythm", 0)
    energy = intention.get("energy", 0)
    
    base_prompt = f"Usuario dice: '{user_text}'\n"
    
    if label == "high_energy_urgent":
        base_prompt += "[Intención detectada: URGENTE - alta energía y ritmo rápido. Responde de manera concisa y directa, priorizando acción.]\n"
    elif label == "hesitant_doubtful":
        base_prompt += "[Intención detectada: DUDA - muchas pausas. Responde con explicaciones claras y ofrece más información sin presión.]\n"
    elif label == "dull_low_mood":
        base_prompt += "[Intención detectada: BAJO ESTADO DE ÁNIMO - tono grave. Responde con empatía y tono calmado.]\n"
    else:
        base_prompt += "[Intención detectada: neutral. Respuesta normal.]\n"
    
    base_prompt += f"\nParámetros adicionales: ritmo={rhythm:.2f} pausas/segundo, energía={energy:.3f}\n"
    base_prompt += "Genera una respuesta adecuada a esta intención:"
    
    return base_prompt

def onda_hz_demo():
    print("=== Onda-HZ Demo ===")
    print("Voy a grabar 5 segundos de tu voz. Habla normalmente.")
    input("Presiona ENTER para empezar a grabar...")
    
    audio_file = "temp_speech.wav"
    record_audio(audio_file, duration=5)
    print("Grabación completada. Analizando intención...")
    
    intention = extract_intention(audio_file)
    print("Intención detectada:", intention)
    
    user_text = input("\nAhora escribe lo que dijiste (transcripción manual, por ahora): ")
    
    enriched_prompt = build_enriched_prompt(intention, user_text)
    print("\n=== Prompt enriquecido ===")
    print(enriched_prompt)
    
    print("\n[Demo sin IA real - este prompt se enviaría a DeepSeek, Claude, etc.]")
    print("El sistema ya puede extraer intención y formatear el prompt. Falta conectar con una API de IA.")
    
    # Limpiar archivo temporal
    import os
    os.remove(audio_file)

if __name__ == "__main__":
    onda_hz_demo()
