import streamlit as st
import plotly.graph_objects as go

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

# Plotly-Diagramm generieren
def plot_raster(grid, active_modules):
    fig = go.Figure()

    # Module als Rechtecke in Plotly einfügen
    for i, row in enumerate(grid):
        for j, name in enumerate(row):
            if name:
                color = 'red' if name in active_modules else 'lightgray'
                fig.add_shape(
                    type="rect",
                    x0=j * 1.5 + 0.2, y0=-i * 1.5 - 0.2,  # Abstand zwischen den Modulen
                    x1=(j + 1) * 1.5 - 0.2, y1=-(i + 1) * 1.5 + 0.2,  # Abstand zwischen den Modulen
                    line=dict(color="black", width=2),
                    fillcolor=color
                )
                # Text zentriert im Rechteck
                fig.add_annotation(
                    x=(j * 1.5 + (j + 1) * 1.5) / 2, y=(-(i + 0.5)),
                    text=name,
                    showarrow=False,
                    font=dict(size=12),
                    align="center",
                    valign="middle"  # Text vertikal zentrieren
                )

    # Pfeile für Abhängigkeiten
    for target, info in module_data.items():
        for source in info["abhaengig_von"]:
            source_pos = next((i, j) for i, row in enumerate(grid) for j, n in enumerate(row) if n == source)
            target_pos = next((i, j) for i, row in enumerate(grid) for j, n in enumerate(row) if n == target)
            
            # Die Pfeile an den Modulen vorbeigehen lassen
            fig.add_annotation(
                x=source_pos[1] * 1.5 + 0.5, y=-source_pos[0] * 1.5 - 1,
                ax=target_pos[1] * 1.5 + 0.5, ay=-target_pos[0] * 1.5 - 1,
                axref="x1", ayref="y1", xref="x1", yref="y1",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red"
            )

    # Layout für die Anzeige
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        width=1000, height=700,
        title="Modulübersicht",
        showlegend=False
    )

    return fig

# Plotly-Grafik anzeigen
st.plotly_chart(plot_raster(grid, st.session_state.active_modules))
