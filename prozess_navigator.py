import streamlit as st

# ===================
# 1) Prozess-Definition
# ===================
prozess = {
    # Lieferungen (werden nie als To-Do angezeigt)
    "MFB von Herter":         {"typ": "lieferung",    "abhaengig_von": []},
    "Fragebögen":             {"typ": "lieferung",    "abhaengig_von": []},
    "Ziel DSB von Destatis":  {"typ": "lieferung",    "abhaengig_von": []},
    "Variste prüf":           {"typ": "lieferung",    "abhaengig_von": []},
    "Metadatenreport":        {"typ": "lieferung",    "abhaengig_von": []},
    "Testdaten":              {"typ": "lieferung",    "abhaengig_von": []},

    # Zwischenschritte & Endprodukte
    "MFB Spalten A-M + Operatoren":      {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter"]},
    "MFB mit Spalten P-Q":               {"typ": "zwischenschritt", "abhaengig_von": ["Fragebögen"]},
    "Schlüsselverzeichnis und IHB":      {"typ": "zwischenschritt", "abhaengig_von": ["MFB mit Spalten P-Q"]},
    "MFB":                               {"typ": "zwischenschritt", "abhaengig_von": ["MFB Spalten A-M + Operatoren","Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 1":                  {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["Schlüsselverzeichnis und IHB"]},
    "Fachserien Tabellen vorbereiten":   {"typ": "zwischenschritt", "abhaengig_von": ["DHB Kommentare 1"]},
    "Vergröberungen + Korrekturen":      {"typ": "zwischenschritt", "abhaengig_von": ["Variste prüf"]},
    "DHB Kommentare 2":                  {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen","Ziel DSB"]},
    "Missingdefinitionen":               {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Tools":                             {"typ": "zwischenschritt", "abhaengig_von": ["Missingdefinitionen"]},
    "Missy Texte":                       {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},

    "Ziel DSB":                          {"typ": "endprodukt",     "abhaengig_von": ["Ziel DSB von Destatis","MFB Spalten A-M + Operatoren","MFB mit Spalten P-Q","Fragebögen"]},
    "ZP Matrix + Thematische Liste":     {"typ": "endprodukt",     "abhaengig_von": ["Ziel DSB"]},
    "Metadatenreport final":             {"typ": "endprodukt",     "abhaengig_von": ["Metadatenreport"]},
    "Tabelle Erhebungsprogramme":        {"typ": "endprodukt",     "abhaengig_von": ["Metadatenreport final"]},
    "Inhaltliche Prüfung":               {"typ": "endprodukt",     "abhaengig_von": ["Testdaten"]},
    "Technische Prüfung":                {"typ": "endprodukt",     "abhaengig_von": ["Testdaten"]},
    "DHB":                               {"typ": "endprodukt",     "abhaengig_von": ["Inhaltliche Prüfung","Technische Prüfung","Fachserien Tabellen vorbereiten"]},
    "Missy Variablenmatrix":             {"typ": "endprodukt",     "abhaengig_von": ["Tools"]},
    "Missy Veröffentlichung":            {"typ": "endprodukt",     "abhaengig_von": ["Missy Variablenmatrix","Missy Texte"]},
}

# ===================
# 2) Logik: nächste Schritte ermitteln
# ===================
def finde_naechste_schritte(prozess, erledigt):
    naechste = []
    for schritt, daten in prozess.items():
        # nicht schon erledigt, kein Lieferungstyp und alle Abhängigkeiten erfüllt?
        if (
            schritt not in erledigt
            and daten["typ"] != "lieferung"
            and all(dep in erledigt for dep in daten["abhaengig_von"])
        ):
            naechste.append(schritt)
    return naechste

# ===================
# 3) Streamlit-App
# ===================
def main():
    st.title("📊 Prozessnavigator")

    # Session-State initialisieren
    if "erledigt" not in st.session_state:
        st.session_state.erledigt = []

    # Sidebar: erledigte Schritte
    st.sidebar.header("✅ Erledigte Schritte")
    for s in st.session_state.erledigt:
        st.sidebar.write(f"- {s}")

    # Berechne und zeige nächste Schritte
    naechste = finde_naechste_schritte(prozess, st.session_state.erledigt)
    st.header("🔜 Nächste Schritte")
    if naechste:
        for schritt in naechste:
            # Jeder Button braucht einen eigenen key
            if st.button(f"Markiere '{schritt}' als erledigt", key=schritt):
                st.session_state.erledigt.append(schritt)
                st.experimental_rerun()
    else:
        st.write("🎉 Alle aktuellen Schritte erledigt oder warte auf neue Lieferungen.")

if __name__ == "__main__":
    main()
