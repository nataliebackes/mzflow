import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
 
# ===================
 # Prozess-Definition
# ===================
 
prozess = { 
    # Lieferungen (werden nie als To-Do angezeigt, kommen aber als Voraussetzung rein)
     "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
     "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
     "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
     "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
     "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
     "Testdaten": {"typ": "lieferung", "abhaengig_von": []},
 
     # Zwischenschritte & Endprodukte
     "MFB Spalten A-M + Operatoren":      {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter"]},
     "MFB mit Spalten P-Q":               {"typ": "zwischenschritt", "abhaengig_von": ["Fragebögen"]},
     "Schlüsselverzeichnis und IHB":      {"typ": "zwischenschritt", "abhaengig_von": ["MFB mit Spalten P-Q"]},
     "MFB":                               {"typ": "zwischenschritt", "abhaengig_von": ["MFB Spalten A-M + Operatoren","Schlüsselverzeichnis und IHB"]},
     "DHB Kommentare 1":                  {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["Schlüsselverzeichnis und IHB","MFB","Ziel DSB"]},
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
 

 # == Logik zum Rendern des Graphen ==
def render_graph(prozess):
    nodes = []
    edges = []

    for step, data in prozess.items():
        # Knoten nur für Zwischenschritte und Endprodukte (nicht für Lieferungen)
        if data["typ"] != "lieferung":
            nodes.append(Node(id=step, label=step, size=30))

        # Abhängigkeiten als Kanten
        for dep in data["abhaengig_von"]:
            edges.append(Edge(source=dep, target=step))

    # Konfiguration für die Visualisierung
    config = Config(width=900, height=500, directed=True)
    return agraph(nodes=nodes, edges=edges, config=config)

# == Streamlit-App ==
def main():
    st.title("Prozessnavigator")

    # Visualisierung des Prozesses
    graph = render_graph(prozess)
    st.write("Interaktive Prozessvisualisierung:")
    st.graphviz_chart(graph)

if __name__ == "__main__":
    main()

# ===================
# 3) Logik: nächste Schritte ermitteln
# ===================
def finde_naechste_schritte(prozess, erledigt):
    naechste = []
    for schritt, daten in prozess.items():
        if (
            schritt not in erledigt
            and daten["typ"] != "lieferung"
            and all(dep in erledigt for dep in daten["abhaengig_von"] )
        ):
            naechste.append(schritt)
    return naechste

# ===================
# 4) Streamlit-App
# ===================
def main():
    st.set_page_config(page_title="Prozessnavigator", layout="wide")
    st.title("📊 Prozessnavigator")

    # Diagramm anzeigen
    st.subheader("Prozessdiagramm")
    dot = render_graph(prozess)
    st.graphviz_chart(dot)

    # Sidebar: erledigte Schritte
    if "erledigt" not in st.session_state:
        st.session_state.erledigt = []
    st.sidebar.header("✅ Erledigte Schritte")
    # Auswahl in Sidebar
    erledigt = st.sidebar.multiselect(
        "Wähle erledigte Schritte:",
        options=[n for n in prozess if prozess[n]["typ"] != "lieferung"],
        default=st.session_state.erledigt
    )
    st.session_state.erledigt = erledigt

    # Nächste Schritte
    st.subheader("🔜 Nächste Schritte")
    naechste = finde_naechste_schritte(prozess, st.session_state.erledigt)
    if naechste:
        for s in naechste:
            if st.button(f"Erledige {s}", key=s):
                st.session_state.erledigt.append(s)
                st.experimental_rerun()
    else:
        st.info("Keine weiteren Schritte – alles erledigt oder warte auf neue Lieferungen.")

if __name__ == "__main__":
    main()
