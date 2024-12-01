import pandas as pd

def load_firing_data(file_path = '',export_csv = None):
    # Creazione del dataset
    pd.read_csv(file_path, encoding='utf8')
    # Creare un DataFrame
    df = pd.DataFrame(file_path)
    return df