import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir la columna 'fecha' a tipo datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Eliminar las filas donde el 'precio' sea negativo
    df = df[df['precio'] >= 0].reset_index(drop=True)
    
    # Calcular el 'total' como el 'precio' multiplicado por 'cantidad', considerando el 'descuento'
    df['total'] = (pd.to_numeric(df['precio'], errors='coerce') * pd.to_numeric(df['cantidad'], errors='coerce') * (1 - pd.to_numeric(df['descuento'], errors='coerce'))).round(2)
    
    # Eliminar las columnas 'precio' y 'descuento' del DataFrame final
    df = df.drop(columns=['precio', 'descuento'])
    
    return df