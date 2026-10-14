
import requests
import os
import sys
from datetime import datetime

PAGE_ID = os.environ.get("PAGE_ID")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GRAPH_VERSION = "v19.0"

if not PAGE_ID or not PAGE_ACCESS_TOKEN:
    print("❌ Faltan Secrets")
    sys.exit(1)

# DESCANSO PARA EL ALMA - Nueva filosofía
# Estructura: 1. Gancho  2. Situación humana  3. Oración corta  4. Cierre con esperanza  5. CTA único
# Sin hashtags. Tono íntimo, como compañía.
# Mix: 50% dolor/emocional, 30% protección/oración, 20% agradecimiento/esperanza

CALENDARIO = {
    0: { # LUNES
        "manana": """Si hoy te levantaste con el corazón pesado y nadie sabe todo lo que cargas, haz esta oración conmigo.

Señor, tú ves lo que no le cuento a nadie. El trabajo, los pendientes, las deudas que me quitan el sueño. Hoy no te pido que me quites todo de golpe, solo dame fuerza para este día.

Que tu paz me acompañe a donde vaya.

Escribe Amén si hoy caminas con Él.""",

        "tarde": """Tal vez hoy necesitabas escuchar esto.

Si te has sentido cansado, haciendo todo tú solo, sosteniendo a todos y nadie te pregunta cómo estás tú...

Quiero decirte algo: Dios sí te ve. Ve ese esfuerzo que nadie aplaude.

Respira. No tienes que poder con todo hoy. Hoy solo da un paso más.

Guárdala para cuando sientas que ya no puedes.""",

        "noche": """Antes de dormir escucha esto.

Si tu mente no se apaga, si das vueltas pensando en lo de mañana, en lo que no salió bien hoy...

Cierra tus ojos un segundo y hagamos esto juntos:

Señor, en tus manos dejo lo que no pude resolver hoy. Cuida mi casa mientras duermo. Dame la paz que hoy no encontré.

Que esta noche descanses de verdad.

Escribe 'En tus manos' si dejas todo ahí hoy."""
    },
    1: { # MARTES
        "manana": """Esta oración es para ti que saliste de casa preocupado.

Preocupado por el trabajo, por si va a alcanzar, por esa llamada que esperas.

Señor, tú ya estás en mi martes. Ve delante de mí, abre lo que tenga que abrirse y cierra lo que me hace daño.

Yo hoy solo camino, tú me llevas.

Compártela con alguien que hoy salió con miedo.""",

        "tarde": """Esta oración es para la madre que está preocupada por sus hijos.

Si hoy tu hijo te preocupa, si no sabes si lo estás haciendo bien, si te duele verlo sufrir y no poder quitarle ese dolor...

Tú estás haciendo lo mejor que puedes, y eso Dios lo ve.

Oremos: Señor, pon tu mano sobre mis hijos donde yo no alcanzo. Cuídalos tú.

Escribe Amén si eres esa mamá, ese papá hoy.""",

        "noche": """Si hoy te duele el corazón por la parte económica...

Si abriste la cartera y sentiste ese nudo en el estómago, si no sabes cómo le vas a hacer este mes.

Escucha esto: no estás solo en esto. 

Señor, tú conoces mis cuentas, mis miedos. Hoy te pido provisión y sabiduría. Que no falte el pan en mi mesa.

Que esta noche duermas con un poco más de esperanza.

Escribe 'Yo confío' si lo dejas en sus manos."""
    },
    2: { # MIERCOLES
        "manana": """Si hoy ya te sientes a mitad de semana y sin fuerzas...

Si sientes que diste mucho y avanzaste poco, haz esta oración conmigo.

Señor, estoy cansado. No te lo digo bonito, te lo digo real. Renueva mis fuerzas, como prometiste.

Ayúdame a terminar este día en paz.

Escribe Amén si hoy necesitas fuerza nueva.""",

        "tarde": """Tal vez hoy estás orando por alguien que está enfermo.

Por tu mamá, tu papá, tu pareja, tu hijo. Por alguien que amas y está en una cama de hospital o en casa sin mejoría.

Es muy duro amar a alguien y no poder quitarle el dolor.

Oremos juntos: Señor, pon tu mano donde está el dolor. Donde el doctor no llega, llega tú.

Guárdala para orar esta noche por esa persona.""",

        "noche": """Antes de dormir, si hoy te sentiste solo...

Aunque estuviste rodeado de gente, por dentro sentiste ese vacío. Nadie te preguntó de verdad cómo estabas.

Quiero decirte: Dios sí estuvo ahí, en ese momento solo.

Señor, hoy me sentí solo, pero ahora sé que no lo estoy. Quédate conmigo esta noche.

Escribe 'No estoy solo' si esta oración era para ti."""
    },
    3: { # JUEVES
        "manana": """Haz esta oración conmigo por tu familia.

Por los que están en casa, por los que se fueron lejos, por los que hoy están pasando por algo difícil y no te han dicho.

Señor, cubre mi casa. Que tu paz entre por la puerta y se quede. Protege a los míos de todo mal.

Que hoy mi familia sienta tu abrazo.

Escribe Amén por tu familia.""",

        "tarde": """Si hoy el trabajo te pesó más que otros días...

Si te sentiste presionado, no valorado, si piensas en renunciar, si sientes que por más que trabajas no alcanza.

Respira. Tu valor no lo define tu trabajo. Tu valor lo conoce Dios.

Señor, dame sabiduría en mi trabajo y paz cuando salga de ahí.

Compártela con alguien que hoy está cansado del trabajo.""",

        "noche": """Esta noche es para quien extraña a alguien.

Si hoy extrañaste a alguien que ya no está, si te hizo falta su voz, si lloraste en silencio para que nadie te viera...

Tu amor sigue vivo, y eso es hermoso.

Señor, abraza mi corazón que extraña. Dale paz a quien hoy no está conmigo y paz a mí que sigo aquí.

Escribe el nombre de quien extrañas, lo ponemos en oración."""
    },
    4: { # VIERNES
        "manana": """Hoy no te pido nada, hoy solo te doy gracias.

Gracias Señor por esta semana. Por lo bueno que me diste y por lo difícil que me enseñó. Aquí sigo, de pie, por tu misericordia.

Si hoy puedes agradecer por algo, aunque sea pequeño, escríbelo aquí abajo. Agradecer cambia el corazón.

Escribe Gracias por una cosa que hoy agradeces.""",

        "tarde": """Si esta semana alguien te decepcionó...

Si confiaste y te fallaron, si diste mucho y recibiste poco, si hoy te duele una traición o una palabra.

Duele, y es válido que duela.

Pero no dejes que ese dolor te haga duro.

Señor, sana mi corazón de lo que me hicieron. Que no me vuelva desconfiado, que me vuelva más sabio.

Guárdala si hoy necesitas sanar esa herida.""",

        "noche": """Antes de dormir, deja el cansancio de la semana aquí.

Si tu cuerpo está agotado, si tu espalda duele de tanto cargar, si tu mente ya no quiere pensar más.

Esta es tu oración de descanso:

Señor, hoy dejo la semana en tus manos. Renueva mis fuerzas. Que mañana despierte ligero.

Que esta noche duermas profundo, sin el peso de la semana.

Escribe 'Me rindo a tu descanso' si hoy lo necesitas."""
    },
    5: { # SABADO
        "manana": """Hoy es sábado. Hoy no corras.

Si toda la semana corriste, hoy haz una pausa. Siéntate con tu café, mira por la ventana, respira.

Señor, hoy quiero descansar en ti. Que no sea un día de más pendientes, que sea un día de volver a mi casa, a mi familia, a mí.

Que hoy encuentres 5 minutos solo para ti.

Compártela con alguien que necesita parar hoy.""",

        "tarde": """Tal vez hoy necesitabas escuchar esto:

No todo es problema. Hoy también hay algo bonito, aunque sea pequeño. El abrazo de tu hijo, el mensaje de alguien, el sol que entró por la ventana.

Hoy agradece lo pequeño. Ahí también está Dios.

Señor, abre mis ojos para ver lo bueno de hoy.

Escribe algo bonito que te pasó hoy, por pequeño que sea.""",

        "noche": """Si este sábado por la noche te sientes solo en casa...

Si todos salieron, si tu casa está en silencio y ese silencio pesa.

Pon tu mano en tu corazón y escucha esto: no estás solo. En esta misma hora, alguien más está orando por lo mismo que tú.

Señor, quédate conmigo esta noche de sábado. Que tu compañía llene esta casa.

Escribe 'Quédate conmigo' si hoy te sientes así."""
    },
    6: { # DOMINGO
        "manana": """Hoy es domingo. Día de volver a casa.

Si puedes ir a la iglesia, ve. Si no, haz de tu casa una iglesia hoy. Apaga el ruido un momento y agradece.

Señor, gracias por mi familia, por mi techo, por la vida. Bendice este domingo, que haya paz en mi mesa.

Que hoy tu casa se sienta diferente.

Escribe Amén si hoy pones a Dios primero en tu casa.""",

        "tarde": """Tal vez esta semana sentiste que no avanzaste.

Que oraste y no viste respuesta. Que lo intentaste y no salió.

Escucha esto: lo que no pudiste hacer en toda la semana, Dios lo puede hacer en un segundo.

No te rindas hoy. Tu domingo puede ser el inicio de tu milagro.

Guárdala para cuando sientas que no avanzas.""",

        "noche": """Antes de dormir, cierra tu semana aquí.

Deja lo que dolió, lo que no entendiste, lo que te preocupó. Mañana es lunes y lo empiezas libre.

Oración para esta noche:

Señor, aquí te dejo mi semana. Perdona mis errores, sana mis heridas y prepárame para lo que viene. Que duerma en paz, porque tú cuidas de mí.

Que esta noche descanses como hace mucho no lo haces.

Escribe 'Soy libre' y empieza tu semana en paz."""
    }
}

def publicar(mensaje):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed"
    r = requests.post(url, data={"message": mensaje, "access_token": PAGE_ACCESS_TOKEN})
    print(f"Status: {r.status_code}")
    print(f"Respuesta: {r.text[:500]}")
    data = r.json()
    if "error" in data:
        print(f"❌ Error Facebook: {data['error']}")
        sys.exit(1)
    print(f"✅ Publicado ID: {data.get('id')}")
    return data

if __name__ == "__main__":
    tipo = sys.argv[1] if len(sys.argv) > 1 else "manana"
    dia = datetime.now().weekday()
    # Ajuste simple Texas vs UTC
    # Si es madrugada UTC (1:30am) en realidad es 8:30pm del día anterior en Texas
    import os as _os
    # Forzamos dia Texas: si la hora UTC es <5, es aún ayer en Texas
    hora_utc = datetime.utcnow().hour
    if hora_utc < 5:
        dia = (dia - 1) % 7

    mensaje = CALENDARIO.get(dia, CALENDARIO[0]).get(tipo)
    print(f"Publicando {tipo} del día {dia} (Texas)")
    publicar(mensaje)
