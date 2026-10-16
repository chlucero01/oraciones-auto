import requests, os, sys, time, json

PAGE_ID = os.getenv("PAGE_ID")
TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VIDEO = sys.argv[1] if len(sys.argv)>1 else "reel.mp4"
CAPTION = sys.argv[2] if len(sys.argv)>2 else "Oración de la Noche 🙏"

def log(msg, data=""):
    print(f"\n=== {msg} ===")
    if data:
        print(json.dumps(data, indent=2) if isinstance(data, dict) else str(data)[:2000])

if not os.path.exists(VIDEO):
    print(f"ERROR: No existe {VIDEO}")
    sys.exit(1)

size = os.path.getsize(VIDEO)
print(f"PAGE_ID: {PAGE_ID} | Archivo: {VIDEO} | Tamaño: {size} bytes")

# 1. START
print("\n1/3 START...")
r = requests.post(f"https://graph.facebook.com/v20.0/{PAGE_ID}/video_reels",
    data={"upload_phase":"start","file_size":size,"access_token":TOKEN})
log("RESPUESTA START", r.text)
js = r.json()
video_id = js.get("video_id")
upload_url = js.get("upload_url")

if not video_id or not upload_url:
    print("ERROR: Facebook no dio video_id / upload_url. Revisa tu PAGE_ACCESS_TOKEN")
    print("¿Tu token tiene permisos pages_manage_posts y pages_read_engagement?")
    sys.exit(1)

# 2. UPLOAD
print(f"\n2/3 UPLOAD a {upload_url[:80]}...")
with open(VIDEO, 'rb') as f:
    r2 = requests.post(upload_url, headers={"Authorization": f"OAuth {TOKEN}"}, data=f.read())
log("RESPUESTA UPLOAD", r2.text)
if r2.status_code!= 200:
    print(f"ERROR upload status {r2.status_code}")
    sys.exit(1)

print("Esperando 10s que procese...")
time.sleep(10)

# 3. FINISH
print("\n3/3 FINISH - Publicando...")
r3 = requests.post(f"https://graph.facebook.com/v20.0/{PAGE_ID}/video_reels",
    data={"upload_phase":"finish","video_id":video_id,"video_state":"PUBLISHED","description":CAPTION,"access_token":TOKEN})
log("RESPUESTA FINISH", r3.text)

if "success" in r3.text.lower() or r3.status_code==200:
    print("\n✅ Reel enviado a Facebook. Revisa tu Page en 1-2 min.")
else:
    print("\n❌ Facebook no publicó. Copia todo este log y mándamelo.")
