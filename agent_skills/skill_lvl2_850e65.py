import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Convertir 'estado' a minúsculas
    df['estado'] = df['estado'].str.lower()
    
    return df