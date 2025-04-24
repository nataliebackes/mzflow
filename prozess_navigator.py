import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

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
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["MFB","Schlüsselverzeichnis und IHB"]},
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
# 2) Generiere Nodes & Edges für AGraph
# ===================
nodes = []
edges = []

for step, data in prozess.items():
    # Farbe nach Typ
    color = "#D3D3D3"
    if data["typ"] == "lieferung": color = "#800080"  # lila
    if data["typ"] == "zwischenschritt": color = "#00008B"  # dunkelblau
    if data["typ"] == "endprodukt": color = "#40E0D0"  # türkis

    # Node hinzufügen
    nodes.append(Node(id=step, label=step, color=color))

    # Kanten (Abhängigkeiten)
    for dep in data["abhaengig_von"]:
        edges.append(Edge(source=dep, target=step))

# Config für AGraph
config = Config(
    width=800,
    height=400,
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor="#F0A202"
)

# ===================
# 3) Streamlit-App
# ===================

def main():
    st.title("📊 Prozessnavigator mit interaktivem Graphen")

    # Session-State initialisieren
    if "erledigt" not in st.session_state:
        st.session_state.erledigt = []

    # Render interaktiven Graph und fange Klicks ab
    selected = agraph(nodes=nodes, edges=edges, config=config)
    if selected and selected not in st.session_state.erledigt:
        st.session_state.erledigt.append(selected)

    # Zeige erledigte Schritte
    st.sidebar.header("✅ Erledigte Schritte")
    for s in st.session_state.erledigt:
        st.sidebar.write(f"- {s}")

    # Berechne nächste Schritte
    def finde_naechste_schritte(prozess, erledigt):
        return [s for s, d in prozess.items()
                if s not in erledigt
                and d["typ"] != "lieferung"
                and all(dep in erledigt for dep in d["abhaengig_von"])]

    naechste = finde_naechste_schritte(prozess, st.session_state.erledigt)
    st.header("🔜 Nächste Schritte")
    if naechste:
        for s in naechste:
            st.write(f"- {s}")
    else:
        st.write("🎉 Alle aktuellen Schritte erledigt oder Warte auf neue Lieferungen.")

if __name__ == "__main__":
    main()
