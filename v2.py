import streamlit as st
import graphviz

# Layout und Titel
st.set_page_config(layout="wide")
st.title("Interaktive Modulübersicht")

# Deine Modul-Daten
module_data = {
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},
    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter", "Fragebögen"]},
    "MFB mit Spalten P-Q": {"typ": "lieferung", "abhaengig_von": []},
    "Vergröberungen + Korrekturen": {"typ": "zwischenschritt", "abhaengig_von": ["Variste prüf"]},
    "Metadatenreport final": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Inhaltliche Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "Fachserien Tabellen vorbereiten"]},
    "Missingdefinitionen": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missy Texte": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Schlüsselverzeichnis und IHB": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis", "MFB mit Spalten P-Q", "Fragebögen", "Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 2": {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen"]},
    "Tabelle Erhebungsprogramme": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Technische Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten"]},
    "Tools": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missy Veröffentlichung": {"typ": "endprodukt", "abhaengig_von": ["Missy Variablenmatrix", "Missy Texte"]},
    "MFB": {"typ": "endprodukt", "abhaengig_von": ["MFB mit Spalten P-Q", "Schlüsselverzeichnis und IHB", "Ziel DSB"]},
    "DHB": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "DHB Kommentare 2", "DHB Kommentare 1"]},
    "Missy Variablenmatrix": {"typ": "endprodukt", "abhaengig_von": ["ZP Matrix + Thematische Liste"]},
    "DHB Kommentare 1": {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["MFB", "Ziel DSB"]},
    "ZP Matrix + Thematische Liste": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB"]},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": []}
}

# Interaktive Modulauswahl
if "active_modules" not in st.session_state:
    st.session_state.active_modules = set()

st.markdown("### Wählen Sie die Module aus:")
for name in module_data.keys():
    checked = name in st.session_state.active_modules
    if st.checkbox(name, value=checked, key=f"chk_{name}"):
        st.session_state.active_modules.add(name)
    else:
        st.session_state.active_modules.discard(name)

# Raster-Grid mit 8 Spalten und 6 Zeilen
grid = [
    ["MFB von Herter", "Fragebögen", "Ziel DSB von Destatis", "Variste prüf", "Metadatenreport", "Testdaten", "Testdaten", ""],
    ["MFB Spalten A-M + Operatoren", "MFB mit Spalten P-Q", "", "Vergröberungen + Korrekturen", "Metadatenreport final", "Inhaltliche Prüfung", "Missingdefinitionen", "Missy Texte"],
    ["", "Schlüsselverzeichnis und IHB", "Ziel DSB", "DHB Kommentare 2", "Tabelle Erhebungsprogramme", "Technische Prüfung", "Tools", "Missy Veröffentlichung"],
    ["MFB", "", "", "", "", "DHB", "", "Missy Variablenmatrix"],
    ["DHB Kommentare 1", "Routinen für Filtermissings an IT NRW", "ZP Matrix + Thematische Liste", "", "", "", "", ""],
    ["", "Fachserien Tabellen vorbereiten", "", "", "", "", "", ""]
]

# Graphviz Graph generieren
def build_graph(grid, active_modules):
    def node_style(name):
        if name in active_modules:
            return 'color=red, penwidth=3'
        typ = module_data[name]["typ"]
        if typ == "lieferung":
            return 'style=filled, fillcolor=lightblue'
        elif typ == "zwischenschritt":
            return 'style=filled, fillcolor=lightyellow'
        elif typ == "endprodukt":
            return 'style=filled, fillcolor=lightgreen'
        return ''

    dot = 'digraph G {\n  rankdir=LR;\n  node [shape=box, width=1.5, height=1.0, fixedsize=true];\n'

    # Subgraphs für Reihenfolge und feste Positionen
    for i, row in enumerate(grid):
        dot += f'  subgraph cluster_row_{i} {{\n    rank=same;\n'
        for j, name in enumerate(row):
            if name:
                dot += f'    "{name}" [{node_style(name)}];\n'
            # Leere Felder werden als invisible Knoten behandelt
            else:
                dot += f'    "{i}_{j}" [style=invisible, width=0, height=0];\n'
        dot += '  }\n'

    # Kanten (Abhängigkeiten) hinzufügen
    for target, info in module_data.items():
        for source in info["abhaengig_von"]:
            style = 'color=red, penwidth=2' if source in active_modules else ''
            dot += f'  "{source}" -> "{target}" [{style}];\n'

    dot += '}'
    return dot

# Visualisierung anzeigen
st.graphviz_chart(build_graph(grid, st.session_state.active_modules))
