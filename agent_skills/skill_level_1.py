import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Elimina filas con valores nulos
    df = df.dropna()
    
    # Convierte la columna 'fecha' a formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Redondea el valor de 'precio' a dos decimales
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce').round(2)
    
    # Elimina filas con valores nulos después de la conversión
    df = df.dropna()
    
    # Reset del índice
    df = df.reset_index(drop=True)
    
    return df