import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos en la columna 'nombre'
    df = df.dropna(subset=['nombre']).reset_index(drop=True)
    
    # Convertir la columna 'edad' a tipo de dato numérico
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    
    # Eliminar duplicados en la columna 'nombre'
    df = df.drop_duplicates(subset=['nombre']).reset_index(drop=True)
    
    return df