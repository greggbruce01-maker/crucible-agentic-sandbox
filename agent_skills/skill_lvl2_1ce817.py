import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes
    df = df.dropna()
    
    # Convertir columnas a tipos numéricos y corregir errores
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    
    # Renombrar columnas
    df.rename(columns={'id': 'ID', 'fecha': 'Fecha', 'precio': 'Precio', 'cantidad': 'Cantidad', 'descuento': 'Descuento'}, inplace=True)
    
    # Resetear el índice
    df = df.reset_index(drop=True)
    
    return df