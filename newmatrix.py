import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Raster-Layout
grid = [
    ["MFB von Herter", "MFB Spalten A-M + Operatoren", "MFB mit Spalten P-Q", "", "", "MFB", "", "", "", "", "", ""],
    ["","Fragebögen","Ziel DSB von Destatis", "Schlüsselverzeichnis und IHB", "Ziel DSB", "", "", "", "", "", "", ""],
    ["", "", "ZP Matrix + Thematische Liste", "", "", "", "", "Missy Variablenmatrix", "", "", "", ""],
    ["", "", "", "", "Varliste prüf", "Vergröberungen + Korrekturen", "", "", "", "", "", ""],
    ["", "", "", "DHB Kommentare 1", "DHB Kommentare 2", "", "", "", "", "", "", ""],
    ["", "", "", "", "Metadatenreport", "Metadatenreport final", "Tabelle Erhebungsprogramme", "", "", "", "", ""],
    ["", "", "", "", "Varliste mit allen Infos", "", "", "", "", "", "", ""],
    ["", "", "", "", "Testdaten", "Technische Prüfung", "Inhaltliche Prüfung", "Erstellung Stata Systemfile", "Finaler Datensatz", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "Missingdefinitionen", "", ""],
    ["", "", "", "", "", "", "Tools", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "Missy Texte", "Missy Veröffentlichung"]
]

# Modulinformationen
module_data = {
    "Varliste mit allen Infos": {"typ": "zwischenschritt", "abhaengig_von": ["MFB", "Varliste prüf"]},
    "Finaler Datensatz": {"typ": "endprodukt", "abhaengig_von": ["Technische Prüfung", "Inhaltliche Prüfung"]},
    "MFB von Herter": {"typ": "lieferung", "abhaengig_von": []},
    "Fragebögen": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB von Destatis": {"typ": "lieferung", "abhaengig_von": []},
    "Varliste prüf": {"typ": "lieferung", "abhaengig_von": []},
    "Metadatenreport": {"typ": "lieferung", "abhaengig_von": []},
    "Testdaten": {"typ": "lieferung", "abhaengig_von": []},
    "MFB Spalten A-M + Operatoren": {"typ": "zwischenschritt", "abhaengig_von": ["MFB von Herter", "Fragebögen"]},
    "MFB mit Spalten P-Q": {"typ": "lieferung", "abhaengig_von": []},
    "Vergröberungen + Korrekturen": {"typ": "zwischenschritt", "abhaengig_von": ["Varliste prüf"]},
    "Metadatenreport final": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Inhaltliche Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "Fachserien Tabellen vorbereiten"]},
    "Missingdefinitionen": {"typ": "zwischenschritt", "abhaengig_von": ["Finaler Datensatz"]},
    "Missy Texte": {"typ": "zwischenschritt", "abhaengig_von": ["Testdaten"]},
    "Schlüsselverzeichnis und IHB": {"typ": "lieferung", "abhaengig_von": []},
    "Ziel DSB": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB von Destatis", "MFB mit Spalten P-Q", "Fragebögen", "Schlüsselverzeichnis und IHB"]},
    "DHB Kommentare 2": {"typ": "zwischenschritt", "abhaengig_von": ["Vergröberungen + Korrekturen"]},
    "Tabelle Erhebungsprogramme": {"typ": "endprodukt", "abhaengig_von": ["Metadatenreport"]},
    "Technische Prüfung": {"typ": "endprodukt", "abhaengig_von": ["Testdaten"]},
    "Tools": {"typ": "zwischenschritt", "abhaengig_von": ["Finaler Datensatz"]},
    "Missy Veröffentlichung": {"typ": "endprodukt", "abhaengig_von": ["Missy Variablenmatrix", "Missy Texte"]},
    "MFB": {"typ": "endprodukt", "abhaengig_von": ["MFB mit Spalten P-Q", "Schlüsselverzeichnis und IHB", "Ziel DSB"]},
    "DHB": {"typ": "endprodukt", "abhaengig_von": ["Testdaten", "DHB Kommentare 2", "DHB Kommentare 1", "Varliste mit allen Infos", "Finaler Datensatz"]},
    "Missy Variablenmatrix": {"typ": "endprodukt", "abhaengig_von": ["ZP Matrix + Thematische Liste"]},
    "DHB Kommentare 1": {"typ": "zwischenschritt", "abhaengig_von": ["MFB"]},
    "Routinen für Filtermissings an IT NRW": {"typ": "zwischenschritt", "abhaengig_von": ["MFB", "Ziel DSB"]},
    "ZP Matrix + Thematische Liste": {"typ": "endprodukt", "abhaengig_von": ["Ziel DSB"]},
    "Erstellung Stata Systemfile": {"typ": "endprodukt", "abhaengig_von": ["Testdaten"]},
    "Fachserien Tabellen vorbereiten": {"typ": "zwischenschritt", "abhaengig_von": []}
}

all_modules = [m for row in grid for m in row if m]

# Layout
# Layout
app.layout = dbc.Container([
    html.H2("Mikrozensus SUF Prozess", className="text-center my-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="module-graph", style={"height": "900px"}), md=9),
        dbc.Col([
            html.H5("📝 Zu erledigen"),
            html.Ul(id="todo-list"),
            html.H5("✅ Erledigt"),
            html.Ul(id="done-list")
        ], md=3),
    ]),
    dcc.Store(id="selected-modules", data=[])
], fluid=True)

# Grafik zeichnen
@app.callback(
    Output("module-graph", "figure"),
    Input("selected-modules", "data")
)
def draw_graph(selected_modules):
    fig = go.Figure()
    spacing_x, spacing_y = 250, 120
    node_positions = {}

    for row_idx, row in enumerate(reversed(grid)):
        for col_idx, name in enumerate(row):
            if name == "":
                continue
            x = col_idx * spacing_x
            y = row_idx * spacing_y
            node_positions[name] = (x, y)

            color = "#ffcccc" if name in selected_modules else "#ffffff"

            fig.add_shape(type="rect",
                          x0=x-80, y0=y-30, x1=x+80, y1=y+30,
                          line=dict(color="red" if name in selected_modules else "#333"),
                          fillcolor=color, layer="below")

            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                text=[name],
                mode="text",
                hoverinfo="text",
                textposition="middle center",
                textfont=dict(size=11),
                name=name,
                customdata=[name],
                showlegend=False
            ))

    for target, info in module_data.items():
        for source in info["abhaengig_von"]:
            if source in node_positions and target in node_positions:
                x0, y0 = node_positions[source]
                x1, y1 = node_positions[target]
                arrow_color = "red" if source in selected_modules else "#888"
                fig.add_annotation(
                    ax=x0, ay=y0,
                    x=x1, y=y1,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=1.5,
                    arrowcolor=arrow_color
                )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#f8f9fa",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        clickmode='event+select'
    )
    return fig

# Klickverarbeitung – Mehrfachauswahl
@app.callback(
    Output("selected-modules", "data", allow_duplicate=True),
    Input("module-graph", "clickData"),
    State("selected-modules", "data"),
    prevent_initial_call=True
)
def update_selection(clickData, selected_modules):
    if not clickData:
        return dash.no_update

    clicked = clickData["points"][0]["customdata"]
    if clicked in selected_modules:
        selected_modules.remove(clicked)
    else:
        selected_modules.append(clicked)

    return selected_modules

# To-Do- und Erledigt-Liste aktualisieren
@app.callback(
    Output("todo-list", "children"),
    Output("done-list", "children"),
    Input("selected-modules", "data")
)
def update_lists(selected_modules):
    done = [html.Li(name) for name in selected_modules if module_data[name]["typ"] != "lieferung"]

    todo = []
    for name in all_modules:
        if name in selected_modules:
            continue

        info = module_data.get(name, {})
        typ = info.get("typ", "")
        deps = info.get("abhaengig_von", [])

        if typ != "lieferung" and all(dep in selected_modules for dep in deps):
            todo.append(html.Li(name))

    return todo, done

if __name__ == "__main__":
    app.run(debug=True)