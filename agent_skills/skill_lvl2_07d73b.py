import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df.dropna(subset=['precio'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['fecha'])
    df = df.reset_index(drop=True)
    return df