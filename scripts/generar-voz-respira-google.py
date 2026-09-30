#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las locuciones de "Respira conmigo" con la API de Google (Gemini TTS).

Equivalente a generar-voz-respira.py (ElevenLabs) pero usando Gemini, útil
cuando la credencial de Google está configurada en el entorno (la clave la
inyecta la pasarela como cabecera x-goog-api-key; si no, exporta
GEMINI_API_KEY y se envía como parámetro).

    python scripts/generar-voz-respira-google.py [voz]   # por defecto: Sulafat

Voces femeninas que encajan (cálidas/serenas): Sulafat, Enceladus (susurrante),
Achernar (suave), Vindemiatrix (gentil), Aoede, Leda.
Guarda WAV (PCM 24 kHz) directamente: sin dependencias externas.
"""
import base64, json, os, sys, urllib.request, wave

MODELO = "gemini-3.8-flash-tts"
VOZ = sys.argv[1] if len(sys.argv) > 1 else "Sulafat"
# OJO: este modelo TTS lee TODO el texto literalmente (no interpreta
# instrucciones de estilo), así que el texto va pelado y el tono lo da la voz.

CLIPS = {
    "inhala.wav":  "Inhala…",
    "sosten.wav":  "Sostén…",
    "exhala.wav":  "Suelta el aire… despacio.",
    "muybien.wav": "Así… muy bien.",
}

def main():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
    clave = os.environ.get("GEMINI_API_KEY", "").strip()
    if clave:
        url += f"?key={clave}"

    destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio")
    os.makedirs(destino, exist_ok=True)

    for nombre, texto in CLIPS.items():
        cuerpo = {
            "contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ}}},
            },
        }
        req = urllib.request.Request(url, data=json.dumps(cuerpo).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.load(r)
        parte = resp["candidates"][0]["content"]["parts"][0]["inlineData"]
        pcm = base64.b64decode(parte["data"])          # audio/L16 (PCM 24 kHz mono)
        with wave.open(os.path.join(destino, nombre), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes(pcm)
        print(f"✓ {nombre}  ({parte.get('mimeType','?')}, {len(pcm)//1000} KB pcm)")

    print(f"\nListo: {len(CLIPS)} clips en {destino}/ con la voz {VOZ}.")

if __name__ == "__main__":
    main()
