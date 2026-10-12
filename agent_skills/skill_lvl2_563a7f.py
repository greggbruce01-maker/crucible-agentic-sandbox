import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Convertir columnas a tipos numéricos y manejar errores
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    # Eliminar filas con valores nulos en las columnas 'id', 'fecha' y 'precio'
    df = df.dropna(subset=['id', 'fecha', 'precio']).reset_index(drop=True)
    
    # Eliminar filas donde el 'precio' sea menor o igual a cero
    df = df[df['precio'] > 0].reset_index(drop=True)
    
    # Renombrar las columnas
    df.rename(columns={'id': 'ProductoID', 'fecha': 'FechaVenta', 'precio': 'PrecioProducto'}, inplace=True)
    
    return df