import streamlit as st
from graphviz import Digraph

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
# Funktion für nächste Schritte (ohne Lieferungen)
# ===================
def finde_naechste_schritte(prozess, erledigt):
    return [
        schritt for schritt, daten in prozess.items()
        # Lieferungen (typ "lieferung") nicht als To-Do listen
        if daten["typ"] != "lieferung"
        and schritt not in erledigt
        and all(dep in erledigt for dep in daten["abhaengig_von"])
    ]

# ===================
# Streamlit UI
# ===================
st.set_page_config(page_title="Prozess-Navigator", layout="wide")
st.title("📊 Prozessnavigator")

view = st.sidebar.radio("Ansicht wählen:", ["Diagramm", "Checkliste"]);

if view == "Diagramm":
    # Graphviz-Diagramm rendern
    dot = Digraph()
    # Knoten mit Farben nach Typ
    farben = {"lieferung": "purple", "zwischenschritt": "blue", "endprodukt": "turquoise"}
    for schritt, daten in prozess.items():
        dot.node(schritt, schritt, style="filled", fillcolor=farben[daten["typ"]])
        for dep in daten["abhaengig_von"]:
            dot.edge(dep, schritt)
    st.graphviz_chart(dot)

else:
    st.write("Markiere die Schritte, die du **bereits erledigt** hast:")
    alle_schritte = list(prozess.keys())
    erledigt = st.multiselect("✅ Erledigte Schritte auswählen", options=alle_schritte)
    moeglich = finde_naechste_schritte(prozess, erledigt)

    st.divider()
    st.subheader("🔜 Mögliche nächste Schritte")

    if moeglich:
        st.success("Diese Schritte kannst du jetzt durchführen:")
        for schritt in moeglich:
            typ = prozess[schritt]["typ"]
            st.markdown(f"✅ **{schritt}** *(Typ: {typ})*")
    else:
        st.info("Keine weiteren Schritte möglich – entweder alles erledigt oder Abhängigkeiten fehlen.")
