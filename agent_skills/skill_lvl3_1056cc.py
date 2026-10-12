import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir columnas a tipos numéricos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    # Calcular el precio final
    df['precio_final'] = df['precio'] - (df['precio'] * (df['descuento'] / 100))
    
    # Eliminar filas donde la cantidad es negativa o cero
    df = df[df['cantidad'] > 0].reset_index(drop=True)
    
    # Seleccionar las columnas de salida
    df = df[['id', 'fecha', 'precio_final', 'categoria']]
    
    return df