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

# 2) Graphviz-DOT als String bauen
def build_dot(prozess):
    dot = ["digraph G {", "  rankdir=LR;"]
    colors = {"lieferung":"purple","zwischenschritt":"darkblue","endprodukt":"turquoise"}
    for n,d in prozess.items():
        dot.append(f'  "{n}" [style=filled fillcolor={colors[d["typ"]]}];')
        for p in d["abhaengig_von"]:
            dot.append(f'  "{p}" -> "{n}";')
    dot.append("}")
    return "\n".join(dot)

# 3) Nächste-Schritte-Logik
def next_steps(prozess, done):
    out=[]
    for n,d in prozess.items():
        if d["typ"]!="lieferung" and n not in done and all(p in done for p in d["abhaengig_von"]):
            out.append(n)
    return out

# 4) Streamlit-App
def main():
    st.title("📊 Prozessnavigator")

    # Session-State initialisieren
    if "done" not in st.session_state:
        st.session_state.done=[]

    # oben: statischer Graph
    dot = build_dot(prozess)
    st.graphviz_chart(dot)

    # mittendrin: Checkboxen zum Anklicken
    st.subheader("✅ Markiere erledigte Schritte")
    for step in [s for s in prozess if prozess[s]["typ"]!="lieferung"]:
        checked = st.checkbox(step, value=(step in st.session_state.done))
        if checked and step not in st.session_state.done:
            st.session_state.done.append(step)
        if not checked and step in st.session_state.done:
            st.session_state.done.remove(step)

    # unten: nächste Schritte
    st.subheader("🔜 Nächste Schritte")
    naechste = next_steps(prozess, st.session_state.done)
    if naechste:
        for s in naechste:
            st.write(f"- {s}")
    else:
        st.write("🎉 Alle erledigt oder warte auf neue Lieferungen.")

if __name__=="__main__":
    main()
