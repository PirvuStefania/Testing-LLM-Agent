import os
import sqlite3
from typing import List, Dict

DB_PATH = "absolute path" #mereu calea absoluta, pentru ca SQLite nu suporta relative path in mod consistent, mai ales cand ruleaza in containere sau din alte foldere.
VAULT_DIR = "obsidian_vault"
PLAYBOOK_DIR = "playbooks"

def load_playbook(language: str) -> str:
    """
    Incarca playbook-ul static pentru limbajul cerut.
    Nu trece prin index vectorial -  e continut fix, nu retrieval semantic.
    """
    path = os.path.join(PLAYBOOK_DIR, f"{language}.md")
    if not os.path.exists(path):
        return f"(Niciun playbook disponibil pentru limbajul {language}; genereaza folosind cele mai bune practici generale. )"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# fa un singleton function la baza de date care returneaza cursorul
#adica nu deschide si inchide conexiunea la fiecare query, ci tine conexiunea deschisa cat timp e nevoie.
#daca nu exista creezi altfel daca exista returnezi cursorul. La final, cand se inchide programul, inchizi conexiunea.
#se ichide la finalul proc
def init_vault_db():
    """
    Creeaza baza de date SQLite locala pentru notele din Obsidian.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Creeaza tabelul pentru notele din Obsidian
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT, 
            author TEXT
        )
    """)

    conn.commit()
    conn.close()

def index_vault_notes():
    """
    Citeste fisierele .md din folder si salveaza-le in SQLite.
    """
    init_vault_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #golire tabel pentru reindexare curata la fiecare pornire
    cursor.execute("DELETE FROM notes")

    if not os.path.exists(VAULT_DIR):
        print(f"Folderul {VAULT_DIR} nu exista.")
        conn.close()
        return
    
    for filename in os.listdir(VAULT_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(VAULT_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                title = filename.replace(".md", "")
                cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def search_vault(query: str) -> List[Dict[str, str]]:
    """
    Cauta in notele din SQLite dupa un cuvant cheie (ex: auth, database).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Cauta in titlu si continut
    cursor.execute("SELECT title, content FROM notes WHERE title LIKE ? OR content LIKE ?", (f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "vault_note_ref": row[0], #titlul notei devine ref ceruta in arhitectura
            "content": row[1]
        })
    return results
