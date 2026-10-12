import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con datos faltantes
    df = df.dropna().reset_index(drop=True)
    
    # Corregir errores tipográficos en los nombres de productos
    df['producto'] = df['producto'].str.lower().str.strip()
    df['producto'] = df['producto'].replace({'manzana': 'Manzana', 'banana': 'Banana'})
    
    # Convertir las fechas a un formato estándar
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    
    # Convertir los precios y cantidades a tipos numéricos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    return df