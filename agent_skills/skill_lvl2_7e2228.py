import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    return df