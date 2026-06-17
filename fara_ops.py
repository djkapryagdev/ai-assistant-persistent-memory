
Fara Ops - Personal Intelligence Assistant
-------------------------------------------
Public GitHub version — v0.2

A local productivity and research assistant that learns your interests,
tracks AI developments, manages reminders and helps you stay organized.

Features
- Persistent local memory (JSON)
- Reminders and alarms (active while program runs)
- AI competitor and tech watchlist
- Personal notes and improvement ideas
- Session history log
- Safe defensive security checklist
- Safe folder nameextension review (read-only, no file execution)

Security note
This program does NOT execute, copy, delete, quarantine or modify files.
All folder review is read-only nameextension inspection only.


import datetime as dt
import json
import os
import re
import unicodedata
from pathlib import Path

APP_NAME = Fara
VERSION = 0.2
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR  data
MEMORY_FILE = DATA_DIR  fara_memory.json
SESSIONS_DIR = DATA_DIR  sessions
DATA_DIR.mkdir(exist_ok=True)
SESSIONS_DIR.mkdir(exist_ok=True)

CURRENT_SESSION_FILE = 


# ──────────────────────────────────────────────
# Memory
# ──────────────────────────────────────────────

def default_memory() - dict
    return {
        name ,
        interests [],
        research_topics [
            AI updates,
            large language models,
            machine learning,
            cybersecurity,
            productivity tools,
        ],
        ai_watchlist [
            {name ChatGPT, notes },
            {name Gemini, notes },
            {name Mistral, notes },
            {name Llama, notes },
        ],
        improvement_ideas [],
        reminders [],
        notes [],
        times_opened 0,
        last_opened ,
    }


def load_memory() - dict
    base = default_memory()
    if not MEMORY_FILE.exists()
        return base
    try
        with MEMORY_FILE.open(r, encoding=utf-8) as f
            memory = json.load(f)
        if not isinstance(memory, dict)
            return base
        for key, value in base.items()
            memory.setdefault(key, value)
        return memory
    except (json.JSONDecodeError, OSError)
        return base


def save_memory(memory dict) - None
    with MEMORY_FILE.open(w, encoding=utf-8) as f
        json.dump(memory, f, ensure_ascii=False, indent=4)


# ──────────────────────────────────────────────
# Session log
# ──────────────────────────────────────────────

def start_session(name str) - str
    timestamp = dt.datetime.now().strftime(%Y-%m-%d_%H-%M-%S)
    filename = fsession_{name.replace(' ', '_')}_{timestamp}.txt
    path = SESSIONS_DIR  filename
    with path.open(w, encoding=utf-8) as f
        f.write(fFARA OPS — SESSION LOGn)
        f.write(fUser {name}n)
        f.write(fStart {now_text()}n)
        f.write(-  50 + nn)
    return str(path)


def log_to_session(session_path str, speaker str, text str) - None
    if not session_path
        return
    timestamp = dt.datetime.now().strftime(%H%M%S)
    with open(session_path, a, encoding=utf-8) as f
        f.write(f[{timestamp}] {speaker} {text}n)


def close_session(session_path str) - None
    if not session_path
        return
    with open(session_path, a, encoding=utf-8) as f
        f.write(fn + -  50 + n)
        f.write(fEnd {now_text()}n)
    print(f{APP_NAME} Session saved to {session_path})


# ──────────────────────────────────────────────
# Text helpers
# ──────────────────────────────────────────────

def normalize(text str) - str
    text = text.lower().strip()
    text = re.sub(r[¿¡!,.], , text)
    text = unicodedata.normalize(NFD, text)
    return .join(c for c in text if unicodedata.category(c) != Mn)


def now_text() - str
    return dt.datetime.now().strftime(%Y-%m-%d %H%M)


def time_of_day() - str
    hour = dt.datetime.now().hour
    if 5 = hour  12
        return morning
    elif 12 = hour  19
        return afternoon
    elif 19 = hour  24
        return evening
    return late night


def say(message str, session_path str = ) - None
    print(f{APP_NAME} {message})
    if session_path
        log_to_session(session_path, APP_NAME, message)


def show_list(title str, items list) - None
    print(fn── {title} ──)
    if not items
        print(  (empty))
        return
    for i, item in enumerate(items, 1)
        print(f  {i}. {item})
    print()


# ──────────────────────────────────────────────
# Reminders
# ──────────────────────────────────────────────

def parse_reminder(text str)
    match = re.search(
        r(remind mereminderalarm)s+(.+)s+ats+(d{1,2}d{2}),
        text, re.IGNORECASE
    )
    if not match
        # Spanish support
        match = re.search(
            r(recordarmealarma)s+(.+)s+a lass+(d{1,2}d{2}),
            text, re.IGNORECASE
        )
    if not match
        return None

    task = match.group(1).strip()
    time_str = match.group(2).strip()
    try
        hour, minute = map(int, time_str.split())
        if not (0 = hour = 23 and 0 = minute = 59)
            return None
    except ValueError
        return None

    scheduled = dt.datetime.combine(dt.date.today(), dt.time(hour=hour, minute=minute))
    if scheduled  dt.datetime.now()
        scheduled += dt.timedelta(days=1)

    return {task task, time scheduled.strftime(%Y-%m-%d %H%M), done False}


def check_reminders(memory dict, session_path str) - None
    now = dt.datetime.now()
    changed = False
    for reminder in memory[reminders]
        if reminder.get(done)
            continue
        try
            rt = dt.datetime.strptime(reminder[time], %Y-%m-%d %H%M)
        except (KeyError, ValueError)
            continue
        if now = rt
            say(f⏰ REMINDER {reminder['task']}, session_path)
            reminder[done] = True
            changed = True
    if changed
        save_memory(memory)


# ──────────────────────────────────────────────
# AI Watchlist
# ──────────────────────────────────────────────

def show_ai_watchlist(memory dict) - None
    print(n── AI Watchlist ──)
    if not memory[ai_watchlist]
        print(  (empty))
        return
    for entry in memory[ai_watchlist]
        notes = entry.get(notes) or no notes yet
        print(f  • {entry['name']} {notes})
    print()


def update_ai_note(memory dict, text str) - str
    
    Format 'note AI name note text'
    Example 'note ChatGPT added memory feature in May 2025'
    
    match = re.match(rnotes+(.+)s+(.+), text, re.IGNORECASE)
    if not match
        return Use format note AI name note text

    ai_name = match.group(1).strip()
    note_text = match.group(2).strip()

    for entry in memory[ai_watchlist]
        if entry[name].lower() == ai_name.lower()
            entry[notes] = f[{now_text()}] {note_text}
            save_memory(memory)
            return fUpdated notes for {entry['name']}.

    # Add new entry if not found
    memory[ai_watchlist].append({name ai_name, notes f[{now_text()}] {note_text}})
    save_memory(memory)
    return fAdded {ai_name} to watchlist with your note.


# ──────────────────────────────────────────────
# Defensive security tools
# ──────────────────────────────────────────────

SUSPICIOUS_EXTENSIONS = {
    .exe, .bat, .cmd, .scr, .vbs, .js, .ps1,
    .jar, .msi, .hta, .pif, .com,
}

SUSPICIOUS_WORDS = [
    crack, keygen, patch, activator, trojan, payload,
    stealer, rat, malware, virus, backdoor, loader, ransomware,
]


def security_checklist() - list
    return [
        Keep your operating system and apps updated.,
        Use official antivirus with real-time protection.,
        Never run cracks, keygens or unknown executables.,
        Review browser extensions and remove unknown ones.,
        Enable automatic backups for important files.,
        Don't open suspicious attachments or unknown links.,
        Use unique passwords and enable two-factor authentication.,
        Regularly review app permissions on your devices.,
        Use a VPN on public Wi-Fi networks.,
        Monitor unusual CPUnetwork activity with Task Manager.,
    ]


def review_folder(path_text str) - list
    
    Read-only safe review.
    Only checks file names and extensions.
    Does NOT open, copy, execute, delete or modify any file.
    
    folder = Path(path_text).expanduser()
    results = []

    if not folder.exists() or not folder.is_dir()
        return [Folder does not exist or is not a valid directory.]

    try
        for item in folder.iterdir()
            if not item.is_file()
                continue
            lower_name = item.name.lower()
            ext = item.suffix.lower()
            reasons = []
            if ext in SUSPICIOUS_EXTENSIONS
                reasons.append(fsensitive extension {ext})
            for word in SUSPICIOUS_WORDS
                if word in lower_name
                    reasons.append(fname contains '{word}')
            if reasons
                results.append(f{item.name}  →  possible risk {', '.join(reasons)})
    except PermissionError
        return [Permission denied for that folder.]

    return results if results else [No suspicious names or extensions found.]


# ──────────────────────────────────────────────
# Help
# ──────────────────────────────────────────────

def print_help() - None
    print(f
┌─────────────────────────────────────────┐
│  {APP_NAME} {VERSION} — Available Commands           │
└─────────────────────────────────────────┘

PROFILE
  add interest text       Save a personal interest
  add topic text          Add a research topic
  view profile               Show interests and topics

REMINDERS
  remind me task at HHMM     Set a reminder (English)
  recordarme tarea a las HHMM  Set a reminder (Spanish)
  view reminders             Show pending reminders

AI WATCHLIST
  view watchlist             Show tracked AI systems
  add ai name             Add an AI to the watchlist
  note AI name text     Add a note about an AI

NOTES & IDEAS
  note text               Save a quick note
  idea text               Save an improvement idea for Fara
  view notes                 Show all notes
  view ideas                 Show all improvement ideas

SECURITY
  security checklist         Show defensive security tips
  review folder path      Safe read-only folder check

SESSION
  exit  salir               Close Fara and save session
)


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main() - None
    global CURRENT_SESSION_FILE

    memory = load_memory()
    memory[times_opened] += 1
    memory[last_opened] = now_text()
    save_memory(memory)

    if not memory[name]
        memory[name] = input(f{APP_NAME} Hello! What's your name ).strip() or User
        save_memory(memory)

    name = memory[name]
    session_path = start_session(name)
    CURRENT_SESSION_FILE = session_path

    tod = time_of_day()
    say(fGood {tod}, {name}. Fara v{VERSION} is ready. Type 'help' for commands., session_path)

    while True
        check_reminders(memory, session_path)

        try
            original = input(You ).strip()
        except (KeyboardInterrupt, EOFError)
            print()
            break

        if not original
            continue

        msg = normalize(original)
        log_to_session(session_path, You, original)

        # ── Exit ──
        if msg in (exit, salir, quit)
            say(fGoodbye, {name}. See you next time., session_path)
            close_session(session_path)
            break

        # ── Help ──
        if msg in (help, ayuda)
            print_help()
            continue

        # ── Reminder ──
        reminder = parse_reminder(original)
        if reminder
            memory[reminders].append(reminder)
            save_memory(memory)
            say(fReminder set '{reminder['task']}' at {reminder['time']}, session_path)
            continue

        # ── Add interest ──
        if msg.startswith(add interest)
            value = original.split(, 1)[1].strip()
            if value and value not in memory[interests]
                memory[interests].append(value)
                save_memory(memory)
                say(fSaved interest {value}, session_path)
            else
                say(Already saved or empty., session_path)
            continue

        # ── Add topic ──
        if msg.startswith(add topic)
            value = original.split(, 1)[1].strip()
            if value and value not in memory[research_topics]
                memory[research_topics].append(value)
                save_memory(memory)
                say(fAdded research topic {value}, session_path)
            else
                say(Topic already exists or is empty., session_path)
            continue

        # ── Add AI to watchlist ──
        if msg.startswith(add ai)
            ai_name = original.split(, 1)[1].strip()
            existing = [e[name].lower() for e in memory[ai_watchlist]]
            if ai_name and ai_name.lower() not in existing
                memory[ai_watchlist].append({name ai_name, notes })
                save_memory(memory)
                say(fAdded {ai_name} to AI watchlist., session_path)
            else
                say(Already on watchlist or empty., session_path)
            continue

        # ── Note about AI ──
        if msg.startswith(note ) and  in original
            # Check if it's an AI note (not a plain note)
            parts = original.split(, 1)
            potential_ai = parts[0].replace(note , ).strip()
            ai_names = [e[name].lower() for e in memory[ai_watchlist]]
            if potential_ai.lower() in ai_names or len(potential_ai.split()) = 3
                result = update_ai_note(memory, original)
                say(result, session_path)
                continue

        # ── Quick note ──
        if msg.startswith(note)
            value = original.split(, 1)[1].strip()
            if value
                entry = {date now_text(), text value}
                memory[notes].append(entry)
                save_memory(memory)
                say(Note saved., session_path)
            else
                say(Write something after 'note', session_path)
            continue

        # ── Idea ──
        if msg.startswith(idea)
            value = original.split(, 1)[1].strip()
            if value
                entry = {date now_text(), idea value}
                memory[improvement_ideas].append(entry)
                save_memory(memory)
                say(Improvement idea saved., session_path)
            else
                say(Write an idea after 'idea', session_path)
            continue

        # ── View profile ──
        if msg == view profile
            show_list(Interests, memory[interests])
            show_list(Research Topics, memory[research_topics])
            continue

        # ── View reminders ──
        if msg == view reminders
            pending = [
                f{r['task']} → {r['time']}
                for r in memory[reminders] if not r.get(done)
            ]
            show_list(Pending Reminders, pending)
            continue

        # ── View watchlist ──
        if msg == view watchlist
            show_ai_watchlist(memory)
            continue

        # ── View notes ──
        if msg == view notes
            show_list(Notes, [f[{n['date']}] {n['text']} for n in memory[notes]])
            continue

        # ── View ideas ──
        if msg == view ideas
            show_list(Improvement Ideas, [f[{i['date']}] {i['idea']} for i in memory[improvement_ideas]])
            continue

        # ── Security checklist ──
        if security checklist in msg or checklist in msg
            show_list(Defensive Security Checklist, security_checklist())
            continue

        # ── Review folder ──
        if msg.startswith(review folder)
            path_text = original.split(, 1)[1].strip()
            results = review_folder(path_text)
            show_list(Safe Folder Review (read-only), results)
            continue

        # ── Time awareness ──
        if what time in msg or hora in msg
            say(fIt's {dt.datetime.now().strftime('%H%M')} — {time_of_day()}., session_path)
            continue

        if what day in msg or fecha in msg
            say(fToday is {dt.datetime.now().strftime('%A, %B %d %Y')}., session_path)
            continue

        # ── Fallback ──
        say(
            I didn't catch that. Try 'help' to see available commands.,
            session_path
        )


if __name__ == __main__
    main()