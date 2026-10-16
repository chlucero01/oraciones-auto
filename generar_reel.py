from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap, subprocess, os, random

ORACIONES = [
    "Señor, al caer la noche te entrego mis preocupaciones, mis alegrías y mi familia. Gracias por este día. Dame descanso y paz. Amén.",
]

def crear_reel(oracion=None, salida="reel.mp4"):
    if not oracion: oracion = random.choice(ORACIONES)

    # Usa el fondo bonito si existe
    if os.path.exists("fondo_noche.jpg"):
        bg = Image.open("fondo_noche.jpg").convert("RGB").resize((1080,1920))
    else:
        bg = Image.new("RGB", (1080,1920), (10,15,40))

    draw = ImageDraw.Draw(bg)
    try:
        font_title = ImageFont.truetype("DejaVuSerif-Bold.ttf", 78)
        font_body = ImageFont.truetype("DejaVuSerif.ttf", 42)
    except:
        font_title = ImageFont.load_default()
        font_body = font_title

    # Texto estilo original
    title = "Oración de\nla Noche"
    draw.multiline_text((540, 380), title, font=font_title, fill="white", align="center", anchor="mm", spacing=10)

    body = "\n".join(textwrap.wrap(oracion, width=26))
    draw.multiline_text((540, 850), body, font=font_body, fill=(255,250,220), align="center", anchor="mm", spacing=16)

    bg.save("fondo.png")
    gTTS(oracion, lang='es').save("voz.mp3")

    cmd = ["ffmpeg","-y","-loop","1","-i","fondo.png","-i","voz.mp3","-c:v","libx264","-t","12","-pix_fmt","yuv420p","-vf","scale=1080:1920","-shortest",salida]
    if os.path.exists("musica.mp3"):
        cmd = ["ffmpeg","-y","-loop","1","-i","fondo.png","-i","voz.mp3","-i","musica.mp3","-filter_complex","[1:a]volume=1.0[a1];[2:a]volume=0.12[a2];[a1][a2]amix=inputs=2:duration=longest[a]","-map","0:v","-map","[a]","-c:v","libx264","-t","12","-pix_fmt","yuv420p","-vf","scale=1080:1920","-shortest",salida]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    crear_reel()
