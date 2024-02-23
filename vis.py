from wp1 import *
from wp2 import *
import pandas as pd
import plotly.express as px


def get_possible_filter_values(data, filter_column):
    if data[filter_column].nunique() > 10:
        return data[filter_column].unique()[:10], True
    else:
        return data[filter_column].unique(), False


def apply_filters(data, filters):
    for filter_column, filter_value in filters:
        data = data[data[filter_column] == filter_value]
    return data


def visualize_csv_interactive(csv_file):
    data = pd.read_csv(csv_file, sep=",")
    data.columns = data.columns.str.lower()

    while True:
        print("\nVerfügbare Spalten:")
        print(", ".join(data.columns))
        x_column = input(
            "Bitte geben Sie den Namen für die x-Achse ein (oder 'exit' zum Beenden): "
        )

        if x_column.lower() == "exit":
            break

        y_column = input("Bitte geben Sie den Namen für die y-Achse ein: ")

        if x_column not in data.columns or y_column not in data.columns:
            print(
                "Fehler: Die ausgewählten Spalten existieren nicht. Bitte erneut versuchen."
            )
            continue

        print("\nVerfügbare Spalten für den Filter:")
        print(", ".join(data.columns))

        filters = []
        while True:
            filter_column = input(
                "Bitte geben Sie den Namen der Spalte für den Filter ein (oder 'done' wenn Sie fertig sind): "
            )

            if filter_column.lower() == "done":
                break

            if filter_column not in data.columns:
                print(
                    "Fehler: Die ausgewählte Spalte existiert nicht. Bitte erneut versuchen."
                )
                continue

            possible_values, more_values_available = get_possible_filter_values(
                data, filter_column
            )

            print(
                f"Verfügbare Werte für '{filter_column}': {', '.join(map(str, possible_values))}"
            )

            if more_values_available:
                print(
                    "(Es gibt mehr Werte für '{filter_column}', aber nur die ersten 10 werden angezeigt.)"
                )

            filter_value = input(
                f"Bitte geben Sie den Wert für den Filter in der Spalte {filter_column} ein (oder 'none' für keinen Filter): "
            )

            if filter_value.lower() != "none":
                filters.append((filter_column, filter_value))

        data_filtered = apply_filters(data, filters)

        # Auswahl des Plot-Typs
        plot_type = input(
            "Bitte geben Sie den gewünschten Plot-Typ ein (scatter, violin, box): "
        ).lower()

        if plot_type == "scatter":
            fig = px.scatter(
                data_filtered,
                x=x_column,
                y=y_column,
                title=f"{y_column} vs. {x_column}",
                labels={x_column: x_column, y_column: y_column},
            )
        elif plot_type == "violin":
            fig = px.violin(
                data_filtered,
                y=y_column,
                color=x_column,
                box=True,
                labels={y_column: y_column},
            )
        elif plot_type == "box":
            fig = px.box(
                data_filtered,
                y=y_column,
                color=x_column,
                labels={y_column: y_column},
            )
        else:
            print("Ungültiger Plot-Typ. Bitte versuchen Sie es erneut.")
            continue

        fig.show()


# Beispielaufruf
csv_file = "csv/wp2.csv"
visualize_csv_interactive(csv_file)
