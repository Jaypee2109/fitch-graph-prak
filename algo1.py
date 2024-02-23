import pandas as pd
import plotly.express as px

# Beispiel-Daten erstellen
# String in einen DataFrame konvertieren
df = pd.read_csv("csv/wp1.csv", sep=",")
# Filtere nach TYP "DI_COGRAPH"
df_di_cograph = df[df["ALGO_ONE_DIFF"] > -1]

# Violin Plot erstellen
fig = px.box(
    df_di_cograph,
    y="ALGO_ONE_DIFF",
    labels={
        "DELETION_RATE": "Deletion rate",
        "ALGO_ONE_DIFF": "Symmetric difference",
    },
    color="HGT",
    x="DELETION_RATE",
    title="Performance of algorithm one on different horizontal gene transfer rates",
)

# Diagramm anzeigen
fig.show()
