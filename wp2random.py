import pandas as pd
import plotly.express as px

# Beispiel-Daten erstellen
# String in einen DataFrame konvertieren
df = pd.read_csv("csv/wp2.csv", sep=",")
# Filtere nach TYP "DI_COGRAPH"

# Violin Plot erstellen
fig = px.box(
    df,
    y="DIFF",
    x="HGT",
    facet_col="METHOD",
    color="SCORE",
    title="Comparison of louvain and random bipartition on different horizontal gene transfer rates",
    labels={
        "DIFF": "Symmetric difference",
    },
)

# Diagramm anzeigen
fig.show()
