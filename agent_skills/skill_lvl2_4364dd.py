import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes en 'precio'
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    
    # Corregir errores tipográficos en los nombres de productos
    df['producto'] = df['producto'].str.strip().str.lower()
    df['producto'] = df['producto'].replace({
        'manzana': 'Manzana',
        'banana': 'Banana',
        'naranja': 'Naranja'
    })
    
    # Normalizar los precios a dos decimales
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce').round(2)
    
    return df