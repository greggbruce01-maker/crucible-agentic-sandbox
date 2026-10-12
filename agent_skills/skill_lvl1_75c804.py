import pandas as pd

def limpiar_precios(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df.dropna(subset=['precio'])
    df['precio'] = df['precio'].round(2)
    df = df.reset_index(drop=True)
    return df