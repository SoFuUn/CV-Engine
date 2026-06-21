# Automated Python CV Creator 📄🚀

Ein automatisiertes Python-Tool zur dynamischen Generierung von modernen, professionellen Lebensläufen im PDF-Format. Die Steuerung erfolgt vollständig datengetrieben über eine zentrale JSON-Datei. Das Layout passt sich dynamisch an: Auf Seite 1 wird eine Sidebar links generiert, auf Seite 2 wechselt das System automatisch zu einer gespiegelten Sidebar auf der rechten Seite, um Platz für ein erweitertes technisches Profil zu schaffen.

Das Projekt ist nach fortgeschrittenen Python-Design-Standards objektorientiert implementiert.

## Features ✨

* **100% Datengetrieben:** Keine Code-Änderungen für inhaltliche oder strukturelle Updates nötig – reine Steuerung über JSON.
* **Intelligentes Multi-Page-Layout:** Erkennt automatisch den Übergang zu Seite 2, spiegelt die Sidebar nach rechts und platziert dort erweiterte Qualifikationen.
* **Modernes Text-Rendering:** Verhindert unschöne Lücken im Layout durch sauberen, linksbündigen Satz bei Spalten-Texten.
* **Custom Assets:** Einfacher Austausch von Profilbild und Kontaktsymbolen über den `assets`-Ordner mit flexibler Erkennung von `.png`, `.jpg` und `.jpeg`.
* **Kaskadierendes Fallback-System:** Dreistufige Absicherung (Hauptdatei -> Template-Datei -> Hardcoded Speicher-Fallback), die einen Programmabsturz selbst bei gelöschten Datenordnern verhindert.
* **Logging:** Integriertes Datei- und Konsolen-Logging zur lückenlosen Fehlernachverfolgung mit Zeitstempeln und Zeilennummern.

---

## Projektstruktur 📂

├── assets/                  # Visuelle Ressourcen (Bilder & Icons)
│   ├── mail.png             # Icon für E-Mail (Unterstützt png, jpg, jpeg)
│   ├── phone.png            # Icon für Telefonnummer
│   ├── pin.png              # Icon für Adresse / Standort
│   └── portrait.jpg         # Profilbild (wird automatisch via glob erkannt)
├── data/                    # Daten-Input & Vorlagen
│   ├── cv_data.json         # Die zentrale Inhalts-Datei (Hauptdatei)
│   └── template_data.json   # Lokales Sicherheits-Template (Fallback)
├── logs/                    # Automatisch generierte Log-Dateien
│   └── cv_generator.log     # Fehler- und Systemprotokolle
├── output/                  # Ausgabe-Verzeichnis
│   └── Lebenslauf.pdf       # Das fertig generierte, mehrseitige PDF
├── main.py                  # Hauptskript (Ausführung, Datenvalidierung & Orchestrierung)
├── lebenslauf.py            # PDF-Klassenarchitektur (Erweiterung von FPDF2 mit Event-Handling)
└── README.md                # Projektdokumentation

---

## Installation & Vorbereitung ⚙️

### 1. Voraussetzungen
Stelle sicher, dass Python 3.8+ installiert ist.

### 2. Abhängigkeiten installieren
Das Projekt basiert auf der modernen fpdf2-Bibliothek. Installiere die benötigten Pakete über dein Terminal:

pip install fpdf2

---

## Konfiguration & Anpassung 🛠️

### 1. Inhalt & Skills anpassen (`data/cv_data.json`)
Die Inhalte deines Lebenslaufs werden in der `cv_data.json` gepflegt. Für die erweiterte zweite Seite wurde das logische Keyword `technical_profile` implementiert.

Struktur-Beispiel:
{
    "contact": {
        "name": "Max Mustermann",
        "jobtitle": "Python Developer",
        "certificate": "PCEP, PCAP, PCPP1",
        "address": ["Musterstraße 1"],
        "email": ["max@beispiel.de"],
        "phone": ["+49 123 456789"]
    },
    "profile_summary": "Ambitionierter Python-Entwickler mit Fokus auf saubere Software-Architektur...",
    "sections": {
        "Praktika": [
            {
                "period": "2024 - Heute",
                "title": "Senior Python Engineer",
                "company": "Tech Solutions GmbH"
            }
        ]
    },
    "technical_profile": {
        "programming_languages": [
            {"name": "Python", "level": 5},
            {"name": "SQL", "level": 4},
            {"name": "JavaScript", "level": 3}
        ],
        "tools_frameworks": [
            "Git & GitHub", "Docker", "Django", "Flask"
        ],
        "focus_areas": [
            "Object-Oriented Programming (OOP)",
            "Clean Code & PEP 8",
            "Test-Driven Development (TDD)"
        ]
    }
}

### 2. Design & Medien austauschen (`assets/`)
* **Profilbild:** Ersetze die Datei im `assets/`-Ordner. Das Skript erkennt das Bild dynamisch, solange der Dateiname mit `portrait.` beginnt.
* **Icons:** Die Symbole für Adresse, Mail und Telefon können durch beliebige PNG- oder JPG-Dateien mit den Namen `pin`, `mail` und `phone` ersetzt werden (Groß-/Kleinschreibung wird ignoriert).
* **Ausfallsicherheit:** Sollten Assets fehlen, fängt das Programm dies ab und generiert minimalistische, geometrische Platzhalter im PDF.

---

## Anwendung 🚀

Führe das Hauptprogramm aus, um den Lebenslauf zu generieren:

python main.py

Nach erfolgreicher Ausführung findest du dein fertiges Dokument unter:
`output/Lebenslauf.pdf`

---

## Robustes Error-Handling & Logging 📋

Das Projekt ist für den produktiven Einsatz vorkonfiguriert:
* **JSON-Schutz:** Ungültige JSON-Formate in der Hauptdatei werden abgefangen und führen zu einem kontrollierten Programmende mit Fehlermeldung statt zu einem unschönen Python-Crash.
* **Hierarchischer Daten-Fallback:** Wenn die Hauptdatei fehlt, wird die `template_data.json` geladen. Fehlt auch diese, generiert das System die Daten direkt aus einem Hardcoded-Dictionary im Arbeitsspeicher.
* **Log-Protokoll:** Unter `logs/cv_generator.log` werden Systemwarnungen (z. B. fehlende Bilder) mit präzisen Zeitstempeln und Dateizeilen für das Debugging festgehalten.