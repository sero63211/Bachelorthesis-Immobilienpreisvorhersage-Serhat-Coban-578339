import os
import glob
import pandas as pd

# Liste der zu verarbeitenden Standorte/Bundesländer
locations = [
    'baden-wuerttemberg', 'bayern', 'berlin', 'brandenburg', 'bremen', 'hamburg',
    'hessen', 'mecklenburg-vorpommern', 'niedersachsen', 'nordrhein-westfalen',
    'rheinland-pfalz', 'saarland', 'sachsen', 'sachsen-anhalt', 'schleswig-holstein', 'thueringen'
]

# Verzeichnis, in dem sich die CSV-Dateien befinden (angenommen, sie befinden sich im gleichen Verzeichnis wie das Skript)
directory = os.getcwd()

# Verarbeiten jeder Region/Bundesland
for location in locations:
    # Muster für das Auffinden aller CSV-Dateien, die zu dem aktuellen Bundesland gehören
    pattern = f'HAUS_property_data_{location}_page_*.csv'
    csv_files = glob.glob(os.path.join(directory, pattern))

    # Initialisierung einer leeren Liste zur Speicherung der DataFrames
    df_list = []

    # Einlesen jeder gefundenen CSV-Datei und Anhängen an die Liste
    for file in csv_files:
        df = pd.read_csv(file)
        df_list.append(df)

    # Wenn DataFrames gefunden wurden, diese zusammenführen und speichern
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)

        # Name der Ausgabedatei basierend auf dem aktuellen Standort/Bundesland
        output_file = f'properties_{location}.csv'

        # Speichern des zusammengeführten DataFrames in eine neue CSV-Datei
        combined_df.to_csv(os.path.join(directory, output_file), index=False)

        print(f"All CSV files for {location} have been combined into {output_file}")
    else:
        print(f"No CSV files found for {location}.")
