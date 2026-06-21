import json
import pathlib
import sys
import cv

OUTPUT_FOLDER = pathlib.Path("output")
DATA_PATH = pathlib.Path("data/cv_data.json")
OUTPUT_PATH = OUTPUT_FOLDER / "Lebenslauf.pdf"


def lebenslauf_erstellen(cv_data: dict, ziel_pfad: pathlib.Path) -> None:
    """Erstellt das PDF-Dokument basierend auf den übergebenen CV-Daten."""
    try:
        ziel_pfad.parent.mkdir(parents=True, exist_ok=True)

        pdf = cv.CV(
            sidebar_x=140, 
            sidebar_w=70, 
            sidebar_h=297, 
            tech_profile=cv_data.get("technical_profile", {})
        )
        pdf.add_contact_info(
            cv_data["contact"]["address"],
            cv_data["contact"]["email"],
            cv_data["contact"]["phone"],
        )
        pdf.add_header_name(
            cv_data["contact"]["name"],
            cv_data["contact"]["jobtitle"],
            cv_data["contact"]["certificate"],
        )
        pdf.add_profile_summary(cv_data["profile_summary"])

        for key, values in cv_data["sections"].items():
            pdf.add_section(key, values)
        
        pdf.ensure_page2()

        pdf.output(ziel_pfad)
        print(f"✅ Erfolg: Lebenslauf wurde unter {ziel_pfad} erstellt!")

    except KeyError as e:
        print(f"❌ Strukturfehler in den Daten: Vermisse Schlüssel {e}")
    except PermissionError:
        print(
            f"❌ Fehler: Keine Schreibrechte für den Pfad '{ziel_pfad}'."
        )
    except Exception as e:
        print(f"❌ Unerwarteter Fehler bei der PDF-Erstellung: {e}")


def daten_laden(pfad: pathlib.Path) -> dict:
    """Lädt die JSON-Daten.

    Falls nicht gefunden, wird ein Template-Pfad versucht. Falls dieser
    auch fehlt, greift ein Hardcoded-Fallback.
    """
    try:
        with open(pfad, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(
            f"⚠️ Hinweis: Hauptdatei '{pfad}' nicht gefunden. Versuche Template..."
        )

        template_pfad = pfad.parent / "template_data.json"

        try:
            with open(template_pfad, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(
                f"❌ Schwerer Fehler: Auch Template '{template_pfad}' konnte nicht geladen werden ({e})."
            )
            print("🔄 Nutze minimalen Programm-Fallback im Arbeitsspeicher.")

            return {
                "contact": {
                    "name": "Max Mustermann",
                    "jobtitle": "Python Developer",
                    "certificate": "PCPP1",
                    "address": ["Musterstraße 1"],
                    "email": ["max@beispiel.de"],
                    "phone": ["+49 123"],
                },
                "profile_summary": "Fallback-Lebenslauf, da alle JSON-Dateien fehlen.",
                "sections": {},
            }

    except json.JSONDecodeError as e:
        print(f"❌ Fehler: Ungültiges JSON in Hauptdatei '{pfad}'.")
        print(f"Details: {e}")
        sys.exit(1)


def main() -> None:
    cv_data = daten_laden(DATA_PATH)
    lebenslauf_erstellen(cv_data, OUTPUT_PATH)


if __name__ == "__main__":
    main()