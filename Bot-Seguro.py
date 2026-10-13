
import requests
import os
from datetime import datetime

# Lee las llaves desde GitHub Secrets - no las escribas aquí
PAGE_ID = os.environ.get("PAGE_ID")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GRAPH_VERSION = "v19.0"

CONTENIDO = {
    "manana": "☀️ Oración de la mañana\n\nSeñor, hoy salgo con tu bendición. Guía mis pasos, cuida mi camino y que todo lo que haga sea para tu gloria. Amén. 🙏\n\n#OracionDeLaManana #DiosAcompañameHoy",
    "tarde": "✨ Dios ya está trabajando en lo que te preocupa. Solo confía.\n\nComparte si lo crees. 🙏\n\n#Reflexion #Fe",
    "noche": "🌙 Oración de la noche - Hoy se rompen las cadenas\n\nEn el nombre de Jesús, toda cadena de enfermedad, deuda y tristeza se rompe hoy. Escribe SOY LIBRE 🙏⛓️‍💥\n\n#OracionDeLaNoche #RompeCadenas"
}

def publicar(mensaje):
    if not PAGE_ID or not PAGE_ACCESS_TOKEN:
        print("ERROR: Faltan PAGE_ID o PAGE_ACCESS_TOKEN en Secrets")
        return
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed"
    r = requests.post(url, data={"message": mensaje, "access_token": PAGE_ACCESS_TOKEN})
    print(f"Status: {r.status_code} - {r.json()}")

if __name__ == "__main__":
    hora_utc = datetime.utcnow().hour
    # Texas es UTC-5, convertimos: 7am TX = 12 UTC, 1pm TX = 18 UTC, 8:30pm TX = 1:30 UTC
    print(f"Hora UTC actual: {hora_utc}")
    # Publica según la hora que GitHub lo ejecutó
    # Si lo ejecutas manual, publica el de la mañana por defecto
    import sys
    tipo = sys.argv[1] if len(sys.argv) > 1 else "manana"
    print(f">>> Publicando: {tipo}")
    publicar(CONTENIDO.get(tipo, CONTENIDO["manana"]))
