import pandas as pd
import plotly.express as px

# String in einen DataFrame konvertieren
df = pd.read_csv("csv/wp1.csv", sep=",")

numNodes = 15

# Filtere nach TYP "DI_COGRAPH"
df_di_cograph = df[df["TYP"] == "DI_COGRAPH"]
df_di_cograph = df_di_cograph[df_di_cograph["KNOTENZAHL"] == numNodes]

# Aggregiere die Daten nach DELETION_RATE und berechne den Prozentsatz von PARTIAL_FITCH=True
agg_df = df_di_cograph.groupby("DELETION_RATE")["PARTIAL_FITCH"].mean().reset_index()

# Erstelle das Plotly-Diagramm
fig = px.bar(
    agg_df,
    x="DELETION_RATE",
    y="PARTIAL_FITCH",
    title="DI_COGRAPH with " + str(numNodes) + " nodes",
    labels={
        "DELETION_RATE": "Deletion rate",
        "PARTIAL_FITCH": "Percentage of fitch",
    },
)

# Zeige das Diagramm an
fig.show()
