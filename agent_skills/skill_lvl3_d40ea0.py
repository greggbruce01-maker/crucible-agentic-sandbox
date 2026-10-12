import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar duplicados
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Convertir tipos de datos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['stock'] = pd.to_numeric(df['stock'], errors='coerce')
    
    # Crear nueva columna basada en operaciones existentes
    df['precio_stock'] = df['precio'] * df['stock']
    
    # Eliminar la columna 'precio_stock' si no es necesaria
    df = df.drop(columns=['precio_stock'])
    
    return df