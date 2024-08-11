import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Daten laden
data = pd.read_csv("../../../Desktop/Cleaned_HAUS_Properties.csv")

# Sicherstellen, dass die Spalten als numerisch behandelt werden
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['price_per_m2'] = pd.to_numeric(data['price_per_m2'], errors='coerce')
data['usable_area'] = pd.to_numeric(data['usable_area'], errors='coerce')

# Fehlende Werte in numerischen Spalten mit dem Median füllen
data['price'] = data['price'].fillna(data['price'].median())
data['price_per_m2'] = data['price_per_m2'].fillna(data['price_per_m2'].median())
data['usable_area'] = data['usable_area'].fillna(data['usable_area'].median())

# Fehlende Werte in nicht-numerischen Spalten mit "nil" ersetzen
non_numeric_columns = data.select_dtypes(exclude=[np.number]).columns
data[non_numeric_columns] = data[non_numeric_columns].fillna("nil")

# Identifikation der Ausreißer
Q1 = data['price'].quantile(0.25)
Q3 = data['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
data_cleaned = data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)].copy()

# Log-Transformation der bereinigten 'price' Spalte
data_cleaned['log_price'] = np.log1p(data_cleaned['price'])

# Berechnung der Schiefe und Kurtosis für die log-transformierte bereinigte 'price' Spalte
log_price_skewness = data_cleaned['log_price'].skew()
log_price_kurtosis = data_cleaned['log_price'].kurt()

# Ausgabe der Schiefe und Kurtosis
print("Schiefe der log Preisverteilung:", log_price_skewness)
print("Kurtosis der log Preisverteilung:", log_price_kurtosis)

# Boxplot zur visuellen Identifikation von Ausreißern für die bereinigte 'log_price' Spalte
plt.figure(figsize=(10, 6))
sns.boxplot(x=data_cleaned['log_price'])
plt.title('Boxplot für log Preis nach Bereinigung')
plt.show()

# Histogramm und statistische Verteilung der bereinigten 'log_price' Spalte analysieren
plt.figure(figsize=(10, 6))
sns.histplot(data_cleaned['log_price'], kde=True)
plt.title('Histogramm der log Preisverteilung')
plt.show()
