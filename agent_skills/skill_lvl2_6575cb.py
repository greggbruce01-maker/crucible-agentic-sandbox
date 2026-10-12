import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Convertir la columna 'fecha' a formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Eliminar cualquier fila con valores faltantes
    df = df.dropna().reset_index(drop=True)
    
    # Asegurarse de que todos los valores en la columna 'precio' sean positivos
    df = df[df['precio'] > 0].reset_index(drop=True)
    
    return df