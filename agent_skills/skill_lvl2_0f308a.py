import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['fecha']).reset_index(drop=True)
    return df