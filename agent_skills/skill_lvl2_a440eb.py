import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes
    df = df.dropna(subset=['precio', 'cantidad'])
    
    # Convertir tipos de datos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    # Resetear el índice
    df = df.reset_index(drop=True)
    
    return df