import streamlit as st

st.title("Interaktive Modul-Visualisierung (Mehrfachauswahl)")

# Module definieren
modules = ["A", "B", "C"]

# Initialisierung in session_state
if "active_modules" not in st.session_state:
    st.session_state.active_modules = set()

# Checkbox-UI
st.markdown("### Wähle aktive Module:")
for mod in modules:
    checked = mod in st.session_state.active_modules
    if st.checkbox(f"Modul {mod}", value=checked, key=f"chk_{mod}"):
        st.session_state.active_modules.add(mod)
    else:
        st.session_state.active_modules.discard(mod)

# Struktur der Pfeile
edges = {
    "A": ["B", "C"],
    "B": [],
    "C": []
}

# Graph-Generierung
def build_graph(active_modules):
    style = lambda node: 'color=red, penwidth=3' if node in active_modules else ''
    graph = 'digraph G {\n'
    for node in modules:
        graph += f'  {node} [label="Modul {node}", shape=box, {style(node)}];\n'
    for src, targets in edges.items():
        for tgt in targets:
            edge_attr = 'color=red, penwidth=2' if src in active_modules else ''
            graph += f'  {src} -> {tgt} [{edge_attr}];\n'
    graph += '}'
    return graph

# Darstellung des Graphen
st.graphviz_chart(build_graph(st.session_state.active_modules))
