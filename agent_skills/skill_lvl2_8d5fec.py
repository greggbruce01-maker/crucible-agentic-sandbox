import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos
    df = df.dropna()
    
    # Convertir las fechas a un formato estándar
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Eliminar duplicados
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Añadir una nueva columna que calcule el valor total de la venta
    df['valor_total'] = df['cantidad'] * df['precio']
    
    # Redondear los valores de las columnas 'precio' y 'valor_total' a dos decimales
    df['precio'] = df['precio'].round(2)
    df['valor_total'] = df['valor_total'].round(2)
    
    return df