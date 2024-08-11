"""
Dieses Skript lädt ein Immobilien-Datenset, bereinigt die Daten, führt statistische Tests durch
und visualisiert die Ergebnisse. Ziel ist es, Unterschiede zwischen städtischen und ländlichen
Regionen in Bezug auf verschiedene Immobilienmerkmale zu analysieren.
"""

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Datensatz laden
file_path = '../../../../Desktop/HAUS_Regionale_Einordnung.csv'
df = pd.read_csv(file_path)

# Erste Übersicht über die Daten anzeigen
print("Erste Übersicht über die Daten:")
print(df.info())

# Relevante Spalten spezifizieren
columns_of_interest = ['price_per_m2', 'rooms', 'living_space', 'property_area',
                       'bedrooms', 'bathrooms', 'garage_parking', 'buyer_commission', 'Kategorie']

# Typumwandlung für bestimmte Spalten vornehmen
for col in ['rooms', 'bedrooms', 'bathrooms']:
    if df[col].dtype == 'object':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Bereinigung der Spalte 'garage_parking' durch Extrahieren von Zahlen
df['garage_parking'] = df['garage_parking'].str.extract(r'(\d+)').astype(float)

# Bereinigung der Spalte 'buyer_commission', um Prozentsätze in float umzuwandeln
df['buyer_commission'] = df['buyer_commission'].str.extract(r'(\d+,\d+) %')
df['buyer_commission'] = df['buyer_commission'].str.replace(',', '.').astype(float)

# Überprüfung auf NaN-Werte in den interessierenden Spalten
print("\nAnzahl der NaN-Werte nach Umwandlung in den relevanten Spalten:")
print(df[columns_of_interest].isna().sum())

# Entfernen von Zeilen mit NaN-Werten in den relevanten Spalten
df_filtered = df[columns_of_interest].dropna()

# Funktion zum Durchführen eines ungepaarten t-Tests
def unpaired_t_test(data, category_column, value_column):
    group1 = data[data[category_column] == 'städtisch'][value_column]
    group2 = data[data[category_column] == 'ländlich'][value_column]
    return stats.ttest_ind(group1, group2, equal_var=False)

# Durchführung des ungepaarten t-Tests für jede relevante Spalte
t_test_results = {}
for column in columns_of_interest[:-1]:  # 'Kategorie' ausschließen
    t_statistic, p_value = unpaired_t_test(df_filtered, 'Kategorie', column)
    t_test_results[column] = {'T-statistic': t_statistic, 'P-value': p_value}

# Ergebnisse des t-Tests ausgeben
print("\nErgebnisse des ungepaarten T-Tests:")
for key, value in t_test_results.items():
    print(f"{key}: T-Statistik = {value['T-statistic']}, P-Wert = {value['P-value']}")

# Visualisierung der Verteilungen zum Vergleich
plt.figure(figsize=(14, 16))
for i, column in enumerate(columns_of_interest[:-1], 1):  # 'Kategorie' ausschließen
    plt.subplot(4, 2, i)
    sns.boxplot(x='Kategorie', y=column, data=df_filtered)
    plt.title(f'{column} nach Kategorie (städtisch vs. ländlich)')
    plt.xlabel('Kategorie')
    plt.ylabel(column)

plt.tight_layout()
plt.show()
