import numpy as np

import pandas as pd

def clean_dataset_strict(df):
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    for col in ['precio', 'cantidad', 'id']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna().reset_index(drop=True)
    return df.copy()