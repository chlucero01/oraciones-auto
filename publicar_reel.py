import requests
import os
import sys

PAGE_ID = os.getenv("PAGE_ID")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

VIDEO_PATH = sys.argv[1] if len(sys.argv) > 1 else "reel.mp4"
CAPTION = sys.argv[2] if len(sys.argv) > 2 else "Oración de la Noche 🙏 #oracion #noche"

def publicar_reel(video_path, caption):
    file_size = os.path.getsize(video_path)
    print(f"Tamaño video: {file_size}")

    # 1. START
    print("1/3 Iniciando...")
    r = requests.post(
        f"https://graph.facebook.com/v20.0/{PAGE_ID}/video_reels",
        data={
            "upload_phase": "start",
            "file_size": file_size,
            "access_token": PAGE_TOKEN
        }
    )
    print(r.text)
    data = r.json()
    video_id = data.get("video_id")
    upload_url = data.get("upload_url")

    if not video_id:
        print("Error: no video_id")
        return

    # 2. UPLOAD
    print("2/3 Subiendo video...")
    with open(video_path, 'rb') as f:
        r2 = requests.post(
            upload_url,
            headers={"Authorization": f"OAuth {PAGE_TOKEN}"},
            data=f.read()
        )
    print(r2.text)

    # 3. FINISH y PUBLICAR
    print("3/3 Publicando como Reel...")
    r3 = requests.post(
        f"https://graph.facebook.com/v20.0/{PAGE_ID}/video_reels",
        data={
            "upload_phase": "finish",
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "description": caption,
            "access_token": PAGE_TOKEN
        }
    )
    print(r3.text)
    print("¡Reel publicado!")

if __name__ == "__main__":
    publicar_reel(VIDEO_PATH, CAPTION)
