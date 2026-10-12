import pandas as pd

def limpiar_datos(df):
    df = df.copy()
    
    # Normalizar la columna 'fecha' a formato YYYY-MM-DD
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    
    # Eliminar filas duplicadas en función de las columnas 'id' y 'fecha'
    df = df.drop_duplicates(subset=['id', 'fecha']).reset_index(drop=True)
    
    return df