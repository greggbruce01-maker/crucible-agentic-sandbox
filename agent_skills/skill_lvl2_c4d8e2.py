import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes en la columna 'precio'
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    
    # Normalizar los valores de precio a tipo numérico
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    return df