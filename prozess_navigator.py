import streamlit as st
from streamlit_cytoscape import cyto

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
# Interaktive Graph-Darstellung mit Cytoscape
# ===================
def build_elements(prozess):
    elements = []
    # Nodes
    for schritt, daten in prozess.items():
        elements.append({
            "data": {"id": schritt, "label": schritt, "typ": daten["typ"]}
        })
    # Edges
    for schritt, daten in prozess.items():
        for dep in daten["abhaengig_von"]:
            elements.append({
                "data": {"source": dep, "target": schritt}
            })
    return elements

# Cytoscape Style-Definition
style = [
    {"selector": 'node[typ="lieferung"]', "style": {"background-color": "purple"}},
    {"selector": 'node[typ="zwischenschritt"]', "style": {"background-color": "blue"}},
    {"selector": 'node[typ="endprodukt"]', "style": {"background-color": "turquoise"}},
    {"selector": 'edge', "style": {"line-color": "gray"}}
]

# ===================
# Streamlit UI
# ===================
st.set_page_config(page_title="Prozess-Navigator", layout="wide")
st.title("📊 Prozessnavigator")

# Sidebar: Ansicht & erledigte Schritte
view = st.sidebar.radio("Ansicht wählen:", ["Diagramm", "Checkliste"])
if "erledigt" not in st.session_state:
    st.session_state.erledigt = []

if view == "Diagramm":
    st.write("**Klicke auf einen Knoten, um ihn als erledigt zu markieren.**")
    elements = build_elements(prozess)
    # render interactive cytoscape graph
    selected = cyto.cytoscape(
        id="cytoscape",
        elements=elements,
        layout={"name": "dagre"},
        style={"width": "100%", "height": "600px"},
        stylesheet=style,
    )
    # Wenn ein Node geklickt wird, füge zu erledigt hinzu
    if selected and hasattr(selected, 'last_clicked_node'):
        node_id = selected.last_clicked_node
        if node_id not in st.session_state.erledigt and prozess[node_id]["typ"] != "lieferung":
            st.session_state.erledigt.append(node_id)
    # Anzeige der aktuell erledigten
    st.sidebar.write("## Erledigte Schritte:")
    for s in st.session_state.erledigt:
        st.sidebar.markdown(f"- {s}")

else:
    st.write("Markiere die Schritte, die du **bereits erledigt** hast:")
    alle_schritte = [s for s,d in prozess.items() if d["typ"] != "lieferung"]
    erledigt = st.multiselect("✅ Erledigte Schritte auswählen", options=alle_schritte, default=st.session_state.erledigt)
    st.session_state.erledigt = erledigt
    # nächste Schritte ohne Lieferungen
    moeglich = [
        schritt for schritt, daten in prozess.items()
        if daten["typ"] != "lieferung"
        and schritt not in st.session_state.erledigt
        and all(dep in st.session_state.erledigt for dep in daten["abhaengig_von"])
    ]
    st.divider()
    st.subheader("🔜 Mögliche nächste Schritte")
    if moeglich:
        st.success("Diese Schritte kannst du jetzt durchführen:")
        for schritt in moeglich:
            typ = prozess[schritt]["typ"]
            st.markdown(f"✅ **{schritt}** *(Typ: {typ})*")
    else:
        st.info("Keine weiteren Schritte möglich – entweder alles erledigt oder Abhängigkeiten fehlen.")
