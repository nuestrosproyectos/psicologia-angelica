#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera con ElevenLabs las locuciones del ejercicio "Respira conmigo":

    assets/audio/inhala.wav    "Inhala…"
    assets/audio/sosten.wav    "Sostén…"
    assets/audio/exhala.wav    "Suelta el aire… despacio."
    assets/audio/muybien.wav   "Así… muy bien."

En cuanto existen, la web muestra sola el botón "🔊 con la voz de Angélica"
(nunca suena de forma automática: el visitante lo activa).

Uso:
    export ELEVENLABS_API_KEY=...      (o ponla como secreto del entorno)
    python scripts/generar-voz-respira.py            # genera los 4 clips
    python scripts/generar-voz-respira.py --listar   # lista voces disponibles
    ELEVEN_VOICE_ID=<id> python scripts/generar-voz-respira.py  # otra voz

La voz por defecto es "Sarah" (cálida, sirve en español con el modelo
multilingüe). Cuando Angélica grabe o elija su voz clonada, pasa su
voice_id por ELEVEN_VOICE_ID y regenera.
"""
import json, os, sys, urllib.request, wave

API = "https://api.elevenlabs.io/v1"
CLAVE = os.environ.get("ELEVENLABS_API_KEY", "").strip()
VOZ = os.environ.get("ELEVEN_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Sarah

CLIPS = {
    "inhala.wav":  "Inhala…",
    "sosten.wav":  "Sostén…",
    "exhala.wav":  "Suelta el aire… despacio.",
    "muybien.wav": "Así… muy bien.",
}

def pedir(url, datos=None):
    # Si no hay clave en el entorno, la inyecta la pasarela de Claude (credencial
    # del entorno): en ese caso NO mandamos la cabecera para no pisarla en vacío.
    cab = {"Content-Type": "application/json"}
    if CLAVE: cab["xi-api-key"] = CLAVE
    req = urllib.request.Request(url, headers=cab,
                                 data=json.dumps(datos).encode() if datos else None)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def main():
    if "--listar" in sys.argv:
        voces = json.loads(pedir(API + "/voices"))["voices"]
        for v in voces:
            print(f"{v['voice_id']}  {v['name']}  {v.get('labels', {})}")
        return

    destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio")
    os.makedirs(destino, exist_ok=True)
    for nombre, texto in CLIPS.items():
        print(f"→ {nombre}: “{texto}”")
        audio = pedir(f"{API}/text-to-speech/{VOZ}?output_format=pcm_24000", {
            "text": texto,
            "model_id": "eleven_multilingual_v2",
            # Ajustes para una voz serena, lenta y cercana (no locutora de anuncio)
            "voice_settings": {"stability": 0.6, "similarity_boost": 0.75, "style": 0.25, "speed": 0.85},
        })
        with wave.open(os.path.join(destino, nombre), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes(audio)
    print(f"\nListo: {len(CLIPS)} clips en {destino}/")
    print("Sube los cambios y el botón de voz aparecerá solo en la web.")

if __name__ == "__main__":
    main()
