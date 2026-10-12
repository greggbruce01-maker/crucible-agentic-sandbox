import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos en las columnas 'fecha' y 'precio'
    df = df.dropna(subset=['fecha', 'precio']).reset_index(drop=True)
    
    # Convertir las columnas a los tipos de datos correctos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    return df