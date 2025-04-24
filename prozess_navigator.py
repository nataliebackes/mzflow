import streamlit as st

# Beispielhafte Prozessdaten (dies sollten deine echten Daten sein)
prozess_daten = [
    {"id": "MFB von Herter", "name": "MFB von Herter", "typ": "Zwischenschritt"},
    {"id": "Fragebögen", "name": "Fragebögen", "typ": "Zwischenschritt"},
    {"id": "Ziel DSB von Destatis", "name": "Ziel DSB von Destatis", "typ": "Zwischenschritt"},
    {"id": "Variste prüf", "name": "Variste prüf", "typ": "Zwischenschritt"},
    {"id": "Metadatenreport", "name": "Metadatenreport", "typ": "Zwischenschritt"},
    {"id": "Testdaten", "name": "Testdaten", "typ": "Zwischenschritt"},
    {"id": "MFB Spalten A-M + Operatoren", "name": "MFB Spalten A-M + Operatoren", "typ": "Zwischenschritt"},
    {"id": "MFB mit Spalten P-Q", "name": "MFB mit Spalten P-Q", "typ": "Zwischenschritt"},
    {"id": "Schlüsselverzeichnis und IHB", "name": "Schlüsselverzeichnis und IHB", "typ": "Zwischenschritt"},
    {"id": "MFB", "name": "MFB", "typ": "Zwischenschritt"},
    {"id": "DHB Kommentare 1", "name": "DHB Kommentare 1", "typ": "Zwischenschritt"},
    {"id": "Routinen für Filtermissings an IT NRW", "name": "Routinen für Filtermissings an IT NRW", "typ": "Zwischenschritt"},
    {"id": "Fachserien Tabellen vorbereiten", "name": "Fachserien Tabellen vorbereiten", "typ": "Zwischenschritt"},
    {"id": "Vergröberungen + Korrekturen", "name": "Vergröberungen + Korrekturen", "typ": "Zwischenschritt"},
    {"id": "DHB Kommentare 2", "name": "DHB Kommentare 2", "typ": "Zwischenschritt"},
    {"id": "Ziel DSB", "name": "Ziel DSB", "typ": "Endprodukt"},
    {"id": "ZP Matrix + Thematische Liste", "name": "ZP Matrix + Thematische Liste", "typ": "Endprodukt"},
    {"id": "Metadatenreport final", "name": "Metadatenreport final", "typ": "Endprodukt"},
    {"id": "Tabelle Erhebungsprogramme", "name": "Tabelle Erhebungsprogramme", "typ": "Endprodukt"},
    {"id": "Inhaltliche Prüfung", "name": "Inhaltliche Prüfung", "typ": "Endprodukt"},
    {"id": "Technische Prüfung", "name": "Technische Prüfung", "typ": "Endprodukt"},
    {"id": "DHB", "name": "DHB", "typ": "Endprodukt"},
    {"id": "Missingdefinitionen", "name": "Missingdefinitionen", "typ": "Endprodukt"},
    {"id": "Tools", "name": "Tools", "typ": "Endprodukt"},
    {"id": "Missy Texte", "name": "Missy Texte", "typ": "Endprodukt"},
    {"id": "Missy Variablenmatrix", "name": "Missy Variablenmatrix", "typ": "Endprodukt"},
    {"id": "Missy Veröffentlichung", "name": "Missy Veröffentlichung", "typ": "Endprodukt"},
]

# Abhängigkeiten definieren: Wer muss vorher erledigt sein
abhaengigkeiten = {
    "MFB von Herter": [],
    "Fragebögen": [],
    "Ziel DSB von Destatis": [],
    "Variste prüf": [],
    "Metadatenreport": [],
    "Testdaten": [],
    "MFB Spalten A-M + Operatoren": ["MFB von Herter"],
    "MFB mit Spalten P-Q": ["Fragebögen"],
    "Schlüsselverzeichnis und IHB": ["MFB mit Spalten P-Q"],
    "MFB": ["MFB Spalten A-M + Operatoren", "Schlüsselverzeichnis und IHB"],
    "DHB Kommentare 1": ["MFB"],
    "Routinen für Filtermissings an IT NRW": ["Schlüsselverzeichnis und IHB"],
    "Fachserien Tabellen vorbereiten": ["DHB Kommentare 1"],
    "Vergröberungen + Korrekturen": ["Variste prüf"],
    "DHB Kommentare 2": ["Vergröberungen + Korrekturen", "Ziel DSB"],
    "Ziel DSB": ["Ziel DSB von Destatis", "MFB Spalten A-M + Operatoren", "MFB mit Spalten P-Q", "Fragebögen"],
    "ZP Matrix + Thematische Liste": ["Ziel DSB"],
    "Metadatenreport final": ["Metadatenreport"],
    "Tabelle Erhebungsprogramme": ["Metadatenreport final"],
    "Inhaltliche Prüfung": ["Testdaten"],
    "Technische Prüfung": ["Testdaten"],
    "DHB": ["Inhaltliche Prüfung", "Technische Prüfung", "Fachserien Tabellen vorbereiten"],
    "Missingdefinitionen": ["Testdaten"],
    "Tools": ["Missingdefinitionen"],
    "Missy Texte": ["Testdaten"],
    "Missy Variablenmatrix": ["Tools"],
    "Missy Veröffentlichung": ["Missy Variablenmatrix", "Missy Texte"],
}

# Funktion zum Finden der nächsten Schritte unter Berücksichtigung der Abhängigkeiten
def finde_naechste_schritte(daten, erledigte_schritte):
    naechste_schritte = []
    
    # Durchlaufe alle Schritte und prüfe, ob deren Abhängigkeiten erledigt sind
    for schritt in daten:
        schritt_name = schritt["name"]
        
        # Prüfe, ob der Schritt nicht erledigt ist und alle Abhängigkeiten erledigt sind
        if schritt_name not in erledigte_schritte and all(abh in erledigte_schritte for abh in abhaengigkeiten.get(schritt_name, [])):
            naechste_schritte.append(schritt_name)
    
    return naechste_schritte

# Haupt-Streamlit App
def main():
    st.title("Prozessnavigator")
    
    # Lade den Fortschritt der erledigten Schritte (Verwendung von Session-State)
    if "erledigte_schritte" not in st.session_state:
        st.session_state.erledigte_schritte = []

    # Zeige aktuelle erledigte Schritte in der Sidebar
    st.sidebar.header("Erledigte Schritte")
    for schritt in st.session_state.erledigte_schritte:
        st.sidebar.write(f"- {schritt}")

    # Finde die nächsten Schritte, die erledigt werden müssen
    naechste_schritte = finde_naechste_schritte(prozess_daten, st.session_state.erledigte_schritte)
    
    st.header("Nächste Schritte")
    if naechste_schritte:
        for schritt in naechste_schritte:
            if schritt != "Lieferung 1":  # Lieferungen nicht als To-Do anzeigen
                if st.button(f"Markiere {schritt} als erledigt"):
                    st.session_state.erledigte_schritte.append(schritt)
                    st.experimental_rerun()  # Die Seite neu laden, um den neuen Status zu reflektieren
    else:
        st.write("Keine weiteren Schritte zum Erledigen! 🎉")

# Starte die App
if __name__ == "__main__":
    main()
