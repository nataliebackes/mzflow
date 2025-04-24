import streamlit as st

# ===================
# Prozess-Definition
# ===================
prozess = {
    # Lieferungen (werden nie als To-Do angezeigt, kommen aber als Voraussetzung rein)
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Schlüsselverzeichnis und IHB": {"typ": "zwischenschritt", "abhaengig_von": []},
    "MFB mit Spalten P-Q": {"typ": "zwischenschritt", "abhaengig_von": []},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},

    # Zwischenschritte & Endprodukte
    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter", "Fragebögen"]},
    "MFB": {"typ": "zwischenschritt", "abhaengig_von": ["MFB mit Spalten P-Q", "Schlüsselverzeichnis und IHB", "Ziel DSB"]},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis", "MFB Spalten P-Q", "Fragebögen", "Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 1": {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["MFB", "Ziel DSB"]},
    "ZP Matrix + Thematische Liste": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB"]},
    "Vergröberungen + Korrekturen": {"typ": "zwischenschritt", "abhaengig_von": ["Variste prüf"]},
    "DHB Kommentare 2": {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen"]},
    "Missingdefinitionen": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Tools": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missy Texte": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Metadatenreport final": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Tabelle Erhebungsprogramme": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Inhaltliche Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "Fachserien Tabellen vorbereiten"]},
    "Technische Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten"]},
    "DHB": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "DHB Kommentare 2", "DHB Kommentare 1"]},
    "Missy Variablenmatrix": {"typ": "endprodukt", "abhaengig_von": ["ZP Matrix + Thematische Liste"]},
    "Missy Veröffentlichung": {"typ": "endprodukt", "abhaengig_von": ["Missy Variablenmatrix", "Missy Texte"]},
}

# ===================
# Logik: nächste Schritte ermitteln
# ===================
def finde_naechste_schritte(prozess, erledigt):
    naechste = []
    for schritt, daten in prozess.items():
        if (
            daten["typ"] != "lieferung"
            and schritt not in erledigt
            and all(dep in erledigt for dep in daten["abhaengig_von"])
        ):
            naechste.append(schritt)
    return naechste

# ===================
# Streamlit-App
# ===================
def main():
    st.set_page_config(page_title="Prozessnavigator", layout="wide")
    st.title("📊 Prozessnavigator")

    # Initialisiere Session-State für Lieferungen und erledigte Schritte
    if "arrived" not in st.session_state:
        st.session_state.arrived = []
    if "completed" not in st.session_state:
        st.session_state.completed = []
    if "completed_endprodukte" not in st.session_state:
        st.session_state.completed_endprodukte = []

    # Sidebar: Lieferungen markieren
    st.sidebar.header("🔌 Lieferungen")
    lieferungen = [s for s, d in prozess.items() if d["typ"] == "lieferung"]
    st.session_state.arrived = st.sidebar.multiselect(
        "Welche Lieferungen sind da?", lieferungen, default=st.session_state.arrived
    )

    # Sidebar: Erledigte Schritte markieren (inklusive Endprodukte)
    st.sidebar.header("✅ Erledigte Schritte")
    schritte = [s for s, d in prozess.items() if d["typ"] != "lieferung" and d["typ"] != "endprodukt"]
    st.session_state.completed = st.sidebar.multiselect(
        "Welche Schritte sind erledigt?", schritte, default=st.session_state.completed
    )

    # Sidebar: Erledigte Endprodukte markieren
    st.sidebar.header("✅ Erledigte Endprodukte")
    endprodukte = [s for s, d in prozess.items() if d["typ"] == "endprodukt"]
    st.session_state.completed_endprodukte = st.sidebar.multiselect(
        "Welche Endprodukte sind erledigt?", endprodukte, default=st.session_state.completed_endprodukte
    )

    # Kombiniere Lieferungen + erledigte Schritte + erledigte Endprodukte als Erledigt-Voraussetzungen
    erledigt = list(set(st.session_state.arrived + st.session_state.completed + st.session_state.completed_endprodukte))

    # Hauptbereich: nächste Schritte
    st.subheader("🔜 Nächste Schritte")
    naechste = finde_naechste_schritte(prozess, erledigt)
    if naechste:
        for schritt in naechste:
            st.write(f"- {schritt}")
    else:
        st.write("🎉 Keine weiteren Schritte möglich oder alles erledigt.")

if __name__ == "__main__":
    main()
