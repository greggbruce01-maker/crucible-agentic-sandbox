import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes en 'precio' y 'cantidad'
    df = df.dropna(subset=['precio', 'cantidad']).reset_index(drop=True)
    
    # Convertir 'precio' y 'cantidad' a numéricos, coerciendo errores a NaN
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    # Eliminar filas con valores NaN en 'precio' y 'cantidad' después de la conversión
    df = df.dropna(subset=['precio', 'cantidad']).reset_index(drop=True)
    
    return df