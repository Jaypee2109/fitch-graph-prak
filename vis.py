from wp1 import *
from wp2 import *
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt


def get_possible_filter_values(data, filter_column):
    # Wenn der Wertebereich größer als 10 ist, gib die ersten 10 Werte zurück
    if data[filter_column].nunique() > 10:
        return data[filter_column].unique()[:10], True
    else:
        return data[filter_column].unique(), False


def apply_filters(data, filters):
    for filter_column, filter_value in filters:
        data = data[data[filter_column] == filter_value]
    return data


def visualize_csv_interactive(csv_file):
    # Daten aus CSV-Datei laden, dabei Semikolon als Trennzeichen verwenden
    data = pd.read_csv(csv_file, sep=",")

    # Spaltennamen in Kleinbuchstaben umwandeln
    data.columns = data.columns.str.lower()

    while True:
        # Interaktiv Achsen auswählen
        print("\nVerfügbare Spalten:")
        print(", ".join(data.columns))
        x_column = input(
            "Bitte geben Sie den Namen für die x-Achse ein (oder 'exit' zum Beenden): "
        )

        # Überprüfen, ob der Benutzer das Programm beenden möchte
        if x_column.lower() == "exit":
            break

        y_column = input("Bitte geben Sie den Namen für die y-Achse ein: ")

        # Überprüfen, ob die ausgewählten Spalten vorhanden sind
        if x_column not in data.columns or y_column not in data.columns:
            print(
                "Fehler: Die ausgewählten Spalten existieren nicht. Bitte erneut versuchen."
            )
            continue

        # Liste aller Filter-Optionen anzeigen
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
                    f"(Es gibt mehr Werte für '{filter_column}', aber nur die ersten 10 werden angezeigt.)"
                )

            filter_value = input(
                f"Bitte geben Sie den Wert für den Filter in der Spalte {filter_column} ein (oder 'none' für keinen Filter): "
            )

            if filter_value.lower() != "none":
                filters.append((filter_column, filter_value))

        # Filter anwenden
        data_filtered = apply_filters(data, filters)

        # Diagramm erstellen
        plt.scatter(data_filtered[x_column], data_filtered[y_column])
        plt.title(f"{y_column} vs. {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()


# Beispielaufruf
csv_file = "csv/wp1.csv"
visualize_csv_interactive(csv_file)
