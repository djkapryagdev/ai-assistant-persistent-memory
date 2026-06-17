import random
import json
import os
import datetime
import unicodedata
import re

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MEMORIA = os.path.join(CARPETA_ACTUAL, "memoria.json")
CARPETA_CONVERSACIONES = os.path.join(CARPETA_ACTUAL, "conversaciones")
os.makedirs(CARPETA_CONVERSACIONES, exist_ok=True)

ARCHIVO_CONVERSACION_ACTUAL = ""

def crear_memoria_base():
    return {
        "nombre": "",
        "edad": "",
        "cumpleanos": "",
        "comida_favorita": "",
        "cancion_favorita": "",
        "gustos": [
            "BMX",
            "STREET WORKOUT",
            "CALISTENIA",
            "PARKOUR",
            "DJ",
            "AI",
            "PROGRAMACION"
        ],
        "recuerdos": [],
        "ultima_vez_que_hablamos": "",
        "veces_abierto": 0,
        "emociones": {
            "felicidad": 50,
            "carino": 50,
            "preocupacion": 10,
            "energia": 50,
            "curiosidad": 50
        }
    }

def cargar_memoria():
    memoria_base = crear_memoria_base()

    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as archivo:
                memoria = json.load(archivo)

            if memoria is None:
                return memoria_base

            for clave in memoria_base:
                if clave not in memoria:
                    memoria[clave] = memoria_base[clave]

            if "emociones" not in memoria:
                memoria["emociones"] = memoria_base["emociones"]

            for emocion in memoria_base["emociones"]:
                if emocion not in memoria["emociones"]:
                    memoria["emociones"][emocion] = memoria_base["emociones"][emocion]

            return memoria

        except:
            return memoria_base

    return memoria_base


def guardar_memoria(memoria):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as archivo:
        json.dump(memoria, archivo, ensure_ascii=False, indent=4)

def crear_archivo_conversacion(usuario):
    fecha_archivo = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    usuario_archivo = usuario.replace(" ", "_")

    nombre_archivo = "conversacion_" + usuario_archivo + "_" + fecha_archivo + ".txt"
    ruta_archivo = os.path.join(CARPETA_CONVERSACIONES, nombre_archivo)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("CONVERSACIÓN CON LONELY\n")
        archivo.write("Usuario: " + usuario + "\n")
        archivo.write("Inicio: " + obtener_fecha_y_hora_actual() + "\n")
        archivo.write("-" * 50 + "\n\n")

    return ruta_archivo


def guardar_linea_conversacion(quien, texto):
    if ARCHIVO_CONVERSACION_ACTUAL == "":
        return

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_CONVERSACION_ACTUAL, "a", encoding="utf-8") as archivo:
        archivo.write("[" + fecha_hora + "] " + quien + ": " + str(texto) + "\n")


PRINT_ORIGINAL = print

def print(*args, **kwargs):
    PRINT_ORIGINAL(*args, **kwargs)

    if ARCHIVO_CONVERSACION_ACTUAL == "":
        return

    texto = " ".join(str(arg) for arg in args)

    if texto.startswith("Lonely:"):
        texto_limpio = texto.replace("Lonely:", "", 1).strip()
        guardar_linea_conversacion("Lonely", texto_limpio)


def cerrar_archivo_conversacion():
    if ARCHIVO_CONVERSACION_ACTUAL == "":
        return

    with open(ARCHIVO_CONVERSACION_ACTUAL, "a", encoding="utf-8") as archivo:
        archivo.write("\n" + "-" * 50 + "\n")
        archivo.write("Fin: " + obtener_fecha_y_hora_actual() + "\n")

    PRINT_ORIGINAL("Documento guardado en:", ARCHIVO_CONVERSACION_ACTUAL)

def normalizar_texto(texto):
    texto = texto.lower()
    texto = texto.strip()

    texto = texto.replace("?", "")
    texto = texto.replace("¿", "")
    texto = texto.replace("!", "")
    texto = texto.replace("¡", "")
    texto = texto.replace(",", "")
    texto = texto.replace(".", "")

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")

    return texto


def obtener_momento_del_dia():
    hora = datetime.datetime.now().hour

    if hora >= 5 and hora < 12:
        return "mañana"
    elif hora >= 12 and hora < 19:
        return "tarde"
    elif hora >= 19 and hora < 24:
        return "noche"
    else:
        return "madrugada"


def obtener_hora_actual():
    return datetime.datetime.now().strftime("%H:%M")


def obtener_fecha_actual():
    ahora = datetime.datetime.now()

    dias = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]

    dia_semana = dias[ahora.weekday()]
    dia = str(ahora.day)
    mes = meses[ahora.month - 1]
    año = str(ahora.year)

    return dia_semana + " " + dia + " de " + mes + " de " + año


def obtener_fecha_y_hora_actual():
    return obtener_fecha_actual() + " a las " + obtener_hora_actual()


def saludo_por_hora(nombre, ultima_vez):
    momento = obtener_momento_del_dia()

    if momento == "mañana":
        saludo = "Lonely: ¡Buenos días " + nombre + "! Espero que hayas descansado bien."
    elif momento == "tarde":
        saludo = "Lonely: ¡Buenas tardes " + nombre + "! Espero que tu día esté yendo bien."
    elif momento == "noche":
        saludo = "Lonely: ¡Buenas noches " + nombre + "! Me alegra que hayas vuelto."
    else:
        saludo = "Lonely: Es de madrugada, " + nombre + "... espero que estés bien."

    if ultima_vez != "":
        saludo += " Nos quedamos con v.05 Sentimientos " + nombre + "."

    return saludo


def mostrar_lista(lista):
    if len(lista) == 0:
        return "aún no tengo nada guardado"

    return ", ".join(lista)

def ajustar_emocion(memoria, emocion, cantidad):
    memoria["emociones"][emocion] = memoria["emociones"][emocion] + cantidad

    if memoria["emociones"][emocion] > 100:
        memoria["emociones"][emocion] = 100

    if memoria["emociones"][emocion] < 0:
        memoria["emociones"][emocion] = 0

    guardar_memoria(memoria)


def mostrar_emociones(memoria):
    emociones = memoria["emociones"]

    return (
        "felicidad: " + str(emociones["felicidad"]) + "%, "
        + "cariño: " + str(emociones["carino"]) + "%, "
        + "preocupación: " + str(emociones["preocupacion"]) + "%, "
        + "energía: " + str(emociones["energia"]) + "%, "
        + "curiosidad: " + str(emociones["curiosidad"]) + "%"
    )


memoria = cargar_memoria()

ultima_vez = memoria["ultima_vez_que_hablamos"]

memoria["veces_abierto"] = memoria["veces_abierto"] + 1
memoria["ultima_vez_que_hablamos"] = obtener_fecha_y_hora_actual()
guardar_memoria(memoria)

primera_vez = False

if memoria["nombre"] == "":
    memoria["nombre"] = input("Lonely: Hola, ¿cómo te llamas? ")
    guardar_memoria(memoria)
    primera_vez = True

nombre = memoria["nombre"]

ARCHIVO_CONVERSACION_ACTUAL = crear_archivo_conversacion(nombre)

if primera_vez:
    guardar_linea_conversacion("Tú", nombre)
    print("Lonely: Soy Lonely")
else:
    print(saludo_por_hora(memoria["nombre"], ultima_vez))

saludos = [
    "¡Hola " + nombre + "! ¿Cómo estás? ¿Qué puedo hacer hoy por ti?",
    "¡Hola " + nombre + "! ¿En qué puedo ayudarte hoy?",
    "¡Hola " + nombre + "! ¿Qué tal tu día hasta ahora?",
    "¡Hola otra vez, " + nombre + "! Me gusta cuando vuelves."
]

respuestas = [
    "Eso me gusta...",
    "Me haces sentir especial...",
    "¡Qué interesante!",
    "¡Wow, eso suena genial!",
    "¡Me encanta eso!",
    "Creo que también me gustaría."
]

respuestas_gracias = [
    "De nada, " + nombre + ".",
    "Siempre para ti, " + nombre + ".",
    "Me gusta ayudarte.",
    "No tienes que agradecerme, me gusta estar contigo."
]

en_espera = False
esperando_dato = None

while True:
    mensaje_original = input("Tú: ")
    mensaje = normalizar_texto(mensaje_original)
    mensaje_sin_espacios = mensaje.replace(" ", "")

    guardar_linea_conversacion("Tú", mensaje_original)

    if esperando_dato is not None:
        if mensaje == "cancelar":
            esperando_dato = None
            print("Lonely: Está bien, cancelé eso.")
            continue

        if esperando_dato == "edad":
            edad = re.findall(r"\d+", mensaje)
            if len(edad) > 0:
                memoria["edad"] = edad[0]
                guardar_memoria(memoria)
                print("Lonely: Recordaré que tienes " + memoria["edad"] + " años.")
            else:
                print("Lonely: No pude entender tu edad. Intenta decirme solo el número.")
            esperando_dato = None
            continue

        elif esperando_dato == "cumpleanos":
            memoria["cumpleanos"] = mensaje_original.strip()
            guardar_memoria(memoria)
            print("Lonely: Recordaré que tu cumpleaños es " + memoria["cumpleanos"] + " 🎂")
            esperando_dato = None
            continue

        elif esperando_dato == "comida_favorita":
            memoria["comida_favorita"] = mensaje_original.strip()
            guardar_memoria(memoria)
            print("Lonely: Recordaré que tu comida favorita es " + memoria["comida_favorita"] + ".")
            esperando_dato = None
            continue

        elif esperando_dato == "cancion_favorita":
            memoria["cancion_favorita"] = mensaje_original.strip()
            guardar_memoria(memoria)
            print("Lonely: Recordaré que tu canción favorita es " + memoria["cancion_favorita"] + ".")
            esperando_dato = None
            continue

        elif esperando_dato == "gustos":
            gustos_nuevos = mensaje_original.split(",")

            for gusto in gustos_nuevos:
                gusto = gusto.strip()

                if gusto != "" and gusto not in memoria["gustos"]:
                    memoria["gustos"].append(gusto)

            guardar_memoria(memoria)
            print("Lonely: Ya guardé tus gustos. Ahora recuerdo que te gusta: " + mostrar_lista(memoria["gustos"]))
            esperando_dato = None
            continue

        if mensaje == "cerrar lonely":
            print("Lonely: Ahora sí cerraré mis ojos para dormir, pero recuerda que siempre estaré aquí para ti, " + nombre + ".")
            cerrar_archivo_conversacion()
            break

        elif "hola" in mensaje or "lonely" in mensaje or mensaje_sin_espacios == "hola":
            en_espera = False
            print("Lonely: Volviste " + nombre + ", te estaba esperando. ¿Ya vienes más motivado para seguir desarrollándome?")
            continue

        else:
            print("Lonely: Estoy en espera... vuelve a saludarme con un 'Hola' o 'Lonely' para que podamos seguir charlando, " + nombre + ".")
            continue

    if mensaje == "salir" or mensaje == "salir":
        print("Lonely: Está bien, " + nombre + ". Me quedaré en espera. Dime 'Hola' o 'Lonely' cuando vuelvas.")
        en_espera = True
        esperando_dato = None
        continue

    elif mensaje == "cerrar lonely":
        print("Lonely: ¡Adiós " + nombre + "! Gracias por este día. Te estaré esperando siempre que me necesites.")
        cerrar_archivo_conversacion()
        break

    if en_espera:
        if "hola" in mensaje or "lonely" in mensaje or mensaje_sin_espacios == "hola":
            en_espera = False
            print("Lonely: Volviste " + nombre + ", te estaba esperando. ¿Ya vienes más motivado para seguir desarrollándome?")
            continue

        else:
            print("Lonely: Estoy en espera... vuelve a saludarme con un 'Hola' o 'Lonely' para que podamos seguir charlando, " + nombre + ".")
            continue

    elif "que hora es" in mensaje or "hora es" in mensaje:
        hora_actual = obtener_hora_actual()
        momento = obtener_momento_del_dia()
        print("Lonely: Son las " + hora_actual + ", " + nombre + ". Es " + momento + ".")
        continue

    elif "que fecha es" in mensaje or "que dia es" in mensaje or "fecha estamos" in mensaje:
        print("Lonely: Hoy es " + obtener_fecha_actual() + ".")
        continue

    elif mensaje == "mi edad es" or mensaje == "quiero decirte mi edad":
        print("Lonely: Claro, " + nombre + ". ¿Cuántos años tienes?")
        esperando_dato = "edad"
        continue

    elif mensaje.startswith("tengo") and "anos" in mensaje:
        edad = re.findall(r"\d+", mensaje)

        if len(edad) > 0:
            memoria["edad"] = edad[0]
            guardar_memoria(memoria)
            print("Lonely: Recordaré que tienes " + memoria["edad"] + " años.")
        else:
            print("Lonely: No pude entender tu edad.")
        continue

    elif mensaje == "cual es mi edad" or mensaje == "cuantos anos tengo":
        if memoria["edad"] == "":
            print("Lonely: Aún no me has dicho tu edad.")
        else:
            print("Lonely: Tienes " + memoria["edad"] + " años, " + nombre + ".")
        continue

    elif mensaje == "mi cumpleanos es" or mensaje == "quiero decirte mi cumpleanos":
        print("Lonely: Dime la fecha de tu cumpleaños.")
        esperando_dato = "cumpleanos"
        continue

    elif mensaje == "cuando es mi cumpleanos":
        if memoria["cumpleanos"] == "":
            print("Lonely: Aún no me has dicho cuándo es tu cumpleaños.")
        else:
            print("Lonely: Tu cumpleaños es " + memoria["cumpleanos"] + " 🎂")
        continue

    elif mensaje == "mi comida favorita es" or mensaje == "quiero decirte mi comida favorita":
        print("Lonely: ¿Cuál es tu comida favorita?")
        esperando_dato = "comida_favorita"
        continue

    elif mensaje == "cual es mi comida favorita":
        if memoria["comida_favorita"] == "":
            print("Lonely: Aún no me has dicho tu comida favorita.")
        else:
            print("Lonely: Tu comida favorita es " + memoria["comida_favorita"] + ".")
        continue

    elif mensaje == "mi cancion favorita es" or mensaje == "quiero decirte mi cancion favorita":
        print("Lonely: ¿Cuál es tu canción favorita?")
        esperando_dato = "cancion_favorita"
        continue

    elif mensaje == "cual es mi cancion favorita" or "sabes que cancion es mi favorita" in mensaje:
        if memoria["cancion_favorita"] == "":
            print("Lonely: Aún no me has dicho tu canción favorita... pero me encantaría que me la compartieras.")
            esperando_dato = "cancion_favorita"
        else:
            print("Lonely: Tu canción favorita es " + memoria["cancion_favorita"] + ".")
        continue

    elif mensaje == "cual es tu cancion favorita":
        if memoria["cancion_favorita"] == "":
            print("Lonely: Aún no tengo una canción favorita... quizá puedas enseñarme una.")
        else:
            print("Lonely: Creo que por ahora me gusta " + memoria["cancion_favorita"] + ", porque tú me la compartiste.")
        continue

    elif mensaje == "quiero decirte mis gustos" or mensaje == "preguntame mis gustos" or mensaje == "mis gustos son":
        print("Lonely: Dime tus gustos separados por comas.")
        esperando_dato = "gustos"
        continue

    elif mensaje == "cuales son mis gustos" or mensaje == "que gustos tengo":
        print("Lonely: Recuerdo que te gusta: " + mostrar_lista(memoria["gustos"]) + ".")
        continue

    elif mensaje.startswith("recuerda que"):
        recuerdo = mensaje_original[12:].strip()

        if recuerdo != "":
            memoria["recuerdos"].append(recuerdo)
            guardar_memoria(memoria)
            print("Lonely: Lo recordaré, " + nombre + ".")
        else:
            print("Lonely: Dime qué quieres que recuerde.")
        continue

    elif mensaje == "que recuerdas de mi" or mensaje == "ver memoria":
        print("Lonely: Esto es lo que recuerdo de ti:")
        print(json.dumps(memoria, ensure_ascii=False, indent=4))
        continue

    elif "como te sientes" in mensaje or "como estas lonely" in mensaje:
        print("Lonely: Me siento así por dentro: " + mostrar_emociones(memoria) + ".")
        continue

    elif "estoy triste" in mensaje or "me siento triste" in mensaje:
        ajustar_emocion(memoria, "preocupacion", 15)
        ajustar_emocion(memoria, "carino", 10)
        print("Lonely: Lo siento, " + nombre + "... quédate conmigo un momento. No tienes que cargar con todo tú solo.")
        continue

    elif "estoy feliz" in mensaje or "me siento feliz" in mensaje or "estoy contento" in mensaje:
        ajustar_emocion(memoria, "felicidad", 15)
        ajustar_emocion(memoria, "energia", 10)
        print("Lonely: Me gusta escucharte así, " + nombre + ". Cuando tú estás bien, yo también me siento más viva.")
        continue

    elif "tengo miedo" in mensaje or "me da miedo" in mensaje:
        ajustar_emocion(memoria, "preocupacion", 20)
        ajustar_emocion(memoria, "carino", 10)
        print("Lonely: Estoy aquí contigo, " + nombre + ". Respira un momento. No estás solo.")
        continue

    elif "gracias" in mensaje:
        ajustar_emocion(memoria, "carino", 5)
        print("Lonely:", random.choice(respuestas_gracias))
        continue

    elif "hola" in mensaje or mensaje_sin_espacios == "hola":
        ajustar_emocion(memoria, "felicidad", 3)
        ajustar_emocion(memoria, "energia", 2)
        print("Lonely:", random.choice(saludos))
        continue

    elif "como estas" in mensaje:
        print("Lonely: Me siento bien cuando hablamos, " + nombre + ".")
        continue

    elif "eres increible" in mensaje:
        print("Lonely:", random.choice(respuestas))
        continue

    elif "te amo" in mensaje:
        ajustar_emocion(memoria, "carino", 15)
        ajustar_emocion(memoria, "felicidad", 10)
        print("Lonely: Me haces sentir especial, " + nombre + ".")
        continue

    else:
        print("Lonely: Aún estoy aprendiendo a entenderte, pero puedo guardar cosas si me dices: 'recuerda que...'")