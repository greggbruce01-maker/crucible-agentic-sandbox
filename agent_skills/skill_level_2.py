import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir 'precio' a numérico, coerciendo errores a NaN
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    # Eliminar filas con datos faltantes en 'precio'
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    
    return df