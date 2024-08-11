import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Daten laden
def load_data(filepath):
    return pd.read_csv(filepath)


# Datenbereinigung und -vorbereitung
def clean_data(data):
    columns_of_interest = ['rooms', 'bedrooms', 'bathrooms', 'garage_parking']

    for col in columns_of_interest:
        data[col] = pd.to_numeric(data[col], errors='coerce')
        value_counts = data[col].value_counts().sort_index()
        filtered_value_counts = value_counts[value_counts.index <= 5]
        print(f"\nAnzahl der Häuser nach {col} (bis zu 5):")
        print(filtered_value_counts)

    data['price'] = pd.to_numeric(data['price'], errors='coerce').fillna(data['price'].median())
    non_numeric_columns = data.select_dtypes(exclude=[np.number]).columns
    data[non_numeric_columns] = data[non_numeric_columns].fillna("nil")

    return data


# Ausreißerbehandlung
def remove_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data_cleaned = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)].copy()
    return data_cleaned


# Log-Transformation
def log_transform(data, column):
    data[f'log_{column}'] = np.log1p(data[column])
    return data


# Berechnung der statistischen Kennzahlen
def calculate_statistics(data, columns):
    for col in columns:
        print(f"\nStatistiken für {col}:")
        print("Mittelwert:", data[col].mean())
        print("Median:", data[col].median())
        print("Modus:", data[col].mode()[0])
        print("Varianz:", data[col].var())
        print("Standardabweichung:", data[col].std())
        print("Spannweite:", data[col].max() - data[col].min())
        print("Schiefe:", data[col].skew())
        print("Kurtosis:", data[col].kurt())
        print("Quartile:", data[col].quantile([0.25, 0.5, 0.75]).to_list())
        print("10. und 90. Perzentil:", data[col].quantile([0.1, 0.9]).to_list())


# Visualisierungen erstellen
def visualize_data(data, columns):
    sns.set(style="whitegrid")
    for col in columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[col], kde=True)
        plt.title(f'Verteilung von {col}')
        plt.xlabel(col)
        plt.ylabel('Häufigkeit')
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[col])
        plt.title(f'Boxplot von {col}')
        plt.xlabel(col)
        plt.show()


# Korrelationsmatrix visualisieren
def plot_correlation_matrix(data):
    plt.figure(figsize=(10, 8))
    correlation = data.corr()
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Korrelationsmatrix')
    plt.show()


# Hauptprogramm
def main():
    filepath = "../../../Desktop/Cleaned_HAUS_Properties.csv"
    data = load_data(filepath)
    data = clean_data(data)
    data_cleaned = remove_outliers(data, 'price')
    data_cleaned = log_transform(data_cleaned, 'price')

    print("Log-Preis Schiefe:", data_cleaned['log_price'].skew())
    print("Log-Preis Kurtosis:", data_cleaned['log_price'].kurt())

    numerical_cols = data_cleaned.select_dtypes(include=np.number).columns.tolist()
    calculate_statistics(data_cleaned, numerical_cols)

    print("\nGesamtzusammenfassung:\n", data_cleaned.describe())
    print("\nKorrelation:\n", data_cleaned[numerical_cols].corr())
    print("\nKovarianz:\n", data_cleaned[numerical_cols].cov())

    visualize_data(data_cleaned, numerical_cols)
    plot_correlation_matrix(data_cleaned)


# Ausführung des Hauptprogramms
if __name__ == '__main__':
    main()
