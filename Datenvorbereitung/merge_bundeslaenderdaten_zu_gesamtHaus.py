import os
import pandas as pd


def load_csv_files(folder_path):
    """
    Lädt alle CSV-Dateien aus einem angegebenen Verzeichnis, behandelt verschiedene Codierungen und
    kombiniert sie in einem DataFrame.

    Args:
        folder_path (str): Pfad zum Verzeichnis, das die CSV-Dateien enthält.

    Returns:
        pd.DataFrame: Zusammengeführter DataFrame, der alle CSV-Daten enthält.
    """
    # Liste aller Dateien im Verzeichnis
    all_files = os.listdir(folder_path)

    # Filterung der CSV-Dateien
    csv_files = [f for f in all_files if f.endswith('.csv')]

    # Liste zur Speicherung der DataFrames
    df_list = []

    # Einlesen jeder CSV-Datei
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        try:
            # Versuch, die Datei im UTF-8-Format einzulesen
            df = pd.read_csv(file_path)
            df_list.append(df)
        except UnicodeDecodeError:
            try:
                # Falls UTF-8 fehlschlägt, versuche UTF-16 mit Tabulator-Trennung
                df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
                df_list.append(df)
            except Exception as e:
                print(f"Could not read file {csv_file} due to error: {e}")
        except Exception as e:
            print(f"Could not read file {csv_file} due to error: {e}")

    # Zusammenführung aller DataFrames in einen einzigen DataFrame
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        return combined_df
    else:
        print("No valid CSV files found.")
        return pd.DataFrame()


def save_combined_data(df, output_path):
    """
    Speichert den kombinierten DataFrame in eine neue CSV-Datei.

    Args:
        df (pd.DataFrame): Der zu speichernde DataFrame.
        output_path (str): Pfad zur Ausgabedatei.
    """
    df.to_csv(output_path, index=False)
    print(f"Combined data saved to {output_path}")


def main():
    folder_path = r'Bundesländer_HAUS_CSV/'  # Pfad zum Verzeichnis mit den CSV-Dateien
    output_file = 'ALL_HAUS.csv'  # Name der Ausgabedatei
    output_path = os.path.join(folder_path, output_file)

    # Lade und kombiniere die CSV-Dateien
    combined_df = load_csv_files(folder_path)

    # Speichere den kombinierten DataFrame
    if not combined_df.empty:
        save_combined_data(combined_df, output_path)


if __name__ == '__main__':
    main()
