import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Convertir columnas a tipos numéricos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['descuento'] = pd.to_numeric(df['descuento'], errors='coerce')
    
    # Calcular el precio total
    df['precio_total'] = df['precio'] * df['cantidad'] * (1 - df['descuento'])
    
    # Seleccionar las columnas deseadas
    df = df[['id', 'fecha', 'precio_total', 'cantidad']]
    
    # Resetear el índice
    df = df.reset_index(drop=True)
    
    return df