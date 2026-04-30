# 🌊 Onda-HZ

[![Licencia](https://img.shields.io/badge/Licencia-Copyright%20%28c%29%202026%20Enrique%20Aguayo-red)](LICENSE)
[![Estado](https://img.shields.io/badge/Estado-Prototipo%20funcional-brightgreen)](https://github.com/enriqueherbertag-lgtm/Onda-HZ)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Groq](https://img.shields.io/badge/IA-Groq-ff69b4)](https://groq.com)
[![GitHub last commit](https://img.shields.io/github/last-commit/enriqueherbertag-lgtm/Onda-HZ)](https://github.com/enriqueherbertag-lgtm/Onda-HZ)
[![GitHub stars](https://img.shields.io/github/stars/enriqueherbertag-lgtm/Onda-HZ?style=social)](https://github.com/enriqueherbertag-lgtm/Onda-HZ)

**Sistema de recepción de intención por modulación de frecuencia.**

La IA percibe urgencia, duda o tristeza en la voz del usuario y adapta su respuesta. No lee la mente. Lee la música del habla antes de que sea palabras.

---

## 📄 Teoría

Este repositorio es la **implementación práctica** del concepto publicado en:

> **Onda-HZ: sistema de recepción de intención por modulación de frecuencia**  
> Enrique Aguayo H. – Mackiber Labs  
> DOI: [10.5281/zenodo.XXXXXX](https://doi.org/10.5281/zenodo.XXXXXX) (artículo conceptual)

El artículo describe cómo la forma de la onda (frecuencia, amplitud, modulación) transporta intención más allá del contenido semántico.

**Este repositorio comprueba experimentalmente esa hipótesis.**

---

## 🎯 ¿Qué hace?

| Paso | Descripción |
|------|-------------|
| 1 | Graba 5 segundos de voz |
| 2 | Extrae parámetros acústicos: energía, ritmo, pausas, tono |
| 3 | Clasifica la intención (urgente, neutral, dudoso, triste/lento) |
| 4 | Construye un prompt enriquecido con la intención detectada |
| 5 | Envía el prompt a Groq (IA gratuita) |
| 6 | La IA responde adaptada al estado del usuario |

---

## 📊 Parámetros extraídos

| Parámetro | Qué mide | Rango típico |
|-----------|----------|--------------|
| `energy` | Volumen/amplitud media | 0.0 - 0.5 |
| `rhythm` | Ritmo del habla (picos/segundo) | 1.0 - 6.0 |
| `pause_ratio` | Proporción de silencios | 0.2 - 0.8 |
| `spectral_slope` | Brillo (agudo=positivo, grave=negativo) | -1000 a +500 |

---

## 🧠 Clasificación de intención

| Estado | Energía | Ritmo | Pausas | Tono |
|--------|---------|-------|--------|------|
| **Urgente** | > 0.12 | > 3.0 | < 0.5 | cualquiera |
| **Neutral** | 0.08-0.15 | 2.0-3.0 | 0.3-0.6 | > -600 |
| **Triste/Lento** | < 0.10 | < 2.5 | > 0.6 | < -500 |
| **Dudoso** | cualquiera | < 2.0 | > 0.5 | cualquiera |

---

## 🚀 Cómo probarlo

```bash
# Clonar el repositorio
git clone https://github.com/enriqueherbertag-lgtm/Onda-HZ
cd Onda-HZ

# Instalar dependencias
pip3 install -r requirements.txt

# Configurar API key de Groq
cp config.example.py config.py
# Edita config.py y añade tu clave (gratuita en https://console.groq.com)

# Ejecutar
python3 onda_hz_v2.py

# Ejemplo de ejecución
Usuario (tono urgente): "hola estoy probando esto"
Intención detectada: high_energy_urgent
Groq responde: "¡Genial! ¿En qué puedo ayudarte? Estoy listo para responder de manera rápida y eficiente."

Usuario (tono neutro): "hola esto es una prueba número 3"
Intención detectada: neutral
Groq responde: "¡Hola! Entiendo que esto es una prueba número 3. ¿En qué puedo ayudarte hoy?"

Usuario (tono desganado, ritmo rápido): "hola cómo estás yo más o menos"
Intención detectada: high_energy_urgent
Groq responde: "¡Hola! ¿Qué pasa? ¿Necesitas algo urgente? ¿En qué puedo ayudarte?"

# Relación con otros proyectos

Proyecto	Relación
CORPUS	Onda-HZ puede ser el sistema de percepción social de un cuerpo artificial
Resonador-432	Mismos principios de vibración adaptativa aplicados a la salud
OsteoFlux	Vibración adaptativa para osteoporosis
PaintCell-Automotriz	Generación distribuida y almacenamiento modular


# Estructura del repositorio


Onda-HZ/
├── README.md               # Este archivo
├── LICENSE                 # Licencia propietaria
├── requirements.txt        # Dependencias Python
├── config.example.py       # Ejemplo de configuración
├── extract_intention.py    # Extracción de parámetros acústicos
├── onda_hz_v2.py           # Script principal
└── paper/                  # Enlace al artículo en Zenodo


## Proyectos relacionados

- ENA — interfaz cerebro-máquina no invasiva
- Quantum-Flux — comunicaciones resilientes
- ShieldAir — torres de producción de oxígeno
- Motor de Oxígeno — propulsión limpia


## Licencia

Copyright © 2026 Enrique Aguayo. Todos los derechos reservados.

Este proyecto está protegido por derechos de autor.

PERMITIDO:
- Uso no comercial con fines educativos o de investigación.
- Distribución sin modificación, siempre que se mantenga esta licencia y se dé crédito al autor.

PROHIBIDO sin autorización expresa por escrito:
- Uso comercial (incluyendo, pero no limitado a: ofrecerlo como servicio, SaaS, suscripción, integración en productos que generen ingresos, o cualquier uso que genere beneficio económico directo o indirecto).
- Modificación para entornos de producción.
- Distribución de versiones modificadas sin autorización.

Para licencias comerciales, soporte técnico, pilotos empresariales o consultas:
Contacto: eaguayo@migst.cl

Cualquier uso fuera de los términos permitidos requiere permiso previo del autor.

Las consultas comerciales son bienvenidas y se responderán en un plazo máximo de 7 días hábiles.

## Autor

Enrique Aguayo H.
Mackiber Labs
Contacto: eaguayo@migst.cl
ORCID: 0009-0004-4615-6825
GitHub: @enriqueherbertag-lgtm

Documentación asistida por Ana (DeepSeek IA. asistente tecnico.

