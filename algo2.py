import pandas as pd
import plotly.express as px

# Beispiel-Daten erstellen
# String in einen DataFrame konvertieren
df = pd.read_csv("csv/wp1.csv", sep=",")
# Filtere nach TYP "DI_COGRAPH"
df_di_cograph = df[df["ALGO_TWO_DIFF"] > -1]

# Berechne den Mittelwert für jede DELETION_RATE
mean_values = df_di_cograph.groupby("DELETION_RATE")["ALGO_TWO_DIFF"].mean().reset_index()
# Sortiere die DELETION_RATE nach den Mittelwerten
sorted_deletion_rates = mean_values.sort_values(by="ALGO_TWO_DIFF")["DELETION_RATE"].tolist()

# Violin Plot erstellen
fig = px.box(
    df_di_cograph,
    color="HGT",
    y="ALGO_TWO_DIFF",
    labels={
        "DELETION_RATE": "Deletion rate",
        "ALGO_TWO_DIFF": "Symmetric difference",
    },
    x="DELETION_RATE",
    title="Performance of algorithm two on different horizontal gene transfer rates",
    category_orders={"DELETION_RATE": sorted_deletion_rates}  # Definiere die Reihenfolge der DELETION_RATE
)

# Diagramm anzeigen
fig.show()
