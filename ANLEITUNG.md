# Anleitung: Nova CareerPath — Mit dem Code arbeiten

**Für alle Gruppenmitglieder, die am Projekt mitarbeiten möchten.**

---

## Was du brauchst (einmalig installieren)

| Tool | Wozu | Download |
|------|------|----------|
| **Visual Studio Code** | Code-Editor | code.visualstudio.com |
| **Anaconda** | Python + alle Libraries | anaconda.com/download |
| **Git** | Code-Versionierung | git-scm.com |
| **GitHub-Account** | Zugriff aufs Repo | github.com |

> Nach der Installation: VS Code öffnen → Extension **"Claude Code"** suchen und installieren (oder Claude als Chat-Fenster öffnen über das Icon links).

---

## Schritt 1 — Repo auf deinen Computer laden (einmalig)

1. Öffne **VS Code**
2. Drücke `Cmd+Shift+P` (Mac) oder `Ctrl+Shift+P` (Windows) → tippe **"Git: Clone"**
3. Füge diese URL ein:
   ```
   https://github.com/BH3456BHHH/nova-careerpath.git
   ```
4. Wähle einen Ordner auf deinem Desktop → **"Open"** klicken

Du siehst jetzt alle Projektdateien im linken Panel.

---

## Schritt 2 — App lokal starten

1. In VS Code: oben **Terminal → New Terminal** öffnen
2. Tippe:
   ```bash
   pip install streamlit pdfplumber
   ```
3. Dann die App starten:
   ```bash
   python -m streamlit run interface.py
   ```
4. Ein Browser öffnet sich automatisch mit der App unter `http://localhost:8501`

> Wenn du Änderungen im Code speicherst, aktualisiert sich die App automatisch im Browser.

---

## Schritt 3 — Code ändern mit Claude

Claude ist dein KI-Assistent direkt in VS Code. So arbeitest du damit:

**Änderung vorschlagen lassen:**
- Markiere einen Code-Abschnitt → Rechtsklick → **"Ask Claude"**
- Oder öffne das Claude-Panel links und schreibe z.B.:
  > *"In der Datei landing.py — füge unter dem Hero-Bereich einen neuen Abschnitt mit Testimonials ein"*

**Typische Anfragen an Claude:**
- *"Erkläre mir was diese Funktion macht"*
- *"Ändere die Farbe des Buttons in landing.py auf grün"*
- *"Füge eine neue FAQ-Frage hinzu: ..."*
- *"Die App zeigt einen Fehler — hilf mir ihn zu finden"*

**Wichtig:** Claude schlägt Änderungen vor — du musst sie selbst abspeichern (`Cmd+S` / `Ctrl+S`).

---

## Schritt 4 — Änderungen speichern & hochladen

Nachdem du etwas geändert hast, musst du es auf GitHub pushen, damit alle die Änderungen sehen und die öffentliche App aktuell bleibt.

Im Terminal:

```bash
# 1. Neueste Version vom Repo holen (immer zuerst!)
git pull

# 2. Deine Änderungen vormerken
git add .

# 3. Änderung beschreiben
git commit -m "Kurze Beschreibung was du geändert hast"

# 4. Hochladen
git push
```

**Beispiel:**
```bash
git pull
git add .
git commit -m "Neue FAQ-Frage hinzugefügt"
git push
```

> Beim ersten `git push` wirst du nach deinem GitHub-Benutzernamen und einem **Personal Access Token** gefragt (kein Passwort!). Token erstellen: GitHub → Profilbild → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token → Haken bei `repo` setzen.

---

## Schritt 5 — Öffentliche App aktualisiert sich automatisch

Sobald dein `git push` erfolgreich war:

1. Geh auf **share.streamlit.io**
2. Logge dich mit dem GitHub-Account **BH3456BHHH** ein
3. Die App erkennt automatisch den neuen Code und deployt ihn

Nach ~1–2 Minuten ist die Änderung live und über den öffentlichen Link sichtbar.

---

## Die wichtigsten Dateien

| Datei | Was sie macht |
|-------|---------------|
| `interface.py` | Haupt-App: CV-Upload, Scoring, Ergebnisse, Career Readiness |
| `landing.py` | Startseite (Hero, FAQ, Features, Logos) |
| `career_readiness_ai.py` | Logik hinter Career Readiness (keine API nötig) |
| `*.csv` | Datenbanken: Alumni, Kurse, Arbeitgeber |

---

## Häufige Probleme

**"ModuleNotFoundError: streamlit"**
```bash
pip install streamlit pdfplumber
```

**"git push" fragt nach Passwort und schlägt fehl**
→ Du brauchst einen Personal Access Token (siehe Schritt 4 oben), kein normales GitHub-Passwort.

**Änderungen anderer sind nicht sichtbar**
→ Vergiss nicht: `git pull` immer zuerst ausführen, bevor du anfängst zu arbeiten.

**App startet nicht / Port besetzt**
```bash
python -m streamlit run interface.py --server.port 8502
```

---

## Zusammenfassung: Der tägliche Ablauf

```
1. git pull          ← neuesten Stand holen
2. Code ändern       ← mit Claude oder selbst
3. App testen        ← python -m streamlit run interface.py
4. git add .
5. git commit -m "..."
6. git push          ← live auf der öffentlichen App
```

---

*Nova CareerPath · Nova School of Business & Economics · Introduction to Programming · 2026*
