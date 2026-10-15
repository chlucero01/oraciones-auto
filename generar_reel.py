from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
import numpy as np

def crear_imagen_texto(texto, size=(1080,1920)):
    # Fondo oscuro
    img = Image.new('RGB', size, (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuente grande, si no usa la default
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 68)
    except:
        font = ImageFont.load_default()

    # Envolver texto
    lineas = textwrap.wrap(texto, width=22)
    texto_envuelto = "\n".join(lineas)

    # Calcular centro
    bbox = draw.multiline_textbbox((0,0), texto_envuelto, font=font, align="center", spacing=15)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size[0] - w)//2
    y = (size[1] - h)//2

    # Sombra + texto blanco
    draw.multiline_text((x+4, y+4), texto_envuelto, font=font, fill=(0,0,0,180), align="center", spacing=15)
    draw.multiline_text((x, y), texto_envuelto, font=font, fill="white", align="center", spacing=15)

    return np.array(img)

def crear_reel(oracion, salida="reel.mp4"):
    # 1. Crear voz en español
    print("Creando voz...")
    tts = gTTS(text=oracion, lang='es', slow=False)
    tts.save("voz.mp3")
    audio_voz = AudioFileClip("voz.mp3")

    duracion = audio_voz.duration + 1.2

    # 2. Fondo animado simple (zoom lento)
    fondo_img = crear_imagen_texto(oracion)
    fondo_clip = ImageClip(fondo_img, duration=duracion)
    # efecto zoom lento para que se vea animado
    fondo_clip = fondo_clip.resize(lambda t: 1 + 0.03*t)
    fondo_clip = fondo_clip.set_position(('center','center'))

    # Fondo base de color para rellenar
    base = ColorClip(size=(1080,1920), color=(15,23,42), duration=duracion)

    video = CompositeVideoClip([base, fondo_clip], size=(1080,1920))
    video = video.set_audio(audio_voz)

    print(f"Exportando {salida}...")
    video.write_videofile(salida, fps=24, codec='libx264', audio_codec='aac')
    print("Listo!")
    return salida

if __name__ == "__main__":
    oracion_prueba = "Señor, en este día te pido paz para mi corazón y para mi familia. Amén."
    crear_reel(oracion_prueba)
