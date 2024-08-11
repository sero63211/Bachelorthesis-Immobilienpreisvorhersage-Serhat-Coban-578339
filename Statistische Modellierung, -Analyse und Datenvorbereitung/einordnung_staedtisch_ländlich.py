import pandas as pd

# Daten laden
data = pd.read_excel("Deutschlandatlas-Daten.xlsx", sheet_name='Deutschlandatlas_GEM1221', usecols=['GKZ1221', 'Gemeindename', 'bev_dicht'])

# Quartilberechnung für die Bevölkerungsdichte
data['Quartil'] = pd.qcut(data['bev_dicht'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# Schwellenwert bestimmen, z.B. zwischen dem dritten Quartil und dem Maximum als städtisch
threshold = data['bev_dicht'].quantile(0.75)

# Kategorisierung in "städtisch" und "ländlich"
data['Kategorie'] = data['bev_dicht'].apply(lambda x: 'städtisch' if x > threshold else 'ländlich')

# Auswahl der relevanten Spalten und Speichern in einer neuen CSV-Datei
data[['Gemeindename', 'bev_dicht', 'Quartil', 'Kategorie']].to_csv('kategorisierte_gemeinden.csv', index=False)
