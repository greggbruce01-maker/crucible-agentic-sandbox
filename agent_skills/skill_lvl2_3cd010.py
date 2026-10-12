import pandas as pd

def limpiar_precios(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['precio'].fillna(0.0, inplace=True)
    return df.reset_index(drop=True)