import streamlit as st

st.set_page_config(layout="wide")
st.title("Modulübersicht mit fester Anordnung")

# Deine Daten (gekürzt dargestellt)
module_data = {
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},
    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter","Fragebögen"]},
    "MFB mit Spalten P-Q": {"typ": "lieferung", "abhaengig_von": []},
    "Vergröberungen + Korrekturen": {"typ": "zwischenschritt", "abhaengig_von": ["Variste prüf"]},
    "Metadatenreport final": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Inhaltliche Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten","Fachserien Tabellen vorbereiten"]},
    "Missingdefinitionen": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missy Texte": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Schlüsselverzeichnis und IHB": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis","MFB mit Spalten P-Q","Fragebögen","Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 2": {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen"]},
    "Tabelle Erhebungsprogramme": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Technische Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten"]},
    "Tools": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Missy Veröffentlichung": {"typ": "endprodukt", "abhaengig_von": ["Missy Variablenmatrix", "Missy Texte"]},
    "MFB": {"typ": "endprodukt", "abhaengig_von": ["MFB mit Spalten P-Q","Schlüsselverzeichnis und IHB","Ziel DSB"]},
    "DHB": {"typ": "endprodukt", "abhaengig_von": ["Testdaten","DHB Kommentare 2", "DHB Kommentare 1"]},
    "Missy Variablenmatrix": {"typ": "endprodukt", "abhaengig_von": ["ZP Matrix + Thematische Liste"]},
    "DHB Kommentare 1": {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["MFB","Ziel DSB"]},
    "ZP Matrix + Thematische Liste": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB"]},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": []}
}

# Modul-Grid (8 Spalten pro Zeile)
grid = [
    ["MFB von Herter", "MFB Spalten A-M + Operatoren", "", "MFB", "DHB Kommentare 1", ""],
    ["Fragebögen", "MFB mit Spalten P-Q", "Schlüsselverzeichnis und IHB", "", "Routinen für Filtermissings an IT NRW", "Fachserien Tabellen vorbereiten"],
    ["Ziel DSB von Destatis", "", "Ziel DSB", "", "ZP Matrix + Thematische Liste", ""],
    ["Variste prüf", "Vergröberungen + Korrekturen", "DHB Kommentare 2", "", "", ""],
    ["Metadatenreport", "Metadatenreport final", "Tabelle Erhebungsprogramme", "", "", ""],
    ["Testdaten", "Inhaltliche Prüfung", "Technische Prüfung", "DHB", "", ""],
    ["Testdaten", "Missingdefinitionen", "Tools", "", "", ""],
    ["", "Missy Texte", "Missy Veröffentlichung", "Missy Variablenmatrix", "", ""],
]


# User-Auswahl
if "active_modules" not in st.session_state:
    st.session_state.active_modules = set()

st.markdown("### Module auswählen:")
for name in module_data.keys():
    checked = name in st.session_state.active_modules
    if st.checkbox(name, value=checked, key=f"chk_{name}"):
        st.session_state.active_modules.add(name)
    else:
        st.session_state.active_modules.discard(name)

# Graph generieren
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

    dot = 'digraph G {\n  rankdir=LR;\n  node [shape=box];\n'

    # Subgraphs für Reihenfolge
    for i, row in enumerate(grid):
        dot += f'  subgraph cluster_row_{i} {{\n    rank=same;\n'
        for name in row:
            if name:
                dot += f'    "{name}" [{node_style(name)}];\n'
        dot += '  }\n'

    # Kanten
    for target, info in module_data.items():
        for source in info["abhaengig_von"]:
            style = 'color=red, penwidth=2' if source in active_modules else ''
            dot += f'  "{source}" -> "{target}" [{style}];\n'

    dot += '}'
    return dot

# Visualisierung
st.graphviz_chart(build_graph(grid, st.session_state.active_modules))
