import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import pearsonr

# Untersuchung: Zusammenhang zwischen den Immobilienfaktoren, speziell mit Hinblick auf den Preis
# Daten laden und bereinigen
def load_and_clean_data(filepath):
    data = pd.read_csv(filepath)
    pd.set_option('display.max_columns', None)

    # Konvertieren von Spalten in numerische Werte
    for col in ['rooms', 'bedrooms', 'bathrooms']:
        if data[col].dtype == 'object':
            data[col] = pd.to_numeric(data[col], errors='coerce')

    data['living_space'] = pd.to_numeric(data['living_space'].replace('nil', np.nan), errors='coerce')
    data['property_area'] = pd.to_numeric(data['property_area'].replace('nil', np.nan), errors='coerce')
    data['price'] = pd.to_numeric(data['price'].replace('nil', np.nan), errors='coerce')
    data['usable_area'] = pd.to_numeric(data['usable_area'].replace('nil', np.nan), errors='coerce')

    return data


# Entfernen von Zeilen mit fehlenden Werten
def filter_data(data):
    numerical_cols = ['living_space', 'bedrooms', 'bathrooms', 'buyer_commission',
                      'property_area', 'price', 'rooms', 'usable_area']
    data_filtered = data[numerical_cols].dropna()

    return data_filtered


# Logarithmische Transformation der Daten
def logarithmic_transformation(data):
    for col in ['living_space', 'bedrooms', 'bathrooms', 'buyer_commission',
                'property_area', 'price', 'rooms', 'usable_area', 'garage_parking']:
        if col in data.columns:
            data[f'log_{col}'] = np.log(data[col].replace(0, np.nan))

    return data


# Berechnung der Pearson-Korrelation
def calculate_pearson_correlation(data, variable1, variable2):
    if data[variable1].isna().all() or data[variable2].isna().all():
        return None, None

    if data[variable1].nunique() <= 1 or data[variable2].nunique() <= 1:
        return None, None

    correlation, p_value = pearsonr(data[variable1], data[variable2])

    return correlation, p_value


# Korrelationen berechnen und plotten
def plot_correlation_matrix(data, columns_for_correlation, german_column_names):
    corr_matrix = data[columns_for_correlation].corr(method='spearman')
    corr_matrix.columns = german_column_names
    corr_matrix.index = german_column_names

    plt.figure(figsize=(20, 20))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1,
                annot_kws={"size": 16}, cbar_kws={"shrink": 0.8})
    plt.title('Korrelationsmatrix der Immobilienmerkmale (logarithmierte Werte)', fontsize=24)
    plt.xticks(fontsize=16, rotation=45, ha='right')
    plt.yticks(fontsize=16, rotation=0)
    plt.show()


# Random Forest Modell
def random_forest_model(data, features, target):
    X = data[features].replace([np.inf, -np.inf], np.nan).dropna()
    y = data[target].loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    feature_importances = pd.DataFrame(model.feature_importances_, X.columns, columns=['Importance'])

    plt.figure(figsize=(10, 10))
    plt.scatter(y_test, y_pred, color='blue', label='Predicted vs Actual', alpha=0.5)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linewidth=2)
    plt.xlabel('Tatsächlicher Preis')
    plt.ylabel('Vorhergesagter Preis')
    plt.title('Random Forest - Komplexes Modell')
    plt.legend()
    plt.grid(True)
    plt.show()

    return mse, r2, feature_importances


# Lineares Regressionsmodell
def linear_regression_model(data, feature, target):
    X = data[[feature]].fillna(data[feature].median())
    y = data[target].fillna(data[target].median())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    plt.figure(figsize=(10, 10))
    plt.scatter(X_test, y_test, color='blue', label='Actual')
    plt.scatter(X_test, y_pred, color='red', label='Predicted', alpha=0.5)
    plt.xlabel(feature)
    plt.ylabel(target)
    plt.title(f'Lineare Regression - {feature}')
    plt.legend()
    plt.grid(True)
    plt.show()

    return mse, r2, model


# Hauptprogramm
def main():
    filepath = '../../../../../Desktop/Cleaned_HAUS_Properties.csv'
    data = load_and_clean_data(filepath)

    data_filtered = filter_data(data)
    data_filtered = logarithmic_transformation(data_filtered)

    columns_for_correlation = ['log_living_space', 'log_bedrooms', 'log_bathrooms',
                               'log_buyer_commission', 'log_property_area', 'log_price',
                               'log_rooms', 'log_usable_area']
    german_column_names = ['Wohnfläche', 'Schlafzimmer', 'Badezimmer', 'Käuferprovision',
                           'Grundstücksfläche', 'Preis', 'Zimmer', 'Nutzungsfläche']

    plot_correlation_matrix(data_filtered, columns_for_correlation, german_column_names)

    features = ['log_living_space', 'log_bedrooms', 'log_bathrooms', 'log_garage_parking',
                'log_buyer_commission', 'log_property_area', 'log_rooms', 'log_usable_area']

    for feature in features:
        if feature in data_filtered.columns:
            linear_regression_model(data_filtered, feature, 'log_price')

    available_features = [feature for feature in features if feature in data_filtered.columns]
    mse, r2, feature_importances = random_forest_model(data_filtered, available_features, 'log_price')

    print("\nFeature Importances des RandomForest-Regressors:\n", feature_importances)


# Ausführung des Hauptprogramms
if __name__ == '__main__':
    main()
