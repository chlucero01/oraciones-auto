import requests, os, sys, time, json

PAGE_ID = os.getenv("PAGE_ID")
TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VIDEO = sys.argv[1] if len(sys.argv)>1 else "reel.mp4"
CAPTION = sys.argv[2] if len(sys.argv)>2 else "Oración de la Noche 🙏"

if not os.path.exists(VIDEO):
    print(f"ERROR: No existe {VIDEO}")
    sys.exit(1)

size = os.path.getsize(VIDEO)
print(f"Archivo: {VIDEO} | {size} bytes")

# 1. START
print("\n1/3 START...")
r = requests.post(f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels",
    data={"upload_phase":"start","file_size":size,"access_token":TOKEN})
print(r.text)
js = r.json()
video_id = js.get("video_id")
upload_url = js.get("upload_url")
if not video_id:
    print("Fallo START - revisa token")
    sys.exit(1)

# 2. UPLOAD - FIX DEFINITIVO
print(f"\n2/3 UPLOAD...")
with open(VIDEO, 'rb') as f:
    data = f.read()
    headers = {
        "Authorization": f"OAuth {TOKEN}",
        "offset": "0",
        "file_size": str(size),
        "Content-Type": "application/octet-stream"
    }
    r2 = requests.post(upload_url, headers=headers, data=data)

print(f"Status UPLOAD: {r2.status_code}")
print(r2.text[:2000])
if r2.status_code!= 200:
    sys.exit(1)

time.sleep(10)

# 3. FINISH
print("\n3/3 FINISH...")
r3 = requests.post(f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels",
    data={"upload_phase":"finish","video_id":video_id,"video_state":"PUBLISHED","description":CAPTION,"access_token":TOKEN})
print(r3.text)
print("\n✅ Si ves 'success' ya está en tu Page")
