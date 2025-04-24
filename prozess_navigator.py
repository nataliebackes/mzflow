import streamlit as st
from st_cytoscape import cytoscape

# ===================
# 1) Prozess-Definition
# ===================
prozess = {
    # Lieferungen (lila)
    "MFB von Herter":         {"typ": "lieferung",    "abhaengig_von": []},
    "Fragebögen":             {"typ": "lieferung",    "abhaengig_von": []},
    "Ziel DSB von Destatis":  {"typ": "lieferung",    "abhaengig_von": []},
    "Variste prüf":           {"typ": "lieferung",    "abhaengig_von": []},
    "Metadatenreport":        {"typ": "lieferung",    "abhaengig_von": []},
    "Testdaten":              {"typ": "lieferung",    "abhaengig_von": []},
    # Zwischenschritte (dunkelblau)
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
    # Endprodukte (türkis)
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
# 2) Erzeuge Cytoscape-Elemente
# ===================
def make_elements(prozess, erledigt):
    elements = []
    # Nodes
    for step, data in prozess.items():
        elements.append({
            "data": {"id": step, "label": step},
            "classes": data["typ"],
            "selected": step in erledigt,
            "selectable": data["typ"] != "lieferung"
        })
    # Edges
    for step, data in prozess.items():
        for dep in data["abhaengig_von"]:
            elements.append({"data": {"source": dep, "target": step, "id": f"{dep}->{step}"}})
    return elements

# ===================
# 3) Logik: nächste Schritte
# ===================
def finde_naechste_schritte(prozess, erledigt):
    return [
        s for s,d in prozess.items()
        if d["typ"]!="lieferung"
        and s not in erledigt
        and all(dep in erledigt for dep in d["abhaengig_von"] )
    ]

# ===================
# 4) Streamlit-App
# ===================
def main():
    st.title("📊 Prozessnavigator")

    if "erledigt" not in st.session_state:
        st.session_state.erledigt = []

    # Cytoscape Graph oben
    elements = make_elements(prozess, st.session_state.erledigt)
    stylesheet = [
        {"selector": "node.leiferung", "style": {"background-color": "purple", "label": "data(label)"}},
        {"selector": "node.zwischenschritt", "style": {"background-color": "darkblue", "label": "data(label)"}},
        {"selector": "node.endprodukt", "style": {"background-color": "turquoise", "label": "data(label)"}},
        {"selector": "edge", "style": {"curve-style": "bezier", "target-arrow-shape": "triangle"}}
    ]
    selected = cytoscape(
        elements=elements,
        stylesheet=stylesheet,
        layout={"name": "breadthfirst", "directed": True, "padding": 10},
        key="cytograph",
        height="500px"
    )

    # Update erledigt based on selection
    st.session_state.erledigt = selected.get("nodes", [])

    # Nächste Schritte
    naechste = finde_naechste_schritte(prozess, st.session_state.erledigt)
    st.subheader("🔜 Nächste Schritte")
    if naechste:
        for s in naechste:
            st.write(f"- {s}")
    else:
        st.write("🎉 Alle aktuelle Schritte erledigt oder warte auf neue Lieferungen.")

if __name__ == "__main__":
    main()
