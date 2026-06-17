"""
Fara Ops - Personal Intelligence Assistant Demo
-------------------------------------------------
Public GitHub version.

This version presents Fara as a productivity, research and device-safety
assistant prototype. It intentionally avoids revealing private emotional-companion
logic from the main Fara project.

Features:
- Local user profile and interests
- Reminders / alarms while the program is running
- Research watchlist for topics like AI updates, stocks or technology
- Notes for competitor tracking and project improvement ideas
- Safe device-security checklist
- Safe folder review that only reports suspicious names/extensions

Important security note:
This prototype does NOT attack devices, execute files, copy malware, collect
viruses, bypass permissions or remove system files. It only provides defensive
organization and safe local checks.
"""

import datetime as dt
import json
import os
import re
import unicodedata
from pathlib import Path

APP_NAME = "Fara Ops"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEMORY_FILE = DATA_DIR / "Fara_ops_memory.json"
DATA_DIR.mkdir(exist_ok=True)


# -----------------------------
# Memory
# -----------------------------

def default_memory() -> dict:
    return {
        "name": "",
        "interests": [],
        "research_topics": [
            "AI updates",
            "stock market",
            "cybersecurity",
            "productivity tools",
        ],
        "competitors": [],
        "improvement_ideas": [],
        "reminders": [],
        "security_notes": [],
        "times_opened": 0,
        "last_opened": "",
    }


def load_memory() -> dict:
    base = default_memory()
    if not MEMORY_FILE.exists():
        return base

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            memory = json.load(file)

        if not isinstance(memory, dict):
            return base

        for key, value in base.items():
            memory.setdefault(key, value)

        return memory

    except (json.JSONDecodeError, OSError):
        return base


def save_memory(memory: dict) -> None:
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)


# -----------------------------
# Text helpers
# -----------------------------

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[¿?¡!,.]", "", text)
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def now_text() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def say(message: str) -> None:
    print(f"{APP_NAME}: {message}")


def show_list(title: str, items: list) -> None:
    print(f"\n{title}")
    if not items:
        print("  - No hay elementos todavía.")
        return

    for index, item in enumerate(items, start=1):
        print(f"  {index}. {item}")


# -----------------------------
# Reminders / alarms
# -----------------------------

def parse_reminder(text: str):
    """
    Supported examples:
    - recordarme estudiar python a las 21:30
    - alarma revisar noticias de AI a las 08:00
    """
    match = re.search(r"(?:recordarme|alarma)\s+(.+?)\s+a las\s+(\d{1,2}:\d{2})", text, re.IGNORECASE)
    if not match:
        return None

    task = match.group(1).strip()
    time_value = match.group(2).strip()

    try:
        hour, minute = map(int, time_value.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
    except ValueError:
        return None

    today = dt.date.today()
    scheduled = dt.datetime.combine(today, dt.time(hour=hour, minute=minute))

    if scheduled < dt.datetime.now():
        scheduled += dt.timedelta(days=1)

    return {
        "task": task,
        "time": scheduled.strftime("%Y-%m-%d %H:%M"),
        "done": False,
    }


def check_reminders(memory: dict) -> None:
    current = dt.datetime.now()
    changed = False

    for reminder in memory["reminders"]:
        if reminder.get("done"):
            continue

        try:
            reminder_time = dt.datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M")
        except (KeyError, ValueError):
            continue

        if current >= reminder_time:
            say(f"Recordatorio: {reminder['task']}")
            reminder["done"] = True
            changed = True

    if changed:
        save_memory(memory)


# -----------------------------
# Safe security tools
# -----------------------------

SUSPICIOUS_EXTENSIONS = {
    ".exe", ".bat", ".cmd", ".scr", ".vbs", ".js", ".ps1", ".jar", ".msi",
}

SUSPICIOUS_WORDS = [
    "crack", "keygen", "patch", "activator", "trojan", "payload", "stealer",
    "rat", "malware", "virus", "backdoor", "loader",
]


def security_checklist() -> list[str]:
    return [
        "Mantén el sistema operativo actualizado.",
        "Usa antivirus oficial y protección en tiempo real.",
        "No ejecutes cracks, keygens ni archivos desconocidos.",
        "Revisa extensiones del navegador y elimina las desconocidas.",
        "Activa copias de seguridad de archivos importantes.",
        "No abras adjuntos sospechosos ni enlaces raros.",
        "Usa contraseñas únicas y verificación en dos pasos.",
    ]


def review_folder(path_text: str) -> list[str]:
    """
    Safe folder review.
    It only checks names/extensions. It does not open, copy, execute, delete,
    quarantine or modify files.
    """
    folder = Path(path_text).expanduser()
    results = []

    if not folder.exists() or not folder.is_dir():
        return ["La carpeta no existe o no es una carpeta válida."]

    try:
        for item in folder.iterdir():
            if not item.is_file():
                continue

            lower_name = item.name.lower()
            extension = item.suffix.lower()
            reasons = []

            if extension in SUSPICIOUS_EXTENSIONS:
                reasons.append(f"extensión sensible {extension}")

            for word in SUSPICIOUS_WORDS:
                if word in lower_name:
                    reasons.append(f"nombre contiene '{word}'")

            if reasons:
                results.append(f"{item.name} -> posible riesgo: {', '.join(reasons)}")

    except PermissionError:
        return ["No tengo permiso para revisar esa carpeta."]

    if not results:
        return ["No encontré nombres o extensiones sospechosas en esa carpeta."]

    return results


# -----------------------------
# Main app
# -----------------------------

def print_help() -> None:
    print("""
Comandos disponibles:

  ayuda
    Muestra esta lista.

  agregar gusto: <texto>
    Guarda un gusto o interés personal.

  agregar tema: <texto>
    Agrega un tema de investigación, por ejemplo AI, bolsa, ciberseguridad.

  agregar rival: <nombre>
    Guarda una empresa o IA para dar seguimiento manual.

  idea Fara: <texto>
    Guarda una idea de mejora para el proyecto.

  recordarme <tarea> a las HH:MM
    Crea una alarma local mientras el programa esté abierto.

  ver perfil
    Muestra intereses, temas, rivales e ideas guardadas.

  ver recordatorios
    Muestra las alarmas pendientes.

  checklist seguridad
    Muestra una lista segura de protección del dispositivo.

  revisar carpeta: <ruta>
    Revisa nombres/extensiones sospechosas sin abrir, copiar, borrar ni ejecutar archivos.

  salir
    Cierra el programa.
""")


def main() -> None:
    memory = load_memory()
    memory["times_opened"] += 1
    memory["last_opened"] = now_text()
    save_memory(memory)

    if not memory["name"]:
        memory["name"] = input(f"{APP_NAME}: Hola, ¿cómo te llamas? ").strip() or "Usuario"
        save_memory(memory)

    name = memory["name"]
    say(f"Hola {name}. Estoy listo para ayudarte con recordatorios, investigación y seguridad básica.")
    say("Escribe 'ayuda' para ver los comandos.")

    while True:
        check_reminders(memory)

        original = input("Tú: ").strip()
        message = normalize(original)

        if not original:
            continue

        if message == "salir":
            say("Cerrando sesión. Guardé tu información local.")
            save_memory(memory)
            break

        if message == "ayuda":
            print_help()
            continue

        reminder = parse_reminder(original)
        if reminder:
            memory["reminders"].append(reminder)
            save_memory(memory)
            say(f"Listo. Te recordaré: {reminder['task']} -> {reminder['time']}")
            continue

        if message.startswith("agregar gusto:"):
            value = original.split(":", 1)[1].strip()
            if value and value not in memory["interests"]:
                memory["interests"].append(value)
                save_memory(memory)
                say(f"Guardé este gusto/interés: {value}")
            else:
                say("No agregué nada nuevo.")
            continue

        if message.startswith("agregar tema:"):
            value = original.split(":", 1)[1].strip()
            if value and value not in memory["research_topics"]:
                memory["research_topics"].append(value)
                save_memory(memory)
                say(f"Agregué este tema de investigación: {value}")
            else:
                say("Ese tema ya existe o está vacío.")
            continue

        if message.startswith("agregar rival:"):
            value = original.split(":", 1)[1].strip()
            if value and value not in memory["competitors"]:
                memory["competitors"].append(value)
                save_memory(memory)
                say(f"Agregué a la lista de seguimiento: {value}")
            else:
                say("Ese rival ya existe o está vacío.")
            continue

        if message.startswith("idea Fara:"):
            value = original.split(":", 1)[1].strip()
            if value:
                entry = {"date": now_text(), "idea": value}
                memory["improvement_ideas"].append(entry)
                save_memory(memory)
                say("Guardé esa idea de mejora para Fara.")
            else:
                say("Escribe una idea después de 'idea Fara:'.")
            continue

        if message == "ver perfil":
            show_list("Gustos e intereses", memory["interests"])
            show_list("Temas de investigación", memory["research_topics"])
            show_list("Rivales / empresas a seguir", memory["competitors"])
            show_list("Ideas de mejora", [item["idea"] for item in memory["improvement_ideas"]])
            continue

        if message == "ver recordatorios":
            pending = [f"{item['task']} -> {item['time']}" for item in memory["reminders"] if not item.get("done")]
            show_list("Recordatorios pendientes", pending)
            continue

        if message == "checklist seguridad":
            show_list("Checklist de seguridad defensiva", security_checklist())
            continue

        if message.startswith("revisar carpeta:"):
            path_text = original.split(":", 1)[1].strip()
            results = review_folder(path_text)
            show_list("Resultado de revisión segura", results)
            continue

        if "bolsa" in message or "acciones" in message:
            say("Puedo guardar bolsa de valores como tema de investigación. En una versión futura se podría conectar a una API financiera.")
            continue

        if "actualizaciones" in message or "noticias" in message or "ai" in message:
            say("Puedo guardar temas y rivales para seguimiento. En una versión futura se podría conectar a fuentes RSS o APIs de noticias.")
            continue

        if "virus" in message or "seguridad" in message:
            say("Puedo ayudarte con revisión segura y checklist defensivo. No ejecuto, copio ni manipulo archivos peligrosos.")
            continue

        say("Entendido. Puedo guardarlo como gusto, tema, rival, idea o recordatorio. Escribe 'ayuda' para ver ejemplos.")


if __name__ == "__main__":
    main()
