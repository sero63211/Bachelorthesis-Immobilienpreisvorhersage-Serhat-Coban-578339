import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import ttest_ind, mannwhitneyu


# Funktion zum Laden der Daten
def load_data(population_density_path, properties_path):
    population_density_data = pd.read_csv(population_density_path)
    immobilien_data = pd.read_csv(properties_path)
    immobilien_data.sort_values('address', inplace=True)
    return population_density_data, immobilien_data


# Funktion zur Bereinigung der Gemeindenamen
def clean_gemeindename(name):
    if ',' in name:
        return name.split(',')[0]
    if '/' in name:
        return name.split('/')[0]
    return name


# Bereinigung der Gemeindenamen in den Bevölkerungsdichte-Daten
def clean_population_density_data(population_density_data):
    population_density_data['clean_Gemeindename'] = population_density_data['Gemeindename'].apply(clean_gemeindename)
    return population_density_data


# Funktion zur Extraktion und Zuordnung der Gemeindenamen und Kategorien mit Debugging
def extract_gemeindename_debug(row, population_density_data):
    for index, pd_row in population_density_data.iterrows():
        if pd_row['clean_Gemeindename'] in row['address'] or pd_row['clean_Gemeindename'] in row['title']:
            print(f"Match gefunden: {pd_row['clean_Gemeindename']} in Adresse oder Titel von {row['title']}")
            return pd_row['clean_Gemeindename']
    print(f"Kein Match für: {row['title']} mit Adresse: {row['address']}")
    return None


# Anwenden der Match-Funktion auf die Immobilien-Daten
def match_gemeindename(immobilien_data, population_density_data):
    immobilien_data['Gemeindename'] = immobilien_data.apply(
        lambda row: extract_gemeindename_debug(row, population_density_data), axis=1)
    return immobilien_data


# Zusammenführen der Daten, die ein Match gefunden haben
def merge_matched_data(immobilien_data, population_density_data):
    matched_data = pd.merge(immobilien_data.dropna(subset=['Gemeindename']), population_density_data,
                            left_on='Gemeindename', right_on='clean_Gemeindename', how='left')
    return matched_data


# Speichern der angepassten Immobiliendaten in eine neue CSV-Datei
def save_matched_data(matched_data, output_path):
    matched_data.to_csv(output_path, index=False)


# Hauptprogramm
def main():
    population_density_path = "./kategorisierte_gemeinden.csv"
    properties_path = "../../../Desktop/Cleaned_HAUS_Properties.csv"
    output_path = "../../../../Desktop/adjusted_properties_partial.csv"

    # Laden der Daten
    population_density_data, immobilien_data = load_data(population_density_path, properties_path)

    # Bereinigung der Gemeindenamen
    population_density_data = clean_population_density_data(population_density_data)

    # Match der Gemeindenamen
    immobilien_data = match_gemeindename(immobilien_data, population_density_data)

    # Zusammenführen der gematchten Daten
    matched_data = merge_matched_data(immobilien_data, population_density_data)

    # Speichern der gematchten Daten
    save_matched_data(matched_data, output_path)


# Ausführung des Hauptprogramms
if __name__ == '__main__':
    main()
