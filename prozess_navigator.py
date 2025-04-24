import streamlit as st

# ===================
# Prozessstruktur
# ===================
prozess = {
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},
    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter"]},
    "MFB mit Spalten P-Q": {"typ": "zwischenschritt", "abhaengig_von": ["Fragebögen"]},
    "Schlüsselverzeichnis und IHB": {"typ": "zwischenschritt", "abhaengig_von": ["MFB mit Spalten P-Q"]},
    "MFB": {"typ": "zwischenschritt", "abhaengig_von": ["MFB Spalten A-M + Operatoren", "Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 1": {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["Schlüsselverzeichnis und IHB"]},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": ["DHB Kommentare 1"]},
    "Vergröberungen + Korrekturen": {"typ": "zwischenschritt", "abhaengig_von": ["Variste prüf"]},
    "DHB Kommentare 2": {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen", "Ziel DSB"]},
    "Tabelle Erhebungsprogramme": {"typ": "zwischenschritt", "abhaengig_von": ["Metadatenreport final"]},
    "Inhaltliche Prüfung": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Technische Prüfung": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missingdefinitionen": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Tools": {"typ": "zwischenschritt", "abhaengig_von": ["Missingdefinitionen"]},
    "Missy Texte": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis", "MFB mit Spalten P-Q", "MFB Spalten A-M + Operatoren"]},
    "ZP Matrix + Thematische Liste": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB"]},
    "Metadatenreport final": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "DHB": {"typ": "endprodukt", "abhaengig_von": ["Technische Prüfung", "Inhaltliche Prüfung"]},
    "Missy Variablenmatrix": {"typ": "endprodukt", "abhaengig_von": ["Tools"]},
    "Missy Veröffentlichung": {"typ": "endprodukt", "abhaengig_von": ["Missy Variablenmatrix", "Missy Texte"]},
}

# ===================
# Funktion: nächste Schritte
# ===================
def finde_naechste_schritte(prozess, erledigt):
    return [
        schritt for schritt, daten in prozess.items()
        if daten["typ"] != "lieferung"
        and schritt not in erledigt
        and all(dep in erledigt for dep in daten["abhaengig_von"])
    ]

# ===================
# Streamlit UI
# ===================
st.set_page_config(page_title="Prozess-Navigator", layout="wide")
st.title("📊 Prozessnavigator")

if "erledigt" not in st.session_state:
    st.session_state.erledigt = []

# Sidebar: erledigte Schritte
st.sidebar.header("✅ Erledigte Schritte")
for schritt in list(st.session_state.erledigt):
    if st.sidebar.button(f"Entferne: {schritt}", key=schritt):
        st.session_state.erledigt.remove(schritt)

# Sidebar: Diagramm-Links zum Klicken
st.sidebar.header("🔗 Prozessdiagramm")
for schritt, daten in prozess.items():
    if daten["typ"] != "lieferung":
        if st.sidebar.button(schritt, key=schritt+"btn"):
            if schritt not in st.session_state.erledigt:
                st.session_state.erledigt.append(schritt)

# Hauptbereich: Checkliste und nächste Schritte
st.subheader("Deine To-Dos")
st.write("Klicke in der Sidebar auf einen Schritt, um ihn als erledigt hinzuzufügen oder zu entfernen.")

moeglich = finde_naechste_schritte(prozess, st.session_state.erledigt)

st.markdown("**Mögliche nächste Schritte:**")
if moeglich:
    for schritt in moeglich:
        st.markdown(f"- {schritt}")
else:
    st.markdown("_Keine weiteren Schritte verfügbar._")
