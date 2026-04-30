from config import GROQ_API_KEY
import pyaudio
import wave
import numpy as np
import requests
import json
import os
from extract_intention import extract_intention  # Asegúrate de tener este módulo

GROQ_API_KEY = "  "
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def record_audio(filename, duration=5, rate=16000):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=1024)
    frames = []
    for _ in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024, exception_on_overflow=False)
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

def classify_intention(energy, rhythm, pause_ratio, spectral_slope):
    if energy > 0.12 and rhythm > 3.0 and pause_ratio < 0.5:
        return "high_energy_urgent"
    elif energy < 0.10 and rhythm < 2.5 and pause_ratio > 0.6 and spectral_slope < -500:
        return "low_mood_slow"
    elif rhythm < 2.0 and pause_ratio > 0.5:
        return "hesitant_doubtful"
    else:
        return "neutral"

def build_enriched_prompt(intention, user_text):
    label = intention.get("label", "neutral")
    rhythm = intention.get("rhythm", 0)
    energy = intention.get("energy", 0)
    pause_ratio = intention.get("pause_ratio", 0)
    
    base_prompt = f"Usuario dice: '{user_text}'\n"
    
    if label == "high_energy_urgent":
        base_prompt += "[Intención: URGENTE - alta energía, ritmo rápido. Responde conciso, directo y prioriza acción.]\n"
    elif label == "low_mood_slow":
        base_prompt += "[Intención: TRISTE/LENTO - baja energía, ritmo lento, tono grave. Responde con empatía, calidez y sin prisas.]\n"
    elif label == "hesitant_doubtful":
        base_prompt += "[Intención: DUDOSO - muchas pausas, ritmo lento. Responde con explicaciones claras, evitando lenguaje complejo.]\n"
    else:
        base_prompt += "[Intención: NEUTRAL - tono equilibrado. Respuesta estándar.]\n"
    
    base_prompt += f"\nParámetros: ritmo={rhythm:.2f} | pausas={pause_ratio:.2f} | energía={energy:.3f}\n"
    base_prompt += "Genera respuesta adaptada a esta intención:"
    
    return base_prompt

def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def onda_hz_v2():
    print("=== Onda-HZ v2 (mejores umbrales) ===")
    input("Presiona ENTER para grabar 5 segundos...")
    
    audio_file = "temp_speech.wav"
    record_audio(audio_file, duration=5)
    print("Grabación completada. Analizando intención...")
    
    intention_raw = extract_intention(audio_file)  # Diccionario con todos los parámetros
    # Añadir la clasificación mejorada
    intention_raw["label"] = classify_intention(
        intention_raw["energy"],
        intention_raw["rhythm"],
        intention_raw["pause_ratio"],
        intention_raw["spectral_slope"]
    )
    
    print("\n--- Intención detectada ---")
    for key, value in intention_raw.items():
        print(f"{key}: {value}")
    
    user_text = input("\nEscribe lo que dijiste: ")
    enriched_prompt = build_enriched_prompt(intention_raw, user_text)
    
    print("\n--- Prompt enviado a Groq ---")
    print(enriched_prompt)
    
    print("\n--- Respuesta de Groq ---")
    response = call_groq(enriched_prompt)
    print(response)
    
    os.remove(audio_file)

if __name__ == "__main__":
    onda_hz_v2()
