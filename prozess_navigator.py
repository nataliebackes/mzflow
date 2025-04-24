import streamlit as st

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
# 2) Generiere DOT-String ohne graphviz-Python
# ===================
def generate_dot(prozess):
    # Header
    lines = ["digraph Prozess {", "  rankdir=LR;", "  node [style=filled, fontname=Helvetica];"]
    # Node-Definitionen
    color_map = {"lieferung": "purple", "zwischenschritt": "darkblue", "endprodukt": "turquoise"}
    for step, data in prozess.items():
        fill = color_map[data["typ"]]
        # Escape quotes
        label = step.replace('"', '\\"')
        lines.append(f'  "{label}" [fillcolor={fill}];')
    # Kanten
    for step, data in prozess.items():
        for dep in data["abhaengig_von"]:
            lines.append(f'  "{dep}" -> "{step}";')
    lines.append("}")
    return "\n".join(lines)

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

    # Session-State initialisieren
    if "erledigt" not in st.session_state:
        st.session_state.erledigt = []

    #  Graph oben anzeigen
    dot_source = generate_dot(prozess)
    st.graphviz_chart(dot_source)

    # Checkboxes unter dem Graph
    st.subheader("✅ Markiere erledigte Schritte")
    for step in [s for s in prozess if prozess[s]["typ"]!="lieferung"]:
        checked = st.checkbox(step, value=(step in st.session_state.erledigt))
        if checked and step not in st.session_state.erledigt:
            st.session_state.erledigt.append(step)
        if not checked and step in st.session_state.erledigt:
            st.session_state.erledigt.remove(step)

    # nächste Schritte
    naechste = finde_naechste_schritte(prozess, st.session_state.erledigt)
    st.subheader("🔜 Nächste Schritte")
    if naechste:
        for s in naechste:
            st.write(f"- {s}")
    else:
        st.write("🎉 Alle erledigt oder warte auf neue Lieferungen.")

if __name__=="__main__":
    main()
