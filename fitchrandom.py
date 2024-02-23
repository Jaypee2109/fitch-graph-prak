import pandas as pd
import plotly.express as px

# String in einen DataFrame konvertieren
df = pd.read_csv("csv/wp1.csv", sep=",")

special = False
# Filtere nach TYP "DI_COGRAPH"
df_di_cograph = df[df["TYP"] == "DI_COGRAPH"]
df_di_cograph = df_di_cograph[df_di_cograph["SPECIAL"] == special]

# Aggregiere die Daten nach DELETION_RATE und berechne den Prozentsatz von PARTIAL_FITCH=True
agg_df = df_di_cograph.groupby("KNOTENZAHL")["FITCH"].mean().reset_index()

# Erstelle das Plotly-Diagramm
fig = px.bar(
    agg_df,
    x="KNOTENZAHL",
    y="FITCH",
    title="Random DI_COGRAPH",
    labels={
        "KNOTENZAHL": "Number of nodes",
        "FITCH": "Percentage of fitch",
    },
)

# Zeige das Diagramm an
fig.show()
