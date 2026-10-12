import pandas as pd

def limpiar_datos(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df.dropna(subset=['precio'])
    df = df[['precio']].reset_index(drop=True)
    return df