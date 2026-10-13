
import requests
import json
from datetime import datetime

# CONFIGURACION - Llena esto con tus datos
PAGE_ID = "1105755881848979"
PAGE_ACCESS_TOKEN = "EAAPtrdqLwJMBSnAApDqS8Rcf9qjmCO63jNc9TxiUH2OlaAUZCEe7u48cXPaNSHLfIolfTvzPTOG1sPDBe89MZCE8kM2ILLmA4dPuriqNDPgr9AZAoqFslkaHZATstTc7X8yfvG1ho0Rx065ITk2kAkxxdkjoPHnf7srq8079tcZCBxC86MgJJ6ozQDv1nPaRk3jZAIZCogOZBCRiovBzImaV9uK5b8uC9uicLw2CqifAqS7bPpu4ZAx7YLQvRAd4Flkp2NekxgpXEfj6ZBuiFzGrG6HwDE5cLjK0aW78QZD"
GRAPH_VERSION = "v19.0"

# Tu calendario de contenido - Ya viene con tus 4 oraciones
CONTENIDO = {
    "manana": {
        "texto": "☀️ Oración de la mañana\n\nSeñor, hoy salgo con tu bendición. Guía mis pasos, cuida mi camino y que todo lo que haga sea para tu gloria. Amén. 🙏\n\n#OracionDeLaManana #DiosAcompañameHoy",
        "video_path": None  # Puedes poner URL del video
    },
    "tarde": {
        "texto": "✨ Dios ya está trabajando en lo que te preocupa. Solo confía.\n\nComparte si lo crees. 🙏\n\n#Reflexion #Fe",
        "imagen_url": "https://ejemplo.com/imagen.jpg"
    },
    "noche": {
        "texto": "🌙 Oración de la noche - Hoy se rompen las cadenas\n\nEn el nombre de Jesús, toda cadena de enfermedad, deuda y tristeza se rompe hoy. Escribe SOY LIBRE 🙏⛓️‍💥\n\n#OracionDeLaNoche #RompeCadenas"
    }
}

def publicar_texto_en_pagina(mensaje):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed"
    payload = {
        "message": mensaje,
        "access_token": PAGE_ACCESS_TOKEN
    }
    r = requests.post(url, data=payload)
    print(f"Publicando texto: {r.status_code}")
    print(r.json())
    return r.json()

def publicar_imagen_en_pagina(mensaje, imagen_url):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/photos"
    payload = {
        "message": mensaje,
        "url": imagen_url,
        "access_token": PAGE_ACCESS_TOKEN
    }
    r = requests.post(url, data=payload)
    print(f"Publicando imagen: {r.status_code}")
    print(r.json())
    return r.json()

def publicar_reel_en_pagina(video_url, descripcion):
    # PASO 1: Iniciar subida de reel
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/video_reels"
    payload = {
        "upload_phase": "start",
        "access_token": PAGE_ACCESS_TOKEN
    }
    r = requests.post(url, data=payload)
    data = r.json()
    print("Inicio reel:", data)
    
    video_id = data.get("video_id")
    
    # PASO 2: Subir video (simplificado - necesitas subir el archivo)
    # Para Reels necesitas usar Resumable Upload, aquí te dejo la base
    # En produccion usar: https://graph.facebook.com/v19.0/{video_id}
    
    # PASO 3: Publicar
    publish_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/video_reels"
    publish_payload = {
        "video_id": video_id,
        "upload_phase": "finish",
        "video_state": "PUBLISHED",
        "description": descripcion,
        "access_token": PAGE_ACCESS_TOKEN
    }
    r2 = requests.post(publish_url, data=publish_payload)
    print("Publicar reel:", r2.json())
    return r2.json()

if __name__ == "__main__":
    ahora = datetime.now()
    hora = ahora.hour
    
    if 7 <= hora < 9:
        print(">>> Publicando ORACION DE LA MAÑANA")
        publicar_texto_en_pagina(CONTENIDO["manana"]["texto"])
    elif 12 <= hora < 14:
        print(">>> Publicando REFLEXION DE TARDE")
        # Si tienes imagen usa publicar_imagen_en_pagina
        publicar_texto_en_pagina(CONTENIDO["tarde"]["texto"])
    elif 19 <= hora < 22:
        print(">>> Publicando REEL DE NOCHE")
        publicar_texto_en_pagina(CONTENIDO["noche"]["texto"])
    else:
        print(f"Fuera de horario programado ({hora}h). No se publica nada.")
