import streamlit as st

st.set_page_config(layout="wide")
st.title("Interaktives Abhängigkeitsdiagramm")

# Die Modulstruktur mit Abhängigkeiten
module_data = {
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Schlüsselverzeichnis und IHB": {"typ": "lieferung", "abhaengig_von": []},
    "MFB mit Spalten P-Q": {"typ": "lieferung", "abhaengig_von": []},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Variste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},

    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter", "Fragebögen"]},
    "MFB": {"typ": "endprodukt", "abhaengig_von": ["MFB mit Spalten P-Q", "Schlüsselverzeichnis und IHB", "Ziel DSB"]},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis", "MFB mit Spalten P-Q", "Fragebögen", "Schlüsselverzeichnis und IHB"]},
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

module_names = list(module_data.keys())

# Session State für aktive Module
if "active_modules" not in st.session_state:
    st.session_state.active_modules = set()

# Checkbox-Auswahl
st.markdown("### Module auswählen (Mehrfachauswahl möglich):")
for mod in module_names:
    checked = mod in st.session_state.active_modules
    if st.checkbox(mod, value=checked, key=f"chk_{mod}"):
        st.session_state.active_modules.add(mod)
    else:
        st.session_state.active_modules.discard(mod)

# Umkehren der Abhängigkeiten für gerichtete Pfeile
edges = []
for target, info in module_data.items():
    for source in info["abhaengig_von"]:
        edges.append((source, target))

# Graphviz-Generierung
def build_graph(active_modules):
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

    graph = "digraph G {\n  rankdir=LR;\n  node [shape=box];\n"
    for name in module_names:
        graph += f'  "{name}" [{node_style(name)}];\n'
    for src, tgt in edges:
        style = 'color=red, penwidth=2' if src in active_modules else ''
        graph += f'  "{src}" -> "{tgt}" [{style}];\n'
    graph += "}"
    return graph

# Visualisierung anzeigen
st.graphviz_chart(build_graph(st.session_state.active_modules))
