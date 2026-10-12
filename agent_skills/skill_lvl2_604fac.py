import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos en las columnas 'precio' y 'fecha'
    df = df.dropna(subset=['precio', 'fecha']).reset_index(drop=True)
    
    # Convertir la columna 'fecha' a un formato estándar
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    return df