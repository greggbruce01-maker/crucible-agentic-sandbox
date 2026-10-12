import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos
    df = df.dropna()
    
    # Convertir tipos de datos
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    
    # Eliminar duplicados
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Crear nuevas columnas
    df['precio_final'] = df['precio'] * (1 - df['descuento'] / 100)
    df['total'] = df['precio_final'] * df['cantidad']
    
    return df