import pandas as pd

def clean_sales_data(df):
    df = df.copy()
    
    # Eliminar filas con valores nulos en las columnas 'precio' y 'cantidad'
    df = df.dropna(subset=['precio', 'cantidad']).reset_index(drop=True)
    
    # Convertir los valores de la columna 'fecha' a un formato estándar
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    return df