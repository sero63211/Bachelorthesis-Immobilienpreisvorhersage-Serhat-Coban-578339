import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Pfad zur CSV-Datei
file_path = './BundesLänder_HAUS_CSV/ALL_HAUs.csv'

# Daten laden
data = pd.read_csv(file_path)

# Funktionen zur Datenbereinigung und -transformation
def clean_garage_parking(value):
    """
    Bereinigt die Werte in der Spalte 'garage_parking', indem alle nicht-numerischen Zeichen entfernt werden.
    Konvertiert den bereinigten Wert in einen float.
    """
    if isinstance(value, str):
        value = re.sub(r'[^\d]', '', value)
        return float(value) if value else np.nan
    return np.nan

def clean_buyer_commission(value):
    """
    Extrahiert den prozentualen Anteil der Käuferprovision aus dem String.
    """
    if isinstance(value, str):
        match = re.search(r'(\d+,\d+)\s*%', value)
        if match:
            return float(match.group(1).replace(',', '.'))
    return np.nan

def clean_price(value):
    """
    Bereinigt den Preiswert, indem Währungszeichen und andere unerwünschte Zeichen entfernt werden.
    Konvertiert den Wert in einen float.
    """
    if isinstance(value, str):
        value = value.replace('€', '').replace('.', '').replace(',', '.').strip()
        if 'Auf Anfrage' in value or value == '':
            return np.nan
        try:
            return float(value)
        except ValueError:
            return np.nan
    return value if pd.notna(value) else np.nan

def clean_area(value):
    """
    Bereinigt Werte in Flächenangaben, indem alle nicht-numerischen Zeichen entfernt werden.
    Konvertiert den Wert in einen float.
    """
    if isinstance(value, str):
        value = re.sub(r'[^\d,]', '', value).replace(',', '.')
        return float(value) if value else np.nan
    return value

def clean_generic_numeric(value):
    """
    Generische Bereinigungsfunktion für numerische Spalten.
    Entfernt nicht-numerische Zeichen und konvertiert in float.
    """
    if isinstance(value, str):
        value = re.sub(r'[^\d,]', '', value).replace(',', '.')
        return float(value) if value else np.nan
    return value

# Anwendung der Bereinigungsfunktionen auf die relevanten Spalten
data['garage_parking'] = data['garage_parking'].apply(clean_garage_parking)
data['buyer_commission'] = data['buyer_commission'].apply(clean_buyer_commission)
data['price'] = data['price'].apply(clean_price)
data['living_space'] = data['living_space'].apply(clean_area)
data['property_area'] = data['property_area'].apply(clean_area)
data['price_per_m2'] = data['price_per_m2'].apply(clean_generic_numeric)
data['usable_area'] = data['usable_area'].apply(clean_generic_numeric)

# Funktion zur Identifikation und Behandlung von Ausreißern
def remove_outliers_and_print(data, column):
    """
    Identifiziert Ausreißer in der angegebenen Spalte mittels des IQR-Verfahrens (Interquartilsabstand).
    Entfernt diese Ausreißer, indem sie auf NaN gesetzt werden, und ersetzt die NaN-Werte durch den Median.
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_before = data[(data[column] < lower_bound) | (data[column] > upper_bound)][column]

    print(f"\nVor der Behandlung der Ausreißer in '{column}':")
    print(outliers_before)

    # Entferne die Ausreißer durch Setzen auf NaN
    data[column] = np.where((data[column] < lower_bound) | (data[column] > upper_bound), np.nan, data[column])

    # Fülle NaN-Werte mit dem Median der Spalte
    median_value = data[column].median()
    data[column].fillna(median_value, inplace=True)

    outliers_after = data.loc[outliers_before.index, column]

    print(f"\nNach der Behandlung der Ausreißer in '{column}':")
    print(outliers_after)

# Anwendung der Ausreißer-Entfernung auf numerische Spalten
#remove_outliers_and_print(data, 'price')
# Weitere numerische Spalten bereinigen
#for col in data.select_dtypes(include=[np.number]).columns:
#    if col != 'price':  # 'price' wurde bereits behandelt
#        remove_outliers_and_print(data, col)

# Zusätzliche Überprüfung auf extrem hohe oder niedrige Preise
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['price'])
plt.title('Boxplot von Preis')
plt.xlabel('Preis')
plt.show()

# Log-Transformation der bereinigten 'price' Spalte
data['log_price'] = np.log1p(data['price'])

# Berechnung der Schiefe und Kurtosis für die log-transformierte 'price' Spalte
log_price_skewness = data['log_price'].skew()
log_price_kurtosis = data['log_price'].kurt()

# Visualisierungen für numerische Daten
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(data['log_price'], kde=True)
plt.title('Log-Preis Verteilung')
plt.xlabel('Log-Preis')
plt.ylabel('Häufigkeit')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=data['log_price'])
plt.title('Boxplot von Log-Preis')
plt.xlabel('Log-Preis')
plt.show()

# Ausgabe der berechneten Schiefe und Kurtosis
print("Log-Preis Schiefe:", log_price_skewness)
print("Log-Preis Kurtosis:", log_price_kurtosis)

# Gesamtzusammenfassung der Daten nach der Bereinigung
print("\nGesamtzusammenfassung nach Bereinigung:\n", data.describe())

# Speichern der bereinigten Daten
cleaned_file_path = '../../../Desktop/Cleaned_HAUS_Properties.csv'
data.to_csv(cleaned_file_path, index=False)
print("Daten wurden bereinigt und gespeichert in:", cleaned_file_path)
