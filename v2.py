import streamlit as st

# Titel
st.title("Interaktive Modul-Visualisierung")

# Initialisierung der Session State
if "active_module" not in st.session_state:
    st.session_state.active_module = None

# Modul-Buttons
cols = st.columns(3)
modules = ["A", "B", "C"]

for i, mod in enumerate(modules):
    if cols[i].button(f"Modul {mod}"):
        st.session_state.active_module = mod

# Definition der Graph-Struktur
edges = {
    "A": ["B", "C"],
    "B": [],
    "C": []
}

# Erzeugung des Graphviz-Codes
def build_graph(active):
    style = lambda node: f'color=red, penwidth=3' if node == active else ''
    edge_style = lambda src: 'color=red, penwidth=2' if src == active else ''

    graph = 'digraph G {\n'
    for node in modules:
        graph += f'  {node} [label="Modul {node}", shape=box, {style(node)}];\n'
    for src, targets in edges.items():
        for tgt in targets:
            graph += f'  {src} -> {tgt} [{edge_style(src)}];\n'
    graph += '}'
    return graph

# Anzeige des Graphen
st.graphviz_chart(build_graph(st.session_state.active_module))
