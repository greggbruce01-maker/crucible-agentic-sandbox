import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes en 'precio'
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    
    # Convertir 'precio' a tipo numérico
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    # Devolver el DataFrame limpio
    return df