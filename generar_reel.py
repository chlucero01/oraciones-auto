from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap, subprocess, os, random

ORACIONES = [
    "Señor, al caer la noche te entrego mis preocupaciones, mis alegrías y mi familia. Gracias por este día. Dame descanso y paz. Amén.",
    "Padre amado, gracias por tu protección hoy. En tus manos dejo mi noche y mi descanso. Amén."
]

def crear_imagen(texto, salida="fondo.png"):
    img = Image.new('RGB', (1080,1920), (15,23,42))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
    except: font = ImageFont.load_default()
    t = "\n".join(textwrap.wrap(texto, width=22))
    bbox = draw.multiline_textbbox((0,0), t, font=font, align="center", spacing=15)
    x = (1080-(bbox[2]-bbox[0]))//2
    y = (1920-(bbox[3]-bbox[1]))//2
    draw.multiline_text((x+4,y+4), t, font=font, fill=(0,0,0,180), align="center", spacing=15)
    draw.multiline_text((x,y), t, font=font, fill="white", align="center", spacing=15)
    img.save(salida)

def crear_reel(oracion=None, salida="reel.mp4"):
    if not oracion: oracion = random.choice(ORACIONES)
    crear_imagen(oracion, "fondo.png")
    gTTS(oracion, lang='es').save("voz.mp3")

    if os.path.exists("musica.mp3"):
        cmd = ["ffmpeg","-y","-loop","1","-i","fondo.png","-i","voz.mp3","-i","musica.mp3","-filter_complex","[1:a]volume=1.0;[2:a]volume=0.15;amix=inputs=2:duration=longest[a]","-map","0:v","-map","[a]","-c:v","libx264","-t","12","-pix_fmt","yuv420p","-vf","scale=1080:1920","-shortest",salida]
    else:
        cmd = ["ffmpeg","-y","-loop","1","-i","fondo.png","-i","voz.mp3","-c:v","libx264","-t","12","-pix_fmt","yuv420p","-vf","scale=1080:1920","-shortest",salida]
    subprocess.run(cmd, check=True)
    print(f"Listo {salida}")

if __name__ == "__main__":
    crear_reel()
