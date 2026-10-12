import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir tipos de datos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    # Eliminar filas con valores faltantes
    df = df.dropna(subset=['precio', 'cantidad']).reset_index(drop=True)
    
    # Eliminar duplicados
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df