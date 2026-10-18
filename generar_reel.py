from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap, subprocess, os, json, random
from datetime import datetime
import pytz

def obtener_oracion_del_plan():
    tipo = "noche"
    hora_utc = datetime.utcnow().hour
    if hora_utc in [11,12,13]: tipo = "mañana"
    elif hora_utc in [17,18,19]: tipo = "tarde"
    else: tipo = "noche"

    # dia en Texas
    try:
        tz = pytz.timezone("America/Chicago")
        dia = datetime.now(tz).strftime("%A").lower()
        mapa = {"monday":"lunes","tuesday":"martes","wednesday":"miercoles","thursday":"jueves","friday":"viernes","saturday":"sabado","sunday":"domingo"}
        dia = mapa.get(dia, "lunes")
    except:
        dia = "lunes"

    if os.path.exists("plan_semanal.json"):
        with open("plan_semanal.json","r",encoding="utf-8") as f:
            data = json.load(f)
            oracion = data["plan"].get(dia, {}).get(tipo)
            if oracion:
                return tipo, oracion

    # fallback si no hay plan
    return tipo, "Señor, gracias por este día. Dame paz y descanso. Amén."

def crear_reel(salida="reel.mp4"):
    tipo, oracion = obtener_oracion_del_plan()
    titulo = f"Oración de la {tipo.capitalize()}"
    print(f"Publicando: {titulo}")

    bg = Image.open("fondo_noche.jpg").convert("RGB").resize((1080,1920)) if os.path.exists("fondo_noche.jpg") else Image.new("RGB",(1080,1920),(15,23,60))
    draw = ImageDraw.Draw(bg)
    try:
        font_title = ImageFont.truetype("DejaVuSerif-Bold.ttf", 80)
        font_body = ImageFont.truetype("DejaVuSerif.ttf", 44)
    except:
        font_title = ImageFont.load_default()
        font_body = font_title

    draw.multiline_text((540, 380), titulo, font=font_title, fill="white", align="center", anchor="mm", stroke_width=3, stroke_fill=(0,0,0,100))
    body = "\n".join(textwrap.wrap(oracion, width=26))
    draw.multiline_text((540, 850), body, font=font_body, fill=(255,250,210), align="center", anchor="mm", spacing=18, stroke_width=2, stroke_fill=(0,0,0,80))
    bg.save("fondo.png")

    with open("caption.txt","w",encoding="utf-8") as f:
        f.write(f"{titulo} 🙏 {oracion} #oracion #{tipo} #fe")

    gTTS(oracion, lang='es').save("voz.mp3")
    subprocess.run(["ffmpeg","-y","-loop","1","-i","fondo.png","-i","voz.mp3","-c:v","libx264","-t","12","-pix_fmt","yuv420p","-vf","scale=1080:1920","-shortest",salida], check=True)

if __name__ == "__main__":
    crear_reel()
