import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes
    df = df.dropna(subset=['precio', 'fecha'])
    df = df.reset_index(drop=True)
    
    # Normalizar la columna 'precio'
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['precio_normalizado'] = df['precio'] * (1 - df['descuento'])
    
    # Normalizar la columna 'fecha'
    df['fecha_normalizada'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
    
    # Seleccionar las columnas de salida
    df = df[['id', 'fecha_normalizada', 'precio_normalizado', 'cantidad', 'descuento']]
    
    return df