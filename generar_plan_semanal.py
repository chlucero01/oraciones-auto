import json, random
from datetime import datetime

MANANA = [
    "Señor, gracias por este nuevo amanecer. Hoy pongo mi familia y mi trabajo en tus manos. Guíame con sabiduría.",
    "Padre, que esta mañana tu luz ilumine mi hogar. Dame paz para enfrentar el día con fe.",
    "Dios, al despertar te doy gracias por la vida. Bendice a mis hijos y mi camino hoy.",
    "Amado Dios, inicia conmigo este lunes. Que todo lo que haga hoy sea para bien.",
    "Señor, en esta mañana te pido fuerza para trabajar y amor para compartir.",
    "Gracias Padre por un día más. Que mi corazón esté lleno de gratitud hoy.",
    "Jesús, guía mis pasos esta mañana y aleja toda preocupación.",
    "Señor, bendice mi mañana y la de toda mi familia."
]
TARDE = [
    "Señor, a mitad del día me detengo a agradecerte. Si estoy cansado, dame nuevas fuerzas.",
    "Padre, gracias por lo vivido hoy. Sigue acompañándome esta tarde con tu paz.",
    "Dios, que esta tarde haya tranquilidad en mi hogar y en mi trabajo.",
    "Señor, en esta tarde te entrego mis cargas. Aligera mi corazón.",
    "Gracias por este día que avanza. Que mi tarde esté llena de tu presencia.",
    "Padre, cuida a mi familia esta tarde donde quiera que estén.",
    "Señor, que mi tarde sea productiva y llena de bendiciones.",
    "Dios, renueva mi ánimo en esta tarde."
]
NOCHE = [
    "Señor, al caer la noche te entrego mis preocupaciones, mis alegrías y mi familia. Gracias por este día. Dame descanso y paz. Amén.",
    "Padre amado, en tus manos dejo mi noche y mi descanso. Que tu paz inunde mi hogar.",
    "Dios, que esta noche tus ángeles cuiden mi casa y mis sueños. Amén.",
    "Señor, gracias por hoy. Perdona mis faltas y dame un sueño tranquilo.",
    "Padre, que mi noche sea de descanso y mi mañana de esperanza.",
    "Gracias Dios por este día. Esta noche descanso en tu amor.",
    "Señor, apaga mis miedos esta noche y enciende mi fe.",
    "Amado Padre, que esta noche haya paz en cada rincón de mi familia."
]

def crear_plan():
    dias = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
    plan = {}
    # elegimos sin repetir en la semana
    m = random.sample(MANANA, 7)
    t = random.sample(TARDE, 7)
    n = random.sample(NOCHE, 7)
    
    for i, dia in enumerate(dias):
        plan[dia] = {
            "mañana": m[i],
            "tarde": t[i],
            "noche": n[i]
        }
    
    data = {
        "semana_creada": datetime.now().strftime("%Y-%m-%d"),
        "plan": plan
    }
    with open("plan_semanal.json","w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Nuevo plan_semanal.json creado para la semana")

if __name__ == "__main__":
    crear_plan()
