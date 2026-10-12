import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes en 'precio'
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    
    # Convertir 'precio' a numérico y corregir valores erróneos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df = df[df['precio'] >= 0].reset_index(drop=True)
    
    return df