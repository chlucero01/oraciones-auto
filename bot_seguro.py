
import requests
import os
import sys
from datetime import datetime

PAGE_ID = os.environ.get("PAGE_ID")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GRAPH_VERSION = "v19.0"

print(f"DEBUG: PAGE_ID recibido = {PAGE_ID}")
print(f"DEBUG: TOKEN recibido = {'SI' if PAGE_ACCESS_TOKEN else 'NO'} - largo {len(PAGE_ACCESS_TOKEN) if PAGE_ACCESS_TOKEN else 0}")

if not PAGE_ID or not PAGE_ACCESS_TOKEN:
    print("❌ ERROR: Faltan PAGE_ID o PAGE_ACCESS_TOKEN en GitHub Secrets")
    print("Ve a Settings > Secrets and variables > Actions")
    sys.exit(1)

CONTENIDO = {
    "manana": "☀️ Oración de la mañana\n\nSeñor, hoy salgo con tu bendición. Guía mis pasos, cuida mi camino y que todo lo que haga sea para tu gloria. Amén. 🙏\n\n#OracionDeLaManana #DiosAcompañameHoy",
    "tarde": "✨ Dios ya está trabajando en lo que te preocupa. Solo confía.\n\nComparte si lo crees. 🙏\n\n#Reflexion #Fe",
    "noche": "🌙 Oración de la noche - Hoy se rompen las cadenas\n\nEn el nombre de Jesús, toda cadena de enfermedad, deuda y tristeza se rompe hoy. Escribe SOY LIBRE 🙏⛓️‍💥\n\n#OracionDeLaNoche #RompeCadenas"
}

def publicar(mensaje):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed"
    print(f"Intentando publicar en: https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed")
    r = requests.post(url, data={"message": mensaje, "access_token": PAGE_ACCESS_TOKEN})
    print(f"Status Code: {r.status_code}")
    print(f"Respuesta de Facebook: {r.text}")

    data = r.json()
    if "error" in data:
        print(f"❌ ERROR DE FACEBOOK: {data['error']}")
        # Si el ID es incorrecto
        if data['error'].get('code') == 803:
            print("👉 Tu PAGE_ID está mal. Es el ID de la App, no de la Página.")
        if data['error'].get('code') == 190:
            print("👉 Tu TOKEN expiró o es de usuario, no de Página. Saca uno nuevo en Graph API Explorer > Get Page Access Token")
        sys.exit(1)  # Esto hace que GitHub marque la X roja para que veas el error
    else:
        print(f"✅ ¡PUBLICADO! Post ID: {data.get('id')}")
        return data

if __name__ == "__main__":
    tipo = sys.argv[1] if len(sys.argv) > 1 else "manana"
    print(f">>> Intentando publicar: {tipo}")
    publicar(CONTENIDO.get(tipo, CONTENIDO["manana"]))
