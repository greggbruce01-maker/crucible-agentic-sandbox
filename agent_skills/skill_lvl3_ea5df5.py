import pandas as pd

def clean_data(df):
    df = df.copy()
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    return df[['precio']]