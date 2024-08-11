import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dateipfade
file_paths = {
    'Baden-Württemberg': './Cleaned_Bundesland_HAUS/properties_baden-wuerttemberg.csv',
    'Bayern': './Cleaned_Bundesland_HAUS/properties_bayern.csv',
    'Berlin': './Cleaned_Bundesland_HAUS/properties_berlin.csv',
    'Brandenburg': './Cleaned_Bundesland_HAUS/properties_brandenburg.csv',
    'Bremen': './Cleaned_Bundesland_HAUS/properties_bremen.csv',
    'Hamburg': './Cleaned_Bundesland_HAUS/properties_hamburg.csv',
    'Hessen': './Cleaned_Bundesland_HAUS/properties_hessen.csv',
    'Mecklenburg-Vorpommern': './Cleaned_Bundesland_HAUS/properties_mecklenburg-vorpommern.csv',
    'Niedersachsen': './Cleaned_Bundesland_HAUS/properties_niedersachsen.csv',
    'Nordrhein-Westfalen': './Cleaned_Bundesland_HAUS/properties_nordrhein-westfalen.csv',
    'Thüringen': './Cleaned_Bundesland_HAUS/properties_thueringen.csv',
    'Saarland': './Cleaned_Bundesland_HAUS/properties_saarland.csv',
    'Sachsen': './Cleaned_Bundesland_HAUS/properties_sachsen.csv',
    'Sachsen-Anhalt': './Cleaned_Bundesland_HAUS/properties_sachsen-anhalt.csv',
    'Rheinland-Pfalz': './Cleaned_Bundesland_HAUS/properties_rheinland-pfalz.csv',
    'Schleswig-Holstein': './Cleaned_Bundesland_HAUS/properties_schleswig-holstein.csv'
}

# Laden der Daten und Berechnung der durchschnittlichen Preise
average_prices = {}

for state, path in file_paths.items():
    # Lese die CSV-Datei für den aktuellen Bundesstaat ein
    data = pd.read_csv(path)

    # Zeige die ersten fünf Zeilen der Daten für den aktuellen Bundesstaat an
    print(f'Daten für {state} geladen:\n', data.head(), '\n')

    # Überprüfe, ob die Spalte 'price' in den Daten vorhanden ist
    if 'price' in data.columns:
        # Berechne den Durchschnittspreis und konvertiere ihn in Tausend Euro
        average_price = data['price'].mean() / 1e3  # Umrechnung in Tausend Euro

        # Speichere den Durchschnittspreis für den aktuellen Bundesstaat
        average_prices[state] = average_price

        # Gebe den Durchschnittspreis für den aktuellen Bundesstaat aus
        print(f'Durchschnittspreis für {state}: {average_price:.2f} Tausend Euro\n')

# Sortieren der Bundesländer nach dem durchschnittlichen Preis, absteigend
sorted_average_prices = dict(sorted(average_prices.items(), key=lambda item: item[1], reverse=True))

# Sortierte Durchschnittspreise anzeigen
print('Sortierte durchschnittliche Preise:\n')
for state, price in sorted_average_prices.items():
    print(f'{state}: {price:.2f} Tausend Euro')

# Einstellen des Stils
sns.set(style="whitegrid")
plt.figure(figsize=(14, 10))

# Erstellen des Balkendiagramms
bars = plt.bar(sorted_average_prices.keys(), sorted_average_prices.values(), color=sns.color_palette("viridis", len(sorted_average_prices)))

# Farbverlauf für die Balken
for bar in bars:
    bar.set_color(plt.cm.viridis(bar.get_height() / max(sorted_average_prices.values())))

plt.xlabel('Bundesland', fontsize=14, labelpad=10)
plt.ylabel('Durchschnittspreis in Tausend Euro', fontsize=14, labelpad=10)
plt.title('Durchschnittliche Immobilienpreise für Häuser pro Bundesland', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Erstellen einer Colorbar
ax = plt.gca()
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(sorted_average_prices.values()), vmax=max(sorted_average_prices.values())))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Preisniveau in T€', rotation=270, labelpad=20, fontsize=12)

plt.tight_layout()

# Diagramm anzeigen
plt.show()
