import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

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
# Helper: next steps
# ===================
def finde_naechste_schritte(prozess, erledigt):
    return [
        schritt for schritt, daten in prozess.items()
        if daten["typ"] != "lieferung"
        and schritt not in erledigt
        and all(dep in erledigt for dep in daten["abhaengig_von"])
    ]

# ===================
# Build nodes & edges for AGraph
# ===================
nodes = []
edges = []
for schritt, daten in prozess.items():
    color = "lightgray" if daten["typ"] == "lieferung" else ("lightblue" if daten["typ"] == "zwischenschritt" else "lightgreen")
    nodes.append(Node(id=schritt, label=schritt, color=color, size=400))
    for dep in daten["abhaengig_von"]:
        edges.append(Edge(source=dep, target=schritt))

config = Config(
    height=600,
    width="100%",
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    collapsible=True,
)

# ===================
# Streamlit UI
# ===================
st.set_page_config(page_title="Prozess-Navigator", layout="wide")
st.title("📊 Prozessnavigator")

view = st.sidebar.radio("Ansicht wählen:", ["Diagramm", "Checkliste"])
if "erledigt" not in st.session_state:
    st.session_state.erledigt = []

if view == "Diagramm":
    st.write("**Klicke auf einen Knoten, um ihn als erledigt zu markieren.**")
    selected = agraph(nodes=nodes, edges=edges, config=config)
    if selected:
        # selected is list of clicked node ids
        for node_id in selected:
            if node_id not in st.session_state.erledigt and prozess[node_id]["typ"] != "lieferung":
                st.session_state.erledigt.append(node_id)
    st.sidebar.write("## Erledigte Schritte:")
    for s in st.session_state.erledigt:
        st.sidebar.markdown(f"- {s}")

else:
    st.write("Markiere die Schritte, die du **bereits erledigt** hast:")
    alle_schritte = [s for s,d in prozess.items() if d["typ"] != "lieferung"]
    erledigt = st.multiselect("✅ Erledigte Schritte auswählen", options=alle_schritte, default=st.session_state.erledigt)
    st.session_state.erledigt = erledigt
    moeglich = finde_naechste_schritte(prozess, st.session_state.erledigt)
    st.divider()
    st.subheader("🔜 Mögliche nächste Schritte")
    if moeglich:
        st.success("Diese Schritte kannst du jetzt durchführen:")
        for schritt in moeglich:
            typ = prozess[schritt]["typ"]
            st.markdown(f"✅ **{schritt}** *(Typ: {typ})*")
    else:
        st.info("Keine weiteren Schritte möglich – entweder alles erledigt oder Abhängigkeiten fehlen.")
