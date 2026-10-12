import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes
    df = df.dropna(subset=['precio', 'descuento']).reset_index(drop=True)
    
    # Convertir tipos de datos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    
    # Renombrar columnas (si es necesario)
    # df = df.rename(columns={'old_name': 'new_name'})
    
    return df