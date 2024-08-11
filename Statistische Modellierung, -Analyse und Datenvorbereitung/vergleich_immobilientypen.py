import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal

# Untersuchung: Schauen, ob es einen signifikanten Unterschied zwischen den Immobilientypen:
# Einfamilienhäuser, Mehrfamilienhäuser und Doppelhaushälften gibt
# Daten laden und bereinigen
def load_data(filepath):
    return pd.read_csv(filepath)

# Funktion zum Filtern der Typen
def match_type(row, house_type):
    type_pattern = fr'\b{house_type}.*\b'  # Suche nach Mustern, die auf den Typ hinweisen
    for col in row.index:
        if isinstance(row[col], str) and pd.notna(row[col]):
            if pd.Series(row[col]).str.contains(type_pattern, regex=True, na=False).any():
                return True
    return False

# Filtern der Typen und Prüfen auf Matches
def filter_house_types(data, types):
    filtered_data = pd.DataFrame()
    for house_type in types:
        matches = data[data.apply(lambda row: match_type(row, house_type), axis=1)]
        filtered_data = pd.concat([filtered_data, matches])
        print(f"Matches für {house_type}: {len(matches)}")
        print(f"Beispiele für {house_type}:")
        print(matches[['type', 'price', 'price_per_m2']].head())  # Beispielzeilen anzeigen

    filtered_data.reset_index(drop=True, inplace=True)
    return filtered_data

# Beibehalten der drei Haupttypen
def retain_main_types(filtered_data, types):
    filtered_data = filtered_data[filtered_data['type'].str.contains('|'.join(types), na=False)]
    return filtered_data

# Entfernen von Einträgen mit 0 oder negativem Preis pro m2
def filter_price_per_m2(filtered_data):
    return filtered_data[filtered_data['price_per_m2'] > 0]

# Ausreißer im Preis pro Quadratmeter durch den Median ersetzen
def replace_outliers_with_median(data, column):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    median_value = data[column].median()
    data.loc[(data[column] < lower_bound) | (data[column] > upper_bound), column] = median_value

# Boxplot für Preis pro Quadratmeter erstellen
def plot_price_per_m2(filtered_data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='type', y='price_per_m2', data=filtered_data)
    plt.xlabel('Immobilientyp')
    plt.ylabel('Preis pro Quadratmeter')
    plt.title('Vergleich des Preises pro Quadratmeter nach Immobilientyp')
    plt.show()

# Überprüfen der Gruppengröße
def check_group_sizes(filtered_data, types):
    data_groups = [filtered_data[filtered_data['type'].str.contains(house_type, na=False)]['price_per_m2'].dropna() for house_type in types]
    for house_type, group in zip(types, data_groups):
        print(f"{house_type}: {len(group)} Einträge")
    return data_groups

# Durchführung des Kruskal-Wallis-Tests
def perform_kruskal_test(data_groups):
    if all(group.size >= 5 for group in data_groups) and any(group.var() > 0 for group in data_groups):
        kruskal_result = kruskal(*data_groups)
        print(f"\nKruskal-Wallis Ergebnis für price_per_m2: H-statistic={kruskal_result.statistic}, p-value={kruskal_result.pvalue}")
    else:
        print("\nNicht genug Daten oder keine Varianz für den Kruskal-Wallis-Test.")

# Hauptprogramm
def main():
    data_path = '../../../../../Desktop/Cleaned_HAUS_Properties.csv'
    data = load_data(data_path)

    types = ['Einfamilienhaus', 'Mehrfamilienhaus', 'Doppelhaushälfte']
    filtered_data = filter_house_types(data, types)

    print("\nTypen nach dem Filtern:")
    print(filtered_data['type'].value_counts())  # Richtig geschriebene Methode

    filtered_data = retain_main_types(filtered_data, types)

    print("\nTypen nach dem Beibehalten der drei Haupttypen:")
    print(filtered_data['type'].value_counts())  # Richtig geschriebene Methode

    filtered_data = filter_price_per_m2(filtered_data)

    replace_outliers_with_median(filtered_data, 'price_per_m2')

    plot_price_per_m2(filtered_data)

    data_groups = check_group_sizes(filtered_data, types)

    perform_kruskal_test(data_groups)

# Ausführung des Hauptprogramms
if __name__ == '__main__':
    main()
