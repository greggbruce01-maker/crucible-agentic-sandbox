import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Convertir 'precio' y 'descuento' a numéricos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    
    # Calcular 'precio_final'
    df['precio_final'] = df['precio'] * (1 - df['descuento'])
    
    # Eliminar filas con valores nulos en 'precio_final'
    df = df.dropna(subset=['precio_final']).reset_index(drop=True)
    
    # Eliminar la columna 'descuento' si no es necesaria
    df = df.drop(columns=['descuento'])
    
    return df